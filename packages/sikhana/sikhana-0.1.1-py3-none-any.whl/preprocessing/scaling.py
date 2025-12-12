import math
class MinMaxScaler:
    def fit(self,value):
        self.min = min(value)
        self.max = max(value)
        self.value = value
    def get_scaled(self):
        scaled = []
        for i in self.value:
            scaled.append((i-self.min)/(self.max-self.min))
        return scaled
class StandardScaler:
    @staticmethod
    def mean(value):
        return sum(value)/len(value)
    def std(self,v):
        m = self.mean(v)
        deviations =[]
        square_deviation =[]
        for i in v:
            deviations.append(i-m)
        for j in deviations:
            square_deviation.append(j**2)
        add = sum(square_deviation)
        variance = add/(len(v)-1)
        return math.sqrt(variance)
    def fit(self,value):
        scaled = []
        self.average = self.mean(value)
        self.standard_deviation = self.std(value)
        for i in value:
            scaled.append((i-self.average)/self.standard_deviation)
        self.scaled = scaled
    def get_scaled(self):
        return self.scaled 
    def get_scaled_with_preddefined_std_and_mean(self,standard_deviation,average,value):
        scaled = []
        for  i in value:
            scaled.append((i-average)/standard_deviation)
        return scaled
    