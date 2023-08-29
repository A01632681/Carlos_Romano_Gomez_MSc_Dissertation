import torch
import cv2
import numpy
import torch.nn as nn
from torch.nn import Conv2d, MaxPool2d, Sequential
import torch.nn.functional as F
import torch.optim as optim
from tltorch import TRL

def read_frames(pathtoimages, max_frames):
    frames = []
    frame_count = 1
    while True:
        image = pathtoimages + 'Img_' + str(frame_count) + '.png'
        frame = cv2.imread(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print(frame.shape)
        frame_norm = (frame - frame.min())/(frame.max() - frame.min())
        frames.append(frame_norm)
        frame_count += 1
        if frame_count > max_frames:
            break
    return numpy.asarray(frames)

dataset = read_frames('/home/nvidia/Downloads/rectest/path1/rec1/', max_frames=50)
# dataset = torch.from_numpy(dataset)
# dataset = dataset.type(torch.DoubleTensor)
print(dataset.shape)
batch_size = 50

train_loader = torch.utils.data.DataLoader(dataset,batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset,batch_size=batch_size, shuffle=True)


nn = Sequential(
        Conv2d(in_channels=1, out_channels=20, kernel_size=5),
        Conv2d(20, 50, 5),
        MaxPool2d(kernel_size=2, stride=2),
        Conv2d(50, 20, 5),
        Conv2d(20, 50, 5),
        MaxPool2d(2, 2),
        TRL(rank='same', input_shape=(batch_size, 50, 4, 4), output_shape=(batch_size,10)),
)

model = F.log_softmax(nn)
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
criterion = nn.CrossEntropyLoss()

n_epoch = 20 # Number of epochs
regularizer = 0.001

model = model.to('cpu')

def train(n_epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to('cpu'), target.to('cpu')
       
        # Important: do not forget to reset the gradients
        optimizer.zero_grad()
       
        output = model(data)
        loss = criterion(output,target) + regularizer*model.trl.penalty(2)
        loss.backward()
        optimizer.step()
        if batch_idx % 1000 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                n_epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss))

def test():
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        data, target = data.to('cpu'), target.to('cpu')
        output = model(data)
        test_loss = criterion(output,target)
        pred = output.data.max(1, keepdim=True)[1] # get the index of the max log-probability
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(test_loader.dataset)
    print('mean: {}'.format(test_loss))
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
       100. * correct / len(test_loader.dataset)))


for epoch in range(1, n_epoch):
    train(epoch)
    test()