import numpy as np

class ThompsonSamplingStruct:
    """
    Parameters
    ----------
    T: number of runs
    delta: float, 0 < delta < a
            with probability 1-delta, LinTS satisfies the theoretical regret bound.
    R: float, R >= 0, default to 0.01
        assume that the residual: ri(t) - bi(t)^T \hat{\mu}
        is R-sub-gaussian. In this case, R^2 represents the variance for
        residuals of the linear model: bi(t)^T
    """


    def __init__(self, featureDimension, T, delta, R):
        self.d = featureDimension
        self.epsilon = 1 / np.log(T)
        self.delta = delta
        self.R = R

        self.B = np.identity(n=self.d)
        self.mu_hat = np.zeros(self.d)
        self.f = np.zeros(self.d)

        self.time = 0

        

    def updateParameters(self, articlePicked_FeatureVector, click):

        self.B += np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.f += articlePicked_FeatureVector * click
        self.mu_hat = np.dot(np.linalg.inv(self.B), self.f)

        self.time += 1


    def getTheta(self):
        return self.mu_hat

    def getA(self):
        return self.B

    def decide(self, pool_articles):

        v = self.R * np.sqrt(24/self.epsilon * self.d * np.log(1/self.delta))
        maxPTA = float('-inf')
        articlePicked = None

        for article in pool_articles:
            mu_tilde = np.random.multivariate_normal(self.mu_hat, (v**2) * np.linalg.inv(self.B))
            article_pta = np.dot(mu_tilde, article.featureVector)

            if maxPTA < article_pta:
                articlePicked = article
                maxPTA = article_pta
        return articlePicked

class ThompsonSamplingLinearBandit:
    def __init__(self, dimension, T, delta, R):
        self.users = {}
        self.dimension = dimension
        self.T = T
        self.delta = delta
        self.R = R
        self.CanEstimateUserPreference = True

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = ThompsonSamplingStruct(self.dimension, self.T, self.delta, self.R)

        return self.users[userID].decide(pool_articles)

    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.featureVector[:self.dimension], click)

    def getTheta(self, userID):
        return self.users[userID].mu_hat