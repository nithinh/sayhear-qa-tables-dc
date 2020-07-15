import csv
import numpy as np
import sys
import torch
import torch.utils.data as Data
import torch.nn as nn
from torch.nn import Sequential
from torch.optim import SGD
import matplotlib.pyplot as plt


def to_variable(tensor):
    if torch.cuda.is_available():
        tensor = tensor.cuda()
    return torch.autograd.Variable(tensor, requires_grad=True)

def load_data(path, train = False):
    file = open(path, "r")
    reader = csv.reader(file)
    next(reader)
    features = []
    labels = []
    for row in reader:
        features.append(np.array([float(item) for item in row[6:]]))
        labels.append(float(row[5]))
        if not train:
            continue
        if float(row[5]) == 1.0:
            for i in range(43):
                features.append(np.array([float(item) for item in row[6:]]))
                labels.append(float(row[5]))
    return np.array(features), np.array(labels)

class TrainDataset(Data.Dataset):
    def __init__(self, path, train = True):
        self.features, self.labels = load_data(path, train)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return torch.from_numpy(self.features[idx]).float(), torch.from_numpy(np.asarray([self.labels[idx]])).long()

class TestDataset(Data.Dataset):
    def __init__(self, path):
        self.features, self.labels = load_data(path)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return torch.from_numpy(self.features[idx]).float(), torch.from_numpy(np.asarray([self.labels[idx]])).long()

def NN():
    return Sequential(
            nn.Linear(77, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.BatchNorm1d(16),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.BatchNorm1d(8),
            nn.Linear(8, 2),
        )

if __name__ == "__main__":
    train_feature_file = sys.argv[1]
    test_feature_file = sys.argv[2]
    num_of_epoch = int(sys.argv[3])
    output_file = sys.argv[4]
    
    result = open(output_file, "w")
    result.write("epoch,average_loss,accuracy,train_1to1,train_1to0,train_0to1,train_0to0,train_accuracy,train_recall,train_precision,test_1to1,test_1to0,test_0to1,test_0to0,test_accuracy,test_recall,test_precision\n")

    epoch_list = []
    average_loss_list = []
    accuracy_list = []
    train_11_list = []
    train_10_list = []
    train_01_list = []
    train_00_list = []
    train_accuracy_list = []
    train_recall_1_list = []
    train_precision_1_list = []
    test_11_list = []
    test_10_list = []
    test_01_list = []
    test_00_list = []
    test_accuracy_list = []
    test_recall_1_list = []
    test_precision_1_list = []
    
    model = NN()
    optimizer = SGD(model.parameters(), lr = 0.001, momentum = 0.9, weight_decay = 0.001)
    loss_func = nn.CrossEntropyLoss()
    
    for epoch in range(num_of_epoch):
        model.train()
        losses = []
        correct_ans = 0
        training_set = TrainDataset(train_feature_file)
        dataloader = Data.DataLoader(dataset = training_set, batch_size = 64, shuffle = True)
        for feats, labels in dataloader:
            out = model.forward(feats)
            loss = loss_func(out, labels.resize_(feats.shape[0]))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(loss.data.cpu().numpy())
            pred_y = torch.max(out, 1)[1].data.numpy().squeeze()
            labels = labels.data.numpy()
            correct_ans += np.sum(np.equal(pred_y, labels))
        accuracy = correct_ans / len(training_set)
        
        average_loss = np.asscalar(np.mean(losses))

        test_set = TrainDataset(train_feature_file, False)
        dataloader = Data.DataLoader(dataset = test_set, batch_size = 64, shuffle = True)
        correct_ans = 0
        positive_instance = 0
        negative_instance = 0
        true_positive = 0
        true_negative = 0
        model.eval()
        for feats, labels in dataloader:
            out = model.forward(feats)
            loss = loss_func(out, labels.resize_(feats.shape[0]))
    
            pred_y = torch.max(out, 1)[1].data.numpy().squeeze()
            labels = labels.data.numpy()
    
            for i in range(len(labels)):
                if labels[i] == 1:
                    positive_instance += 1
                    if pred_y[i] == 1:
                        true_positive += 1
                else:
                    negative_instance += 1
                    if pred_y[i] == 0:
                        true_negative += 1
            correct_ans += np.sum(np.equal(pred_y, labels))
        accuracy = correct_ans / len(test_set)
        
        train_11 = true_positive
        train_10 = positive_instance - true_positive
        train_01 = negative_instance - true_negative
        train_00 = true_negative
        train_accuracy = accuracy
        train_recall_1 = float(train_11)/(train_11+train_10)
        train_precision_1 = float(train_11)/(train_11+train_01)
    
        test_set = TestDataset(test_feature_file)
        dataloader = Data.DataLoader(dataset = test_set, batch_size = 64, shuffle = True)
        correct_ans = 0
        positive_instance = 0
        negative_instance = 0
        true_positive = 0
        true_negative = 0
        model.eval()
        for feats, labels in dataloader:
            out = model.forward(feats)
            loss = loss_func(out, labels.resize_(feats.shape[0]))
    
            pred_y = torch.max(out, 1)[1].data.numpy().squeeze()
            labels = labels.data.numpy()
            for i in range(len(labels)):
                if labels[i] == 1:
                    positive_instance += 1
                    if pred_y[i] == 1:
                        true_positive += 1
                else:
                    negative_instance += 1
                    if pred_y[i] == 0:
                        true_negative += 1
            correct_ans += np.sum(np.equal(pred_y, labels))
        accuracy = correct_ans / len(test_set)

        test_11 = true_positive
        test_10 = positive_instance - true_positive
        test_01 = negative_instance - true_negative
        test_00 = true_negative
        test_accuracy = accuracy
        test_recall_1 = float(test_11)/(test_11+test_10)
        test_precision_1 = float(test_11)/(test_11+test_01)
        
        epoch_list.append(epoch)
        average_loss_list.append(average_loss)
        accuracy_list.append(accuracy)
        train_11_list.append(train_11)
        train_10_list.append(train_10)
        train_01_list.append(train_01)
        train_00_list.append(train_00)
        train_accuracy_list.append(train_accuracy)
        train_recall_1_list.append(train_recall_1)
        train_precision_1_list.append(train_precision_1)
        test_11_list.append(test_11)
        test_10_list.append(test_10)
        test_01_list.append(test_01)
        test_00_list.append(test_00)
        test_accuracy_list.append(test_accuracy)
        test_recall_1_list.append(test_recall_1)
        test_precision_1_list.append(test_precision_1)

        result.write("{}, {:.4f}, {:.4f}, {}, {}, {}, {}, {:.4f}, {:.4f}, {:.4f}, {}, {}, {}, {}, {:.4f}, {:.4f}, {:.4f}".format(epoch, average_loss, accuracy, train_11, train_10, train_01, train_00, train_accuracy, train_recall_1, train_precision_1, test_11, test_10, test_01, test_00, test_accuracy, test_recall_1, test_precision_1))
        result.write("\n")
              
    result.close()
    plt.figure(figsize=(20,10))
    plt.plot(epoch_list, train_recall_1_list, 'b')
    plt.plot(epoch_list, train_precision_1_list, 'g')
    plt.plot(epoch_list, train_accuracy_list, 'r')
    plt.plot(epoch_list, average_loss_list, 'y')
    plt.show()
    
    plt.figure(figsize=(20,10))
    plt.plot(epoch_list, test_recall_1_list, 'b')
    plt.plot(epoch_list, test_precision_1_list, 'g')
    plt.plot(epoch_list, test_accuracy_list, 'r')
    plt.plot(epoch_list, average_loss_list, 'y')
    plt.show()