import torch
import torch.nn as nn
from torchsummary import summary


class FaceMask_Detection(nn.Module):
    def __init__(self, in_channels=3, hidden_size=64, num_classes=2):
        super().__init__()
        # in: (3, 224, 224)
        self.network = nn.Sequential(
            self._conv_block(in_channels, hidden_size),
            self._conv_block(hidden_size, hidden_size, pool=True, pool_size=2),  # (hidden, 112, 112)
            self._conv_block(hidden_size, hidden_size * 2),
            self._conv_block(hidden_size * 2, hidden_size * 2, pool=True, pool_size=2),  # (hidden*2, 56, 56)
            self._conv_block(hidden_size * 2, hidden_size * 4),
            self._conv_block(hidden_size * 4, hidden_size * 4, pool=True, pool_size=2),  # (hidden*4, 28, 28)
            self._conv_block(hidden_size * 4, hidden_size * 8),
            self._conv_block(hidden_size * 8, hidden_size * 8, pool=True, pool_size=4),  # (hidden*8, 7, 7)
            self._conv_block(hidden_size * 8, hidden_size * 16),
            self._conv_block(hidden_size * 16, hidden_size * 16, pool=True, pool_size=4),  # (hidden*16, 1, 1)
        )

        self.classifier = nn.Sequential(nn.Flatten(),
                                        nn.Linear(hidden_size * 16 * 1 * 1, 256),
                                        nn.Dropout(0.5),
                                        nn.Linear(256, num_classes))

    def forward(self, x):
        x = self.network(x)
        y = self.classifier(x)
        return y

    def _conv_block(self, in_channels, out_channels,
                    kernel_size=3, stride=1, padding=1,
                    pool: bool = False, pool_size: int = None):

        block = [nn.Conv2d(in_channels, out_channels,
                           kernel_size=kernel_size, stride=stride,
                           padding=padding),
                 nn.ReLU(inplace=True)]
        if pool:
            if pool_size is None:
                raise TypeError("'pool_size' must be an integer")
            block.append(nn.MaxPool2d(pool_size))

        return nn.Sequential(*block)

    def summery(self, input_size):
        return summary(self, input_size)



if __name__ == "__main__":
    model = FaceMask_Detection(3, 32, 2)
    model.summery((3, 224, 224))