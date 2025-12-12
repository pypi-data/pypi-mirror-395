import torch
from huggingface_hub import hf_hub_download

REPO_ID = "your_username/zuba-language-classifier"
MODEL_FILE = "language_classifier_model2.pth"

def load_model(model_class):
    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=MODEL_FILE
    )
    model = model_class(num_labels=4)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    return model
