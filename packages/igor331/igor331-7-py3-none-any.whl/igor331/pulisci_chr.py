'''
    pulisce i caratteri () dalla stringa e sostituisce - con spazio
'''

def pulisci_chr(stringa):
    st = stringa.replace("(","")\
                .replace(")","")\
                .replace("-"," ")
    return(st)

def main():
    stringa = "(pippo)"
    x = pulisci_chr(stringa)
    print(x)

if __name__== "__main__":
  main()