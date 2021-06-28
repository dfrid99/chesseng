import torch
import torch.nn as nn
class PreActConv(nn.Module):
    def __init__(self, in_channels, kernel_size,padding = 1, act = nn.ReLU()):
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

class class_head(nn.Module):
    def __init__(self, in_channels, conv_channels = 8, hidden_dim = 256, out_dim = 64, act = nn.ReLU()):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, conv_channels, 1),
            nn.BatchNorm2d(conv_channels),
            act
        )
        self.fc1 = nn.Sequential(
            nn.Linear(8*8*conv_channels, hidden_dim),
            act,
            nn.Linear(hidden_dim, out_dim),
            nn.Softmax(dim=1)
        )
        self.fc2 = nn.Sequential(
            nn.Linear(8 * 8 * conv_channels, hidden_dim),
            act,
            nn.Linear(hidden_dim, out_dim),
            nn.Softmax(dim=1)
        )

    def forward(self,x):
        x = self.conv(x)
        x = torch.flatten(x, start_dim=1)
        x1 = self.fc1(x)
        x2 = self.fc2(x)
        return x1, x2

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

class Model(nn.Module):
    def __init__(self, res_layers = 4):
        super().__init__()
        self.conv1 = nn.Conv2d(17, 256, 3, padding=1)
        self.hidden_res = nn.ModuleList()
        for i in range(res_layers):
            self.hidden_res.append(PreActConv(256, 3))
        self.fc_head = class_head(256)

    def forward(self, x):
        x = self.conv1(x)
        for layer in self.hidden_res:
            x = x + layer(x)
        x1 , x2 = self.fc_head(x)
        return x1, x2