
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


class Resource(AutoLower):
    pass


class DataResource(Resource):

    UNKNOWN= auto()  # type: ignore
    NOTSET= auto()  # type: ignore

    # --- Generic Reference ---
    DATA = auto()  # type: ignore
    DATASET = auto()  # type: ignore
    LOG=auto()  # type: ignore
    METADATA= auto()  # type: ignore
    CATALOG= auto()  # type: ignore
    IN_MEMORY_DATA = auto()  # type: ignore
    IN_MEMORY_METADATA = auto()  # type: ignore
    # --- COMMUNICATION  ---
    API = auto()  # type: ignore
    API_INTERNAL = auto()  # type: ignore
    API_EXTERNAL = auto()  # type: ignore
    SDK_EXTERNAL = auto()  # type: ignore
    SDK_INTERNAL = auto()  # type: ignore
    WEBSITE = auto()  # type: ignore
    INTERNET = auto()  # type: ignore
    RPC = auto()  # type: ignore
    GRPC = auto()  # type: ignore

    # --- Messaging ---
    MESSAGING_KAFKA = auto()  # type: ignore
    MESSAGING_SQS = auto()  # type: ignore
    MESSAGING_PUBSUB_TOPIC = auto()  # type: ignore
    # --- Real-time Communication ---
    REALTIME_WEBSOCKET = auto()  # type: ignore
     # --- Notifications ---
    NOTIFICATION_WEBHOOK = auto()  # type: ignore

    #-----------------
    #------ DBs ------
    #-----------------

    # --Generic Reference --
    DB= auto()  # type: ignore
    DB_TABLE = auto()  # type: ignore
    DB_RECORD = auto()  # type: ignore
    DB_COLLECTION = auto()  # type: ignore
    DB_DOCUMENT = auto()  # type: ignore
    DB_VIEW = auto()  # type: ignore

    # --SQL Databases--
    DB_ORACLE = auto()  # type: ignore
    DB_POSTGRESQL = auto()  # type: ignore
    DB_SQLSERVER = auto()  # type: ignore
    DB_MYSQL = auto()  # type: ignore
    DB_BIGQUERY = auto()  # type: ignore
    DB_BIGQUERY_TABLE = auto()  # type: ignore
    DB_SNOWFLAKE = auto()  # type: ignore
    DB_REDSHIFT = auto()  # type: ignore
    DB_ATHENA = auto()  # type: ignore
    # --NOSQL Databases--
    DB_MONGO = auto()  # type: ignore
    DB_REDIS = auto()  # type: ignore
    DB_CASSANDRA = auto()  # type: ignore
    DB_NEO4J = auto()  # type: ignore
    DB_FIRESTORE = auto()  # type: ignore
    DB_FIRESTORE_DOC = auto()  # type: ignore
    DB_FIRESTORE_COLLECTION = auto()  # type: ignore
    DB_DYNAMODB = auto()  # type: ignore
    # --NEWSQL Databases--
    DB_COCKROACHDB = auto()  # type: ignore
    DB_SPANNER = auto()  # type: ignore

    # --- Storage and DATA ---
    GCP_SECRET_MANAGER = auto()  # type: ignore
    LOCAL_STORAGE = auto()  # type: ignore
    GCS = auto()  # type: ignore
    S3 = auto()  # type: ignore
    AZURE_BLOB = auto()  # type: ignore
    HDFS = auto()  # type: ignore
    NFS = auto()  # type: ignore
    FTP = auto()  # type: ignore
    SFTP = auto()  # type: ignore
    # --- Files ---
    FILE = auto()  # type: ignore
    FILE_TXT = auto()  # type: ignore
    FILE_MARKDOWN = auto()  # type: ignore
    FILE_JSON = auto()  # type: ignore
    FILE_NDJSON = auto()  # type: ignore
    FILE_CSV = auto()  # type: ignore  
    FILE_WORD = auto()  # type: ignore
    FILE_EXCEL = auto()  # type: ignore
    FILE_PPT = auto()  # type: ignore
    FILE_PDF = auto()  # type: ignore
    FILE_PARQUET = auto()  # type: ignore
    FILE_AVRO = auto()  # type: ignore
    FILE_HTML = auto()  # type: ignore
    FILE_PYTHON = auto()  # type: ignore
    FILE_JAVA = auto()  # type: ignore
    FILE_JAVASCRIPT = auto()  # type: ignore
    FILE_CSS = auto()  # type: ignore
    FILE_R = auto()  # type: ignore
    FILE_SQL = auto()  # type: ignore
    FILE_XML = auto()  # type: ignore
    FILE_YAML = auto()  # type: ignore
    FILE_TOML = auto()  # type: ignore
    FILE_JPG = auto()  # type: ignore
    FILE_JPEG = auto()  # type: ignore
    FILE_PNG = auto()  # type: ignore
    FILE_GIF = auto()  # type: ignore
    FILE_SVG = auto()  # type: ignore
    FILE_MP4 = auto()  # type: ignore
    FILE_MP3 = auto()  # type: ignore
    FILE_WAV = auto()  # type: ignore
    FILE_AVI = auto()  # type: ignore
    FILE_MOV = auto()  # type: ignore
    FILE_MKV = auto()  # type: ignore
    FILE_ZIP = auto()  # type: ignore
    FILE_TAR = auto()  # type: ignore
    FILE_GZ = auto()  # type: ignore
    FILE_RAR = auto()  # type: ignore
    FILE_7Z = auto()  # type: ignore
    FILE_OTHER = auto()  # type: ignore

