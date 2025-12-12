import math
from collections import Counter
import random
import sys  
sys.setrecursionlimit(10000)
def mean(v):
    sum = 0
    for i in v:
        sum = sum + i
    return sum/len(v)
def std(p):
    m = mean(p)
    dif = []
    dif_sqr = []
    for i in p:
        dif.append(i-m)
    for j in dif:
        dif_sqr.append(j**2)
    r = sum(dif_sqr)/len(p)
    final = math.sqrt(r)
    return final if r!=0 else 1e-8
class DecisionTreeClassifier:
    def __build_tree__(self,X,y,method="Equality",criterion="impurity",max_depth=None):
        if  max_depth==None:
            fully_continue=True
        else:
            fully_continue=False
            if max_depth==0:
                v = Counter(y)
                value = v.most_common()[0]
                return {"leaf":value[0]}   
        unique = list(dict.fromkeys(y))
        total = len(y)
        proportions = []
        for i in unique:
            t = y.count(i)
            proportions.append(t/total)
        if criterion=="impurity":
            G_main = 1 -sum(p**2 for p in proportions)
        else:
            G_main = -sum(p*math.log2(p) for p in proportions)
        features = []
        for j in zip(*X):
            features.append(j)
        uniques = []
        for k in features:
            uniques.append(list(dict.fromkeys(k)))
        best_gain = -1
        best_feature_index = None
        best_split_value = None
        best_X_psplit = None
        best_y_psplit = None
        best_X_qsplit = None
        best_y_qsplit = None
        for f_idx,(i,j) in enumerate(zip(features,uniques)):
            for n in j:
                p = []
                q = []
                for ij,kl in enumerate(i):
                    if method == "Equality":
                        if kl == n:
                            p.append(ij)
                        else:
                            q.append(ij)
                    else:
                        if kl <= n:
                            p.append(ij)
                        else:
                            q.append(ij)
                if len(p) == 0 or len(q) == 0:
                    continue
                X_psplit = [X[ml]for ml in p]
                y_psplit = [y[nl]for nl in p]
                X_qsplit = [X[bn]for bn in q]
                y_qsplit = [y[something]for something in q]
                p_unique = list(dict.fromkeys(y_psplit))
                q_unique = list(dict.fromkeys(y_qsplit))
                p_prop = []
                q_prop = []
                for s in p_unique:
                    count = y_psplit.count(s)
                    p_prop.append(count/len(p))
                for t in q_unique:
                    c = y_qsplit.count(t)
                    q_prop.append(c/len(q))
                if criterion=="impurity":
                    p_gini = 1 - sum(proportion**2 for proportion in p_prop)
                    q_gini = 1 - sum(propo**2 for propo in q_prop)
                else:
                    p_gini = -sum(proportion*math.log2(proportion)for proportion in p_prop)
                    q_gini = -sum(prop*math.log2(prop)for prop in q_prop)
                tota = len(p)+len(q)
                g_weight = (len(p)/tota)*p_gini + (len(q)/tota)*q_gini
                gini_gain = G_main - g_weight
                if gini_gain > best_gain:
                    best_gain = gini_gain
                    best_X_psplit =X_psplit
                    best_X_qsplit = X_qsplit
                    best_y_psplit =  y_psplit
                    best_y_qsplit = y_qsplit
                    best_feature_index = f_idx
                    best_split_value = n      
        nodes = {}   
        if best_gain<=0:
            v = Counter(y)
            value = v.most_common()[0]
            nodes.update({"leaf":value[0]})
        else:
            if fully_continue:
                left = self.__build_tree__(best_X_psplit,best_y_psplit,method)
                right = self.__build_tree__(best_X_qsplit,best_y_qsplit,method)
                nodes.update({"left":left,
                          "right":right,
                          "feature_index":best_feature_index,
                          "split_value":best_split_value})
            else:
                left = self.__build_tree__(best_X_psplit,best_y_psplit,method,max_depth=max_depth-1) #type:ignore
                right = self.__build_tree__(best_X_qsplit,best_y_qsplit,method,max_depth=max_depth-1) #type:ignore
                nodes.update({"left":left,
                          "right":right,
                          "feature_index":best_feature_index,
                          "split_value":best_split_value})             
        return nodes
    def  fit(self,X,y,method="Equality",criterion="impurity",max_depth=None):
        self.tree = self.__build_tree__(X,y,method,criterion=criterion,max_depth=max_depth)
        self.method = method
    def _predict_sample_(self,X,node):
        if "leaf" in node:
            return node["leaf"]
        else:
            feature_index = node["feature_index"]
            split_value = node["split_value"]
            raja = X[feature_index]
            if self.method == "Equality":
                if raja == split_value:
                    return self._predict_sample_(X,node["left"])
                else:
                    return self._predict_sample_(X,node["right"])
            else:
                if raja <= split_value:
                    return self._predict_sample_(X,node["left"])
                else:
                    return self._predict_sample_(X,node["right"])
    def predict(self,X):
        ans = self._predict_sample_(X,self.tree)
        return ans
