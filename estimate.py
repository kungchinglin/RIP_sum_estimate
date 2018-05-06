import random
import numpy as np
import matplotlib.pyplot as plt
import cmath
import math
import pylab
import os
script_dir = os.path.dirname(__file__)
rel_path = "../images/"
abs_file_path = os.path.join(script_dir, rel_path)


def calculateLegendre(a, p):
    if isPrime(p):
        A= a % p
        B=1
        Range=int((p-1)/2)
        for i in range(Range):
            B*=A
            B=B%p
        #print(B)
    
        if B == (p-1):
            B=B-p
        #    print(B)
        return B
    else:
        print(p,'is not a prime')



def isPrime(a):
    return all(a % i for i in range(2, a))



def calculateRIPestimate(SetM, p, Array):
    est=0
    L=len(SetM)
    
    #Set up the shifted array
    Array2=np.zeros(p)
    for i in range(L):
        Array2+=np.roll(Array,-SetM[i])
        #for k in range(p):
            #s=(k+SetM[i])%p
            #Array2[k]+=Array[s]

    Array3=np.multiply(Array,Array2)
    Array4=np.fft.fft(Array3)
    est=np.amax(Array4)
    #for n in range(p):
        #hold=0
        #for k in range(p):
        #    temp_sum=0
        #    K1=Array[k]
        #    K2=Array2[k]
        #    temp_sum+=K1*K2*cmath.exp(2j*cmath.pi*k*n/p)
        #hold=abs(temp_sum)
        #if hold>est:
            #est=hold
    return abs(est)



#Make a list of Legendre symbols instead of computing them again and again
def makeLegendre(p):
    if isPrime(p):
        Array=np.zeros(p)
        half=int((p-1)/2)
        for i in range(p):
            Array[i]=(i**half)%p
            if Array[i]== (p-1):
                Array[i]-=p
        return Array
    else:
        print(p,'is not a prime')



def main(p,n):
    #p=397
    proot=math.floor(math.sqrt(p))
    pSet=range(1,p)                 #We won't have any case when m1=m2. Thus, M don't have to have 0 in it.
    est_value=[]
    Array=makeLegendre(p)
    
    for i in range(proot):
        value=0
        for j in range(n):
            setM=random.sample(pSet,i+1)
            hold=calculateRIPestimate(setM,p,Array)
            if hold>value:
                value=hold                               #Find the largest one

            #print(j)
        est_value+=[value]
        #print(est_value)
        print('i=',i)
    return est_value
    
def saving(est_value,p,n):
    first_sent="p="+str(p)
    second_sent="Sum estimate with respect to size M:"+ str(est_value)
    nor_est=np.multiply(est_value,1/math.sqrt(p))
    third_sent="Normalized sum estimate by square root of p:"+ str(nor_est)
    
    drname="n="+str(n)+"/"
    results_dir=os.path.join(script_dir, drname)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    
    file=open(results_dir+"data.txt", "a+")
    file.write("\n\n"+first_sent)
    file.write("\n"+second_sent)
    file.write("\n"+third_sent)
    file.close()
    
def plotting(est_value,p,n):
    L=len(est_value)
    power_line1=np.zeros(L)
    power_line2=np.zeros(L)
    power_line3=np.zeros(L)
    power_line4=np.zeros(L)
    for i in range(L):
        power_line1[i]=2*math.sqrt(i+1)
        power_line2[i]=2*float(i+1)
        power_line3[i]=2*(i+1)**0.7
        power_line4[i]=2*(i+1)**0.8
    nor_est=np.multiply(est_value,1/math.sqrt(p))
    #plt.loglog(range(1,L+1),est_value)
    nor_plot,=plt.loglog(range(1,L+1),nor_est,marker='.', label='Normalized value')
    plot_1,=plt.loglog(range(1,L+1),power_line1,marker='o',label='square-root line')
    plot_2,=plt.loglog(range(1,L+1),power_line2,marker=',',label='linear line')
    plot_3,=plt.loglog(range(1,L+1),power_line3,marker='h',label='Exponent=0.7')
    plot_4,=plt.loglog(range(1,L+1),power_line4,marker='v',label='Exponent=0.8')
    plt.legend(handles=[nor_plot,plot_1,plot_2,plot_3,plot_4])
    plt.title("p="+str(p)+", n="+str(n))
    #plt.set_yscale('log')

    drname="n="+str(n)+"/images/"
    filename="p="+str(p)+"_n="+str(n)+"_plot_max.png"
    results_dir=os.path.join(script_dir, drname)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.savefig(drname+filename)
    return 0

def execute():
    p=613
    n=1000
    #Estimation=[35.2485130323809, 64.85942191628388, 81.94752544618797, 103.21852804999484, 113.1793485982225, 123.18968297392804, 144.5526886093207, 145.28530400029322, 151.48474242658304, 182.4727839144673, 177.29809290065936, 175.80465495795875, 182.97830932614946, 200.9103795479744, 188.63953010211264, 201.95482091429741, 201.1866597563131]

    Estimation=main(p,n)
    saving(Estimation,p,n)
    plotting(Estimation,p,n)
execute()

#print(makeLegendre(97))
