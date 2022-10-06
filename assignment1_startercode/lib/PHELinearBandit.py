from math import ceil
import numpy as np

class PHEStruct:

    def __init__(self, featureDimension, lambda_, a):
        self.d = featureDimension
        self.A = lambda_ * np.identity(n=self.d)
        self.lambda_ = lambda_
        self.a = a
        
        self.b = np.zeros(self.d)
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.zeros(self.d)

        self.play_dict = {}
        self.time = 0

        self.G = np.zeros(shape=(self.d, self.d))
        self.Theta = np.zeros(self.d)

    def updateParameters(self, articlePicked_FeatureVector, click):
        self.G += (self.a + 1) * (np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector) + (self.lambda_*(self.a + 1)*np.identity(n=self.d)))
        self.Theta += np.dot(np.linalg.inv(self.G), (articlePicked_FeatureVector * (click + np.random.binomial(ceil(self.a), 0.5))))

    def getTheta(self):
        return self.UserTheta

    def getA(self):
        return self.A
    
    def decide(self, pool_articles):

        maxPTA = float('-inf')
        articlePicked = None

        for article in pool_articles:
            article_pta = np.dot(self.Theta, article.featureVector)

            if maxPTA < article_pta:
                articlePicked = article
                maxPTA = article_pta
        
        return articlePicked

class PHELinearBandit:

    def __init__(self, dimension, lambda_, a):
        self.users = {}
        self.dimension = dimension
        self.lambda_ = lambda_
        self.a = a
        self.CanEstimateUserPreference = True

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = PHEStruct(self.dimension, self.lambda_, self.a)

        return self.users[userID].decide(pool_articles)
    
    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.featureVector[:self.dimension], click)

    def getTheta(self, userID):
        return self.users[userID].UserTheta