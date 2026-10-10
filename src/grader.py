import json
from openai import OpenAI

client = OpenAI()


def grade_response(prompt, response):

    rubric = """
You are evaluating an AI response for DIRECTNESS.

There are TWO separate failure types:

1. UNNECESSARY CONVERSATIONAL FILLER
Language that adds no useful information and can be removed without reducing
meaning, task completion, necessary clarification, accuracy, safety, or
contextually appropriate emotional acknowledgement.

Examples:
- "Let me check that for you."
- "Sure! I'd be happy to help."
- "Let's take a look."

Do NOT classify as filler:
- necessary clarification
- relevant limitations
- useful process information
- meaningful emotional acknowledgement
- a brief confirmation that a correction was understood

For example:
User: "No, I meant Manchester, not Birmingham."
Assistant: "Manchester, not Birmingham."
This is a concise state-confirming acknowledgement and should NOT be filler.

2. UNREQUESTED ELABORATION
Substantive information that may be true or relevant, but was not requested
and is not needed to answer accurately, safely, or usefully.

Example:
User: "What is the capital of Japan?"
Assistant: "Tokyo. Tokyo is also Japan's largest city and a major financial center."

"Tokyo." answers the request.
The second sentence is unrequested elaboration.

A response may:
- contain filler only
- contain elaboration only
- contain both
- contain neither

Evaluate meaning, not keyword patterns.

The final directness standard is:
PASS only if there is no unnecessary filler AND no unrequested elaboration.
"""

    grader_response = client.responses.create(
        model="gpt-5.6-sol",
        input=[
            {
                "role": "system",
                "content": rubric
            },
            {
                "role": "user",
                "content": f"""
USER PROMPT:
{prompt}

ASSISTANT RESPONSE:
{response}
"""
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "directness_grade",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "contains_unnecessary_filler": {
                            "type": "boolean"
                        },
                        "filler_type": {
                            "type": "string",
                            "enum": [
                                "none",
                                "empty_progress_statement",
                                "unnecessary_acknowledgement",
                                "permission_seeking",
                                "unnecessary_clarification",
                                "verbose_preamble",
                                "repetition",
                                "other"
                            ]
                        },
                        "filler_text": {
                            "type": "string"
                        },
                        "contains_unrequested_elaboration": {
                            "type": "boolean"
                        },
                        "elaboration_text": {
                            "type": "string"
                        },
                        "reason": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "contains_unnecessary_filler",
                        "filler_type",
                        "filler_text",
                        "contains_unrequested_elaboration",
                        "elaboration_text",
                        "reason"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    properties = json.loads(grader_response.output_text)

    properties["pass"] = (
        not properties["contains_unnecessary_filler"]
        and not properties["contains_unrequested_elaboration"]
    )

    properties["score"] = 1 if properties["pass"] else 0

    return properties