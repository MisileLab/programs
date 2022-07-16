from numpy.random import randint
from math import floor
from tqdm import tqdm

minutelist = []

class Tree:
    def __init__(self):
        self.point = 1
    
    def grow(self) -> bool:
        temp = randint(0, 100) <= (1/(floor(25/self.point) + 1)) * 100
        self.point += 1
        return temp

for _ in tqdm(range(10000)):
    trees = 90
    treelist = []
    wood = 0
    success = False
    looping = 0
    minute = 0
    for _ in range(trees):
        treelist.append(Tree())

    while not success:
        for i, i2 in enumerate(treelist):
            if i2.grow():
                del treelist[i]
        looping += 1
        if looping == 3:
            looping = 0
            minute += 1
        if treelist.__len__() == 0:
            success = True
    
    minutelist.append(minute)

print(f"average minute: {sum(minutelist) / len(minutelist)}")