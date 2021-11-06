import rpyc

korisnik=input("Unesite vaše ime: ")

c=rpyc.connect('localhost', 35222)

mem=c.root.get_mem()


while True:
    akc=int(input("""\nOdaberi akciju:
    1-Pošalji transakciju
    2-Ispiši blokove
    3-Ispiši blok
    4-Ispiši mempool
    5-Prekini program
    Odabir[1-4]:"""))

    if akc==1:
        primatelj = input("\nUnesite ime primatelja: ")
        iznos=int(input("\nUnesite iznos: "))
        c.root.mem_add(korisnik,primatelj,iznos)
        print("\nTransakcija poslana")
    elif akc==2:
        ch=c.root.chain_get()
        print(ch)
    elif akc==3:
        br_bloka=int(input("\nUnesite broj bloka: "))
        ch=c.root.chain_get()
        selected_block_data=ch[br_bloka-1].split(":")
        prev_block_data=ch[br_bloka-2].split(":")
        selected_block_hash=selected_block_data[0][2:-7]
        next_block_hash=prev_block_data[0][2:-7]
        
        print("HASH PRETHODNOG BLOKA:",next_block_hash)
        print("HASH ODABRANOG BLOKA:", selected_block_hash)

        transakcija = 0
        for i, val in enumerate(selected_block_data):
            if i == 0:
                print("TRANSAKCIJE:")
                continue

            if "#" in val:
                transakcija+=1
                print("Transakcija {0} - {1} -> {2} - Iznos: {3}".format(transakcija, selected_block_data[i-2], selected_block_data[i-1], val.split("#")[0]))

            
        
    elif akc==4:
        mem=c.root.get_mem()
        print(mem)
    elif akc==5:
        break

c.close()

        
