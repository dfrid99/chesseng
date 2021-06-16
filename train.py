from board import *
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

a = np.load("1boardarr.npy")
b = np.load("1movearr.npy")
print(a.shape)
print(b.shape)

tensor_x = torch.Tensor(a)
tensor_y = torch.Tensor(b)
dataset = TensorDataset(tensor_x, tensor_y)
dataloader = DataLoader(dataset, batch_size=24,shuffle=True)

for inp, out in dataloader:
    x = inp
    break

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(17, 64, (1,1))

    def forward(self, x):
        x = self.conv1(x)
        return x

net = Model()
y = net(x)
print(y.shape)