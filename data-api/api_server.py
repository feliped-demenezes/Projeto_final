from fastapi import FastAPI, HTTPException
import pandas as pd
import os
import json

app = FastAPI()
OUTPUT_FILE = "dados_sih_prontos.json"

@app.get("/api/internacoes")
async def get_internacoes():
    """
    Endpoint que retorna os dados de internação previamente processados.
    """
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(status_code=503, detail="Dados ainda não processados (Arquivo não encontrado).")

    try:
        # Tenta carregar o JSON
        with open(OUTPUT_FILE, 'r') as f:
            data = json.load(f)
            
        # 1. VERIFICAÇÃO: Se o JSON for um dicionário de erro (e não uma lista de dados)
        if isinstance(data, dict) and data.get('status') == 'error':
             # Retorna a mensagem de erro do extrator com status 503
             raise HTTPException(status_code=503, detail=data['message'])

        # 2. SUCESSO: Se for uma lista (dados reais), cria o DataFrame e retorna
        # Usamos o 'data' que já foi carregado.
        df = pd.DataFrame(data) 
        
        return df.to_dict(orient='records')
    
    except Exception as e:
        # Erros inesperados, como JSON malformado
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar JSON. Detalhe: {e}")
    
@app.get("/status")
async def get_status():
    return {"status": "online", "message": "API de Dados do SUS está ativa."}