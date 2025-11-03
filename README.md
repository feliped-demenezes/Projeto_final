# 📊 Dashboard Interativo de Saúde Pública (DATASUS)

## Sobre o Projeto
Este é o projeto final do curso de Análise e Desenvolvimento de Sistemas da UNISINOS, focado na democratização e visualização de dados do Sistema de Informações Hospitalares (SIH) do DATASUS.

O objetivo principal é transformar a complexidade dos dados brutos em insights acessíveis, implementando um **Design Centrado no Usuário (DCU)** para facilitar a tomada de decisão de gestores e profissionais de saúde, eliminando a dependência de ferramentas legadas como o TabWin.

### 🌟 Destaques Técnicos

* **Extração e Decodificação:** Utilização da biblioteca `PySUS` para automatizar o download, descompactação (`.dbc`) e decodificação dos arquivos de dados (SIH, SINASC).
* **Visualização Interativa:** Interface desenvolvida com **Dash** (Framework Python para web) e **Plotly** para gráficos dinâmicos.
* **Organização:** Separação clara entre a lógica de dados (`data.py`) e a interface (`app.py`), além de CSS externo (`assets/style.css`).

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **PySUS** (Extração de dados do DATASUS)
* **Pandas** (Tratamento de dados)
* **Dash** (Frontend)
* **Plotly** (Visualização de dados)

## 🚀 Como Rodar o Projeto (Instalação)

Siga os passos abaixo para clonar e executar o projeto em seu ambiente local.

### 1. Pré-requisitos

Você precisa ter o Python 3.x e o `pip` instalados.

**Atenção para usuários Windows:** A biblioteca `pyreaddbc` (dependência do `PySUS`) pode exigir a instalação do **Build Tools para Visual Studio** para compilação. Alternativamente, utilize o WSL (Windows Subsystem for Linux) ou faça a instalação manual do arquivo `.whl` conforme documentado.
