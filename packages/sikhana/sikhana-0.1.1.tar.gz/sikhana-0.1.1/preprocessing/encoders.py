
import string
class encoding_error(Exception):
    pass
class LabelEncoder:
    def fit(self,data:list,dtype=bool):
        unique = list(dict.fromkeys(data))
        encoded= []
        if len(unique)>2:
            raise encoding_error("only two unique values allowed")
        unique_d = list(unique)
        for i in data:
            if i == unique_d[0]:
                encoded.append(dtype(True))
            elif i == unique_d[1]:
                encoded.append(dtype(False))
        self.encoded = encoded
    def get_encode(self):
        return (self.encoded)
class OneHotEncoder():
    def fit(self,data:list,dtype=bool):
        unique = list(dict.fromkeys(data))
        encoded = {}
        for i in unique:
            encoded.update({i:[]})
        for i in data:
            for j in encoded:
                encoded[j].append(dtype(i==j))
        self.encoded = encoded
    def get_encoded(self,string_no=False):
        if string_no:
            ecnoded =[]
            for i in self.encoded:
                ecnoded.append(self.encoded.get(i))
            return ecnoded
        else:
            return self.encoded
class BinaryEncoder():
    def alphabets_to_bin(self,n):
        con = list(string.ascii_letters)
        converter = {}
        mid = []
        for i in range(0,10):
            converter.update({str(i):str(bin(i)).replace("0b","")})
        for i,j in zip(con,range(11,63)):
            converter.update({i:str(bin(j).replace("0b",""))})  
        converter[' '] = str(bin(63)).replace("0b","")
        for y,z in zip(string.punctuation,range(64,64+len(string.punctuation)+1)):
            converter.update({y:str(bin(z)).replace("0b","")})       
        for z in str(n):
            mid.append(str(converter.get(z)))
        result = "".join(mid)
        return result
    def fit(self,data:list,dtype=bool):
        unique = list(dict.fromkeys(data))
        encoded = {}
        compare = {}
        for i in unique:
            encoded.update({self.alphabets_to_bin(i):[]})
            compare.update({i:self.alphabets_to_bin(i)})
        for i in data:
            for j in encoded:
                real_encode = compare.get(i)
                encoded[j].append(dtype(real_encode==j))
        self.encoded = encoded
    def get_encoded(self,string_no=False):
        if string_no:
            ecnoded =[]
            for i in self.encoded:
                ecnoded.append(self.encoded.get(i))
            return ecnoded
        else:
            return self.encoded
class OrdinalEnocder:
    def fit(self,data:list,order=None):
        if order==None:
            raise TypeError('there must be an ordert to use the ordinal encoder is your data has no order please use our one hot encoder or you must give an order in the form od dict (eg,{"low":1,"medium":2}and etc)')
        encoded = []
        for i in data:
            encoded.append(order.get(i))
        self.encoded = encoded
    def get_encoded(self):
        return self.encoded
class multiple_label_encoder:
    def fit(self,data):
        unique = list(dict.fromkeys(data))
        encoded = []
        for i in data:
            for  j in unique:
                if i==j:
                    encoded.append(unique.index(j))
                    break
        self.encoded = encoded
    def get_encoded(self):
        return self.encoded