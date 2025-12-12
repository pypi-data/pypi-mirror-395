from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI()

"""
This utility module provides functions and classes to evaluate the semantic similarity between text responses.
It utilizes OpenAI's language model to score the similarity between an expected response and an actual response
on a numerical scale from 1 to 10.
"""


class Similarity_Score(BaseModel):
    """
    A data model to represent the semantic similarity score.

    Attributes:
        similarity_score (int): A score between 1 and 10 representing the semantic similarity
                                between two responses, where 1 indicates the responses are unrelated
                                and 10 indicates they are identical in meaning.
    """

    similarity_score: int = Field(
        description="Semantic similarity score between 1 and 10, where 1 means unrelated and 10 means identical."
    )


def compare_semantic_similarity(inputs: dict, reference_outputs: dict, outputs: dict):
    """
    Compare the semantic similarity of a given response to a reference response using OpenAI's language model.

    Args:
        inputs (dict): A dictionary with the question or context prompting the responses.
        reference_outputs (dict): A dictionary with the expected or correct response.
        outputs (dict): A dictionary with the actual response generated for evaluation.

    Returns:
        dict: A dictionary containing the similarity score and the key 'similarity'.
              The score is an integer between 1 and 10, where 1 indicates the response
              is entirely unrelated to the reference, and 10 indicates a response identical in meaning.
    """
    input_question = inputs["question"]
    reference_response = reference_outputs["output"]
    run_response = outputs["output"]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a semantic similarity evaluator. Compare the meanings of two responses to a question, "
                    "Reference Response and New Response, where the reference is the correct answer, and we are trying to judge if the new response is similar. "
                    "Provide a score between 1 and 10, where 1 means completely unrelated, and 10 means identical in meaning."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {input_question}\n Reference Response: {reference_response}\n Run Response: {run_response}",
            },
        ],
        response_format=Similarity_Score,
    )

    similarity_score = completion.choices[0].message.parsed
    return {"score": similarity_score.similarity_score, "key": "similarity"}
