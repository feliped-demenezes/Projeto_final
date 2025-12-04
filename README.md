# 📊 Dashboard Interativo de Saúde Pública (DATASUS)

## Sobre o Projeto
Este é o projeto final do curso de Análise e Desenvolvimento de Sistemas da UNISINOS. Ele se concentra na democratização e visualização dos dados do Sistema de Informações Hospitalares (SIH) do DATASUS.

O objetivo principal é transformar a complexidade dos dados brutos em insights acessíveis, implementando um **Design Centrado no Usuário (DCU)** para facilitar a tomada de decisão de gestores e profissionais de saúde, eliminando a dependência de ferramentas legadas como o TabWin.

### 🌟 Destaques Técnicos e Arquitetura 


O projeto adota uma **Arquitetura de Microsserviços de Dados** para garantir a estabilidade do dashboard, isolando o processo de extração do DATASUS:

* **Extração e Decodificação:** Utilização da biblioteca `PySUS` no backend.
* **API/Backend Estável:** A extração e o pré-processamento de dados são feitos dentro de um **Container Docker** que expõe uma API RESTful usando **FastAPI**.
* **Visualização Interativa:** O Frontend é um dashboard desenvolvido com **Dash** (Framework Python para web) e **Plotly** para gráficos dinâmicos.
* **Resiliência:** O Frontend consome a API e, em caso de falha na extração do DATASUS, o Dashboard carrega instantaneamente com dados de *fallback* (fictícios), priorizando a experiência do usuário (DCU).

---

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| **Backend/Extração** | Python 3.11 | Ambiente de execução. |
| | PySUS (v1.0.1) | Download, descompactação (`.dbc`) e decodificação dos dados do DATASUS (SIH). |
| | FastAPI | Criação da API RESTful para servir os dados pré-processados. |
| | **Docker** | Isolamento do ambiente da API e do Extrator, garantindo portabilidade e estabilidade. |
| **Frontend** | Dash | Framework para construção do dashboard web. |
| | Plotly | Geração de gráficos e visualizações interativas. |

---

## 🚀 Como Rodar o Projeto (Instalação)

O projeto é dividido em dois serviços (API/Backend e Frontend/Dashboard). O Backend deve ser rodado via Docker.

### 1. Pré-requisitos

Você deve ter as seguintes ferramentas instaladas:

* **Python 3.11+** (para rodar o Dashboard/Frontend)
* **Git**
* **Docker Desktop** (para rodar a API/Backend)

### 2. Clonar o Repositório

Navegue até o diretório onde você deseja salvar o projeto e execute:

```bash
git clone (https://github.com/feliped-demenezes/Projeto_final)
cd projeto_final
