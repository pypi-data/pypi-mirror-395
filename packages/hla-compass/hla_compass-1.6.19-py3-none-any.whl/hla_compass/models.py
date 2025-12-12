"""
Data models for HLA-Compass SDK.
These models provide strong typing for domain entities.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class BaseEntity(BaseModel):
    """Base model for domain entities"""
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

class Peptide(BaseEntity):
    """Peptide entity"""
    id: Optional[str] = None
    sequence: str
    length: Optional[int] = None
    mass: Optional[float] = None
    charge: Optional[float] = None
    modifications: Optional[List[str]] = None
    
    # Context-specific fields (may be present depending on query)
    abundance: Optional[float] = None 
    is_unique: Optional[bool] = None
    hla_alleles: Optional[List[str]] = None

class Protein(BaseEntity):
    """Protein entity"""
    id: Optional[str] = None
    accession: Optional[str] = None
    gene_name: Optional[str] = None
    organism: Optional[str] = None
    sequence: Optional[str] = None
    length: Optional[int] = None
    description: Optional[str] = None

class Sample(BaseEntity):
    """Sample entity"""
    id: Optional[str] = None
    name: Optional[str] = None
    sample_type: Optional[str] = None
    tissue: Optional[str] = None
    disease: Optional[str] = None
    cell_line: Optional[str] = None
    treatment: Optional[str] = None
    experiment_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BindingPrediction(BaseEntity):
    """HLA Binding Prediction result"""
    peptide: str
    allele: str
    score: float
    percentile: Optional[float] = None
    affinity: Optional[float] = None
    method: Optional[str] = None
