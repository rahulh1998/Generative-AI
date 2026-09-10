from typing import Literal

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser



model = ChatOllama(
    model="gemma4:e2b"
)



class FlightRecommendation(BaseModel):

    flight_number: str

    recommended_fare: float = Field(
        gt=0,
        description="Recommended fare in GBP"
    )

    direction: Literal[
        "increase",
        "decrease",
        "hold"
    ]

    confidence_score: float = Field(
        ge=0,
        le=1,
        description="Confidence score in the range 0 to 1"
    )

    reasons: list[str] = Field(
        min_length=1
    )


parser = PydanticOutputParser(
    pydantic_object=FlightRecommendation
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a flight pricing expert."
    ),
    (
        "human",
        """
Analyse this flight and provide a pricing recommendation.

Flight information:

{flight}

{format_instructions}
"""
    )
])

prompt = prompt.partial(
    format_instructions=parser.get_format_instructions()
)


chain = prompt | model | parser

result = chain.invoke(
    {
        "flight": """
Flight: LS123
Current fare: 135
Load factor: 0.82
DTD: 5
ROS: 1.25
"""
    }
)



print(result)

print("-" * 50)

print("Flight Number:", result.flight_number)
print("Recommended Fare:", result.recommended_fare)
print("Confidence:", result.confidence_score)
print("Direction:", result.direction)
print("Reasons:")
for i, r in enumerate(result.reasons):
    print(f"{i+1}. {r}")