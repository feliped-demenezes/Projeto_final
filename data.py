import pandas as pd
from pysus.online_data.SIH import download_dbf

def extrair_dados_SIH(uf="RS", ano=2023, mes=12):
    print(f"Iniciando extração dos dados do SIH para a UF {uf}, ano {ano} e mês {mes}...")
    try:
        df = download_dbf(uf=uf, ano=ano, mes=mes)
        print("Dados extraídos com sucesso!")
        return df
    except Exception as e:
        print(f"Ocorreu um erro durante a extração dos dados: {e}")
        return None

if __name__ == "__main__":
    df_SIH_RS = extrair_dados_SIH(uf="RS", ano=2023, mes=12)
    if df_SIH_RS is not None:
        print(df_SIH_RS.head())
        print(df_SIH_RS.info())