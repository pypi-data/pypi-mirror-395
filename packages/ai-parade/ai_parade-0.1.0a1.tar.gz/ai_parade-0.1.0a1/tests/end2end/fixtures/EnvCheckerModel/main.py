import sys
import torch
import torch.nn as nn


# Define a simple CNN using Sequential
class SimpleCNN(nn.Module):
	def __init__(self):
		super(SimpleCNN, self).__init__()
		self.model = nn.Sequential(
			nn.Flatten(),
			nn.Linear(3 * 4 * 4, 1),
		)

	def forward(self, x):
		assert sys.version_info.major == 3
		assert sys.version_info.minor == 10

		return self.model(x)


def mock():
	model = SimpleCNN()
	for m in model.modules():
		if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
			nn.init.uniform_(m.weight, a=-1.0, b=1.0)
			nn.init.uniform_(m.bias, a=-1.0, b=1.0)

	print("running")
	model.eval()
	model(torch.ones(1, 3, 4, 4))

	print("saving")
	torch.save(model.state_dict(), "weights.pth")


if __name__ == "__main__":
	mock()
