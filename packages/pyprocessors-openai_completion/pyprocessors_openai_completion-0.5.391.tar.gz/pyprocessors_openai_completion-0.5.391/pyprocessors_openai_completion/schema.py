from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class Span(BaseModel):
    end: int = Field(..., description="End index of the span in the text", example=15)


class SegmentV2(BaseModel):
    id: str = Field(None, description="Identifier of the segment")
    mentions: Optional[Dict[str, List[str]]] = Field(None, description="Mentions grouped by labels")


class NERV2(BaseModel):
    __root__: List[SegmentV2]


class MentionV3(Span):
    label: str = Field(
        None, description="Label of the annotation", example="ORG"
    )
    text: Optional[str] = Field(
        None, description="Covering text of the annotation", example="Kairntech"
    )
    offset: int = Field(
        ..., description="Start index of the span in the text", example=5
    )


class SegmentV3(BaseModel):
    id: str = Field(None, description="Identifier of the segment")
    mentions: Optional[List[MentionV3]] = Field(None, description="Mentions")


class NERV3(BaseModel):
    __root__: List[SegmentV3]
