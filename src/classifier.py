from transformers import pipeline
import torch
torch.set_grad_enabled(False)
import gradio as gr

# Define the classify function
def classify(input):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    result = classifier(
        input,
        candidate_labels=["education", "sports", "business"],
    )
    return result

demo = gr.Interface(
    fn=classify,
    inputs=["text"],
    outputs=["text"],
)

demo.launch()
