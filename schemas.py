from typing import List
from pydantic import BaseModel, Field


# Reflection will hold all information about the reflection
class Reflection(BaseModel):
    # Important information that is missing from the original LLM output
    missing: str = Field(description="Critique of what is missing.")

    # Information that does not add any value
    superfluous: str = Field(description="Critique of what is superfluous.")


class AnswerQuestion(BaseModel):
    """Answer a question based on the provided context."""

    answer: str = Field(description="~250 words detailed answer to the question.")
    reflection: Reflection = Field(description="your reflection on the initial answer.")
    search_queries: List[str] = Field(
        description="3-5 search queries to research improvements to the current answer further."
    )


class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question"""

    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )
