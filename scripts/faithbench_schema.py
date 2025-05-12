# The data schema for FaithBench data released in JSON format

from typing import List, Dict, Any, Literal, TypedDict, Optional
from pydantic import BaseModel, Field
from enum import Enum
# The label of a text span annotated by a human

class FaithBenchLabel(str, Enum):
    Unwanted = "Unwanted"
    Unwanted_Intrinsic = "Unwanted.Intrinsic"
    Unwanted_Extrinsic = "Unwanted.Extrinsic"
    Questionable = "Questionable"
    Benign = "Benign"

# The annotation of a text span by a human
class FaithBenchAnnotation(BaseModel):
    annot_id: int
    annotator_id: str
    annotator_name: str
    label: List[FaithBenchLabel]
    note: str
    summary_span: str
    summary_start: int
    summary_end: int
    source_span: Optional[str] = None
    source_start: Optional[int] = None
    source_end: Optional[int] = None

# meta info about the sample such as the summarizer LLM, the prediction of SOTA detectors, and the raw sample id
class FaithBenchMetaInfo(BaseModel):
    summarizer: str
    hhemv1: float
    hhem_2_1: float = Field(alias="hhem-2.1")
    hhem_2_1_english: float = Field(alias="hhem-2.1-english")
    trueteacher: int
    true_nli: Optional[int] = None # one sample has this exception
    gpt_35_turbo: int = Field(alias="gpt-3.5-turbo")
    gpt_4_turbo: int = Field(alias="gpt-4-turbo")
    gpt_4o: int
    raw_sample_id: int

    class Config:
        populate_by_name = True

# A sample in FaithBench
class FaithBenchSample(BaseModel):
    sample_id: int # ID in this batch
    source: str
    summary: str
    annotations: List[FaithBenchAnnotation]=[] # [] if the sample is not annotated
    metadata: FaithBenchMetaInfo

class FaithBenchBatch(BaseModel):
    samples: List[FaithBenchSample]

class FaithBenchTextPair(BaseModel):
    source: str
    summary: str
    label: Literal[0,1]