class ComputeResource(Resource):

    # --- Compute ---
    CLOUD_FUNCTION = auto()  # type: ignore
    CLOUD_RUN= auto()  # type: ignore
    CLOUD_RUN_SERVICE = auto()  # type: ignore
    CLOUD_RUN_JOB = auto()  # type: ignore
    CLOUD_COMPUTE_ENGINE = auto()  # type: ignore
    CLOUD_DATAPROC = auto()  # type: ignore
    CLOUD_DATAFLOW = auto()  # type: ignore
    CLOUD_BIGQUERY = auto()  # type: ignore
    CLOUD_LAMBDA = auto()  # type: ignore
    CLOUD_EC2 = auto()  # type: ignore
    CLOUD_EMR = auto()  # type: ignore
    CLOUD_GLUE = auto()  # type: ignore
    CLOUD_ATHENA = auto()  # type: ignore
    CLOUD_REDSHIFT = auto()  # type: ignore
    CLOUD_SYNAPSE_ANALYTICS = auto()  # type: ignore
    CLOUD_DATA_FACTORY = auto()  # type: ignore
    CLOUD_VIRTUAL_MACHINES = auto()  # type: ignore
    CLOUD_COMPUTE = auto()  # type: ignore
    CLOUD_DOCKER = auto()  # type: ignore
    CLOUD_KUBERNETES = auto()  # type: ignore
    CLOUD_GKE = auto()  # type: ignore
    CLOUD_AKS = auto()  # type: ignore
    CLOUD_EKS = auto()  # type: ignore
    CLOUD_AZURE_FUNCTIONS = auto()  # type: ignore
    CLOUD_AZURE_VIRTUAL_MACHINES = auto()  # type: ignore
    CLOUD_AZURE_SYNAPSE_ANALYTICS = auto()  # type: ignore
    CLOUD_AZURE_DATA_FACTORY = auto()  # type: ignore
    CLOUD_AZURE_DATABRICKS = auto()  # type: ignore
    CLOUD_AZURE_ANALYTICS = auto()  # type: ignore
    CLOUD_AZURE_SQL = auto()  # type: ignore
    CLOUD_AZURE_COSMOSDB = auto()  # type: ignore
    CLOUD_AZURE_TABLE = auto()  # type: ignore
    CLOUD_AZURE_BLOB = auto()  # type: ignore
    CLOUD_AZURE_FILE = auto()  # type: ignore
    CLOUD_AZURE_QUEUE = auto()  # type: ignore
    CLOUD_AZURE_EVENTHUB = auto()  # type: ignore
    CLOUD_AZURE_NOTIFICATIONHUB = auto()  # type: ignore
    CLOUD_AZURE_CACHE = auto()  # type: ignore
    CLOUD_AZURE_REDIS = auto()  # type: ignore
    CLOUD_AZURE_SEARCH = auto()  # type: ignore
    LOCAL_COMPUTE = auto()  # type: ignore
    LOCAL_JUPYTER_NOTEBOOK = auto()  # type: ignore
    LOCAL_SCRIPT = auto()  # type: ignore
    LOCAL_PIPELINE = auto()  # type: ignore
    LOCAL_ORCHESTRATOR_ETL = auto()  # type: ignore
    LOCAL_ETL = auto()  # type: ignore
    LOCAL_SERVER = auto()  # type: ignore
    LOCAL_DOCKER = auto()  # type: ignore
    LOCAL_KUBERNETES = auto()  # type: ignore
    LOCAL_GCP_CLOUD_FUNCTION = auto()  # type: ignore


class CloudProvider(AutoLower):
    GCP = auto()  # type: ignore
    AWS = auto()  # type: ignore
    AZURE = auto()  # type: ignore
    IBM = auto()  # type: ignore
    ALIBABA = auto()  # type: ignore
    NO_CLOUD = auto()  # type: ignore
    CLOUD_AGNOSTIC = auto()  # type: ignore
    OTHER = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore


class ProcessorResource(Resource):

    CPU_INTEL = auto()  # type: ignore
    CPU_AMD = auto()  # type: ignore
    CPU_ARM = auto()  # type: ignore
    GPU_NVIDIA = auto()  # type: ignore
    GPU_AMD = auto()  # type: ignore
    GPU_INTEL = auto()  # type: ignore
    TPU_GOOGLE = auto()  # type: ignore
    TPU_INTEL = auto()  # type: ignore
    TPU_AMD = auto()  # type: ignore

class AbstractResource(Resource):
    MICROSERVICE = auto()  # type: ignore
    TRACEMON = auto()  # type: ignore

    PIPELINE= auto()  # type: ignore
    PIPELINEFLOW= auto()  # type: ignore
    PIPELINEMON= auto()  # type: ignore
    PIPELINE_STEP= auto()  # type: ignore
    PIPELINE_TASK = auto()  # type: ignore
    PIPELINE_OPERATION = auto()  # type: ignore
    PIPELINE_TASK_SEQUENCE = auto()  # type: ignore
    PIPELINE_GROUP= auto()  # type: ignore
    PIPELINE_DYNAMIC_ITERATOR = auto()  # type: ignore
    PIPELINE_ITERATION = auto()  # type: ignore
    PIPELINE_SUBJECT= auto()  # type: ignore
    PIPELINE_SUBJECT_SEQUENCE= auto()  # type: ignore

    RECORD= auto()  # type: ignore
    SCRIPT = auto()  # type: ignore
    JOB= auto()  # type: ignore
