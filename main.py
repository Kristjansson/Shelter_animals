import numpy as np
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt

def importData():
    print("Data Imported")
    return pd.read_csv("""train.csv""")
def makeHistogram(data):
    """Takes a Counter and produces a histogram"""
    plt.bar(range(len(data.keys())), data.values())
    plt.xticks([x + 0.25 for x in range(len(data.keys()))], data.keys())
    plt.show()

train = importData()
data = [set(train[c]) for c in train.columns]
counts = [Counter(train[c]) for c in train.columns]

fields = train.columns
dataset = [{field: train[field][index] for field in train.columns} for index in range(len(train["AnimalID"]))]
for d in dataset:
    v = d["SexuponOutcome"].lower() if d["SexuponOutcome"] is str else 'unknown'
    if (('spayed' in v) or ('intact' in v) or ('neutered' in v)) and (('male' in v) or ('female' in v)):
        fixed, gender = v.split(' ')
        d['fixed'] = 'no' if fixed == 'intact' else 'yes'
        d['gender'] = gender
    else:
        d['fixed'] = 'unknown'
        d['gender'] = 'unknown'


