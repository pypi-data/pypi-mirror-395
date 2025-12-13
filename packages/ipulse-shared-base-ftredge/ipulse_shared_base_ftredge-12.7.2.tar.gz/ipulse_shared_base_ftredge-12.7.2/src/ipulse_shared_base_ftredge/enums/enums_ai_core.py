# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import StrEnum, auto

# ──────────────────────────────────────────────────────────────────────────────
# Base enum classes following the established patterns
# ──────────────────────────────────────────────────────────────────────────────

class AutoLower(StrEnum):
    """
    StrEnum whose `auto()  # type: ignore` values are lower-case.
    Used for most AI core enums that need string representation.
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

class AutoUpper(StrEnum):
    """
    StrEnum whose `auto()  # type: ignore` values stay as-is (UPPER_CASE).
    Used for status and constant-like enums.
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

# ──────────────────────────────────────────────────────────────────────────────
# Learning Paradigms (Industry Standard)
# ──────────────────────────────────────────────────────────────────────────────

class AILearningParadigm(AutoLower):
    """AI learning paradigm classifications (industry standard)."""
    SUPERVISED = auto()  # type: ignore
    UNSUPERVISED = auto()  # type: ignore
    SEMI_SUPERVISED = auto()  # type: ignore
    REINFORCEMENT = auto()  # type: ignore
    TRANSFER_LEARNING = auto()  # type: ignore
    ACTIVE_LEARNING = auto()  # type: ignore

# ──────────────────────────────────────────────────────────────────────────────
# AI Problem Types - What the AI is designed to solve
# ──────────────────────────────────────────────────────────────────────────────

class AIProblemType(AutoLower):
    """Types of problems that AI models can solve."""
    REGRESSION = auto()  # type: ignore
    CLASSIFICATION = auto()  # type: ignore
    PREDICTION = auto()  # type: ignore
    RANKING = auto()  # type: ignore
    CLUSTERING = auto()  # type: ignore
    ANOMALY_DETECTION = auto()  # type: ignore
    DIMENSIONALITY_REDUCTION = auto()  # type: ignore
    CODING = auto()  # type: ignore
    GENERATION = auto()  # type: ignore
    OBJECT_DETECTION = auto()  # type: ignore
    TRANSLATION = auto()  # type: ignore
    TRANSCRIPTION = auto()  # type: ignore
    ANALYSIS = auto()  # type: ignore
    SUMMARIZATION = auto()  # type: ignore
    QA = auto()  # type: ignore
    RL_CONTROL = auto()  # type: ignore

# ──────────────────────────────────────────────────────────────────────────────
# Unified Algorithm Classification - What specific algorithm is used
# ──────────────────────────────────────────────────────────────────────────────

class AIAlgorithm(AutoLower):
    """Comprehensive algorithm classification covering all AI/ML approaches."""
    
    # Linear / GLM
    LINEAR_REGRESSION = auto()  # type: ignore
    LOGISTIC_REGRESSION = auto()  # type: ignore
    RIDGE = auto()  # type: ignore
    LASSO = auto()  # type: ignore
    ELASTIC_NET = auto()  # type: ignore

    # Neighbors / Bayes / SVM
    KNN = auto()  # type: ignore
    NAIVE_BAYES = auto()  # type: ignore
    SVM = auto()  # type: ignore

    # Trees & boosting
    DECISION_TREE = auto()  # type: ignore
    RANDOM_FOREST = auto()  # type: ignore
    GRADIENT_BOOSTING = auto()  # type: ignore
    XGBOOST = auto()  # type: ignore
    LIGHTGBM = auto()  # type: ignore
    CATBOOST = auto()  # type: ignore

    # Clustering
    KMEANS = auto()  # type: ignore
    HIERARCHICAL = auto()  # type: ignore
    DBSCAN = auto()  # type: ignore
    GMM = auto()  # type: ignore
    SPECTRAL_CLUSTERING = auto()  # type: ignore

    # Dimensionality reduction
    PCA = auto()  # type: ignore
    TSNE = auto()  # type: ignore
    UMAP = auto()  # type: ignore
    LDA = auto()  # type: ignore

    # Time-series (stat + neural)
    AR = auto()  # type: ignore
    ARIMA = auto()  # type: ignore
    SARIMA = auto()  # type: ignore
    EXPONENTIAL_SMOOTHING = auto()  # type: ignore
    STATE_SPACE = auto()  # type: ignore
    PROPHET = auto()  # type: ignore
    N_BEATS = auto()  # type: ignore
    TCN = auto()  # type: ignore

    # Anomaly detection
    ISOLATION_FOREST = auto()  # type: ignore
    ONE_CLASS_SVM = auto()  # type: ignore
    LOF = auto()  # type: ignore
    AUTOENCODER = auto()  # type: ignore

    # Neural blocks
    MLP = auto()  # type: ignore
    CNN = auto()  # type: ignore
    RNN = auto()  # type: ignore
    LSTM = auto()  # type: ignore
    GRU = auto()  # type: ignore
    TRANSFORMER = auto()  # type: ignore
    GNN = auto()  # type: ignore

    # Generative
    VAE = auto()  # type: ignore
    GAN = auto()  # type: ignore
    DIFFUSION = auto()  # type: ignore

