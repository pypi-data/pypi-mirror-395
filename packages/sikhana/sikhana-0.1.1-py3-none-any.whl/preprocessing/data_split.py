import random 
def split(X,y,train_per=80,test_per=20):
    if train_per + test_per!=100:
        raise ValueError("the sum of train percetnge and test percenntage must be 100")
    if type(X)!=list or type(y)!=list:
        raise TypeError("X and y must be lists")
    if len(X)!=len(y):
        raise ValueError("X and y must be same")
    both = [X,y]
    transposed = []
    for i in zip(*both):
        transposed.append(i)
    number_of_instances_in_train = round((train_per/100)*len(X))
    random.shuffle(transposed)
    train_data = transposed[:number_of_instances_in_train]
    test_data = transposed[number_of_instances_in_train:]
    train_X = []
    train_y = []
    for i in train_data:
        train_X.append(i[0])
        train_y.append(i[1])
    test_X = []
    test_y = []
    for i in test_data:
        test_X.append(i[0])
        test_y.append(i[1])
    return train_X,train_y,test_X,test_y 