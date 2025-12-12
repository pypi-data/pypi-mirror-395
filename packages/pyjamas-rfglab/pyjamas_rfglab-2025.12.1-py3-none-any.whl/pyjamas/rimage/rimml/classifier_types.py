from enum import Enum


class classifier_types(Enum):
    # Classifier types.
    UNKNOWN: str = "Unknown"
    SUPPORT_VECTOR_MACHINE: str = "Support vector machine"
    LOGISTIC_REGRESSION: str = "Logistic regression"
    UNET: str = "U-Net"
    RESCUNET: str = "ReSCU-Net"
