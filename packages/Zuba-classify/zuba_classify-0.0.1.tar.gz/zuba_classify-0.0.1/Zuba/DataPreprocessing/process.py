import pandas as pd
import tiktoken
import torch
from Zuba.DataPreprocessing.createLoader import DataLoader
loader=DataLoader(batch_size=8,num_workers=0)



class Tokenizer:
    def __init__(self, file, tokenizer, max_len=None, pad_token_id=50256):
        # Load dataset
        self.file = pd.read_csv(file)
        self.tokenizer = tokenizer
        self.pad_token_id = pad_token_id
        
        # Encode all texts
        self.encodings = [self.tokenizer.encode(text) for text in self.file["tweet"]]
        
        # Determine max length
        if max_len is None:
            self.max_len = self.get_max_len()
        else:
            self.max_len = max_len
        
        # Truncate and pad sequences
        self.encodings = [
            enc[:self.max_len] + [self.pad_token_id] * (self.max_len - len(enc[:self.max_len]))
            for enc in self.encodings
        ]

    # PyTorch-style getter
    def __getitem__(self, idx):
        item = self.encodings[idx]
        label = self.file.iloc[idx]["label"]
        return torch.tensor(item), torch.tensor(label)

    # PyTorch-style length
    def __len__(self):
        return len(self.encodings)

    # Compute max sequence length from data
    def get_max_len(self):
        max_len = max(len(enc) for enc in self.encodings)
        return max_len

    





tokenizer = tiktoken.get_encoding("gpt2") 
train_dataset=Tokenizer("../data/new_dataset/train_data.csv",tokenizer=tokenizer,max_len=None)
val_dataset=Tokenizer("../data/new_dataset/val_data.csv",tokenizer=tokenizer,max_len=train_dataset.max_len)
test_dataset=Tokenizer("../data/new_dataset/test_data.csv",tokenizer=tokenizer,max_len=train_dataset.max_len)
class Return:
 def __init__(self,):
    pass
 def Return():
   torch.manual_seed(42)
   train_loader=loader.get_train_loader(train_dataset)
   val_loader=loader.get_val_loader(val_dataset)
   test_loader=loader.get_test_loader(test_dataset)
   return train_loader,test_loader,val_loader
 
