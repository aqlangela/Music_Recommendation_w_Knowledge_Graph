import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import sys
import pickle

dataset = sys.argv[1]

mf = pickle.load(open("../data/"+str(dataset)+"/mf_result.dat","rb"))
ripple = pickle.load(open("../data/"+str(dataset)+"/ripple_result.dat","rb"))
df = pd.concat([mf,ripple])

precison = df[df.Measure=="Precision"]
recall = df[df.Measure=="Recall"]
F1 = df[df.Measure=="F1"]

sns.set(style='darkgrid')
sns.pointplot(x="K", y="Value",hue="Method", data=precison,
palette={"Ripple": "r", "MF": "b"},
markers=["^", "o"], linestyles=["-", "--"],capsize=0.1)
plt.title("Precision@K")
plt.ylabel("Precision@K")
plt.grid(True)
plt.savefig("Precision")

sns.set(style='darkgrid')
sns.pointplot(x="K", y="Value",hue="Method", data=recall,
palette={"Ripple": "r", "MF": "b"},
markers=["^", "o"], linestyles=["-", "--"],capsize=0.1)
plt.title("Recall@K")
plt.ylabel("Recall@K")
plt.grid(True)
plt.savefig("Recall")

sns.set(style='darkgrid')
sns.pointplot(x="K", y="Value",hue="Method", data=F1,
palette={"Ripple": "r", "MF": "b"},
markers=["^", "o"], linestyles=["-", "--"],capsize=0.1)
plt.title("F1@K")
plt.ylabel("F1@K")
plt.grid(True)
plt.savefig("F1")