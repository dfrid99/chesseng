from board import *
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

a = np.load("1boardarr.npy")
b = np.load("1movearr.npy")
print(a.shape)
print(b.shape)

tensor_x = torch.Tensor(a)
tensor_y = torch.Tensor(b)
tensor_x = torch.tensor(tensor_x, dtype = torch.float)
tensor_y = torch.tensor(tensor_y, dtype = torch.float)
dataset = TensorDataset(tensor_x, tensor_y)
dataloader = DataLoader(dataset, batch_size=128,shuffle=True)

for inp, out in dataloader:
    x = inp
    break
#x = torch.randn(24, 17, 56, 56)
class PreActConv(nn.Module):
    def __init__(self, in_channels, kernel_size, stride = 1,padding = 1, act = nn.ReLU()):
        super().__init__()
        self.model = nn.Sequential(
            nn.BatchNorm2d(in_channels),
            act,
            nn.Conv2d(in_channels, in_channels , kernel_size, padding = padding),
            nn.BatchNorm2d(in_channels),
            act,
            nn.Conv2d(in_channels, in_channels , kernel_size, padding=padding)
        )
    def forward(self, x):
        x = self.model(x)
        return x

class fc_head(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, act = nn.ReLU()):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            act,
            nn.Linear(hidden_dim, out_dim),
            nn.Softmax(dim=1)
        )

    def forward(self,x):
        x = self.model(x)
        return x

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(17, 256, 1)
        self.block1 = PreActConv(256,3)
        self.block2 = PreActConv(256,3)
        self.down1 = nn.Conv2d(256,512, 3, stride=2, padding=1)
        self.block3 = PreActConv(512,3)
        self.block4 = PreActConv(512, 3)
        self.class_head = fc_head(512*4*4, 6000, 4672)

    def forward(self, x):
        x = self.conv1(x)
        x += self.block1(x)
        x += self.block2(x)
        x = self.down1(x)
        x += self.block3(x)
        x += self.block4(x)
        x = torch.flatten(x, start_dim=1)
        x = self.class_head(x)
        return x


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = Model().to(device)
x = x.to(device)
y = net(x)
print(y.shape)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.00015, momentum=0.9)

# for epoch in range(2):  # loop over the dataset multiple times
#
#     running_loss = 0.0
#     for i, data in enumerate(dataloader, 0):
#         # get the inputs; data is a list of [inputs, labels]
#         inputs, labels = data
#         labels = torch.flatten(labels, start_dim=1).long()
#         inputs = inputs.to(device)
#         labels = labels.to(device)
#
#
#         # zero the parameter gradients
#         optimizer.zero_grad()
#
#         # forward + backward + optimize
#         outputs = net(inputs)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()
#
#         # print statistics
#         running_loss += loss.item()
#         if i % 2000 == 1999:    # print every 2000 mini-batches
#             print('[%d, %5d] loss: %.3f' %
#                   (epoch + 1, i + 1, running_loss / 2000))
#             running_loss = 0.0
#
# print('Finished Training')