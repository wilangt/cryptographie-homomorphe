lambdaa, nb_operations = 50, 1000

alice, bob = genererCS(lambdaa, nb_operations)
a = bob.chiffrerentier(5)
b = bob.chiffrerentier(4)
c = (a*b)
print(alice.dechiffrerentier(c))