class DecisionTreeRegression:
    def __build_tree__(self,X,y,method="Thershold",criterion="variance",max_depth=None):
        if max_depth==None:
            fully_continue = True
        else:
            fully_continue = False
            if max_depth==0:
                 return {"leaf": mean(y)}
        if criterion=="variance":
            G_main = std(y)**2
        else:
            m = mean(y)
            l = []
            for each_value in y:
                l.append((each_value-m)**2)
            G_main = mean(l)
        features = []
        for j in zip(*X):
            features.append(j)
        uniques = []
        for k in features:
            uniques.append(list(dict.fromkeys(k)))
        best_gain = -1
        best_feature_index = None
        best_split_value = None
        best_X_psplit = None
        best_y_psplit = None
        best_X_qsplit = None
        best_y_qsplit = None
        for f_idx,(i,j) in enumerate(zip(features,uniques)):
            for n in j:
                p = []
                q = []
                for ij,kl in enumerate(i):
                    if method == "Equality":
                        if kl == n:
                            p.append(ij)
                        else:
                            q.append(ij)
                    else:
                        if kl <= n:
                            p.append(ij)
                        else:
                            q.append(ij)
                if len(p) == 0 or len(q) == 0:
                    continue
                X_psplit = [X[ml]for ml in p]
                y_psplit = [y[nl]for nl in p]
                X_qsplit = [X[bn]for bn in q]
                y_qsplit = [y[something]for something in q]
                tota = len(p)+len(q)
                if criterion=="variance":
                    p_gain = std(y_psplit)**2
                    q_gain = std(y_qsplit)**2
                else:
                    average_p = mean(y_psplit)
                    average_q = mean(y_qsplit)
                    list_for_p = []
                    list_for_q = []
                    for each_number in y_psplit:
                        list_for_p.append((each_number-average_p)**2)
                    p_gain = sum(list_for_p)/len(list_for_p)
                    for each_number in y_qsplit:
                        list_for_q.append((each_number-average_q)**2)
                    q_gain = sum(list_for_q)/len(list_for_q)
                g_weight = (len(p)/tota)*p_gain + (len(q)/tota)*q_gain
                gain = G_main - g_weight
                if gain > best_gain:
                    best_gain = gain
                    best_X_psplit =X_psplit
                    best_X_qsplit = X_qsplit
                    best_y_psplit =  y_psplit
                    best_y_qsplit = y_qsplit
                    best_feature_index = f_idx
                    best_split_value = n      
        nodes = {}   
        if best_gain<=0:
            nodes.update( {"leaf":mean(y)})
        else:
            if fully_continue:
                left = self.__build_tree__(best_X_psplit,best_y_psplit,method)
                right = self.__build_tree__(best_X_qsplit,best_y_qsplit,method)
                nodes.update({"left":left,
                          "right":right,
                          "feature_index":best_feature_index,
                          "split_value":best_split_value})
            else:
                left = self.__build_tree__(best_X_psplit,best_y_psplit,method,max_depth=max_depth-1) #type:ignore
                right = self.__build_tree__(best_X_qsplit,best_y_qsplit,method,max_depth=max_depth-1) #type:ignore
                nodes.update({"left":left,
                          "right":right,
                          "feature_index":best_feature_index,
                          "split_value":best_split_value})
        return nodes
    def  fit(self,X,y,method="Equality",criterion="variance",max_depth=None):
        self.tree = self.__build_tree__(X,y,method,criterion=criterion,max_depth=max_depth)
        self.method = method
    def _predict_sample_(self,X,node):
        if "leaf" in node:
            return node["leaf"]
        else:
            feature_index = node["feature_index"]
            split_value = node["split_value"]
            raja = X[feature_index]
            if self.method == "Equality":
                if raja == split_value:
                    return self._predict_sample_(X,node["left"])
                else:
                    return self._predict_sample_(X,node["right"])
            else:
                if raja <= split_value:
                    return self._predict_sample_(X,node["left"])
                else:
                    return self._predict_sample_(X,node["right"])
    def predict(self,X):
        ans = self._predict_sample_(X,self.tree)
        return  ans
