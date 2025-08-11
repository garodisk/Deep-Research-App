from typing import List, Optional
from pydantic import BaseModel, Field

class WebSearchItem(BaseModel):
    reason: str = Field(description="Why this search matters")
    query: str = Field(description="Search term")

class WebSearchPlan(BaseModel):
    searches: List[WebSearchItem] = Field(description="Searches to perform")

class Citation(BaseModel):
    url: str = Field(description="Exact source URL used in the report")
    title: Optional[str] = Field(default=None, description="Title if known")

class ReportData(BaseModel):
    short_summary: str
    outline_markdown: str
    markdown_report: str
    follow_up_questions: List[str]
    final_citations: List[Citation]