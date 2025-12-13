import os
def sigmoid(sim):
    P = 1/(1+2.7182818284590452353602874713527**(-sim))
    return P
def log(neg,x):
    coun = 0
    while x >= 2:
        x/=2
        coun+=1
    m = x-1
    x = m-(m**2/2)+(m**3/3)-(m**4/4)+(m**5/5)-(m**6/6)+(m**7/7)-(m**8/8)
    x/=2.303585
    sec = coun*0.30103
    x+=sec
    if neg:
        x*=-1
    return x
def uni():
    xn = os.urandom(8)
    xn = int.from_bytes(xn, "big")
    a231 = pow(2,31)
    xn1 = (1103515245*xn + 12345) % a231
    R = xn1/a231
    xn2 = round(R-int(R),2)
    if xn2*100 % 2 == 1:
        xn2*=-1
    return xn2
def similarity(ass,vectors):
    tosum = []
    fina = []
    finb = []
    ID = 0
    similarityr = {}
    for l in ass:
        tosum = []
        fina = []
        finb = []
        liss = ass[l] # the list pulled out of ass
        #print(vectors[liss[0]][0]) # getting the first number of the vector list of the first word in liss (Only this works properly now)
        for pop in range(3):
            tosum.append(vectors[liss[0]][pop] * vectors[liss[1]][pop]) 
        dp = sum(tosum)
        for popi in range(3):
            fina.append(vectors[liss[0]][popi] ** 2) 
        for popo in range(3):
            finb.append(vectors[liss[1]][popo] ** 2) 
        A = sum(fina) ** 0.5
        B = sum(finb) ** 0.5
        similarity = dp/(A*B)
        similarityr[ID] = similarity
        ID+=1
    return similarityr