# ──────────────────────────────────────────────────────────────────────────────
# Architecture Structure - How algorithms are combined/organized
# ──────────────────────────────────────────────────────────────────────────────

class AIArchitectureStructure(AutoLower):
    """How AI algorithms are structured and combined."""
    # Single model (most common)
    SINGLE = auto()  # type: ignore                 # single model
    
    # Sequential approaches
    SEQUENTIAL = auto()  # type: ignore             # sequential stages
    CASCADE = auto()  # type: ignore              # conditional routing
    
    # Ensemble approaches  
    ENSEMBLE = auto()  # type: ignore             # generic ensemble (params define subtype)
    STACKED_ENSEMBLE = auto()  # type: ignore     # meta-learner on top of base learners
    VOTING_ENSEMBLE = auto()  # type: ignore      # hard/soft voting
    BAGGING = auto()  # type: ignore
    BOOSTING = auto()  # type: ignore
    
    # Advanced architectures
    MOE = auto()  # type: ignore                  # mixture-of-experts with router

# ──────────────────────────────────────────────────────────────────────────────
# Training and Update
# ──────────────────────────────────────────────────────────────────────────────


class AIModelTrainingType(AutoLower):
    """Model training and retraining strategies (compute-intensive learning)."""
    # Initial Training Strategies
    INITIAL_TRAINING = auto()  # type: ignore
    # Complete Retraining Strategies
    COMPLETE_RETRAINING = auto()  # type: ignore
    # Incremental/Continuous Training (with backpropagation/optimization)
    INCREMENTAL_TRAINING = auto()  # type: ignore
    ONLINE_LEARNING = auto()  # type: ignore  # real time learning from streaming data
    
    # Neural Network Training Approaches
    STATEFUL_MODEL_STATE_UPDATE = auto()  # type: ignore

    # Transfer and Fine-tuning (compute-intensive)
    TRANSFER_LEARNING = auto()  # type: ignore
    FINE_TUNING = auto()  # type: ignore
    
    # Advanced Strategies
    ENSEMBLE_RETRAINING = auto()  # type: ignore
    A_B_TESTING_RETRAINING = auto()  # type: ignore

# ──────────────────────────────────────────────────────────────────────────────
# Model Performance & Metrics
# ──────────────────────────────────────────────────────────────────────────────

class RegressionMetric(AutoLower):
    """Regression performance metrics."""
    MEAN_ABSOLUTE_ERROR = auto()  # type: ignore
    MEAN_SQUARED_ERROR = auto()  # type: ignore
    ROOT_MEAN_SQUARED_ERROR = auto()  # type: ignore
    MEAN_ABSOLUTE_PERCENTAGE_ERROR = auto()  # type: ignore
    SYMMETRIC_MEAN_ABSOLUTE_PERCENTAGE_ERROR = auto()  # type: ignore
    R_SQUARED = auto()  # type: ignore
    ADJUSTED_R_SQUARED = auto()  # type: ignore
    EXPLAINED_VARIANCE = auto()  # type: ignore
    MAX_ERROR = auto()  # type: ignore
    MEDIAN_ABSOLUTE_ERROR = auto()  # type: ignore
    HUBER_LOSS = auto()  # type: ignore
    LOG_COSH_LOSS = auto()  # type: ignore
    QUANTILE_LOSS = auto()  # type: ignore
    HIT_RATE = auto()  # type: ignore
    DIRECTIONAL_ACCURACY = auto()  # type: ignore

