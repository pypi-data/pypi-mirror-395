"""Inference-only MERaLiON AudioLLM model compatible with HuggingFace weights."""
from functools import lru_cache
from typing import Iterable, List, Mapping, Optional, Tuple, Union

import librosa
import numpy as np
import torch
import torch.nn as nn

from vllm.attention import AttentionMetadata
from vllm.config import VllmConfig
from vllm.inputs import (INPUT_REGISTRY, DecoderOnlyInputs, DummyData,
                         InputContext, token_inputs)
from vllm.logger import init_logger
from vllm.model_executor.layers.logits_processor import LogitsProcessor
from vllm.model_executor.layers.sampler import SamplerOutput, get_sampler
from vllm.model_executor.layers.vocab_parallel_embedding import ParallelLMHead
from vllm.model_executor.model_loader.weight_utils import (
    default_weight_loader, maybe_remap_kv_scale_name)
from vllm.model_executor.models.gemma2 import Gemma2Model
from vllm.model_executor.sampling_metadata import SamplingMetadata
from vllm.multimodal import MULTIMODAL_REGISTRY, MultiModalKwargs
from vllm.multimodal.utils import consecutive_placeholder_ranges
from vllm.sequence import IntermediateTensors, SequenceData
from transformers.models.whisper.modeling_whisper import WhisperEncoder

from vllm.model_executor.models.interfaces import SupportsMultiModal, SupportsLoRA, SupportsPP
from vllm.model_executor.models.utils import maybe_prefix

from .transformers_utils.modules import (autoset_attn_implementation_for_whisper,
    MERaLiON2Inputs, MERaLiON2SpeechAudioAdaper)


logger = init_logger(__name__)


# gemma2 ties word embedding by default
_KEYS_TO_MODIFY_MAPPING = {
    "text_decoder.model": "model",
}

# === Constants === #
DEFAULT_SAMPLE_RATE = 16000
FEATURE_CHUNK_SIZE = DEFAULT_SAMPLE_RATE * 30
OUTPUT_CHUNK_SIZE = 100
MAX_NUMBER_CHUNKS = 10


def dummy_data_for_meralion(ctx: InputContext, seq_len: int,
                               mm_counts: Mapping[str, int]):
    num_audios = mm_counts["audio"]
    max_tokens_per_audio = get_max_meralion_audio_tokens(ctx)
    max_llm_audio_tokens = max_tokens_per_audio * num_audios
    if seq_len - max_llm_audio_tokens - 2 < 0:
        raise RuntimeError(
            f"MERaLiON-AudioLLM cannot process {num_audios} audios in a prompt, "
            "please increase max_model_len or reduce audio limit by "
            "--limit-mm-per-prompt.")

    speech_token_index = ctx.model_config.hf_config.speech_token_index

    dummy_seqdata = SequenceData.from_prompt_token_counts(
        (speech_token_index, max_llm_audio_tokens),
        (0, seq_len - max_llm_audio_tokens),
    )
    dummy_audio = np.full((MAX_NUMBER_CHUNKS * FEATURE_CHUNK_SIZE * num_audios, ), 0.)
    return DummyData(
        dummy_seqdata, {"audio": [(dummy_audio, DEFAULT_SAMPLE_RATE)] * num_audios}, {
            "audio":
            consecutive_placeholder_ranges(num_items=num_audios,
                                           item_size=max_tokens_per_audio)
        })


def get_processor(
    processor_name: str,
    *args,
    trust_remote_code: bool = True,
    **kwargs,
):
    """Gets a processor for the given model name via HuggingFace.

    Derived from `vllm.transformers_utils.image_processor.get_image_processor`.
    """
    # don't put this import at the top level
    # it will call torch.cuda.device_count()
    from transformers import AutoProcessor

    try:
        processor = AutoProcessor.from_pretrained(
            processor_name,
            *args,
            trust_remote_code=trust_remote_code,
            **kwargs)
    except ValueError as e:
        # If the error pertains to the processor class not existing or not
        # currently being imported, suggest using the --trust-remote-code flag.
        # Unlike AutoTokenizer, AutoProcessor does not separate such errors
        if not trust_remote_code:
            err_msg = (
                "Failed to load the processor. If the processor is "
                "a custom processor not yet available in the HuggingFace "
                "transformers library, consider setting "
                "`trust_remote_code=True` in LLM or using the "
                "`--trust-remote-code` flag in the CLI.")
            raise RuntimeError(err_msg) from e
        else:
            raise e

    return processor


