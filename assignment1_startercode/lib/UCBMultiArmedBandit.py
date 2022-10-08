import numpy as np


class UpperConfidenceBoundStruct:
    def __init__(self, num_arm, alpha):
        self.d = num_arm
        self.alpha = alpha

        self.UserArmMean = np.zeros(self.d)
        self.UserArmTrials = np.zeros(self.d)
        self.time = 0
        self.play_dict = {}

    def updateParameters(self, articlePicked_id, click):
        self.UserArmMean[articlePicked_id] = (self.UserArmMean[articlePicked_id]*self.UserArmTrials[articlePicked_id] + click) / (self.UserArmTrials[articlePicked_id]+1)
        self.UserArmTrials[articlePicked_id] += 1

        self.time += 1

    def getTheta(self):
        return self.UserArmMean
    
    def decide(self, pool_articles):
        maxValue = float('-inf')
        articlePicked = None
        for article in pool_articles:
            # play all the arms once first
            if self.UserArmTrials[article.id] == 0:
                return article
            article_value = self.UserArmMean[article.id] + (self.alpha * np.sqrt((2 * np.log(self.time)) / self.UserArmTrials[article.id]))
            if maxValue < article_value:
                articlePicked = article
                maxValue = article_value
        return articlePicked

class UpperConfidenceBoundMultiArmedBandit:
    def __init__(self, num_arm, alpha):
        self.users = {}
        self.num_arm = num_arm
        self.alpha = alpha
        self.CanEstimateUserPreference = False

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = UpperConfidenceBoundStruct(self.num_arm, self.alpha)
        
        # call decide method
        return self.users[userID].decide(pool_articles)
    
    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.id, click)

    def getTheta(self, userID):
        return self.users[userID].UserArmMean