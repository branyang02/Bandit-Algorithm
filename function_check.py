from os import lseek
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

list = [[] for _ in range(3)]
list[2].append(10)
list[2].append(23)
print(list)

highest = -12
list = [1,2,3,3,3]
for num in list:
    if num > highest:
        highest = num

print(list.index(highest))