cached_get_processor = lru_cache(get_processor)


def _get_number_chunks(audios: List[np.ndarray]):
    audio_lengths = np.array([_.shape[0] for _ in audios])
    number_chunks = ((audio_lengths - 1) // FEATURE_CHUNK_SIZE) + 1
    return np.clip(number_chunks, a_min=None, a_max=MAX_NUMBER_CHUNKS)


def _get_chunked_audios(audios: List[np.ndarray]):
    audio_number_chunks = _get_number_chunks(audios)
    chunked_resampled_audios = [] 

    for audio_idx, audio in enumerate(audios):
        for cid in range(audio_number_chunks[audio_idx]):
            chunked_resampled_audios.append(
                audio[cid * FEATURE_CHUNK_SIZE: (cid + 1) * FEATURE_CHUNK_SIZE]
            )
    return chunked_resampled_audios


def _maybe_resample_audio(audio, orig_sample_rate, target_sample_rate):
    if orig_sample_rate != target_sample_rate:
        return librosa.resample(
            audio,
            orig_sr=orig_sample_rate,
            target_sr=target_sample_rate
            )
    return audio


def get_max_meralion_audio_tokens(ctx: InputContext) -> int:
    """
    The max number of tokens after speech audio adapter.
    """
    output_chunk_size = getattr(
        ctx.model_config.hf_config, "fixed_speech_embeds_length", OUTPUT_CHUNK_SIZE)
    return MAX_NUMBER_CHUNKS * output_chunk_size


def input_processor_for_meralion(
        ctx: InputContext, inputs: DecoderOnlyInputs) -> DecoderOnlyInputs:
    multi_modal_data = inputs.get("multi_modal_data")
    if multi_modal_data is None or "audio" not in multi_modal_data:
        return inputs

    audios = multi_modal_data["audio"]
    if not isinstance(audios, list):
        audios = [audios]

    if len(audios) == 0:
        return inputs

    processor = cached_get_processor(ctx.model_config.model)

    resampled_audios = [
        librosa.resample(audio,
                         orig_sr=sampling_rate,
                         target_sr=processor.feature_extractor.sampling_rate)
        for audio, sampling_rate in audios
    ]

    output_chunk_size = getattr(
        ctx.model_config.hf_config, "fixed_speech_embeds_length", OUTPUT_CHUNK_SIZE)
    audio_output_lengths = _get_number_chunks(resampled_audios) * output_chunk_size
    speech_token_index = ctx.model_config.hf_config.speech_token_index

    input_ids = inputs['prompt_token_ids']

    new_input_ids = []
    audio_num = input_ids.count(speech_token_index)
    assert len(audio_output_lengths) == audio_num, \
        (f'The text input contains {audio_num} audio tokens, '
         f'but {len(audio_output_lengths)} audios provided')
    start = 0
    for audio_idx in range(audio_num):
        end = input_ids.index(speech_token_index, start)
        new_input_ids.extend(input_ids[start:end])  # text part

        new_input_ids.extend([speech_token_index] * 
                             audio_output_lengths[audio_idx])
        start = end + 1
    new_input_ids.extend(input_ids[start:])

    return token_inputs(
        prompt_token_ids=new_input_ids,
        prompt=inputs.get('prompt'),
        multi_modal_data=multi_modal_data,
    )


def input_mapper_for_meralion(
    ctx: InputContext,
    multi_modal_data: Union[np.ndarray, List[np.ndarray]],
) -> MultiModalKwargs:
    """Input mapper for MERaLiON-AudioLLM."""
    if not isinstance(multi_modal_data, list):
        multi_modal_data = [multi_modal_data]

    if len(multi_modal_data) == 0:
        return MultiModalKwargs()

    processor = cached_get_processor(ctx.model_config.model)
    audio_feature_extractor = processor.feature_extractor
    if audio_feature_extractor is None:
        raise RuntimeError(
            "No HuggingFace audio_feature_extractor is available "
            "to process the audio object")

    try:
        target_sample_rate = processor.feature_extractor.sampling_rate

        resampled_audios = [
            _maybe_resample_audio(
                audio=audio,
                orig_sample_rate=sampling_rate, 
                target_sample_rate=target_sample_rate, 
                )
            for audio, sampling_rate in multi_modal_data
        ]

        resampled_audios = _get_chunked_audios(resampled_audios)

        batch_data = audio_feature_extractor(resampled_audios,
                                             sampling_rate=target_sample_rate,
                                             return_attention_mask=True,
                                             padding="max_length",
                                             return_tensors="pt",
                                             do_normalize=True).data
        batch_data["feature_attention_mask"] = batch_data.pop("attention_mask")
    except Exception:
        logger.error("Failed to process audio (%s)", multi_modal_data)
        raise

    return MultiModalKwargs(batch_data)


@INPUT_REGISTRY.register_dummy_data(dummy_data_for_meralion)
@INPUT_REGISTRY.register_input_processor(input_processor_for_meralion)
@MULTIMODAL_REGISTRY.register_input_mapper("audio",
                                           input_mapper_for_meralion)
@MULTIMODAL_REGISTRY.register_max_multimodal_tokens(
    "audio", get_max_meralion_audio_tokens)
class MERaLiON2ForConditionalGeneration(nn.Module, SupportsMultiModal,
                                       SupportsLoRA, SupportsPP):
    packed_modules_mapping = {
        "qkv_proj": [
            "q_proj",
            "k_proj",
            "v_proj",
        ],
        "gate_up_proj": [
            "gate_proj",
            "up_proj",
        ],
    }

    # LoRA specific attributes
    supported_lora_modules = [
        "qkv_proj",
        "o_proj",
        "gate_up_proj",
        "down_proj",
    ]

    embedding_modules = {}
    embedding_padding_modules = []

    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        super().__init__()
        config = vllm_config.model_config.hf_config
        quant_config = vllm_config.quant_config
        multimodal_config = vllm_config.model_config.multimodal_config

        self.config = config
        self.multimodal_config = multimodal_config

        config.speech_config = \
            autoset_attn_implementation_for_whisper(config.speech_config)
        self.speech_encoder = WhisperEncoder(config.speech_config)
        self.ln_speech = nn.LayerNorm(config.speech_config.d_model)
        self.speech_audio_adapter = MERaLiON2SpeechAudioAdaper(
            audio_hidden_size = config.speech_config.d_model,
            text_hidden_size = config.text_config.hidden_size,
            speech_mlp_scale_factor = getattr(config, "speech_mlp_scale_factor", 15),
            speech_mlp_use_projection = getattr(config, "speech_mlp_use_projection", True)
        )

        self.quant_config = quant_config

        self.model = Gemma2Model(
            vllm_config=vllm_config.with_hf_config(config.text_config),
            prefix=maybe_prefix(prefix, "model"))
        self.unpadded_vocab_size = config.text_config.vocab_size
        if config.text_config.tie_word_embeddings:
            self.lm_head = self.model.embed_tokens
        else:
            self.lm_head = ParallelLMHead(config.text_config.vocab_size,
                                          config.text_config.hidden_size,
                                          quant_config=quant_config)
        logit_scale = getattr(config, "logit_scale", 1.0)
        self.logits_processor = LogitsProcessor(self.unpadded_vocab_size,
                                                config.text_config.vocab_size,
                                                logit_scale)

        self.sampler = get_sampler()
        self.make_empty_intermediate_tensors = (
            self.model.make_empty_intermediate_tensors)

    def _validate_and_reshape_mm_tensor(self,
                                        mm_input: Union[torch.Tensor,
                                                        List[torch.Tensor]],
                                        name: str) -> torch.Tensor:
        if not isinstance(mm_input, (torch.Tensor, list)):
            raise ValueError(f"Incorrect type of {name}. "
                             f"Got type: {type(mm_input)}")
        if isinstance(mm_input, torch.Tensor):
            return torch.concat(list(mm_input))
        else:
            return torch.concat(mm_input)

    def _parse_and_validate_audio_input(
            self, **kwargs: object) -> Optional[MERaLiON2Inputs]:
        input_features = kwargs.pop('input_features', None)
        feature_attention_mask = kwargs.pop('feature_attention_mask', None)
        if input_features is None:
            return None
        input_features = self._validate_and_reshape_mm_tensor(
            input_features, 'input_features')
        feature_attention_mask = self._validate_and_reshape_mm_tensor(
            feature_attention_mask, 'feature_attention_mask')
        if not isinstance(input_features, (torch.Tensor, list)):
            raise ValueError("Incorrect type of audio input features. "
                             f"Got type: {type(input_features)}")
        return MERaLiON2Inputs(input_features=input_features,
                                feature_attention_mask=feature_attention_mask)

    def _process_audio_input(self,
                             audio_input: MERaLiON2Inputs) -> torch.Tensor:

        input_features = audio_input["input_features"].to(self.speech_encoder.dtype)
        feature_attention_mask = audio_input["feature_attention_mask"]

        audio_outputs = self.speech_encoder(input_features,
                                         attention_mask=feature_attention_mask)
        audio_features = audio_outputs.last_hidden_state
        audio_features = self.ln_speech(audio_features)
        audio_features = self.speech_audio_adapter(audio_features)
        audio_features = audio_features.view(-1, audio_features.size(-1))
        
        return audio_features

    def forward(
        self,
        input_ids: torch.Tensor,
        positions: torch.Tensor,
        kv_caches: List[torch.Tensor],
        attn_metadata: AttentionMetadata,
        intermediate_tensors: Optional[IntermediateTensors] = None,
        **kwargs: object,
    ) -> Union[torch.Tensor, IntermediateTensors]:
        if intermediate_tensors is not None:
            input_ids = None
            inputs_embeds = None
        else:
            audio_input = self._parse_and_validate_audio_input(**kwargs)

            if audio_input is None:
                inputs_embeds = None
            else:
                inputs_embeds = self.model.embed_tokens(input_ids)
                processed_audio_features = self._process_audio_input(audio_input)
                # merge llm embeddings and audio features
                mask = (input_ids == self.config.speech_token_index)
                inputs_embeds[mask, :] = processed_audio_features

                input_ids = None

        hidden_states = self.model(
            input_ids=input_ids,
            positions=positions,
            kv_caches=kv_caches,
            attn_metadata=attn_metadata,
            intermediate_tensors=intermediate_tensors,
            inputs_embeds=inputs_embeds,
        )
        return hidden_states

    def compute_logits(self, hidden_states: torch.Tensor,
                       sampling_metadata: SamplingMetadata) -> torch.Tensor:
        logits = self.logits_processor(self.lm_head, hidden_states,
                                       sampling_metadata)
        return logits

    def sample(
        self,
        logits: torch.Tensor,
        sampling_metadata: SamplingMetadata,
    ) -> Optional[SamplerOutput]:
        next_tokens = self.sampler(logits, sampling_metadata)
        return next_tokens

    def load_weights(self, weights: Iterable[Tuple[str, torch.Tensor]]):
        stacked_params_mapping = [
            # (param_name, shard_name, shard_id)
            ("qkv_proj", "q_proj", "q"),
            ("qkv_proj", "k_proj", "k"),
            ("qkv_proj", "v_proj", "v"),
            ("gate_up_proj", "gate_proj", 0),
            ("gate_up_proj", "up_proj", 1),
        ]
        params_dict = dict(self.named_parameters(remove_duplicate=False))

        for name, loaded_weight in weights:
            if "rotary_emb.inv_freq" in name:
                continue
            if (self.config.text_config.tie_word_embeddings
                    and "lm_head.weight" in name):
                continue
            for key_to_modify, new_key in _KEYS_TO_MODIFY_MAPPING.items():
                if key_to_modify in name:
                    name = name.replace(key_to_modify, new_key)
            for (param_name, weight_name, shard_id) in stacked_params_mapping:
                if weight_name not in name or 'speech_' in name:
                    continue
                name = name.replace(weight_name, param_name)
                # Skip loading extra bias for GPTQ models.
                if name.endswith(".bias") and name not in params_dict:
                    continue
                param = params_dict[name]
                weight_loader = param.weight_loader
                weight_loader(param, loaded_weight, shard_id)
                break
            else:
                # Skip loading extra bias for GPTQ models.
                if name.endswith(".bias") and name not in params_dict:
                    continue
                # Remapping the name of FP8 kv-scale.
                name = maybe_remap_kv_scale_name(name, params_dict)
                if name is None:
                    continue

                param = params_dict[name]
                weight_loader = getattr(param, "weight_loader",
                                        default_weight_loader)
                weight_loader(param, loaded_weight)