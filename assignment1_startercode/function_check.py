import numpy as np

class ThompsonSamplingStructdfdfdf:
    
    def __init__(self, num_arm): 
        self.d = num_arm
        #self.sigma = sigma  # sigma is standard deviation

        # intialize priors
        # average reward for EACH arm: mu = 0; sigma = 1000
        self.priors = [[0, 1] for _ in range(num_arm)]  # this is the flat prior
        # self.priors = [[0,1000], ..., [0, 1000]]
        # index 0: mean
        # index 1: standard deviation

        self.UserArmMean = np.zeros(self.d)
        self.UserArmTrials = np.zeros(self.d)
        self.reward_list = [[] for _ in range(num_arm)]

        self.time = 0

    def updateParameters(self, articlePicked_id, click):
        # compute UserArmMean
        self.UserArmMean[articlePicked_id] = (self.UserArmMean[articlePicked_id]*self.UserArmTrials[articlePicked_id] + click) / \
        (self.UserArmTrials[articlePicked_id]+1)
        # add to list of rewards
        self.reward_list[articlePicked_id].append(click)
        # increment times visited
        self.UserArmTrials[articlePicked_id] += 1
        # update posterior mean
        self.priors[articlePicked_id][0] = sum(self.reward_list[articlePicked_id]) / (self.UserArmTrials[articlePicked_id] + 1)
        #update posterior standard deviation
        self.priors[articlePicked_id][1] = 1 / (self.UserArmTrials[articlePicked_id] + 1)

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

class ThompsonSamplingMultiArmedBandithehehehehh:
    def __init__(self, num_arm):
        self.users = {}
        self.num_arm = num_arm
        self.CanEstimateUserPreference = False

    def decide(self, pool_articles, userID):
        if userID not in self.users:
            self.users[userID] = ThompsonSamplingStructdfdfdf(self.num_arm)
        
        return self.users[userID].decide(pool_articles)
    
    def updateParameters(self, articlePicked, click, userID):
        self.users[userID].updateParameters(articlePicked.id, click)

    def getTheta(self, userID):
        return self.users[userID].UserArmMean

