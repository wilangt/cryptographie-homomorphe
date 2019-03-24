from cryptosysteme import *
import matplotlib.pyplot as plt

def tempsclefs(debut, fin, pas=1, rep=1):
    ord = list(range(debut,fin + 1, pas))
    generationClef = []

    for i in ord:
        t1=perf()
        for j in range(rep):
            alice = Prive(i)
            bob = Publique(alice.publier())
        t2 = perf()

        generationClef.append(t2-t1)

        print(i)

    plt.plot(ord, generationClef, label = "generation clefs ; "+str(debut)+"-"+str(fin)+" pas : "+str(pas)+" repetition : "+str(rep))
    plt.legend()
    plt.show()

def tempscalculs(debut, fin, pas=1, rep=1):
    ord = list(range(debut,fin + 1, pas))
    generationClef = []
    generationChiffre = []
    somme = []
    produit = []

    for i in ord:
        alice = Prive(i)
        bob = Publique(alice.publier())
        tt1=[]
        tt2=[]
        tt3=[]
        tt4=[]
        tt5=[]
        for j in range(rep):
            tt2.append(perf())

            m1 = alice.chiffrer(1)
            m2 = alice.chiffrer(0)
            s=0
            p=0
            tt3.append(perf())

            for j in range(rep):
                c=bob.somme(m1,m2)
            tt4.append(perf())

            for j in range(rep):
                c=bob.somme(m1,m2)
            tt5.append(perf())

        generationChiffre.append(sum([tt3[i]-tt2[i] for i in range(rep)])/rep)
        somme.append(sum([tt4[i]-tt3[i] for i in range(rep)])/rep)
        produit.append(sum([tt5[i]-tt4[i] for i in range(rep)])/rep)
        print(i)

    #plt.plot(ord, generationClef, label = "generation clefs")
    #plt.legend()
    #plt.show()
    #inutile=input("")
    #print(generationChiffre)
    #print(ord)
    plt.plot(ord, generationChiffre, label = "generation chiffré ; "+str(debut)+"-"+str(fin)+" pas : "+str(pas)+" repetition : "+str(rep))
    plt.legend()
    plt.show()
    inutile=input("")
    plt.plot(ord, somme, label = "somme ; "+str(debut)+"-"+str(fin)+" pas : "+str(pas)+" repetition : "+str(rep))
    plt.legend()
    plt.show()
    inutile=input("")
    plt.plot(ord, produit, label = "produit ; "+str(debut)+"-"+str(fin)+" pas : "+str(pas)+" repetition : "+str(rep))
    plt.legend()
    plt.show()

def testclefs(l,rep):
    ord = list(range(rep))
    generationClef = []

    for i in ord:
        t1=perf()
        alice = Prive(l)
        bob = Publique(alice.publier())
        t2 = perf()

        generationClef.append(t2-t1)

        print(i)

    plt.plot(ord, generationClef, label = "generation clefs ; lambdaa : "+str(l)+" ; repetition : "+str(rep))
    plt.legend()
    plt.show()

def testaddition(bob,alice,n):
    m=[]
    for i in range(n):
        m.append(alice.chiffrer(random.randint(0,1)))
    a=0
    for i in m:
        a+=bob.somme(m1,m2)
    return (m1+m2)%2==a

def testmultiplication(bob,alice):
    m1 = alice.chiffrer(random.randint(0,1))
    m2 = alice.chiffrer(random.randint(0,1))
    a=alice.dechiffrer(bob.produit(m1,m2))
    return m1*m2==a

def creerCS (l):
    milan = Prive(l)
    clement = Publique(milan.publier())
    return milan, clement

def testCSbit(l,r):
    milan, clement = creerCS(l)
    s = random.randint(0,1)
    sc = clement.chiffrerbit(s)
    print("somme")
    for i in range(r):
        t = random.randint(0,1)
        s = (s+t)%2
        sc += clement.chiffrerbit(t)
        print(i+1, " ", milan.dechiffrerbit(sc)==s)

    p = random.randint(0,1)
    pc = clement.chiffrerbit(p)
    print("produit")
    for i in range(r):
        t = random.randint(0,1)
        p = (s*t)%2
        pc *= clement.chiffrerbit(t)
        print(i+1, " ", milan.dechiffrerbit(pc)==p)

def testCSent(l,r,e,début,fin,pas):
    milan, clement = creerCS(l)
    ord = list(range(debut,fin + 1, pas))
    tab=[]
    for i in ord:
        m=[]
        for j in range(r): #r représente le nombre d'essai pour lambda = i
            p = random.randint(1,e)
            pc = clement.chiffrerentier(p)
            for k in range(r):
                t = random.randint(1,e)
                p *= t
                pc *= clement.chiffrerentier(t)
            m.append(p==pc)
            #f1 = random.randint(1,e)
            #f2 = random.randint(1,e)
            #m.append(f1*f2==milan.dechiffrerentier(clement.chiffrerentier(f1)*clement.chiffrerentier(f2)))
        tab.append(100*sum(m)/r)
    for i in range(len(tab)):
        print (i+debut, " ",tab[i])

def testCSent(lambdaa,r,e):
    m=0
    for i in range(1,r+1):
        print("essai numero ",i)
        milan, clement = creerCS(lambdaa)

        p = random.randint(1,e)
        pc = clement.chiffrerentier(p)

        produit_correct = (p==milan.dechiffrerentier(pc))

        j=0
        print(j,produit_correct)

        while produit_correct:
            t = random.randint(1,e)
            p *= t
            pc *= clement.chiffrerentier(t)
            j+=1
            produit_correct = (p==milan.dechiffrerentier(pc))
            print(j,produit_correct)
            if j>100 : break
        print("")
        m+=(j-1)
    print(m/r)

def testCSbit(lambdaa,r,e):
    m=0
    for i in range(1,r+1):
        print("essai numero ",i)
        milan, clement = creerCS(lambdaa)

        p = random.randint(0,1)
        pc = clement.chiffrerbit(p)

        produit_correct = (p==milan.dechiffrerbit(pc))

        j=0
        print(j,produit_correct)

        while produit_correct:
            t = random.randint(0,1)
            p *= t
            pc *= clement.chiffrerbit(t)
            j+=1
            produit_correct = (p==milan.dechiffrerbit(pc))
            print(j,produit_correct)
            if j>1000 : break
        print("")
        m+=(j-1)
    print(m/r)

"""
    ord = list(range(debut,fin + 1, pas))
    tab=[]
    for i in ord:
        m=[]
        for j in range(r): #r représente le nombre d'essai pour lambda = i
            p = random.randint(1,e)
            pc = clement.chiffrerentier(p)
            for k in range(r):
                t = random.randint(1,e)
                p *= t
                pc *= clement.chiffrerentier(t)
            m.append(p==pc)
            #f1 = random.randint(1,e)
            #f2 = random.randint(1,e)
            #m.append(f1*f2==milan.dechiffrerentier(clement.chiffrerentier(f1)*clement.chiffrerentier(f2)))
        tab.append(100*sum(m)/r)
    for i in range(len(tab)):
        print (i+debut, " ",tab[i])
"""
