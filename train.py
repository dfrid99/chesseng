import numpy as np
from model import *
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

a = np.load("2boardarr.npy")
b = np.load("2movearr.npy")
print(a.shape)
print(b.shape)

tensor_x = torch.tensor(a, dtype = torch.float)
tensor_y = torch.tensor(b, dtype = torch.float)
dataset = TensorDataset(tensor_x, tensor_y)
dataloader = DataLoader(dataset, batch_size=24,shuffle=True)

# for inp, out in dataloader:
#     x = inp
#     y = out
#     break
#x = torch.randn(24, 17, 56, 56)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#device = "cpu"
net = Model().to(device)

criterion = nn.BCELoss(reduction='sum')
optimizer = optim.Adam(net.parameters(), lr=1e-4, weight_decay=1e-5)

for epoch in range(10):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(dataloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data
        labels = torch.flatten(labels, start_dim=2)
        labels1 = torch.index_select(labels, 1, torch.tensor([0]))
        labels1 = torch.flatten(labels1, start_dim=1)
        labels2 = torch.index_select(labels, 1, torch.tensor([1]))
        labels2 = torch.flatten(labels2, start_dim=1)
        inputs = inputs.to(device)
        labels1 = labels1.to(device)
        labels2 = labels2.to(device)


        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        out1, out2 = net(inputs)
        loss1 = criterion(out1, labels1)
        loss2 = criterion(out2, labels2)
        loss = loss1 + loss2
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 400 == 399:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')
PATH = "model4"
torch.save(net.state_dict(), PATH)
print('saved')