"""
Constants for HLA-Compass SDK
"""

# Amino acids
AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"
AMINO_ACID_NAMES = {
    "A": "Alanine",
    "C": "Cysteine",
    "D": "Aspartic acid",
    "E": "Glutamic acid",
    "F": "Phenylalanine",
    "G": "Glycine",
    "H": "Histidine",
    "I": "Isoleucine",
    "K": "Lysine",
    "L": "Leucine",
    "M": "Methionine",
    "N": "Asparagine",
    "P": "Proline",
    "Q": "Glutamine",
    "R": "Arginine",
    "S": "Serine",
    "T": "Threonine",
    "V": "Valine",
    "W": "Tryptophan",
    "Y": "Tyrosine",
}

# Amino acid properties
HYDROPHOBIC_AA = set("AILMFWYV")
CHARGED_AA = set("DEKR")
POLAR_AA = set("STNQ")
AROMATIC_AA = set("FWY")
POSITIVE_AA = set("KR")
NEGATIVE_AA = set("DE")

# Peptide lengths
MIN_PEPTIDE_LENGTH = 8
MAX_PEPTIDE_LENGTH = 15
TYPICAL_MHC_I_LENGTHS = [8, 9, 10, 11]
TYPICAL_MHC_II_LENGTHS = [12, 13, 14, 15, 16, 17, 18, 19, 20]

# Common HLA alleles
SUPPORTED_HLA_ALLELES = [
    # HLA Class I - A locus
    "HLA-A*01:01",
    "HLA-A*02:01",
    "HLA-A*03:01",
    "HLA-A*11:01",
    "HLA-A*24:02",
    "HLA-A*26:01",
    "HLA-A*68:01",
    "HLA-A*68:02",
    # HLA Class I - B locus
    "HLA-B*07:02",
    "HLA-B*08:01",
    "HLA-B*15:01",
    "HLA-B*27:05",
    "HLA-B*35:01",
    "HLA-B*40:01",
    "HLA-B*44:02",
    "HLA-B*44:03",
    "HLA-B*51:01",
    "HLA-B*57:01",
    "HLA-B*58:01",
    # HLA Class I - C locus
    "HLA-C*01:02",
    "HLA-C*03:03",
    "HLA-C*04:01",
    "HLA-C*05:01",
    "HLA-C*06:02",
    "HLA-C*07:01",
    "HLA-C*07:02",
    "HLA-C*08:02",
    # HLA Class II - DR locus
    "HLA-DRB1*01:01",
    "HLA-DRB1*03:01",
    "HLA-DRB1*04:01",
    "HLA-DRB1*04:05",
    "HLA-DRB1*07:01",
    "HLA-DRB1*08:02",
    "HLA-DRB1*09:01",
    "HLA-DRB1*11:01",
    "HLA-DRB1*12:01",
    "HLA-DRB1*13:02",
    "HLA-DRB1*15:01",
    # HLA Class II - DQ locus
    "HLA-DQA1*01:01",
    "HLA-DQA1*01:02",
    "HLA-DQA1*03:01",
    "HLA-DQA1*05:01",
    "HLA-DQB1*02:01",
    "HLA-DQB1*03:01",
    "HLA-DQB1*03:02",
    "HLA-DQB1*05:01",
    "HLA-DQB1*06:02",
    # HLA Class II - DP locus
    "HLA-DPA1*01:03",
    "HLA-DPA1*02:01",
    "HLA-DPB1*01:01",
    "HLA-DPB1*02:01",
    "HLA-DPB1*04:01",
    "HLA-DPB1*04:02",
]

# HLA supertypes
HLA_SUPERTYPES = {
    "A1": ["HLA-A*01:01", "HLA-A*26:01", "HLA-A*32:01"],
    "A2": ["HLA-A*02:01", "HLA-A*02:03", "HLA-A*02:06", "HLA-A*68:02"],
    "A3": ["HLA-A*03:01", "HLA-A*11:01", "HLA-A*31:01", "HLA-A*68:01"],
    "A24": ["HLA-A*24:02", "HLA-A*23:01"],
    "B7": ["HLA-B*07:02", "HLA-B*35:01", "HLA-B*51:01", "HLA-B*53:01"],
    "B27": ["HLA-B*27:05", "HLA-B*39:01", "HLA-B*38:01", "HLA-B*48:01"],
    "B44": ["HLA-B*44:02", "HLA-B*44:03", "HLA-B*40:01", "HLA-B*18:01"],
    "B58": ["HLA-B*57:01", "HLA-B*58:01"],
    "B62": ["HLA-B*15:01", "HLA-B*52:01"],
}

