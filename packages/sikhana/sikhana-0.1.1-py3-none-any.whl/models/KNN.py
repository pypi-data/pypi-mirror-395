from collections import Counter
import math
class KNN:
    def fit(self,X,y):
        self.X   = X
        self.y = y
    def predict(self,value,K=2,method="Distance",mode="categerical"):
        D = []
        for i,p in zip(self.X,self.y):
            e = 0
            for y,z in zip(i,value):
                e += (y-z)**2
            d = math.sqrt(e)
            D.append([d,p])
        D.sort()
        K_neighbours = []
        if method == "Distance":
            for i in D:
                if i[0]<=K:
                    K_neighbours.append(i)
        elif method == "Top":
            K_neighbours = D[:K]
        else:
            for i in D:
                if i[0]<=K:
                    K_neighbours.append(i)
        if not K_neighbours:
            return None
        answers = [q[1]for q in K_neighbours]
        if mode == "categerical":
            w = Counter(answers)
            winner = w.most_common()
            return winner[0]
        elif mode == "Regression":
            d = sum(answers)/len(answers)
            return d
        else:
            w = Counter(answers)
            winner = w.most_common()
            return winner[0]