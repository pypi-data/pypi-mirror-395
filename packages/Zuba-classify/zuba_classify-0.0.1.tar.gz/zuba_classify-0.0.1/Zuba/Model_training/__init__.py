# Zuba/Model_training/LanguageClassifier.py

import torch
import torch.nn as nn
from transformers import GPT2Model, GPT2Config

class LanguageClassifier(nn.Module):
    def __init__(self, num_labels=4):
        super(LanguageClassifier, self).__init__()

        # Build GPT-2 from config only — no pretrained weights
        self.config = GPT2Config()
        self.pretrained_model = GPT2Model(self.config)

        # Classification head
        self.classifier_head = nn.Linear(self.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask=None):
        outputs = self.pretrained_model(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.last_hidden_state[:, -1, :]
        logits = self.classifier_head(pooled)
        return logits
