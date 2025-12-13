import re

class lotl:
    def __init__(self,data,nth=-1):
        self.data = data
        self.nth = nth

    def all(self):
        for i in range(len(self.data)):
            if not self.data[i]:
                return False
        return True

    def any(self):
        for i in range(len(self.data)):
            if self.data[i]:
                return True
        return False

    def chain(self):
        hits = []
        for i in range(len(self.data)):
            if isinstance(self.data[i],list) or isinstance(self.data[i],tuple):
                for j in range(len(self.data[i])):
                    hits.append(self.data[i][j])
            else:
                hits = self.data
                break
        return hits

    def dist(self):
        if isinstance(self.data[0], int) and len(self.data) == 2 or isinstance(self.data[0], float) and len(self.data) == 2 and isinstance(self.data[1], int) and len(self.data) == 2 or isinstance(self.data[1], float) and len(self.data) == 2:
            return ((self.data[0] - self.data[1]) ** 2) ** (1 / 2)
        elif isinstance(self.data[0], list) and len(self.data[0]) == 2 or isinstance(self.data[0], tuple) and len(self.data[0]) == 2 and isinstance(self.data[1], list) and len(self.data[0]) == 2 or isinstance(self.data[1], tuple) and len(self.data[1]) == 2:
            return (((self.data[0][0] - self.data[1][0]) ** 2) + ((self.data[0][1] - self.data[1][1]) ** 2)) ** (1 / 2)
        elif isinstance(self.data[0], list) and len(self.data[0]) == 3 or isinstance(self.data[0], tuple) and len(self.data[0]) == 3 and isinstance(self.data[1], list) and len(self.data[0]) == 3 or isinstance(self.data[1], tuple) and len(self.data[1]) == 3:
            return (((self.data[0][0] - self.data[1][0]) ** 2) + ((self.data[0][1] - self.data[1][1]) ** 2) + ((self.data[0][2] - self.data[1][2]) ** 2)) ** (1 / 2)
        else:
            return None

    def flatten(self):
        new_data = self.data
        if self.nth == -1:
            while True:
                if any([True if isinstance(i,list) or isinstance(i,tuple) else False for i in new_data]):
                    add = []
                    for i in new_data:
                        if isinstance(i,list) or isinstance(i,tuple):
                            add += i
                        else:
                            add.append(i)
                    new_data = list(add[:])
                else:
                    break
        else:
            for _ in range(self.nth):
                if any([True if isinstance(i,list) or isinstance(i,tuple) else False for i in new_data]):
                    add = []
                    for i in new_data:
                        if isinstance(i,list) or isinstance(i,tuple):
                            add += i
                        else:
                            add.append(i)
                    new_data = list(add[:])
                else:
                    break
        return new_data

    def mean(self):
        return lotl(self.data).sum() / len(self.data)

    def nested(self):
        count = 0
        new_data = self.data
        while True:
            if any([True if isinstance(i,list) or isinstance(i,tuple) else False for i in new_data]):
                count += 1
                add = []
                for i in new_data:
                    if isinstance(i,list) or isinstance(i,tuple):
                        add += i
                    else:
                        add.append(i)
                new_data = list(add[:])
            else:
                break
        return count

    def stdev(self):
        return (lotl([(i - lotl(self.data).mean()) ** 2 for i in self.data]).sum() / (len(self.data) - 1)) ** (1 / 2)
    
    def sum(self):
        hits = 0
        for i in range(len(self.data)):
            hits += self.data[i]
        return hits

    def tokenizer(self):
        hits = []
        for i in range(1,self.nth):
            tokens = re.findall(r"\w{1," + str(i) + "}", self.data)
            for token in tokens:
                hits.append(token)
        hits = list(dict.fromkeys(hits[:]))
        return hits

    def zscore(self):
        hits = []
        mean = lotl(self.data).mean()
        stdev = lotl(self.data).stdev()
        for i in self.data:
            hits.append((i - mean) / stdev)
        return hits
