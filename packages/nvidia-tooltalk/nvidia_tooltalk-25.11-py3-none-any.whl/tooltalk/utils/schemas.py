from typing_extensions import TypedDict, NotRequired


class BaseGenerationKwargs(TypedDict):
    """
    Configuration for running the evaluation.
    """

    temperature: NotRequired[float]
    top_p: NotRequired[float]
    max_new_tokens: NotRequired[int]



class Hf2OpenAi:
    mapping = {"max_new_tokens": "max_tokens"}

    @staticmethod
    def map(generation_kwargs: dict[str, any]) -> dict[str, any]:
        return {Hf2OpenAi.mapping.get(k, k): v for k, v in generation_kwargs.items()}
