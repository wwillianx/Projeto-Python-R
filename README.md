# Sistema de Análise e Previsão de Vendas de Video Games

---

## 🚀 Introdução

Este projeto visa realizar uma análise exploratória abrangente, prever vendas futuras e segmentar produtos dentro do dinâmico mercado de videogames. Utilizando uma integração robusta entre **R** e **Python**, processamos dados, treinamos modelos de machine learning simples e apresentamos os resultados através de relatórios e gráficos intuitivos.

**Versão do Documento:** 1.3  
**Data:** 10 de abril de 2025  
**Autores:** Giordano Cassini, Lucas Pereira, Mikael Sousa, Tiago Marcelo Dalbosco e Willian Scheuermann. (Disciplina DLPD II)

---

## 🛠️ Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Preparação Inicial

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/wwillianx/Projeto-Python-R.git
    cd Projeto-Python-R
    ```
2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    # No Windows:
    # .\venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```
3.  **Instale as dependências Python:**
    **Execute o seguinte comando para instalar todas as bibliotecas Python necessárias:**
    ```bash
    pip install -r requirements.txt
    ```
    Isso garantirá que todas as dependências do projeto sejam instaladas automaticamente.

4.  **Instale as dependências R:**
    **Para instalar os pacotes R necessários, execute o seguinte script R:**
    ```bash
    Rscript r_requirements.r
    ```
    Este script verificará e instalará automaticamente os pacotes `ggplot2` e `dplyr`.

### 2. Configuração do MongoDB (Crucial para persistência de gráficos)

O sistema pode opcionalmente salvar e recuperar gráficos do MongoDB. Para isso, você precisará configurar sua URI de conexão. **É altamente recomendado usar um arquivo `.env` para segurança.**

1.  **Crie um arquivo `.env` na raiz do seu projeto:**
    Na mesma pasta onde está este `README.md`, crie um arquivo chamado `.env`.
    
2.  **Adicione sua URI do MongoDB ao `.env`:**

    * **Para MongoDB Local (se estiver rodando um servidor local):**
        ```dotenv
        MONGO_URI="mongodb://localhost:27017"
        ```
    * **Para MongoDB Atlas (nuvem - recomendado):**
        Copie a string de conexão do painel do seu cluster no MongoDB Atlas (geralmente na aba "Connect" > "Drivers").
        ```dotenv
        MONGO_URI="mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        ```
        **Lembre-se de substituir `<usuario>`, `<senha>` e `<cluster>` pelos seus seus dados reais.**

    **Importante:** O arquivo `.env` é ignorado pelo Git (graças ao `.gitignore`), garantindo que suas credenciais não sejam publicadas acidentalmente.

### 3. Executando o Projeto

Após a configuração, você pode rodar o script principal:

```bash
python3 main.py