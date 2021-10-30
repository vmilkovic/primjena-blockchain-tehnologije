import rpyc

c =  rpyc.connect("localhost", 25555)
print(c.root.vlasnik())
print(c.root.promet())
c.close()
input()
