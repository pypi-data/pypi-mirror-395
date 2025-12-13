import numpy as np, pandas as pd
'''
   prevedere se df è vuoto
   migliorare gestione dell'errore
   migliorare test
'''
def pd_header_cap(df):
    if isinstance(df, pd.DataFrame):
       #if df.empty:  # se è un dataframe allora converto le colonne, forse fare controllo che ci siano le colonne
       #   print ("---errore df vuoto")
       #   df=pd.DataFrame()
       df.columns = df.columns.map(str.upper)    # sistemo header dei dataframe
    else:
       print("errore non è un dataframe")
       exit()
    return(df)
  
def pd_header_clean(df):
    if isinstance(df, pd.DataFrame):
       df.columns = map(lambda x : x.replace(".", "").replace("#", "").replace("-", "").replace(" ", ""), df.columns)
    else:
       print("errore non è un dataframe")
       exit()
    return(df)

def pd_header(df):
  if isinstance(df, pd.DataFrame):
     df = pd_header_cap(df)
     df = pd_header_clean(df)
  else:
    print("errore non è un dataframe")
    exit()
  return(df)

def main():
    print("function df_header")
    data = {'Name.': ['Tom', 'nick', 'krish', 'jack'],
            'Age': [20, 21, 19, 18]}
    df = pd.DataFrame(data)
    df = pd_header(df)
    print(df)
  
if __name__== "__main__":    
   main()