from transformers import pipeline

classifier = pipeline("zero-shot-classification")
classifier(
    "This is a repository about the Transformers library",
    candidate_labels=["education", "sports", "business"],
)