class TimeSeriesMetric(AutoLower):
    """Time series specific metrics."""
    MEAN_ABSOLUTE_SCALED_ERROR = auto()  # type: ignore
    SYMMETRIC_MEAN_ABSOLUTE_PERCENTAGE_ERROR = auto()  # type: ignore
    MEAN_ABSOLUTE_RANGE_NORMALIZED_ERROR = auto()  # type: ignore
    NORMALIZED_ROOT_MEAN_SQUARED_ERROR = auto()  # type: ignore
    DIRECTIONAL_ACCURACY = auto()  # type: ignore
    HIT_RATE = auto()  # type: ignore
    CUMULATIVE_GAIN = auto()  # type: ignore
    MAXIMUM_DRAWDOWN = auto()  # type: ignore
    SHARPE_RATIO = auto()  # type: ignore
    SORTINO_RATIO = auto()  # type: ignore
    CALMAR_RATIO = auto()  # type: ignore
    VALUE_AT_RISK = auto()  # type: ignore
    CONDITIONAL_VALUE_AT_RISK = auto()  # type: ignore

class ClassificationMetric(AutoLower):
    """Classification performance metrics."""
    ACCURACY = auto()  # type: ignore
    PRECISION = auto()  # type: ignore
    RECALL = auto()  # type: ignore
    F1_SCORE = auto()  # type: ignore
    F2_SCORE = auto()  # type: ignore
    FBETA_SCORE = auto()  # type: ignore
    ROC_AUC = auto()  # type: ignore
    PR_AUC = auto()  # type: ignore
    LOG_LOSS = auto()  # type: ignore
    BRIER_SCORE = auto()  # type: ignore
    MATTHEWS_CORRELATION = auto()  # type: ignore
    BALANCED_ACCURACY = auto()  # type: ignore
    COHEN_KAPPA = auto()  # type: ignore
    HAMMING_LOSS = auto()  # type: ignore
    JACCARD_SCORE = auto()  # type: ignore
    ZERO_ONE_LOSS = auto()  # type: ignore


# ──────────────────────────────────────────────────────────────────────────────
# Model Input/Output Types
# ──────────────────────────────────────────────────────────────────────────────

class ModelOutputType(AutoLower):
    """Types of output data from models."""
    REGRESSION_VALUE = auto()  # type: ignore
    CLASSIFICATION_LABEL = auto()  # type: ignore
    CLASSIFICATION_PROBABILITY = auto()  # type: ignore
    MULTI_CLASS_PROBABILITIES = auto()  # type: ignore
    MULTI_LABEL_PREDICTIONS = auto()  # type: ignore
    SEQUENCE_PREDICTION = auto()  # type: ignore
    TIME_SERIES_FORECAST = auto()  # type: ignore
    CLUSTERING_ASSIGNMENT = auto()  # type: ignore
    ANOMALY_SCORE = auto()  # type: ignore
    RANKING = auto()  # type: ignore
    EMBEDDING = auto()  # type: ignore
    FEATURE_IMPORTANCE = auto()  # type: ignore
    UNCERTAINTY_ESTIMATE = auto()  # type: ignore
    EXPLANATION = auto()  # type: ignore


class ModelOutputPurpose(AutoLower):
    """Purpose of the AI model output."""
    TRAINING = auto()  # type: ignore
    VALIDATION = auto()  # type: ignore
    TESTING = auto()  # type: ignore
    SERVING = auto()  # type: ignore
    SIMULATION = auto()  # type: ignore
    DEMO = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore


# ──────────────────────────────────────────────────────────────────────────────
# Model Architectures & Frameworks
# ──────────────────────────────────────────────────────────────────────────────

class AIFramework(AutoLower):
    """Machine learning frameworks."""
    SCIKIT_LEARN = auto()  # type: ignore
    TENSORFLOW = auto()  # type: ignore
    GENAI_PYTHON_SDK = auto()  # type: ignore
    BIGQUERY_AI = auto()  # type: ignore
    BIGQUERY_ML = auto()  # type: ignore
    PYTORCH = auto()  # type: ignore
    KERAS = auto()  # type: ignore
    XGBOOST = auto()  # type: ignore
    LIGHTGBM = auto()  # type: ignore
    CATBOOST = auto()  # type: ignore
    STATSMODELS = auto()  # type: ignore
    PROPHET = auto()  # type: ignore
    NEURALPROPHET = auto()  # type: ignore
    DARTS = auto()  # type: ignore
    SKTIME = auto()  # type: ignore
    TSFRESH = auto()  # type: ignore
    PYOD = auto()  # type: ignore
    HUGGING_FACE = auto()  # type: ignore
    OPTUNA = auto()  # type: ignore
    HYPEROPT = auto()  # type: ignore
    RAY_TUNE = auto()  # type: ignore
    MLFLOW = auto()  # type: ignore
    WANDB = auto()  # type: ignore
    CUSTOM = auto()  # type: ignore
