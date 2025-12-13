# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import StrEnum, auto
class AutoLower(StrEnum):
    """
    StrEnum contrary to simple Enum is of type `str`, so it can be used as a string.
    StrEnum whose `auto()  # type: ignore` values are lower-case.
    (Identical to StrEnum's own default, but keeps naming symmetrical.)
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()            # StrEnum already does this

class AutoUpper(StrEnum):
    """
    StrEnum contrary to simple Enum is of type `str`, so it can be used as a string.
    StrEnum whose `auto()  # type: ignore` values stay as-is (UPPER_CASE).
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name                    # keep original upper-case


class DataPrimaryCategory(AutoLower):
    ### CORE DATA SPECIFIC ########
    HISTORIC = auto()  # type: ignore # Historical raw data, usually accurate and complete
    LIVE=auto()  # type: ignore # Real-time data, not always certain, can have error. Live and Historic can intersect. Live relates to Streaming data or Websockets data..
    ANALYTICS=auto()  # type: ignore # Analytical data and modelling, derived from historical and prediction data. Normally shall be making Human readable sense. vs. Features
    FEATURES=auto()  # type: ignore # Features data, used for training models
    PREDICTION=auto()  # type: ignore # Predictive data, based on models and simulations
    SIMULATIONS=auto()  # type: ignore # Simulation data, based on models and simulations
    ARCHIVES=auto()  # type: ignore # In the sense of very old and potentially less accurate data, like decades old data, potentially classified , hard to access data

    #### GOVERNANCE AND DIMENSIONAL ########
    GOVERNANCE=auto()  # type: ignore # # control-plane / governance / ops
    OBSERVABILITY=auto()  # type: ignore # Log data, used for logging and monitoring
    #### GENERICS ########
    MULTIPLE = auto()  # type: ignore # Multiple categories, used for data that can belong to multiple categories
    UNKNOWN = auto()  # type: ignore # Used when the primary category is not specified or unknown

class Subdomain(AutoLower): # EXCEPT FOR DATASETS , these are all GOVERNANCE DataPrimaryCategory
    DATASETS = auto()  # type: ignore
    CONTROLS = auto()  # type: ignore  # Includes control plane, reference data , catalogs etc.
    CATALOGS = auto()  # type: ignore  # Asset catalog data, used for asset metadata and discovery
    MONITORING = auto()  # type: ignore  # Log data, used for logging and monitoring
    UNKNOWN = auto()  # type: ignore

class DataStructureLevel(AutoLower):
    STRUCTURED = auto()     # type: ignore   # e.g., table with schema
    SEMI_STRUCTURED = auto()  # type: ignore # JSON, YAML, etc. 
    UNSTRUCTURED = auto()    # type: ignore  # free text, raw image, PDF
    MULTIPLE = auto()    # type: ignore  # Mixed structure types
    UNKNOWN = auto()    # type: ignore  # Used when the data structure level is not specified or unknown

class DataModality(AutoLower):
    """Types of input data for models."""
    TEXT = auto()  # type: ignore # encompasses plain text, documents, articles, books, sql, code etc.
    SCHEMA = auto()  # type: ignore
    TABULAR = auto()  # type: ignore  # rows/cols (can hold numeric + categorical)
    JSON_TEXT = auto()  # type: ignore
    JSON_TABULAR = auto()  # type: ignore
    JSON_MIXED = auto()  # type: ignore
    NUMERICAL = auto()  # type: ignore
    CATEGORICAL = auto()  # type: ignore
    IMAGE = auto()  # type: ignore
    AUDIO = auto()  # type: ignore
    VIDEO = auto()  # type: ignore
    GRAPH = auto()  # type: ignore
    GEOSPATIAL = auto()  # type: ignore
    OMICS = auto()  # type: ignore  # e.g., genomics, proteomics
    MULTIMODAL = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore  # Used when the data modality is not specified or unknown

class ModalityContentDynamics(AutoLower):
    """Dynamics of data modality."""
    STATIC = auto()  # type: ignore  # Static data, does not change over time
    STATIC_VERSIONED = auto()  # type: ignore  # Versioned data, changes over time but retains history
    SEQUENCE= auto()  # type: ignore  # Regular sequence data, e.g., time series with fixed intervals
    TIMESERIES= auto()  # type: ignore  # Regular time series data, e.g., daily stock prices
    MULTIPLE = auto()  # type: ignore  # Mixed data, e.g., text + images
    UNKNOWN = auto()  # type: ignore  # Used when the modality dynamics is not specified or unknown

