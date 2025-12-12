from pydantic import BaseModel, Field
from typing import Optional


class CustomModel(BaseModel):
    """
    Base class for custom models that can be subclassed to define
    custom record types for the TMS integration system.
    
    Subclasses should override the satzart field to define their
    own record type identifier.
    """
    satzart: str = Field(..., description="Record type identifier")
    referenz: str = Field(..., description="Reference identifier")
    
    class Config:
        # Allow arbitrary types for extensibility
        arbitrary_types_allowed = True
        # Allow extra fields in subclasses
        extra = 'allow'
