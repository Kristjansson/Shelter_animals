import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from sklearn import tree

def makeHistogram(data):
    """Takes a Counter and produces a histogram"""
    plt.bar(range(len(data.keys())), data.values())
    plt.xticks([x + 0.25 for x in range(len(data.keys()))], data.keys())
    plt.show()

def chiSquare(dataset, field1, field2):
    """Takes the two columns we wish to compare"""
    categories = {f: set([d[f] for d in dataset]) for f in (field1, field2)}
    countTable = {(c1, c2): len([d for d in dataset if d[field1] == c1 and d[field2] == c2])
                  for c1 in categories[field1]
                  for c2 in categories[field2]}
    print 'part1'
    totals = {c: sum([countTable[(c, other_c)] for other_c in categories[field2]]) for c in categories[field1]}
    totals.update({c: sum([countTable[(other_c, c)] for other_c in categories[field1]]) for c in categories[field2]})
    overall_total = len(dataset)
    expectedValsTable = {(c1, c2): totals[c1]*totals[c2]*(1.0/overall_total)
                  for c1 in categories[field1]
                  for c2 in categories[field2]}
    statTable = {(c1, c2): (countTable[(c1, c2)] - expectedValsTable[(c1, c2)])**2 * 1.0/expectedValsTable[(c1, c2)]
                  for c1 in categories[field1]
                  for c2 in categories[field2]}
    return countTable, statTable

def init():
    """Returns the clean dataset"""
    data = pd.read_csv("""trainFixed_PRUNED.csv""")
    return [{field: data[field][index] for field in data.columns} for index in range(len(data["AnimalID"]))]

def train():
    dataset = init()
    train_a = dataset[0:int(.75*len(dataset))]
    train_b = dataset[int(.75*len(dataset)):]

    X = [[d[f] for f in d.keys() if f != 'Outcome'] for d in train_a]
    Y = [[d[f] for f in d.keys() if f != 'Outcome'] for d in train_a]

    clf = tree.DecisionTreeClassifier(max_depth=3)
    clf.fit(X, Y)
