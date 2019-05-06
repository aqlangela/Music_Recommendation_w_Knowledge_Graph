import numpy as np
from mf_train import load_data
from mf_test import test
import sys#alicia

np.random.seed(555)

dataset = sys.argv[1]#alicia
data_info = load_data(dataset)#alicia
test(data_info,dataset)#alicia
