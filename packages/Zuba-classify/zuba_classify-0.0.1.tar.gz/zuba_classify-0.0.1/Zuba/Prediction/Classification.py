import torch
from Zuba.Model_training import LanguageClassifier
import tiktoken
from pathlib import Path
from huggingface_hub import hf_hub_download

class Classify:
    def __init__(self):
        # Device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load model architecture
        self.model = LanguageClassifier(num_labels=4).to(self.device)

        # Download model from Hugging Face and cache
        # Replace 'username/repo' with your Hugging Face repo
        print("Checking / downloading model from Hugging Face...")
        self.model_path = hf_hub_download(
            repo_id="Laiwola/language_classifier",          # your Hugging Face repo
            filename="language_classifier_model2.pth"
        )

        # Load the model
        print(f"Loading model from: {self.model_path}")
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.eval()
        print("Model loaded successfully")

        # Tokenizer
        self.tokenizer = tiktoken.get_encoding("gpt2")
        self.max_len = 277
        self.pad_id = 50256

        # Label map
        self.id_label = {0: "hausa", 1: "igbo", 2: "Broken English", 3: "Yoruba"}

    def encode_text(self, text):
        """Tokenize → truncate → pad"""
        ids = self.tokenizer.encode(text)
        ids = ids[:self.max_len]  # truncate
        if len(ids) < self.max_len:
            ids += [self.pad_id] * (self.max_len - len(ids))
        return ids

    def predict(self, text_or_list):
        """Predict label for one text or many"""
        if isinstance(text_or_list, str):
            texts = [text_or_list]
            single = True
        else:
            texts = text_or_list
            single = False

        # Encode and convert to tensor
        encoded = [self.encode_text(t) for t in texts]
        input_ids = torch.tensor(encoded, dtype=torch.long).to(self.device)

        # Predict
        with torch.no_grad():
            logits = self.model(input_ids)
        pred_ids = torch.argmax(logits, dim=1).tolist()
        labels = [self.id_label[p] for p in pred_ids]

        return labels[0] if single else labels
