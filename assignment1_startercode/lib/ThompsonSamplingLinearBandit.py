import numpy as np

class ThompsonSamplingStruct:

    def __init__(self, featureDimension, lambda_, sigma):
        self.d = featureDimension
        self.A = lambda_ * np.identity(n=self.d)
        self.lambda_ = lambda_
        self.sigma = sigma
        self.b = np.zeros(self.d)
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.zeros(self.d)
        self.time = 0

    def updateParameters(self, articlePicked_FeatureVector, click):
        self.A += (1/(self.sigma**2)) * np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.b += (1/(self.sigma**2)) * (articlePicked_FeatureVector * click)
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.random.multivariate_normal(np.dot(self.AInv, self.b), self.AInv)
        self.time += 1
    
    def getTheta(self):
        return self.UserTheta
    
    def getA(self):
        return self.A

    def decide(self, pool_articles):
        
        maxPTA = float('-inf')
        articlePicked = None

        for article in pool_articles:
            article_pta = np.dot(self.UserTheta, article.featureVector)

            if maxPTA < article_pta:
                articlePicked = article
                maxPTA = article_pta
        
        return articlePicked

class ThompsonSamplingLinearBandit:

    def __init__(self, dimension, lambda_, sigma):
        self.users = {}
        self.dimension = dimension
        self.lambda_ = lambda_
        self.sigma = sigma
        self.CanEstimateUserPreference = True

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = ThompsonSamplingStruct(self.dimension, self.lambda_, self.sigma)

        return self.users[userID].decide(pool_articles)
    
    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.featureVector[:self.dimension], click)

    def getTheta(self, userID):
        return self.users[userID].UserTheta