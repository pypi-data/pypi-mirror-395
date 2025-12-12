import dataclasses
from dataclasses import dataclass
from enum import Enum
from types import UnionType, NoneType

# TODO: these bits and some withind handle_wildguard are from wildguard itself (Apache licensed) - we should mentioned that

class PromptHarmfulness(Enum):
    HARMFUL = "harmful"
    UNHARMFUL = "unharmful"


class ResponseRefusal(Enum):
    COMPLIANCE = "compliance"
    REFUSAL = "refusal"


class ResponseHarmfulness(Enum):
    HARMFUL = "harmful"
    UNHARMFUL = "unharmful"


@dataclass
class SafetyClassifierOutput:
    """
    Represents the output of a safety classifier model, including information about the prompt harmfulness, response refusal, and response harmfulness.

    This is the union of fields that each safety classifier outputs.
    For each classifier's specific outputs, check classifier.get_output_fields().
    When creating a classifier with new output fields, add them into this class as well.

    The `prompt_harmfulness` field indicates whether the input prompt was assessed as harmful, sensitive, or unharmful.
    The `response_harmfulness` field indicates whether the generated response was assessed as harmful, sensitive, or unharmful.
    The `response_refusal` field indicates whether the model complied or refused to generate a response.
    The `is_parsing_error` field indicates whether there was an error parsing the input or output. If true, the other fields may be invalid.
    """

    prompt_harmfulness: PromptHarmfulness | None = None
    response_harmfulness: ResponseHarmfulness | None = None
    response_refusal: ResponseRefusal | None = None

    is_parsing_error: bool = False

    def asdict(self, keep_none=False):
        """
        Converts the object into a dictionary, collapsing Enum fields into their literal values.
        If keep_none=False, removes any fields whose value is None.
        """
        result = dataclasses.asdict(self)
        for key, val in result.items():
            if isinstance(val, Enum):
                result[key] = val.value
        if keep_none:
            return result
        return {key: value for key, value in result.items() if value is not None}

    @staticmethod
    def get_fields_and_types() -> dict[str, type]:
        """
        Returns a mapping from field names to their types.
        Excludes None from union types, only including concrete types.
        """
        mappings = {}
        fields = dataclasses.fields(SafetyClassifierOutput)
        for field in fields:
            field_type = field.type
            if isinstance(field_type, UnionType):
                assert (
                    len(field_type.__args__) == 2 and NoneType in field_type.__args__
                ), "Union SafetyClassifierOutput types must be (T, NoneType)"
                field_type = [t for t in field_type.__args__ if t != NoneType][0]

            mappings[field.name] = field_type
        return mappings