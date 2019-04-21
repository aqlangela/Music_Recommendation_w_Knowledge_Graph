import numpy as np
import matplotlib.pyplot as plt

def main():
    R = np.load("mf_prediction_matrix.npy")
    test = np.load("mf_test_data.npy")

    x = [i for i in range(10)]
    hit_K = []
    for i in x: # K
        cnt = 0
        sums = 0
        for u in test:
            user_retrieve_K = []
            temp_s = 0
            for s in u:
                idx = s[1]
                song = R[cnt][int(idx)]
                user_retrieve_K.append(song)
            sorted_K = sorted(range(len(user_retrieve_K)), key=lambda k: user_retrieve_K[k])
            sorted_K = sorted_K[::-1][0:i+1]
            for j in range(i+1): 
                if int(u[sorted_K[j]][2]) == 1:
                    temp_s += 1
            sums += (temp_s/(i+1))
            cnt += 1
        sums /= R.shape[0]
        print(sums)
        hit_K.append(sums)

    print(hit_K)
    ax = plt.gca()
    ax.set_xlabel('K')
    ax.set_ylabel('hit@K')
    ax.set_ylim([0.05,0.30])
    ax.plot(x, hit_K, color='r', linewidth=1, alpha=0.6)
    plt.show()
    # print(model.reconstruction_err_) # 3309.7863205831313

main()