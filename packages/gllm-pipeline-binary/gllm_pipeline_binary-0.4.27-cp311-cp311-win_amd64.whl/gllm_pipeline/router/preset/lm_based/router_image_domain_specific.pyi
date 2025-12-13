from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker as BaseLMInvoker
from gllm_inference.output_parser import JSONOutputParser
from gllm_inference.prompt_builder import PromptBuilder

SYSTEM_PROMPT: str
USER_PROMPT: str

def get_router_image_domain_specific(lm_invoker_kwargs: dict | None = None, prompt_builder_kwargs: dict | None = None) -> dict[str, BaseLMInvoker | PromptBuilder | JSONOutputParser]:
    """Returns the domain-specific preset components for image routing.

    Returns:
        dict[str, BaseLMInvoker | PromptBuilder | JSONOutputParser]: The LM invoker,
            prompt builder, and output parser.
    """
