from functools import cached_property
import logging
import time
from typing import Callable, Required, TypedDict
from anthropic import Anthropic as OriginAnthropic
from anthropic.resources.messages import Messages
from anthropic.types.message import Message
from specific_ai.optune.inference import Inference
from specific_ai.optune.lm_response_types import LMResponse
from specific_ai.optune.tracing import Tracing

logger = logging.getLogger(__name__)


def convert_to_anthropic_response(response, parse_specific_ai_response):
    completions = parse_specific_ai_response(response)
    return Message(
        **{
            "id": f"response-{int(time.time())}",
            "model": "specific-ai",
            "role": "assistant",
            "type": "message",
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
            },
            "content": [{"type": "text", "text": completions}],
        }
    )



class OptuneaiParams(TypedDict, total=False):
    task_name: Required[str]
    """The name for this specific task."""

    project_name: str
    """Optional project name for related tasks."""


class OptuneMessages(Messages):
    _client: 'Anthropic'

    def __init__(self, client: 'Anthropic'):
        super().__init__(client)
        self._data_collector = Tracing(client._optune_url)
        self._inference_service = Inference(client._optune_url)

    def create(self, *args, specific_ai: OptuneaiParams, **kwargs):
        prompt = "\n".join(
            message.get("content", "") for message in kwargs.get("messages", [])
        )
        start_time = time.perf_counter()

        inference_error = None
        is_from_optune_model = False
        raw_logits = None
        if self._client._use_optune_inference:
            is_from_optune_model = True
            try:
                inference, raw_logits = self._inference_service.infer(
                    prompt=prompt,
                    usecase_name=specific_ai.get("task_name"),
                    group_name=specific_ai.get("project_name", "default"),
                )
                result = convert_to_anthropic_response(
                    inference, self._client._parse_optune_response
                )
            except Exception as e:
                inference_error = str(e)
                is_from_optune_model = False
                logger.exception(
                    f"Error inference SpecificAI's model. fallback to parent model: {str(e)}"
                )
                result = super().create(*args, **kwargs)

        else:
            result = super().create(*args, **kwargs)
        end_time = time.perf_counter()
        try:
            completion = result.content[0].text
            if completion:
                # Start data collection in background
                self._data_collector.collect(
                    modelname=kwargs.get("model"),
                    prompt=prompt,
                    response=completion,
                    usecase_name=specific_ai.get("task_name"),
                    usecase_group=specific_ai.get("project_name", "default"),
                    response_time=end_time - start_time,
                    is_from_optune_model=is_from_optune_model,
                    inference_error=inference_error,
                    logprobs=None,
                    raw_logits=raw_logits
                )

        except Exception:
            logger.exception("Error in SpecificAICompletions.create")

        return result
    
def default_parse_optune_response(response: list[LMResponse]) -> str:
    return ';'.join(response[0].labels)


class Anthropic(OriginAnthropic):
    def __init__(self,        
        specific_ai_url: str,
        use_specific_ai_inference: bool = False,
        parse_specific_ai_response: Callable[[list[LMResponse]], str] = default_parse_optune_response,
        *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._optune_url = specific_ai_url
        self._use_optune_inference = use_specific_ai_inference
        self._parse_optune_response = parse_specific_ai_response

    @cached_property
    def messages(self) -> OptuneMessages:
        return OptuneMessages(self)