class RandomForestClassifier:
    def fit(self,X,y,n_trees=5,min_samples=None,max_samples=None,min_features=None,max_features=None,method_for_trees="Equality",criterion_for_trees="impurity"):
        if len(X)!=len(y):
            raise TypeError("data must be of same length")
        for  i in X:
            for j in i:
                if type(j)!=int and type(j)!= float:
                    raise ValueError("the data must be be in numbers")
        for i  in y:
            if type(i)!= int and type(i)!=float:
                raise ValueError("the label must in numberds")
        if min_samples==None or max_samples==None:
            min_samples = round((30/100)*len(X))if round((30/100)*len(X))!=0 else 1
            max_samples = round((60/100)*len(X))if round((60/100)*len(X))!=0 or round((60/100)*len(X))>=min_samples else 1
        else:
            min_samples = min_samples
            max_samples = max_samples
            if min_samples==0 or max_samples==0:
                raise TypeError("min andd max samples should not be 0 first go and learn how to use random forests")
        number_of_samples_for_each_tree = []
        random.seed(None)
        for i in range(n_trees):
            number_of_samples_for_each_tree.append(random.randint(min_samples,max_samples))
        indexes_for_samples = []
        for i in range(n_trees):
            n = number_of_samples_for_each_tree[i]
            indexes_for_samples.append(random.choices(range(len(X)),k=n))
        sampled_data = []
        trainng_y = []
        for i in range(n_trees):
            n = indexes_for_samples[i]
            tree_x = []
            tree_y = []
            for j in n:
                tree_x.append(X[j])
                tree_y.append(y[j])
            sampled_data.append(tree_x)
            trainng_y.append(tree_y)
        total_features = len(X[0])
        if min_features==None or max_features==None:
            min_features = round(math.log2(total_features))if round(math.log2(total_features))!=0 else 1
            max_features = round((70/100)*total_features)if round((70/100)*total_features)!=0 or round((70/100)*total_features)>min_features else 1
        else:
            min_features = min_features
            max_features = max_features
            if min_features==0 or max_features==0:
                raise TypeError("the min and max features must be greater than 0")
            if min_features>max_features:
                raise TypeError("the max  features should be larger than min features")
            if max_features>total_features:
                raise ValueError("the max features hsould not be greater than total number of features")
        number_of_features_for_each = []
        for i in range(n_trees):
            number_of_features_for_each.append(random.randint(min_features,max_features))
        feature_indexes = []
        for i in range(n_trees):
            s = number_of_features_for_each[i]
            feature_indexes.append(random.sample(range(total_features),k=s))
        sliced = []
        for i in range(n_trees):
            tree_x = []
            slicing_data = sampled_data[i]
            f = feature_indexes[i]
            for j in slicing_data:
                tree_x.append([j[p] for p in f])
            sliced.append(tree_x)
        model = {}
        for i in range(n_trees):
            model.update({i:DecisionTreeClassifier()})
        for i in range(n_trees):
            model[i].fit(sliced[i], trainng_y[i], method=method_for_trees,criterion=criterion_for_trees)
        self.models = model
        self.features = feature_indexes
    def predict(self,X):
        predictions = []
        for i in range(len(self.models)):
            f = self.features[i]
            t = [X[p] for p in f]
            label = self.models[i].predict(t)
            predictions.append(label)
        count = Counter(predictions)
        return count.most_common(1)[0][0]
