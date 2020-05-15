from cryptosysteme2 import *
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

    plt.plot(ord, generationClef, label = "generation clefs")
    plt.legend()
    plt.title("lambda : "+str(debut)+"-"+str(fin)+" ; pas : "+str(pas)+" ; repetitions : "+str(rep))
    plt.xlabel("lambda")
    plt.ylabel("temps (sec)")
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

            m1 = alice.chiffrerbit(1)
            m2 = alice.chiffrerbit(0)
            s=0
            p=0
            tt3.append(perf())

            for k in range(rep):
                c=m1+m2
            tt4.append(perf())

            """
            for l in range(rep):
                c=m1*m2
            tt5.append(perf())"""

        generationChiffre.append(sum([tt3[i]-tt2[i] for i in range(rep)])/rep)
        somme.append(sum([tt4[i]-tt3[i] for i in range(rep)])/rep)
        #produit.append(sum([tt5[i]-tt4[i] for i in range(rep)])/rep)
        print(i)

    #plt.plot(ord, generationClef, label = "generation clefs")
    #plt.legend()
    #plt.show()
    #inutile=input("")
    #print(generationChiffre)
    #print(ord)

    plt.title("lambda : "+str(debut)+"-"+str(fin)+" ; pas : "+str(pas)+" ; repetitions : "+str(rep))
    plt.plot(ord, generationChiffre, label = "generation chiffré")
    plt.xlabel("lambda")
    plt.ylabel("temps (sec)")
    plt.legend()
    plt.show()

    inutile=input("")
    plt.plot(ord, somme, label = "somme")
    plt.title("lambda : "+str(debut)+"-"+str(fin)+" ; pas : "+str(pas)+" ; repetitions : "+str(rep))
    plt.xlabel("lambda")
    plt.ylabel("temps (sec)")
    plt.legend()
    plt.show()

    """
    inutile=input("")
    plt.plot(ord, produit, label = "produit")
    plt.title("lambda : "+str(debut)+"-"+str(fin)+" ; pas : "+str(pas)+" ; repetitions : "+str(rep))
    plt.xlabel("lambda")
    plt.ylabel("temps (sec)")
    plt.legend()
    plt.show()"""

############## A partir d'ici : pas testé

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