class ModalityContentSemantics(AutoLower):
    """Semantics of data modality content."""

    # Text - NATURAL LANGUAGE
    STORY = auto()  # type: ignore  # Narrative text, articles, books
    FACTUAL = auto()  # type: ignore  # Factual text, reports, documentation
    ARTICLE = auto()  # type: ignore  # News articles, blog posts
    POEM = auto()  # type: ignore  # Poetry, creative writing
    LEGAL = auto()  # type: ignore  # Legal documents, contracts
    MATHEMATICS = auto()  # type: ignore  # Mathematical text, equations
    PHYSICS = auto()  # type: ignore  # Physics papers, research articles
    CHEMISTRY = auto()  # type: ignore  # Chemistry papers, research articles
    BIOLOGY = auto()  # type: ignore  # Biology papers, research articles
    HISTORY = auto()  # type: ignore  # History books, historical documents
    LITERATURE = auto()  # type: ignore  # Literature papers, essays
    ENCYCLOPEDIA = auto()  # type: ignore  # Encyclopedic text, reference materials
    NEWS = auto()  # type: ignore  # News articles, reports
    BLOG = auto()  # type: ignore  # Blog posts, opinion pieces
    REVIEW = auto()  # type: ignore  # Reviews, critiques
    INSTRUCTIONAL = auto()  # type: ignore  # How-to guides, tutorials
    TECHNICAL = auto()  # type: ignore  # Technical manuals, specifications
    SCIENTIFIC = auto()  # type: ignore  # Scientific papers, research articles
    MEDICAL_REPORT = auto()  # type: ignore  # Medical records, clinical notes
    MEDICAL_RECORDS = auto()  # type: ignore  # Medical records, clinical notes
    CHAT = auto()  # type: ignore  # Chat logs, conversations
    SOCIAL_MEDIA_POST = auto()  # type: ignore  # Social media posts, tweets
    FINANCIAL = auto()  # type: ignore  # Financial reports, statements
    FINANCIAL_REPORT = auto()  # type: ignore  # Financial reports, statements

    ## Text - CODE
    CODE = auto()  # type: ignore  # Programming code, scripts
    CODE_JAVA = auto()  # type: ignore  # Java code
    CODE_PYTHON = auto()  # type: ignore  # Python code
    CODE_JAVASCRIPT = auto()  # type: ignore  # JavaScript code
    CODE_HTML = auto()  # type: ignore  # HTML code
    CODE_CSS = auto()  # type: ignore  # CSS code
    CODE_SQL = auto()  # type: ignore  # SQL code, queries
    CODE_R = auto()  # type: ignore  # R code
    CODE_SHELL = auto()  # type: ignore  # Shell scripts, bash
    CODE_OTHER = auto()  # type: ignore  # Other programming languages
    
    ## LOGS
    SYSTEM_LOG = auto()  # type: ignore  # System logs, application logs
    APPLICATION_LOG = auto()  # type: ignore  # Application logs, error logs
    NETWORK_LOG = auto()  # type: ignore  # Network logs, traffic logs
    SENSOR_LOG = auto()  # type: ignore  # Sensor data, IoT logs

     # Image
    IMAGE_PHOTO = auto()  # type: ignore  # Photographs, images
    IMAGE_DIAGRAM = auto()  # type: ignore  # Diagrams, charts
    IMAGE_MEDICAL_SCAN = auto()  # type: ignore  # Medical images, X-rays
    IMAGE_CHART = auto()  # type: ignore  # Charts, graphs
    IMAGE_ART = auto()  # type: ignore  # Artwork, illustrations
    IMAGE_MAP = auto()  # type: ignore  # Maps, geographic data

    # Audio
    AUDIO_SPEECH = auto()  # type: ignore  # Speech audio, recordings
    AUDIO_MUSIC = auto()  # type: ignore  # Music audio, songs
    AUDIO_ENVIRONMENTAL = auto()  # type: ignore  # Environmental sounds, ambience
    AUDIO_PODCAST = auto()  # type: ignore  # Podcasts, spoken word
    AUDIO_VOICE_ASSISTANT = auto()  # type: ignore  # Voice assistant commands, interactions
    AUDIO_CALL = auto()  # type: ignore  # Call center recordings, customer service

    # Video
    VIDEO_CLIP = auto()  # type: ignore  # Short video clips
    VIDEO_MOVIE = auto()  # type: ignore  # Movies, video clips
    VIDEO_SURVEILLANCE = auto()  # type: ignore  # Surveillance footage, security videos
    VIDEO_EDUCATIONAL = auto()  # type: ignore  # Educational videos, tutorials
    VIDEO_LIVE_STREAM = auto()  # type: ignore  # Live streams, broadcasts
    VIDEO_CONFERENCE = auto()  # type: ignore  # Video conference recordings, meetings

    # Graph
    GRAPH_SOCIAL = auto()  # type: ignore  # Social networks, connections
    GRAPH_KNOWLEDGE = auto()  # type: ignore  # Knowledge graphs, ontologies
    GRAPH_BIOLOGICAL = auto()  # type: ignore  # Biological networks, pathways
    GEOSPATIAL_MAP = auto()  # type: ignore  # Maps, geographic data
    GEOSPATIAL_SATELLITE = auto()  # type: ignore  # Satellite imagery, remote sensing
    GEOSPATIAL_URBAN = auto()  # type: ignore  # Urban data, city planning

    # Omics
   
    OMICS_GENOMICS = auto()  # type: ignore  # Genomic data, DNA sequences
    OMICS_VARIANT = auto()  # type: ignore  # Variant data, SNPs, mutations
    OMICS_PROTEOMICS = auto()  # type: ignore  # Proteomic
    OMICS_TRANSCRIPTOMICS = auto()  # type: ignore  # Transcriptomic data, RNA sequences
    OMICS_METABOLOMICS = auto()  # type: ignore  # Metabolomic data, metabolites
    OMICS_EPIGENOMICS = auto()  # type: ignore  # Epigenomic data, DNA modifications
    OMICS_MULTIOMICS = auto()  # type: ignore  # Multi-omics data, integrated datasets
    
    # Mixed / Multimodal
    MULTIMODAL_MIXED = auto()  # type: ignore  # Mixed modalities, e.g., text + images
    UNKNOWN = auto()  # type: ignore  # Used when the content semantics is not specified or unknown

    
