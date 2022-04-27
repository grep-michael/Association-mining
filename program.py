#!/usr/bin/env python3

"""
banana
pear
apple
strawberry
blueberry
raspberry
"""




from operator import truediv
from pprint import pprint

BASKET_TOTAL = 8


def load_items():
    f = open("./data.txt")
    f.seek(0)
    baskets = []
    for i in f:
        baskets.append(i.strip().split(','))
    return baskets

def get_unique_items(baskets):
    #stolen :)
    c =[]
    for basket in baskets:
        for item in basket:
            if item not in c:
                c.append((item,))
    c.sort()
    return c



def generate_pairs(c):
    uniques = []
    for s in c:
        for item in s:
            if item not in uniques:
                uniques.append(item)
    # get all unqie values from L
    #rint("Start of generate pairs")
    pairs =[]
    keys = list(c.keys())
    #print("keys:")
    #pprint(keys)
    #print("pairs:")
    
    for i in uniques:
        for j in keys:
            pair = list(j)
            if i not in pair:
                pair.append(i)
                pair.sort()
                pairs.append(pair)
        
    """
    for i in range(len(keys)-1):
        for j in range(i+1, len(keys)):
            pair =list(keys[i])
            [ pair.append(i) for i in list(keys[j]) if i not in pair]
            #pprint(tuple(pair))

            pair.sort()
            pairs.append(pair)"""
    
    #print("End of generate pairs")
    return pairs

    """
    pairs =[]
    keys = list(c.keys())
    for i in range(len(keys)-1):
        for j in range(i+1, len(keys)):
            pair = [keys[i],keys[j]]
            pair.sort()
            pairs.append(pair)
    return pairs
    """
def generate_cn(pairs,baskets,c1=False):
    if not c1:
        pairs  = generate_pairs(pairs)
    count = {}
    for pair in pairs:
        i = getSupport(pair, baskets)
        count[tuple(pair)] = i
    return count

def subset(t, pair):
    # test is pair (set) is subset of baskets (t)
    subset = True
    for x in pair:
        if x not in t:
            subset = False
    return subset

def filter_c(ct,min_support):
    badSubSets = []
    for k in list(ct.keys()):
        if ct[k]/BASKET_TOTAL < min_support:
            badSubSets.append(k)
            del ct[k]
    return k

def prime(c,listofbadsubsets):
    for i in listofbadsubsets:
        for k in list(c.keys()):
            if subset(i,k):
                del c[k]

def getSupport(set_items,baskets):
    count = 0
    for basket in baskets:
        if subset(basket,set_items):
            count+=1
    return count

def generate_rules(current_c, baskets, min_confidence):
    print("RULES:--")
    for association_set in current_c.keys():
        association_list = list(association_set)
        set_support = getSupport(association_set,baskets)
        #pprint(f"x = {x}")
        for index in range(len(association_list)-1):
            #single item rules
            item = association_list[index]
            remainder = tuple(association_list[index+1:]) #tuple([i for i in association_list if i != item])
            
            remainder_support = getSupport(remainder,baskets) 
            item_support = getSupport((item,),baskets)
            if set_support/item_support >= min_confidence:
                print(f"    {item} => {remainder}  ({set_support}/{item_support}) {round(set_support/item_support,2)}")
                pass
            if set_support/remainder_support > min_confidence:
                print(f"    {remainder} => {item}  ({set_support}/{remainder_support}) {round(set_support/remainder_support,2)}")


if __name__ == "__main__":

    min_support = 0.6
    min_confidence = 0.6
    baskets = load_items()# T
    #pprint(baskets)
    items = get_unique_items(baskets)
    #print(items)
    c = generate_cn(items,baskets,True)
    badSupSets = []
    print("c1:")
    pprint(c)
    badSupSets.append(filter_c(c,min_support))
    print("l1:")
    pprint(c)

    iteration = 1
    while True:
        iteration += 1
        
        #lastCtable = c.copy()
        # generate next c table and l table
        
        c = generate_cn(c,baskets)
        print(f"c{iteration}:")
        pprint(c)
        badSupSets.append(filter_c(c,min_support))
        print(f"l{iteration}:")
        pprint(c)
        print()
        prime(c,badSupSets)
        generate_rules(c,baskets,min_confidence)
        
        if len(c) <= 1:
            break
        
    #pprint(badSupSets)