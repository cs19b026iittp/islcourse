# -*- coding: utf-8 -*-
"""hubconf

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mHRM7eHfshcZzabspNvuE4HBsaADMNB-
"""

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
device = "cuda" if torch.cuda.is_available() else "cpu"

loss_fn = nn.CrossEntropyLoss()
# Define a neural network YOUR ROLL NUMBER (all small letters) should prefix the classname
class cs19b026NN(nn.Module):
  def __init__(self):
    super(cs19b026NN, self).__init__()
      self.flatten = nn.Flatten()
      self.linear_relu_stack = nn.Sequential(
        nn.Linear(28*28, 512),
        nn.ReLU(),
        nn.Linear(512, 512),
        nn.ReLU(),
        nn.Linear(512, 10)
      )

  def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

def load_data():
  training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
  )

# Download test data from open datasets.
  test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
  )
  return training_data, test_data

def create_dataloaders(training_data, test_data, batch_size=64):
    # Create data loaders.
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)

    for X, y in test_dataloader:
        print(f"Shape of X [N, C, H, W]: {X.shape}")
        print(f"Shape of y: {y.shape} {y.dtype}")
        break
    print('returning dataloaders')
    return train_dataloader, test_dataloader

# sample invocation torch.hub.load(myrepo,'get_model',train_data_loader=train_data_loader,n_epochs=5, force_reload=True)
training_data, test_data = load_data();
train_dataloader, test_dataloader = create_dataloaders(training_data, test_data, batch_size=64)

def get_model(train_data_loader=None, n_epochs=10):
  model = cs19b026NN().to(device)
  optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

  for i, (images, labels) in enumerate(train_data_loader):
    images = images.to(device)
    labels = labels.to(device)

    outputs = model(images)
    loss = loss_fn(outputs, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if batch % 100 == 0:
      loss, current = loss.item(), batch * len(X)
      print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
    print ('Returning model... (rollnumber: xx)')
  
    return model

def get_model_advanced(train_data_loader=None, n_epochs=10,lr=1e-4,config=None):
  model = None

  # write your code here as per instructions
  # ... your code ...
  # ... your code ...
  # ... and so on ...
  # Use softmax and cross entropy loss functions
  # set model variable to proper object, make use of train_data
  
  # In addition,
  # Refer to config dict, where learning rate is given, 
  # List of (in_channels, out_channels, kernel_size, stride=1, padding='same')  are specified
  # Example, config = [(1,10,(3,3),1,'same'), (10,3,(5,5),1,'same'), (3,1,(7,7),1,'same')], it can have any number of elements
  # You need to create 2d convoution layers as per specification above in each element
  # You need to add a proper fully connected layer as the last layer
  
  # HINT: You can print sizes of tensors to get an idea of the size of the fc layer required
  # HINT: Flatten function can also be used if required
  return

model = get_model()

# sample invocation torch.hub.load(myrepo,'get_model_advanced',train_data_loader=train_data_loader,n_epochs=5, force_reload=True)
def get_model_advanced(train_data_loader=None, n_epochs=10,lr=1e-4,config=None):
  model = None

  # write your code here as per instructions
  # ... your code ...
  # ... your code ...
  # ... and so on ...
  # Use softmax and cross entropy loss functions
  # set model variable to proper object, make use of train_data
  
  # In addition,
  # Refer to config dict, where learning rate is given, 
  # List of (in_channels, out_channels, kernel_size, stride=1, padding='same')  are specified
  # Example, config = [(1,10,(3,3),1,'same'), (10,3,(5,5),1,'same'), (3,1,(7,7),1,'same')], it can have any number of elements
  # You need to create 2d convoution layers as per specification above in each element
  # You need to add a proper fully connected layer as the last layer
  
  # HINT: You can print sizes of tensors to get an idea of the size of the fc layer required
  # HINT: Flatten function can also be used if required
  return model
  
  
  print ('Returning model... (rollnumber: cs19b026)')
  
  return model

# sample invocation torch.hub.load(myrepo,'test_model',model1=model,test_data_loader=test_data_loader,force_reload=True)
def test_model(model1=model, test_data_loader=test_dataloader,force_reload=True):

  accuracy_val, precision_val, recall_val, f1score_val = 0, 0, 0, 0

  size = len(test_data_loader.dataset)
  num_batches = len(test_data_loader)
  model1.eval()
  test_loss, correct = 0, 0
  with torch.no_grad():
      for X, y in test_data_loader:
          X, y = X.to(device), y.to(device)
          pred = model1(X)
          test_loss += loss_fn(pred, y).item()
          correct += (pred.argmax(1) == y).type(torch.float).sum().item()
  test_loss /= num_batches
  correct /= size


  accuracy_val = correct

  classes = [
    "BMW",
    "Mecedes",
    "Porche",
    "Ducati",
    "Cullinen",
    "Suzuki",
    "Skoda",
    "Volvo",
    "Bentley",
    "Audi",
  ]

  model = model1.eval()
  x = []
  y = [] 
  y1 = []
  for i in test_data :
    x.append(i[0])
    y.append(i[1])
    with torch.no_grad():
      pred = model(i[0])
      predicted = pred[0].argmax(0)
      # print()
      y1.append(classes.index(classes[predicted]))
  
  print ('Returning metrics... (rollnumber: cs19b026)')
  print(y)
  print(y1)
  precision_recall_fscore_support(y, y1, average='macro')
  
  return accuracy_val, precision_val, recall_val, f1score_val

ans = test_model()