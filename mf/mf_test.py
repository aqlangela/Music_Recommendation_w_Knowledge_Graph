import numpy as np
import matplotlib.pyplot as plt

def main():
    R = np.load("../data/mf_prediction_matrix.npy")
    test = np.load("../data/mf_test_data.npy")

    x = [i for i in range(1,11)]
    precision_K = []
    recall_K = []
    F1_K = []
    for i in x: # K
        cnt = 0
        precision = 0
        recall = 0
        for u in test:
            user_retrieve_K = []
            temp_s = 0
            temp_recall = 0
            for s in u:
                if int(s[2]) == 1:
                    temp_recall += 1 
                idx = int(s[1])
                song = R[cnt][idx]
                user_retrieve_K.append(song)
            sorted_K = sorted(range(len(user_retrieve_K)), key=lambda k: user_retrieve_K[k])
            sorted_K = sorted_K[::-1][0:i]
            for j in range(i): 
                if int(u[sorted_K[j]][2]) == 1:
                    temp_s += 1
            cnt += 1
            precision += temp_s
            try:
                recall += temp_s/temp_recall
            except:
                pass

        precision /= R.shape[0]*i
        recall /= R.shape[0]
        F1 = 2*precision*recall/(precision+recall)
        precision_K.append(precision)
        recall_K.append(recall)
        F1_K.append(F1)

    print(precision_K)
    print(recall_K)
    print(F1_K)
    ax1 = plt.gca()
    ax1.set_xlabel('K')
    ax1.set_ylabel('precision@K')
    ax1.set_ylim([0.05,0.30])
    ax1.plot(x, precision_K, color='r', linewidth=1, alpha=0.6)

    # ax2 = plt.gca()
    # ax2.set_xlabel('K')
    # ax2.set_ylabel('recall@K')
    # ax2.plot(x, recall_K, color='r', linewidth=1, alpha=0.6)

    # ax3 = plt.gca()
    # ax3.set_xlabel('K')
    # ax3.set_ylabel('F1@K')
    # ax3.plot(x, F1_K, color='r', linewidth=1, alpha=0.6)

    plt.show()
    # print(model.reconstruction_err_) # 3309.7863205831313

main()