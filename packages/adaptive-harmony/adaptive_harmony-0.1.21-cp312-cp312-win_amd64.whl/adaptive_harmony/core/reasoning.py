import re


def remove_reasoning(completion: str) -> str:
    """Get the completion without the reasoning.

    This is a quick implementation for Qwen3 thinking tags only at the moment.
    """
    # Remove either <think>...</think> tags or content from start to </think> if <think> is a prefix from the chat template.
    result = re.sub(r"<think>.*?</think>|^.*?</think>", "", completion, count=1, flags=re.DOTALL)

    return result.strip()
