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

# Create initial dictionary dataset
fields = train.columns
dataset = [{field: train[field][index] for field in train.columns} for index in range(len(train["AnimalID"]))]

# Refine Dataset
for d in dataset:
    # Split SexuponOutcome col into gender (male/female )and fixed (yes/no)
    val1 = d["SexuponOutcome"].lower() if d["SexuponOutcome"] is str else 'unknown'
    if (('spayed' in val1) or ('intact' in val1) or ('neutered' in val1)) and (('male' in val1) or ('female' in val1)):
        fixed, gender = val1.split(' ')
        d['fixed'] = 'no' if fixed == 'intact' else 'yes'
        d['gender'] = gender
    else:
        d['fixed'] = 'unknown'
        d['gender'] = 'unknown'

    # Bucket age upon outcome into years, for >1yo round up at 6 months
    val2 = d['AgeuponOutcome'].lower() if d['AgeuponOutcome'] is str else ""
    if ('year' in val2) or ('month' in val2):
        age, unit = val2.split(" ")
        age = float(age)
        if 'month' in unit:
            age = 1 if age > 6.0 else 0
        d['Age'] = age
    else:
        d['Age'] = float('nan')

    # Merge OutcomeType and OutcomeSubtype into a single column
    val3, val4 = d['OutcomeType'], d['OutcomeSubtype']
    d['Outcome'] = val3 + '_' + val4 if (val3 is str and val4 is str) else val3
    