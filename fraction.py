import math


class Fraction:
    def __init__(self,p,q):
        if q==0:
            raise "division par 0"
        self.p = p
        self.q = q

    def reduire(self):
        d = math.gcd(self.p, self.q)
        self.p //= d
        self.q //= d
        if self.q<0:
            self.q *= -1
            self.p *= -1

    def __repr__(self):
        self.reduire()
        return str(self.p) + "/" + str(self.q)

    def __str__(self):
        self.reduire()
        return str(self.p)+"/"+str(self.q)

    def __add__(self, x):
        if type(x)==int:
            return self.__add__(Fraction(x,1))
        elif type(x)==Fraction:
            f = Fraction(x.q*self.p+x.p*self.q, x.q*self.q)
            f.reduire()
            return f
        else:
            raise "operation impossible +: Fraction et " + str(type(x))

    def __radd__(self, x):
        return self.__add__(x)

    def __neg__(self):
        return Fraction(-self.p, self.q)

    def __pos__(self):
        return self

    def __sub__(self, x):
        return self.__add__(-x)

    def __rsub__(self, x):
        return -self.__sub__(x)

    def __mul__(self, x):
        if type(x)==int:
            return Fraction(self.p*x, self.q)
        elif type(x)==Fraction:
            return Fraction(x.p*self.p, x.q*self.q)
        else:
            raise "operation impossible *: Fraction et " + str(type(x))

    def __rmul__(self, x):
        return self.__mul__(x)

    def __truediv__(self, x):
        if x==0 or x==Fraction(0,1):
            raise "division par 0"
        elif type(x)==int:
            return Fraction(self.p, self.q*x)
        elif type(x)==Fraction:
            return Fraction(x.q*self.p, x.p*self.q)
        else:
            raise "operation impossible /: Fraction et " + str(type(x))

    def __floordiv__(self, x):
        if x==0 or x==Fraction(0,1):
            raise "division par 0"
        elif type(x)==int:
            return int(self.p/(self.q*x))
        elif type(x)==Fraction:
            return int((x.q*self.p)/(x.p*self.q))
        else:
            raise "operation impossible //: Fraction et " + str(type(x))

    def __mod__(self, x):
        if x==0 or x==Fraction(0,1):
            raise "division par 0"
        elif type(x)==int:
            return Fraction(self.p%(self.q*x), self.q)
        elif type(x)==Fraction:
            f = Fraction((self.p*x.q) % (x.p*self.q), self.q*x.q)
            f.reduire()
            return f
        else:
            raise "operation impossible %: Fraction et " + str(type(x))

    def __eq__(self, x):
        if type(x)==int:
            self.reduire()
            return self.q==1 and self.p==x
        if type(x)==Fraction:
            return self.p*x.q == x.p*self.q

    def __neq__(self, x):
        return not self.__eq__(self, x)

    def __lt__(self, x):
        if type(x)==int:
            return self.p<self.q*x
        if type(x)==Fraction:
            return self.p*x.q<self.q*x.p

    def __le__(self, x):
        if type(x)==int:
            return self.p<=self.q*x
        if type(x)==Fraction:
            return self.p*x.q<=self.q*x.p

    def __gt__(self, x):
        if type(x)==int:
            return self.p>self.q*x
        if type(x)==Fraction:
            return self.p*x.q>self.q*x.p

    def __ge__(self, x):
        if type(x)==int:
            return self.p>=self.q*x
        if type(x)==Fraction:
            return self.p*x.q>=self.q*x.p

    def __round__(self):
        return self.p//self.q
