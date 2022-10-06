from math import ceil
import numpy as np

class PerturbedHistoryExplorationStruct:

    def __init__(self, num_arm, a):
        self.d = num_arm
        self.a = a
        
        self.UserArmMean = np.zeros(self.d)
        self.UserArmTrials = np.zeros(self.d)

        self.T = np.zeros(self.d) # number of times arm is pulled
        self.V = np.zeros(self.d)
        

        self.time = 0

    def updateParameters(self, articlePicked_id, click):
        self.UserArmMean[articlePicked_id] = (self.UserArmMean[articlePicked_id]*self.UserArmTrials[articlePicked_id] + click) / (self.UserArmTrials[articlePicked_id]+1)
        self.UserArmTrials[articlePicked_id] += 1

        self.T[articlePicked_id] += 1
        self.V[articlePicked_id] += click

        self.time += 1
    
    def getTheta(self):
        return self.UserArmMean
    
    def decide(self, pool_articles):

        maxPTA = float('-inf')
        articlePicked = None

        for article in pool_articles:
            s = self.UserArmTrials[article.id]
            if self.T[article.id] > 0:
                U = np.random.binomial(ceil(self.a * s), 0.5)
                mu = (self.V[article.id] + U) / ((self.a + 1) * s)
            else:
                mu = np.inf

            article_pta = mu
            if maxPTA < article_pta:
                articlePicked = article
                maxPTA = article_pta

        return articlePicked

class PHEMultiArmedBandit:
    def __init__(self, num_arm, a):
        self.users = {}
        self.num_arm = num_arm
        self.a = a
        self.CanEstimateUserPreference = False

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = PerturbedHistoryExplorationStruct(self.num_arm, self.a)

        return self.users[userID].decide(pool_articles)

    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.id, click)

    def getTheta(self, userID):
        return self.users[userID].UserArmMean