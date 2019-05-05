import numpy as np
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

def test(data_info):
    print('')
    train_data = data_info[0]
    eval_data = data_info[1]
    test_data = data_info[2]
    R = data_info[3]

    batch_size = 1024
    train_auc, train_acc = evaluation(train_data, R, batch_size)
    eval_auc, eval_acc = evaluation(eval_data, R, batch_size)
    test_auc, test_acc = evaluation(test_data, R, batch_size)

    print('train auc: %.4f  acc: %.4f    eval auc: %.4f  acc: %.4f    test auc: %.4f  acc: %.4f'
        % (train_auc, train_acc, eval_auc, eval_acc, test_auc, test_acc))
    
def evaluation(data, R, batch_size):
    start = 0
    auc_list = []
    acc_list = []
    precision_list = [0 for i in range (1,11)]
    recall_list = [0 for i in range (1,11)]
    F1_list = [0 for i in range (1,11)]
    while start < data.shape[0]:
        feed_size = min(batch_size, data.shape[0]-start)
        end  = start + feed_size
        users = data[start:end, 0]
        items = data[start:end, 1]
        labels = data[start:end, 2]
        auc, acc, precision, recall, F1 = eval(data, R, feed_size, users, items, labels)
        auc_list.append(auc)
        acc_list.append(acc)
        precision_list = [sum(x) for x in zip(precision, precision_list)]
        recall_list = [sum(x) for x in zip(recall, recall_list)]
        F1_list = [sum(x) for x in zip(F1, F1_list)]
        start += batch_size
    print("precision: ", precision_list)
    print("recall: ", recall_list)
    print("F1", F1_list)
    return float(np.mean(auc_list)), float(np.mean(acc_list))

def eval(data, R, feed_size, users, items, labels):
    scores = R[users, items]
    # normalize scores

    auc = roc_auc_score(labels, scores)

    precision_K = []
    recall_K = []
    F1_K = []
        
    K = [i for i in range(1,11)]
    for k in K:
        precision = 0
        recall = 0
        all_for_user = scores
        labels_for_user = np.array(labels)
        sorted_K = sorted(range(len(all_for_user)), key=lambda k: all_for_user[k])[::-1][0:k]
        labels_K = list(labels_for_user[sorted_K])
        relevant_K = len(list(filter(lambda x: x==1, labels_K)))
        precision = relevant_K / (feed_size*k)
        try:
            recall += relevant_K/(len(list(filter(lambda x: x==1, labels_for_user)))*feed_size)
        except:
            pass
        F1 = 2*precision*recall/(precision+recall)
        precision_K.append(precision)
        recall_K.append(recall)
        F1_K.append(F1)

    predictions = [1 if i >= 0.1 else 0 for i in scores]
    acc = np.mean(np.equal(predictions, labels))
    return auc, acc, precision_K, recall_K, F1_K

#     ax1 = plt.gca()
#     ax1.set_xlabel('K')
#     ax1.set_ylabel('precision@K')
#     ax1.set_ylim([0.05,0.30])
#     ax1.plot(x, precision_K, color='r', linewidth=1, alpha=0.6)