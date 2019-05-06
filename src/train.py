import tensorflow as tf
import numpy as np
from model import RippleNet
import pickle
import pandas as pd


def train(args, data_info, show_loss,dataset):#alicia
    train_data = data_info[0]
    eval_data = data_info[1]
    test_data = data_info[2]
    n_entity = data_info[3]
    n_relation = data_info[4]
    ripple_set = data_info[5]

    model = RippleNet(args, n_entity, n_relation)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for step in range(args.n_epoch):
            # training 
            np.random.shuffle(train_data)
            start = 0
            while start < train_data.shape[0]:
                _, loss = model.train(
                    sess, get_feed_dict(args, model, train_data, ripple_set, start, start + args.batch_size))
                start += args.batch_size
                if show_loss:
                    print('%.1f%% %.4f' % (start / train_data.shape[0] * 100, loss))

            # evaluation
            train_auc, train_acc = evaluation(sess, args, model, train_data, ripple_set,args.batch_size,dataset)#alicia
            eval_auc, eval_acc = evaluation(sess, args, model, eval_data, ripple_set,args.batch_size, dataset)#alicia
            test_auc, test_acc = evaluation(sess, args, model, test_data, ripple_set,args.batch_size, dataset,True)#alicia

            print('epoch %d    train auc: %.4f  acc: %.4f    eval auc: %.4f  acc: %.4f    test auc: %.4f  acc: %.4f'
                  % (step, train_auc, train_acc, eval_auc, eval_acc, test_auc, test_acc))


def get_feed_dict(args, model, data, ripple_set, start, end):
    feed_dict = dict()
    feed_dict[model.batch_size] = min(end-start, data.shape[0]-start)
    feed_dict[model.items] = data[start:end, 1]
    feed_dict[model.labels] = data[start:end, 2]
    for i in range(args.n_hop):
        feed_dict[model.memories_h[i]] = [ripple_set[user][i][0] for user in data[start:end, 0]]
        feed_dict[model.memories_r[i]] = [ripple_set[user][i][1] for user in data[start:end, 0]]
        feed_dict[model.memories_t[i]] = [ripple_set[user][i][2] for user in data[start:end, 0]]
    return feed_dict


def evaluation(sess, args, model, data, ripple_set, batch_size,dataset,test=False):#alicia
    start = 0
    auc_list = []
    acc_list = []
    precision_list = [0 for i in range (1,11)]
    recall_list = [0 for i in range (1,11)]
    F1_list = [0 for i in range (1,11)]
    while start < data.shape[0]:
        auc, acc, precision, recall, F1 = model.eval(sess, get_feed_dict(args, model, data, ripple_set, start, start + batch_size))
        auc_list.append(auc)
        acc_list.append(acc)
        precision_list = [sum(x) for x in zip(precision, precision_list)]
        recall_list = [sum(x) for x in zip(recall, recall_list)]
        F1_list = [sum(x) for x in zip(F1, F1_list)]
        start += batch_size
    if test:#alicia
        K = [1,2,5,10,15,20,40,60,80,100]
        df = pd.DataFrame(columns=['K',"Method","Measure","Value"])
        for i in range(len(precision_list)):
            df = df.append({'K':K[i],"Method":"Ripple","Measure":"Precision","Value":precision_list[i]}, ignore_index=True)
            df = df.append({'K':K[i],"Method":"Ripple","Measure":"Recall","Value":recall_list[i]}, ignore_index=True)
            df = df.append({'K':K[i],"Method":"Ripple","Measure":"F1","Value":F1_list[i]}, ignore_index=True)
        ripple_file = open("../data/"+str(dataset)+"/ripple_result.dat","wb")
        pickle.dump(df,ripple_file)
                
    print("precision: ", precision_list)
    print("recall: ", recall_list)
    print("F1", F1_list)
    return float(np.mean(auc_list)), float(np.mean(acc_list))
