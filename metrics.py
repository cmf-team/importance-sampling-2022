import numpy as np
from scipy import stats

def pof_test(var, target, alpha=0.99):
    size=len(var)  
    tg=np.sum(target<var)
    fin=-2*np.log(((alpha**(size-tg))*((1-alpha)**tg))/(((1-tg/size)**(size-tg))*(tg/size)**tg))
    return 1-stats.chi2.cdf(fin,1)

def if_test(var, target):
    counter=np.zeros(4)
    Dummy_=[]
    for i in range(len(var)):
        Dummy_.append(int(target[i]<var[i]))
    #print(Dummy_)
    for i in range(1,len(Dummy_)):
        if Dummy_[i]==0 and Dummy_[i-1]==0:
            counter[0] += 1
        if Dummy_[i]==0 and Dummy_[i-1]==1:
            counter[1] += 1
        if Dummy_[i]==1 and Dummy_[i-1]==0:
            counter[2] += 1
        if Dummy_[i]==1 and Dummy_[i-1]==1:
            counter[3] += 1
    x=counter[1]/(counter[0]+counter[1])
    y=counter[3]/(counter[2]+counter[3])
    total=(counter[1]+counter[3])/(np.sum(counter))
    fin=-2*np.log(((1-total)**(counter[0]+counter[2])*total**(counter[1]+counter[3]))/((1-x)**(counter[0])*x**(counter[1])*(1-y)**counter[2]*y**counter[3]))
    return 1-stats.chi2.cdf(fin, 1)

def quantile_loss(var, target, alpha=0.99):
    loss=np.zeros(len(var))
    for i in range(len(var)):
        if (target[i]<var[i]):
            loss[i]=2*alpha*(var[i]-target[i])
        else:
            loss[i]=2*(1-alpha)*(target[i]-var[i])
    return loss.mean()