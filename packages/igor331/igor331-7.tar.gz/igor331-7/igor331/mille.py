'''
     libreria mille
     divide un numero (int o float) per mille e restituisce un intero
'''

def mille(numero):
    ret=0
    if  isinstance(numero, float) or  isinstance(numero,int):
        ret=int(numero/1000+0.5)
    else:
        print(f"errore {numero}")
        exit(0)
    return (ret)
   
def main(out,log):
    print("function mille")
    input = 10000
    x=mille(10000)
    print(input,mille(input))
    input = 12100.4
    print(input,mille(input))
  
if __name__== "__main__":    
   main(False,9)