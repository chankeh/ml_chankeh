import pandas as pd
import numpy as np
import cv2
import random
import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# opencv 提取hog特征
def get_hog_features(trainset):
    features = []

    hog = cv2.HOGDescriptor('./hog.xml')

    for img in trainset:
        img = np.reshape(img,(28,28))
        cv_img = img.astype(np.uint8)

        hog_feature = hog.compute(cv_img)
        # hog_feature = np.transpose(hog_feature)
        features.append(hog_feature)

    features = np.array(features)
    features = np.reshape(features,(-1,324))

    return features
def Train(trainset,train_labels):
    # get params
    trainset_size = len(train_labels)

    # initialize w and b
    w = np.zeros((feature_length,1)) # define as feature_length = 324 ,which equals 28 * 28
    b = 0

    study_count = 0 #  学习次数记录，只有当分类错误时才会增加
    nochange_count = 0  # 统计连续分类正确数，当分类错误时归为0
    nochange_upper_limit = 100000  # 连续分类正确上界，当连续分类超过上界时，认为已训练好，退出训练

    while True:
        nochange_count += 1
        if nochange_count > nochange_upper_limit:
            break

        # 随机选的数据
        index = random.randint(0, trainset_size - 1)
        img = trainset[index]
        label = train_labels[index]

        # 计算yi(w*xi+b)
        yi = int(label != object_num) * 2 - 1  # 如果等于object_num, yi= 1, 否则yi=1
        result = yi * (np.dot(img, w) + b)

        # 如果yi(w*xi+b) <= 0 则更新 w 与 b 的值
        if result <= 0:
            img = np.reshape(trainset[index], (feature_length, 1))  # 为了维数统一，需重新设定一下维度

            w += img * yi * study_step  # 按算法步骤3更新参数
            b += yi * study_step

            study_count += 1
            if study_count > study_total:
                break
            nochange_count = 0
    return w,b
def Predition(testset,w,b):
    predit = []
    for img in testset:
        result = np.add(np.dot(img,w),b)
        tmp = (result > 0)
        predit.append(tmp)
    return np.array(predit)


study_step = 0.0001                                 # 学习步长
study_total = 10000                                 # 学习次数
feature_length = 324                                # hog特征维度
object_num = 0                                      # 分类的数字

if __name__ == '__main__':
    print('start read data')
    time1 = time.time()
    raw_data = pd.read_csv('./train.csv',header=0)

    data = raw_data.values
    imgs = data[0::,1::]
    labels = data[::,0]

    features = get_hog_features(imgs)
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33,
                                                                                random_state=23323)
    time2 = time.time()
    print('read data cost ',time2 - time1,' second', '\n')
    print('Start training')
    w,b = Train(train_features,train_labels)
    time3 = time.time()
    print('training cost ', time3 - time2, ' second', '\n')
    print('Start predicting')
    test_predict = Predition(test_features,w,b)
    time4 = time.time()
    print('predicting cost ', time4 - time3, ' second', '\n')
    print(test_predict.shape)
    print(test_labels.shape)
    score = accuracy_score(test_labels, test_predict)
    print("The accruacy socre is ", score)