class DatasetLineage(AutoLower):
    """Dataset lineage information."""
    # EXTERNAL DATA
    PRIMARY_SUPPLIER = auto()  # type: ignore
    SECONDARY_SUPPLIER = auto()  # type: ignore

    # INTERNAL DATA
    SOURCE_OF_TRUTH = auto()  # type: ignore
    EXACT_COPY = auto()  # type: ignore
    PACKAGED_COPY = auto()  # type: ignore
    ANALYTICS_DERIVATIVE = auto()  # type: ignore
    FEATURES_DERIVATIVE = auto()  # type: ignore
    PREDICTION_GENERATED = auto()  # type: ignore
    INTERMEDIARY_DERIVATIVE = auto()  # type: ignore
    MIXED_COPIES = auto()  # type: ignore
    MIXED_COPIES_PACKAGED = auto()  # type: ignore #usually means subsampled or aggregated data
    MIXED_ANALYTICS = auto()  # type: ignore
    MIXED_FEATURES = auto()  # type: ignore
    BACKUP = auto()  # type: ignore
    TEMPORARY = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore


class DatasetScope(AutoLower):
    """Types of Dataset scope."""

    FULL_DATASET = auto()  # type: ignore
    LATEST_RECORD = auto()  # type: ignore #IF SINGLE LATEST RECORD
    INCREMENTAL_DATASET = auto()  # type: ignore #IF INCREMENTAL LATEST RECORDS
    BACKFILLING_DATASET = auto()  # type: ignore
    PARTIAL_DATASET = auto()  # type: ignore
    SUBSAMPLED_DATASET = auto()  # type: ignore
    FILTERED_DATASET = auto()  # type: ignore

    TRAINING_DATASET = auto()  # type: ignore
    VALIDATION_DATASET = auto()  # type: ignore
    TEST_DATASET = auto()  # type: ignore
    TRAINING_AND_VALIDATION_DATASET = auto()  # type: ignore
    CUSTOM_RANGE_DATASET = auto()  # type: ignore
    CROSS_VALIDATION_FOLD = auto()  # type: ignore
    HOLDOUT_DATASET = auto()  # type: ignore

    MIXED_DATASETS = auto()  # type: ignore



class DataSplitStrategy(AutoLower):
    """Data splitting strategies."""
    RANDOM_SPLIT = auto()  # type: ignore
    TIME_SERIES_SPLIT = auto()  # type: ignore
    GROUP_SPLIT = auto()  # type: ignore
    GEOGRAPHICAL_SPLIT = auto()  # type: ignore
    TEMPORAL_SPLIT = auto()  # type: ignore
    CROSS_VALIDATION = auto()  # type: ignore
    LEAVE_ONE_OUT = auto()  # type: ignore
    LEAVE_P_OUT = auto()  # type: ignore
    HOLDOUT = auto()  # type: ignore
    BOOTSTRAP = auto()  # type: ignore


class DatasetAttribute(AutoLower):
    RECENT_DATE = auto()  # type: ignore
    RECENT_TIMESTAMP = auto()  # type: ignore
    RECENT_DATETIME = auto()  # type: ignore
    OLDEST_DATE = auto()  # type: ignore
    OLDEST_TIMESTAMP = auto()  # type: ignore
    OLDEST_DATETIME = auto()  # type: ignore
    MAX_VALUE = auto()  # type: ignore
    MIN_VALUE = auto()  # type: ignore
    TOTAL_COUNT = auto()  # type: ignore
    TOTAL_SUM = auto()  # type: ignore
    MEAN = auto()  # type: ignore
    MEDIAN = auto()  # type: ignore
    MODE = auto()  # type: ignore
    STANDARD_DEVIATION = auto()  # type: ignore
    NB_FIELDS_PER_RECORDS = auto()  # type: ignore


