from curses.ascii import US
import re
import numpy as np

class ThompsonSamplingStruct:
    
    def __init__(self, num_arm): 
        self.d = num_arm
        #self.sigma = sigma  # sigma is standard deviation

        # intialize priors
        # average reward for EACH arm: mu = 0; sigma = 1000
        self.priors = [[0, 1000] for _ in range(num_arm)]  # this is the flat prior
        # self.priors = [[0,1000], ..., [0, 1000]]
        # index 0: mean
        # index 1: standard deviation

        self.UserArmMean = np.zeros(self.d)
        self.UserArmTrials = np.zeros(self.d)
        self.reward_list = [[] for _ in range(num_arm)]

        self.time = 0

    def updateParameters(self, articlePicked_id, click):

        # compute reward
        self.UserArmMean[articlePicked_id] = (self.UserArmMean[articlePicked_id]*self.UserArmTrials[articlePicked_id] + click) / (self.UserArmTrials[articlePicked_id]+1)
        # add reward to their corresponding list
        self.reward_list[articlePicked_id].append(self.UserArmMean[articlePicked_id])

        self.UserArmTrials[articlePicked_id] += 1
        # compute varience and standard deviation of newly generated distribution
        varience = ((1 / ((self.priors[articlePicked_id][1])**2)) + self.UserArmTrials[articlePicked_id])**(-1)

        #self.priors[articlePicked_id][0] = varience * sum(self.reward_list[articlePicked_id])
        # update mean
        self.priors[articlePicked_id][0] = sum(self.reward_list[articlePicked_id]) / self.UserArmTrials[articlePicked_id]

        # update standard deviation
        self.priors[articlePicked_id][1] = np.sqrt(varience)

        self.time += 1

    def getTheta(self):
        return self.UserArmMean

    def decide(self, pool_articles):
        # create a list, sample K numbers from each arm's gaussian distribution; pick the arm that has the highest sample.
        
        articlePicked = None
        value_dict = {}  # {article object: value}

        for article in pool_articles:
            # generate value based on the current distribution
            value_dict[article] = np.random.normal(self.priors[article.id][0], self.priors[article.id][1])

        articlePicked = max(value_dict, key=value_dict.get)
        return articlePicked

class ThompsonSamplingMultiArmedBandit:
    def __init__(self, num_arm):
        self.users = {}
        self.num_arm = num_arm
        self.CanEstimateUserPreference = False

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = ThompsonSamplingStruct(self.num_arm)
        
        return self.users[userID].decide(pool_articles)
    
    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.id, click)

    def getTheta(self, userID):
        return self.users[userID].UserArmMean

