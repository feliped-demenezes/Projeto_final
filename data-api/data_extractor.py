import pandas as pd
import os
import json
# CORREÇÃO: Importamos a CLASSE SIH, que contém a função download
from pysus.online_data.SIH import SIH as SIH_Downloader # Renomeamos para evitar conflito
from datetime import datetime

# --- CONFIGURAÇÕES DE EXTRAÇÃO ---
UF = "RS"
ANO = 2023
MES = 12
OUTPUT_FILE = "dados_sih_prontos.json"

def extrair_e_salvar_dados():
    """
    Função neutra que simula a falha de extração para garantir que o JSON de erro
    seja sempre criado, estabilizando a API.
    """
    print(f"[{datetime.now()}] Iniciando a extração NEUTRA para {UF}/{ANO}-{MES}...")

    try:
        # **COMENTE OU REMOVA ESTA LINHA E TUDO ATÉ O TRATAMENTO DE DADOS**
        # df_sih = SIH_Downloader.download(uf=UF, ano=ANO, mes=MES) 
        
        # **SIMULAÇÃO DE FALHA:**
        raise Exception("Erro de Sintaxe do PySUS: O Extrator não pôde rodar.")
        
    except Exception as e:
        # Esta lógica AGORA será executada SEMPRE, criando o JSON de status 503
        
        print(f"ERRO CRÍTICO na extração/processamento: {e}")

        # Cria um JSON de erro que a API saberá identificar (Status 503)
        json_error = {'status': 'error', 'message': f'Falha Crítica ao Rodar o Extrator. Detalhe: {e}'}
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(json_error, f)
        print("Arquivo de status de erro salvo para a API.")

if __name__ == '__main__':
    extrair_e_salvar_dados()