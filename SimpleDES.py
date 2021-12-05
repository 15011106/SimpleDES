
# SimpleDes Created by 15011106

import random
import copy

sbox1 = [[[1,0,1],[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,0],[1,1,1],[0,0,0]],
         [[0,0,1],[1,0,0],[1,1,0],[0,1,0],[0,0,0],[1,1,1],[1,0,1],[0,1,1]]]

sbox2 = [[[1,0,0],[0,0,0],[1,1,0],[1,0,1],[1,1,1],[0,0,1],[0,1,1],[0,1,0]],
         [[1,0,1],[0,1,1],[0,0,0],[1,1,1],[1,1,0],[0,1,0],[0,0,1],[1,0,0]]]

def sdes_genkey() :
    key = []
    for i in range(9):
        a = random.randint(0,1)
        key.append(a)
    return key

def sdes_compute_function(roundkey,rblock) :
    expen =rblock[0:1] + rblock[1:2] + rblock[3:4] + rblock[2:3] +  rblock[3:4] + rblock[2:3] + rblock [4:5] + rblock[5:6]
    xor = []
    S1 = []
    S2 = []    
    for i in range(8):
        xor.append(expen[i]^roundkey[i])

    L = xor[0:4]
    R = xor[4:8]
    num1 = (L[3] * 1) + (L[2] * 2) + (L[1] * 4)
    num2 = (R[3] * 1) + (R[2] * 2) + (R[1] * 4)
   
    if L[0] == 0 :
        S1 = sbox1[0][num1]
        if R[0] == 0 :
            S2 = sbox2[0][num2]
        else :
            S2 = sbox2[1][num2]
    else :
        S1 = sbox1[1][num1]
        if R[0] == 0:
            S2 = sbox2[0][num2]
        else :
            S2 = sbox2[1][num2]
    return S1+S2

def sdes_encrypt(key,pblock) :
    lblock = pblock[0:6]
    rblock = pblock[6:12]
    for i in range(3) :
        if i < 2:
            rkey = key[i:8+i]
        if i >= 2:
            rkey = rkey[1:8]
            rkey.append(key[(i-2)%9])
        result = sdes_compute_function(rkey,rblock)
        
        temp = copy.deepcopy(rblock)
        rblock = []
        for i in range(6):
            rblock.append(result[i]^lblock[i])
        lblock = copy.deepcopy(temp)

    return lblock + rblock

def sdes_decrypt(key,cblock):
    lblock = cblock[0:6]
    rblock = cblock[6:12]
    for i in range(2,-1,-1) :
        if (i+8)%9>=7:
            rkey = key[i%9:(i+8)%9]
        else:
            rkey = key[i%9:9]+key[0:(i+8)%9]
        if i==8:
            rkey = key[8:9]+key[0:7]
        result = sdes_compute_function(rkey,lblock)

        temp = copy.deepcopy(lblock)
        lblock = []
        for i in range(6):
            lblock.append(result[i]^rblock[i])
        rblock = copy.deepcopy(temp)

    return lblock + rblock
