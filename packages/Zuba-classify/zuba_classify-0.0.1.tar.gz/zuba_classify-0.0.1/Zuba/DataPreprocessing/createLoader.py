#this class will create dataloaders for our datasets
import tiktoken
from Zuba.DataPreprocessing.process import Tokenizer
import torch
from torch.utils.data import DataLoader
torch.manual_seed(42)
class DataLoader:
    def __init__(self,batch_size,num_workers,dataset=None,drop_last=True,shuffle=True):
      self.dataset=dataset
      self.batch_size=batch_size
      self.num_workers=num_workers
      self.drop_last=drop_last
    def get_train_loader(self,dataset):
        self.dataset=dataset
        train_loader=DataLoader(
            dataset=self.dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            drop_last=self.drop_last,
            shuffle=self.shuffle
        )
        return train_loader
    def get_val_loader(self,dataset):
        self.dataset=dataset
        val_loader=DataLoader(
            dataset=self.dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            drop_last=self.drop_last,
            shuffle=self.shuffle
        )
        return val_loader
    def get_test_loader(self,dataset):
        self.dataset=dataset
        test_loader=DataLoader(
            dataset=self.dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            drop_last=self.drop_last,
            shuffle=self.shuffle
        )
        return test_loader
