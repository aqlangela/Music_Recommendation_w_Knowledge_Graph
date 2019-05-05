import numpy as np
from mf_train import load_data
from mf_test import test

np.random.seed(555)

data_info = load_data()
test(data_info)
