from Movie.models import Movie
from rate.models import Rate
import numpy as np
from math import sqrt
import pandas as pd
from scipy import sparse

class PrePareData:
    user_id = None
    def __init__(self,id):
        self.user_id=id

    def readData(self):
        dataset = Rate.objects.all()
        userid,movieid,rate,title = [],[],[],[]
        for a in dataset:
            userid.append(a.user_id)
            movieid.append(a.movie_id)
            title.append(a.movie.movie_name)
            if a.rating==None:
                rate.append(0)
            else:
                rate.append(a.rating)
        finaldata = {
            'userid':userid,
            'movieid':movieid,
            'rate':rate,
            'title':title
        }
        df = pd.DataFrame.from_dict(finaldata)
        return df

    def get_user_rate_movie(self):
        user_rate = Rate.objects.filter(user_id=self.user_id)
        rate,movieid,title = [],[],[]
        for r in user_rate:
            rate.append(r.rating)
            movieid.append(r.movie_id)
            title.append(r.movie.movie_name)
        dataset = {
            'title':title,
            'rate':rate,
            'movieid':movieid
        }
        return pd.DataFrame.from_dict(dataset)

    def findSameUserWhoWatchedSameMovie(self):
        allDataset = self.readData()
        userDataset = self.get_user_rate_movie()
        users = allDataset[allDataset['movieid'].isin(userDataset['movieid'].tolist())]
        userSubsetGroup = users.groupby(['userid'])
        userSubsetGroup = sorted(userSubsetGroup, key=lambda x: len(x[1]), reverse=True)
        return userSubsetGroup

    def calcuatePearsonCoffiecient(self):
        pearsonCorDict = {}
        inputMovie = self.get_user_rate_movie()
        userSubsetGroup = self.findSameUserWhoWatchedSameMovie()
        for name,group in userSubsetGroup:
            # Let's start by sorting the input and current user group so the values aren't mixed up later on
            group = group.sort_values(by='movieid')
            inputMovie = inputMovie.sort_values(by='movieid')
            n = len(group)
            temp = inputMovie[inputMovie['movieid'].isin(group['movieid'].tolist())]
            # And then store them in a temporary buffer variable in a list format to facilitate future calculations
            tempRatingList = temp['rate'].tolist()
            # put the current user group reviews in a list format
            tempGroupList = group['rate'].tolist()
            # Now let's calculate the pearson correlation between two users, so called, x and y
            Sxx = sum([i ** 2 for i in tempRatingList]) - pow(sum(tempRatingList), 2) / float(n)
            Syy = sum([i ** 2 for i in tempGroupList]) - pow(sum(tempGroupList), 2) / float(n)
            Sxy = sum(i * j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList) * sum(
                tempGroupList) / float(n)
            if Sxx != 0 and Syy != 0:
                pearsonCorDict[name] = Sxy / sqrt(Sxx * Syy)
            else:
                pearsonCorDict[name] = 0

            return pd.DataFrame.from_dict(pearsonCorDict, orient='index')