class RandomForestRegression:
    def fit(self,X,y,n_trees=5,min_samples=None,max_samples=None,min_features=None,max_features=None,method_for_trees="Thershold",criterion_for_trees="variance",max_depth=None):
        if len(X)!=len(y):
            raise TypeError("data must be of same length")
        for  i in X:
            for j in i:
                if type(j)!=int and type(j)!= float:
                    raise ValueError("the data must be be in numbers")
        for i  in y:
            if type(i)!= int and type(i)!=float:
                raise ValueError("the label must in numberds")
        if min_samples==None or max_samples==None:
            min_samples = round((30/100)*len(X))if round((30/100)*len(X))!=0 else 1
            max_samples = round((60/100)*len(X))if round((60/100)*len(X))!=0 or round((60/100)*len(X))>=min_samples else 1
        else:
            min_samples = min_samples
            max_samples = max_samples
            if min_samples==0 or max_samples==0:
                raise TypeError("min andd max samples should not be 0 first go and learn how to use random forests")
        number_of_samples_for_each_tree = []
        random.seed(None)
        for i in range(n_trees):
            number_of_samples_for_each_tree.append(random.randint(min_samples,max_samples))
        indexes_for_samples = []
        for i in range(n_trees):
            n = number_of_samples_for_each_tree[i]
            indexes_for_samples.append(random.choices(range(len(X)),k=n))
        sampled_data = []
        trainng_y = []
        for i in range(n_trees):
            n = indexes_for_samples[i]
            tree_x = []
            tree_y = []
            for j in n:
                tree_x.append(X[j])
                tree_y.append(y[j])
            sampled_data.append(tree_x)
            trainng_y.append(tree_y)
        total_features = len(X[0])
        if min_features==None or max_features==None:
            min_features = round(math.log2(total_features))if round(math.log2(total_features))!=0 else 1
            max_features = round((70/100)*total_features)if round((70/100)*total_features)!=0 or round((70/100)*total_features)>min_features else 1
        else:
            min_features = min_features
            max_features = max_features
            if min_features==0 or max_features==0:
                raise TypeError("the min and max features must be greater than 0")
            if min_features>max_features:
                raise TypeError("the max  features should be larger than min features")
            if max_features>total_features:
                raise ValueError("the max features hsould not be greater than total number of features")
        number_of_features_for_each = []
        for i in range(n_trees):
            number_of_features_for_each.append(random.randint(min_features,max_features))
        feature_indexes = []
        for i in range(n_trees):
            s = number_of_features_for_each[i]
            feature_indexes.append(random.sample(range(total_features),k=s))
        sliced = []
        for i in range(n_trees):
            tree_x = []
            slicing_data = sampled_data[i]
            f = feature_indexes[i]
            for j in slicing_data:
                tree_x.append([j[p] for p in f])
            sliced.append(tree_x)
        model = {}
        for i in range(n_trees):
            model.update({i:DecisionTreeRegression()})
        for i in range(n_trees):
            model[i].fit(sliced[i], trainng_y[i], method=method_for_trees,criterion=criterion_for_trees,max_depth=max_depth)
        self.models = model
        self.features = feature_indexes
    def predict(self,X):
        predictions = []
        for i in range(len(self.models)):
            f = self.features[i]
            t = [X[p] for p in f]
            label = self.models[i].predict(t)
            predictions.append(label)
        return mean(predictions)