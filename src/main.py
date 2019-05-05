import argparse
import numpy as np
from data_loader import load_data
from train import train

np.random.seed(555)

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='01', help='which dataset to use')
# test auc: 0.7431  acc: 0.6782
parser.add_argument('--dim', type=int, default=4, help='dimension of entity and relation embeddings')
parser.add_argument('--n_hop', type=int, default=2, help='maximum hops')
parser.add_argument('--kge_weight', type=float, default=0.01, help='weight of the KGE term')
parser.add_argument('--l2_weight', type=float, default=1e-6, help='weight of the l2 regularization term')
parser.add_argument('--lr', type=float, default=0.005, help='learning rate')
parser.add_argument('--batch_size', type=int, default=1024, help='batch size')
parser.add_argument('--n_epoch', type=int, default=5, help='the number of epochs')
parser.add_argument('--n_memory', type=int, default=32, help='size of ripple set for each hop')
parser.add_argument('--item_update_mode', type=str, default='plus_transform',
                    help='how to update item at the end of each hop')
parser.add_argument('--using_all_hops', type=bool, default=True,
                    help='whether using outputs of all hops or just the last hop when making prediction')

'''
precision:  [0.0805716565860215, 0.0815482190860215, 0.08187373991935483, 0.0817923597110215, 0.08174353158602149,
0.08187373991935484, 0.08182723694316435, 0.0819144300235215, 0.08198224686379926, 0.0821341565860215]
recall:  [0.00019983724888857229, 0.0004036594815671481, 0.0006075307639703726, 0.0008094081495188851, 0.0010111907042330871,
0.0012149104899376092, 0.001416875459070332, 0.0016206150528626899, 0.0018244117586904036, 0.0020301083915609175]
F1 [nan, 0.0008009354124786336, 0.0012007702766816692, 0.001593589070631008, 0.001983237278448212,
0.002373789038793866, 0.0027579899908077503, 0.003142871428808227, 0.003525084831306348, 0.0039082970850526574]
'''

args = parser.parse_args()

show_loss = False
data_info = load_data(args)
train(args, data_info, show_loss)
