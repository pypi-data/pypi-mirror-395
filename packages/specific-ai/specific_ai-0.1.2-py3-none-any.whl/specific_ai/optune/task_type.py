from enum import Enum

class TaskType(str, Enum):
    classification = "ClassificationResponse"
    summarization = "summarization"
    QA = "QandA"
    ner = "NERResponse"
    chat = "chat"
    domainAdaptation = "domainAdaptation"
