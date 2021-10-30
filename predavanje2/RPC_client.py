import rpyc

c =  rpyc.connect("localhost", 25555)
print(c.root.vrati_izracun(4))
print(c.root.kontrolna_vrijednost)
c.close()

input()