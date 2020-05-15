#amelioration du 27/02/19
from math import *
import random
from fraction import *
from time import perf_counter as perf

def genererCS(l,m):
    """
    fonction qui genere un cryptosysteme
    parametres :
    1/ lambda le parametre de securite
    2/ m le nombre de produit bit a bit souhaite
    renvoie alice, bob
    """
    clef_invalide=True
    while clef_invalide:
        #print("essai numero ",i)
        milan = Prive(l)
        clement = Publique(milan.publier())

        p = random.randint(0,1)
        pc = clement.chiffrerbit(p)
        produit_correct = (p==milan.dechiffrerbit(pc))
        j=0
        #print(j,produit_correct)

        while produit_correct:
            t = random.randint(0,1)
            p *= t
            pc *= clement.chiffrerbit(t)
            j+=1
            produit_correct = (p==milan.dechiffrerbit(pc))
            if not produit_correct : print(j)
            if j>m :
                return milan, clement
                print("clefs OK")
    print("clefs non OK")
    return milan, clement

class Prive:
    """docstring for prive."""
    def __init__(self, lambdaa):
        self.lambdaa = lambdaa
        self.genererParametres()

        self.genererClefs()

    def genererParametres(self):
        self.rho = self.lambdaa
        self.L = 20
        self.eta = int(self.rho + self.L*log2(self.lambdaa))
        self.gamma = int(self.eta*1.05)
        #self.gamma = int(self.lambdaa*self.L**2*log2(self.lambdaa))//30
        self.tau = self.gamma + 2*self.lambdaa + 2
    def _donner_parametres(self):
        print("rho={}, eta={}, gamma={}, tau={}".format(self.rho,
            self.eta, self.gamma, self.tau))

    @staticmethod
    def D2(t):
        return random.getrandbits(t+1)-(1<<t)  # MODIF: signe aletatoire

    @staticmethod
    def AAGCD(X,phi,p):
        q = random.randrange(-abs(X//p), abs(X//p))
        r = phi # TEST <----------------------------------------------------
        return p*q+r

    @staticmethod
    def modTens(u, d): # reste de chaque element list * int -> list
        return [x % d for x in u]

    @staticmethod
    def som(u,v): # somme vectorielle list*list -> list
        assert len(u)==len(v)
        return [u[i]+v[i] for i in range(len(u))]

    @staticmethod
    def tensScaProd(u, x): # produit d'un vecteur par un scalaire list*int -> list
        return [x*e for e in u]

    @staticmethod
    def P(n, y):
        r = [y]
        for i in range(n-1):
            r.append(2*r[-1])
        return r

    @staticmethod
    def prod(u,v): # produit tensoriel list*list -> list
        prod = []
        for x in u:
            for y in v:
                prod.append(x*y)
        return prod

    def genererClefs(self):
        sigma, X= 2**(self.gamma-self.eta), 2**(self.gamma)
        alphe =  2**(self.rho) # - int(log2(self.lambdaa)/2)) # TEST <-------------
        logalpha = self.rho # - int(log2(self.lambdaa)/2)  #TEST

        # clef privee
        p = random.randrange(1, 1<<self.eta)

        # clef publique
        x = [0 for i in range(self.tau)]

        x = [self.AAGCD(X,self.D2(logalpha),p) for i in range(self.tau+1)]

        im = 0
        m = x[0]
        for i, e in enumerate(x):
            if e>m:
                im = i
                m = e
        x[0], x[im] = x[im], x[0]
        i = 1
        while i<=self.tau and round(Fraction(x[i],p))%2==0:
            i += 1

        if not i==self.tau+1:
            x[1], x[i] = x[i], x[1]

        while x[1]>=x[0] or round(Fraction(x[1],p))%2==0:
            x[i] = self.AAGCD(X, self.D2(logalpha), p)

        self.sk = p
        self.pk = x

        # clef de multiplication :
        a = [self.AAGCD(X, self.D2(logalpha), p) for i in range(self.gamma)
                                            for j in range(self.gamma)]
        b = self.modTens(self.P(self.gamma, Fraction(2,p)), 2)
        c = self.tensScaProd(self.prod(b, b), Fraction(p,2))
        self.mk = self.som(a, c)

        # clef de bootstrap
        # on calcul une approxymation de z=2/p a gamma+eta
        # bits pres puis on renvoie son chiffre
        # les eta bits les plus significatifs sont nuls,
        #on ne chiffre donc que les gamma autres bits

        z = []
        #a = 2**(self.eta+1)/p
        a = 2**(self.eta)/p

        self.bk = 0 # temporairement
        # peut poser probleme: les bits de self.bk ne peuvent etre bootstrapes

        for i in range(self.gamma):
            z.append(self.chiffrerbit(int(a%2)))
            a = (2*a)%2

        self.bk = Entierchiffre(z[::-1])


    def publier(self):
        """renvoie les parametres publics"""
        return self.pk, self.mk, self.bk, self.lambdaa, self.rho,\
                self.eta, self.gamma, self.tau

    def dechiffrerbit(self, c):
        return (round(2*c.c/self.sk))%2

    """
    def dechiffrerfloat(self, cx):
        bits = tuple([self.dechiffrerbit(b) for b in cx.bits])
        return floatextras.from_tuple((cx.sign, bits, cx.exponent))
    """

    def dechiffrerentier(self, cn):
        bits = [self.dechiffrerbit(c) for c in cn.bits]
        s = 0
        for b in bits[::-1]:
            s = 2*s + b
        return s

    def chiffrerbit(self, m):
        c = m * round(Fraction(self.pk[1], 2))
        for i in range(1, self.tau+1):
            if random.getrandbits(1):
                c  += self.pk[i] % self.pk[0]
        return Bitchiffre(Publique(self.publier()), c % self.pk[0])


class Publique:
    def __init__(self, publication):
        self.pk, self.mk, self.bk, self.lambdaa, self.rho, self.eta,\
                self.gamma, self.tau = publication

    @staticmethod
    def prod_sca_bool(u, v): # cas ou u est une liste de 0 ou 1
        assert len(u)==len(v)
        s = 0
        for i in range(len(u)):
            if u[i]:
                s += v[i]
        return s

    @staticmethod
    def prod_bool(u,v): # cas ou u est bool
        prod = []
        lv = len(v)
        for x in u:
            if x:
                prod.extend(v)
            else:
                prod.extend([0] * lv)
        return prod

    def BD(self, n, x):
        if n==0:
            return []
        return [x%2]+self.BD(n-1, x//2)

    def chiffrerbit(self, m):
        c = m * round(Fraction(self.pk[1], 2))
        for i in range(1, self.tau+1):
            if random.getrandbits(1):
                c  += self.pk[i] % self.pk[0]
        return Bitchiffre(self, c % self.pk[0])
    """
    @staticmethod
    def float_to_list(x):
        d = floatextras.as_tuple(x)
        return d.sign, d.digits, d.exponent
    """
    def chiffrerentier(self, x):
        bits = [self.chiffrerbit(int(c)) for c in bin(x)[2:][::-1]]
        return Entierchiffre(bits)

    def sommebit(self, c1, c2):  # c1 et c2 entiers, chiffrants deux bits
        return c1+c2 % self.pk[0]

    def produitbit(self, c1, c2):
        return round((self.prod_sca_bool(self.prod_bool(self.BD(self.gamma, c1),
                                  self.BD(self.gamma, c2)),self.mk)) % self.pk[0])

class Bitchiffre:
    def __init__(self, publique, c): # c est le chiffre
        self.publique = publique
        self.c = c

    def __add__(self, c2):
        #assert self.publique == c2.publique
        return Bitchiffre(self.publique, self.publique.sommebit(self.c, c2.c))

    def __mul__(self, c2):
        if type(c2)==Bitchiffre:
        #    assert self.publique == c2.publique
            return Bitchiffre(self.publique, self.publique.produitbit(self.c,
                                                                      c2.c))
        else:
            return c2 * self

    def bootstrap(self):
        z = self.publique.bk
        l = (self.c * z)
        return l.bits[self.publique.eta] #[-1] #l.bits[1+self.publique.eta]


class Entierchiffre:
    def __init__(self, bits):
        """
        bits: liste des bits tel que la valeur soit sum x[i]*2**i
        """
        self.bits = bits
        self.publique = bits[0].publique

    def __add__(self, n2):
        c = []
        l1 = len(self.bits)
        l2 = len(n2.bits)
        l = max(l1 ,l2)
        a = self.bits + (l-l1)*[self.publique.chiffrerbit(0)]
        b = n2.bits + (l-l2)*[self.publique.chiffrerbit(0)]

        r = self.publique.chiffrerbit(0)
        for i in range(0, l):
            temp = b[i] + r
            c.append(a[i]+temp)
            r = a[i] * temp + b[i]*r
        c.append(r)
        return Entierchiffre(c)

    def __lshift__(self, n):
        if n==0:
            return self
        c = Entierchiffre([self.publique.chiffrerbit(0)] + self.bits)
        return c<<(n-1)

    def __mul__(self, n):
        if type(n) == Bitchiffre:
            c = []
            for b in self.bits:
                c.append(n*b)
            return Entierchiffre(c)

        elif type(n) == Entierchiffre:
            c = self.publique.chiffrerentier(0)
            for b in n.bits[::-1]:
                c = (c<<1) + b*self
            return c

        elif type(n) == int:
            c = self.publique.chiffrerentier(0)
            for b in bin(n)[2:]:
                c = (c<<1)
                if b=='1':
                    c = c + self
            return c

    def __rmul__(self, n):
        return self.__mul__(n)
