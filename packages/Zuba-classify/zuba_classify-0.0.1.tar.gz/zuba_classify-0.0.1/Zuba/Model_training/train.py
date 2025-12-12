import torch 
import time
from Zuba.Model_training import LanguageClassifier
from Zuba.DataPreprocessing.process import Return
Return=Return() 
train_loader,test_loader,val_loader=Return.Return()
import torch.nn as nn
device= torch.device("cuda" if torch.cuda.is_available() else "cpu")

def cal_accuracy(data_loader,model,device,num_batches=None):
    model.eval()
    correct_pred,num_examples=0,0
    if num_batches is None:
        num_batches=len(data_loader)
    else:
        num_batches=min(num_batches,len(data_loader))
    for i,(input_ids,labels) in enumerate(data_loader):
     if i<num_batches:
        input_ids=input_ids.to(device)
        labels=labels.to(device)
        with torch.no_grad():
          probas=torch.softmax(model(input_ids),dim=1)
        label_preds=torch.argmax(probas,dim=1)
        correct_pred+=(label_preds==labels).sum().item()
        num_examples+=labels.size(0)
     else:
        break
    return correct_pred/num_examples
       
    
class TrainClassifier:
    def __init__(self, model, train_loader, val_loader, test_loader, device, learning_rate=3e-5, epochs=10):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.device = device
        self.learning_rate = learning_rate
        self.epochs = epochs

        self.train_loss, self.val_loss, self.test_loss = [], [], []
        self.train_acc, self.val_acc, self.test_acc = [], [], []
        self.epochs_list = []

        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.learning_rate)

    def train(self):
        for epoch in range(self.epochs):
            self.model.train()
            epoch_loss = 0

            for input_ids, labels in self.train_loader:
                input_ids = input_ids.to(self.device)
                labels = labels.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(input_ids)  # add attention_mask if needed
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item()

            epoch_loss /= len(self.train_loader)
            self.train_loss.append(epoch_loss)
            print(f"Epoch {epoch+1}/{self.epochs}, Loss={epoch_loss:.4f}")

            # Evaluate
            self.model.eval()
            with torch.no_grad():
                train_acc = cal_accuracy(self.train_loader, self.model, self.device, num_batches=10)
                val_acc = cal_accuracy(self.val_loader, self.model, self.device, num_batches=10)
                test_acc = cal_accuracy(self.test_loader, self.model, self.device, num_batches=10)

            self.train_acc.append(train_acc)
            self.val_acc.append(val_acc)
            self.test_acc.append(test_acc)
            self.epochs_list.append(epoch + 1)

            print(f"Epoch {epoch+1}/{self.epochs}, "
                  f"Train Acc: {train_acc*100:.2f}%, "
                  f"Val Acc: {val_acc*100:.2f}%, "
                  f"Test Acc: {test_acc*100:.2f}%")
        torch.save(self.model.state_dict(), "language_classifier_model.pth")
        return self.train_acc, self.val_acc, self.test_acc, self.epochs_list

# initiate training
if __name__=="__main__":
  start_time=time.time()
  Train=TrainClassifier(model=LanguageClassifier(num_labels=4).to(device),train_loader=train_loader,val_loader=val_loader,test_loader=test_loader,device=device,learning_rate=3e-5,epochs=3)
  train_acc,val_acc,test_acc,epoch_list=Train.train()
  end_time = time.time()
  execution_time=(end_time - start_time)/60
  print(f"Training time: {execution_time} minutes")
