import numpy as np

class EpsilonGreedyStruct:
    def __init__(self, featureDimension, lambda_):
        self.d = featureDimension
        self.A = lambda_ * np.identity(n=self.d)
        self.lambda_ = lambda_
        self.b = np.zeros(self.d)
        self.AInv = np.linalg.inv(self.A)

        self.B = np.identity(n=self.d)
        self.mu = np.zeros(self.d)
        self.f = np.zeros(self.d)


        #constants
        self.T = 5000
        self.R = 0.05
        self.delta = 0.5
        self.epsilon = 0.5
        self.v = self.R * np.sqrt(24 / self.epsilon
                                    * self.d
                                    * np.log(1 / self.epsilon))

        self.time = 0

    def updateParameters(self, articlePicked_FeatureVector, click):
        self.A += np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.b += articlePicked_FeatureVector * click
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.dot(self.AInv, self.b)


        self.B += np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.f += articlePicked_FeatureVector * click
        self.mu = np.dot(np.linalg.inv(self.B), self.f)
        # print(self.UserTheta)
        # exit()
        self.time += 1

    def getTheta(self):
        return self.UserTheta

    def getA(self):
        return self.A

    def decide(self, pool_articles):
        maxPTA = float('-inf')
        articlePicked = None

        for article in pool_articles:
            mu_tilde = np.random.multivariate_normal(self.mu, (self.v ** 2) * np.linalg.inv(self.B))
            article_pta = np.dot(mu_tilde, article.featureVector)
            # pick article with highest Prob
            if maxPTA < article_pta:
                articlePicked = article
                maxPTA = article_pta
        return articlePicked

class HEHEHEHEHE:
    def __init__(self, dimension, lambda_):
        self.users = {}
        self.dimension = dimension
        self.lambda_ = lambda_
        self.CanEstimateUserPreference = True

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = EpsilonGreedyStruct(self.dimension, self.lambda_)

        return self.users[userID].decide(pool_articles)

    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.featureVector[:self.dimension], click)

    def getTheta(self, userID):
        return self.users[userID].UserTheta