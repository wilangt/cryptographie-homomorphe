def genererCS(lambdaa,maxi):
    clef_invalide = True
    while clef_invalide:
        alice = Prive(lambdaa)
        bob = Publique(alice.publier())
        p, pc, j, prod_correct = 1, 1, 0, true
        while prod_correct:
            t = random.randint(0,1)
            p *= t
            pc *= bob.chiffrerbit(t)
            j += 1
            prod_correct = (p==alice.dechiffrerbit(pc))
            if j > maxi : return alice, bob