# Mass constants (in Daltons)
AMINO_ACID_MASSES = {
    "A": 71.03711,
    "C": 103.00919,
    "D": 115.02694,
    "E": 129.04259,
    "F": 147.06841,
    "G": 57.02146,
    "H": 137.05891,
    "I": 113.08406,
    "K": 128.09496,
    "L": 113.08406,
    "M": 131.04049,
    "N": 114.04293,
    "P": 97.05276,
    "Q": 128.05858,
    "R": 156.10111,
    "S": 87.03203,
    "T": 101.04768,
    "V": 99.06841,
    "W": 186.07931,
    "Y": 163.06333,
}
WATER_MASS = 18.01528

# Common post-translational modifications
PTM_MASSES = {
    "Acetylation": 42.01056,
    "Phosphorylation": 79.96633,
    "Methylation": 14.01565,
    "Ubiquitination": 114.04293,
    "Oxidation": 15.99491,
    "Deamidation": 0.98402,
}

# API limits
MAX_PEPTIDES_PER_REQUEST = 1000
MAX_PROTEINS_PER_REQUEST = 100
MAX_SAMPLES_PER_REQUEST = 500
MAX_RESULTS_PER_PAGE = 1000
DEFAULT_PAGE_SIZE = 100

# File size limits
MAX_INPUT_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_OUTPUT_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_TOTAL_OUTPUT_SIZE = 500 * 1024 * 1024  # 500 MB

# Execution limits
DEFAULT_LAMBDA_TIMEOUT = 300  # 5 minutes
MAX_LAMBDA_TIMEOUT = 900  # 15 minutes
DEFAULT_FARGATE_TIMEOUT = 3600  # 1 hour
MAX_FARGATE_TIMEOUT = 28800  # 8 hours

# Memory limits (MB)
MIN_LAMBDA_MEMORY = 128
MAX_LAMBDA_MEMORY = 10240
DEFAULT_LAMBDA_MEMORY = 512
MIN_FARGATE_MEMORY = 512
MAX_FARGATE_MEMORY = 30720
DEFAULT_FARGATE_MEMORY = 2048

# Rate limits per tier
RATE_LIMITS = {
    "foundational": {
        "requests_per_hour": 100,
        "concurrent_jobs": 5,
        "data_export_gb_per_month": 10,
    },
    "advanced": {
        "requests_per_hour": 1000,
        "concurrent_jobs": 50,
        "data_export_gb_per_month": 100,
    },
    "strategic": {
        "requests_per_hour": None,  # Unlimited
        "concurrent_jobs": None,  # Unlimited
        "data_export_gb_per_month": None,  # Unlimited
    },
}

# Scientific constants
AVOGADRO_NUMBER = 6.02214076e23
GAS_CONSTANT = 8.314462618  # J/(mol·K)
STANDARD_TEMPERATURE = 298.15  # K (25°C)

# Binding affinity thresholds (nM)
STRONG_BINDER_THRESHOLD = 50
WEAK_BINDER_THRESHOLD = 500

# Module categories
MODULE_CATEGORIES = [
    "analysis",
    "prediction",
    "visualization",
    "data-processing",
    "machine-learning",
    "quality-control",
    "annotation",
    "export",
    "import",
    "utilities",
]

# Supported file formats
SUPPORTED_INPUT_FORMATS = [
    ".json",
    ".csv",
    ".tsv",
    ".txt",
    ".fasta",
    ".fastq",
    ".mgf",
    ".mzml",
    ".xlsx",
]

SUPPORTED_OUTPUT_FORMATS = [
    ".json",
    ".csv",
    ".tsv",
    ".xlsx",
    ".pdf",
    ".html",
    ".png",
    ".svg",
]

# Documentation URLs for error messages
DOCS_BASE_URL = "https://docs.alithea.bio"
DOCS_URLS = {
    "quickstart": f"{DOCS_BASE_URL}/quickstart",
    "auth": f"{DOCS_BASE_URL}/sdk-reference/guides/authentication",
    "data_access": f"{DOCS_BASE_URL}/sdk-reference/guides/data-access",
    "testing": f"{DOCS_BASE_URL}/sdk-reference/guides/testing",
    "publishing": f"{DOCS_BASE_URL}/sdk-reference/guides/publishing",
    "manifest": f"{DOCS_BASE_URL}/sdk-reference/reference/module#manifest",
    "module_api": f"{DOCS_BASE_URL}/sdk-reference/reference/module",
    "cli": f"{DOCS_BASE_URL}/sdk-reference/reference/cli",
    "llm_context": f"{DOCS_BASE_URL}/llm-context",
    "examples": "https://github.com/AlitheaBio/Compass-WIKI/tree/main/examples",
    "issues": "https://github.com/AlitheaBio/Compass-WIKI/issues",
}


def doc_link(topic: str) -> str:
    """Get documentation URL for a topic. Use in error messages."""
    return DOCS_URLS.get(topic, DOCS_BASE_URL)
