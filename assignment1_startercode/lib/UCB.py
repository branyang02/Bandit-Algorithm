from multiprocessing import pool
import numpy as np

class UpperConfidenceBoundStruct:
    def __init__(self, num_arm):
        self.d = num_arm

        self.UserArmMean = np.zeros(self.d)
        self.UserArmTrials = np.zeros(self.d)
        self.UCBEquationValue = np.zeros(self.d)

        self.time = 0

    def updateParameters(self, articlePicked_id, click):
        self.UserArmMean[articlePicked_id] = (self.UserArmMean[articlePicked_id]*self.UserArmTrials[articlePicked_id] + click) / (self.UserArmTrials[articlePicked_id]+1)
        #compute values following UCB Equation
        self.UCBEquationValue[articlePicked_id] = self.UserArmMean[articlePicked_id] + np.sqrt((2 * np.log(self.time)) / self.UserArmTrials[articlePicked_id])
        
        self.UserArmTrials[articlePicked_id] += 1

        self.time += 1

    def getTheta(self):
        return self.UCBEquationValue
    
    def decide(self, pool_articles):

        maxValue = float('-inf')
        articlePicked = None

        for article in pool_articles:
            article_value = self.UCBEquationValue[article.id]

            if maxValue < article_value:
                articlePicked = article
                maxValue = article_value

        return articlePicked

class UpperConfidenceBoundMultiArmedBandit:
    def __init__(self, num_arm):
        self.users = {}
        self.num_arm = num_arm
        self.CanEstimateUserPreference = False

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = UpperConfidenceBoundStruct(self.num_arm)
        
        # call decide method
        return self.users[userID].decide(pool_articles)
    
    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.id, click)

    def getTheta(self, userID):
        return self.users[userID].UCBEquationValue