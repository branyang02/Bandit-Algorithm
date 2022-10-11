from math import ceil
from os import lseek
from random import random
from re import A
import numpy as np

# d = 3 # num of arms

# UserArmMean = np.zeros(d)
# UserArmTrials = np.zeros(d)
# UCBEquationValue = np.full_like(UserArmMean, np.inf)


# print(UserArmMean)
# print(UserArmTrials)
# print(UCBEquationValue)


# articlePicked_id = 2
# click = -0.12
# time = 4
# UserArmTrials[articlePicked_id] = 100

# UserArmMean[articlePicked_id] = (UserArmMean[articlePicked_id]*UserArmTrials[articlePicked_id] + click) / (UserArmTrials[articlePicked_id]+1)

# UCBEquationValue[articlePicked_id] = UserArmMean[articlePicked_id] + np.sqrt((2 * np.log(time)) / UserArmTrials[articlePicked_id])

# print("--------------")
# print(UserArmMean)
# print(UserArmTrials)
# print(UCBEquationValue)

# list = [[] for _ in range(3)]
# list[2].append(10)
# list[2].append(23)
# print(list)

# highest = -12
# list = [1,2,3,3,3]
# for num in list:
#     if num > highest:
#         highest = num

# print(list.index(highest)

# featureDimension = 5
# A = 0.1 * np.identity(featureDimension)
# b = np.zeros(featureDimension)
# AInv = np.linalg.inv(A)
# UserTheta = np.zeros(featureDimension)

# sigma = 1000
# click = 0.88888888
# articlePicked_FeatureVector = np.ndarray([1,2,3,4,5])

# print(type(articlePicked_FeatureVector))
# A += (1/(sigma**2)) * np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
# b += (1/(sigma**2)) * (articlePicked_FeatureVector * click)
# AInv = np.linalg.inv(A)
# UserTheta = np.random.normal(np.dot(AInv, b), AInv)


a = 0.5
n = 3
list = [1 for _ in range(ceil(a * n)) if random() < 1.0]
print(list)

print(np.random.binomial(ceil(a*n), 0.5))
