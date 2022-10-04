import numpy as np

class UpperConfidenceBoundStruct:

    def __init__(self, featureDimension, lambda_, alpha):
        self.d = featureDimension
        self.A = lambda_ * np.identity(n=self.d)
        self.lambda_ = lambda_
        self.alpha = alpha
        
        self.b = np.zeros(self.d)
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.zeros(self.d)

        self.time = 0

        #self.list = [0,0,0]

    def updateParameters(self, articlePicked_FeatureVector, click):
        # expected value(r_a_t) = E[r(t,a)|x(t|a)]
        self.A += np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.b += articlePicked_FeatureVector * click
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.dot(self.AInv, self.b)

        # self.UCBEquationValue = self.UserTheta + self.alpha * np.sqrt()

        self.time += 1

    def getTheta(self):
        return self.UserTheta
    
    def getA(self):
        return self.A

    def decide(self, pool_articles):

        maxPTA = float('-inf')
        articlePicked = None

        for article in pool_articles:
            article_pta = np.dot(self.UserTheta, article.featureVector) + (self.alpha * np.sqrt(np.dot(np.dot(np.transpose(article.featureVector), self.AInv), article.featureVector)))

            if maxPTA < article_pta:
                articlePicked = article
                maxPTA = article_pta
        #print(pool_articles.index(articlePicked))
        # list = [0,0,0]
        # self.list[pool_articles.index(articlePicked)] += 1
        # print(self.list)
        #exit() if self.time == 4 else print(self.list)
        return articlePicked

class UpperConfidenceBoundLinearBandit:
    def __init__(self, dimension, lambda_, alpha):
        self.users = {}
        self.dimension = dimension
        self.lambda_ = lambda_
        self.alpha = alpha
        self.CanEstimateUserPreference = True

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = UpperConfidenceBoundStruct(self.dimension, self.lambda_, self.alpha)

        return self.users[userID].decide(pool_articles)

    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.featureVector[:self.dimension], click)

    def getTheta(self, userID):
        return self.users[userID].UserTheta