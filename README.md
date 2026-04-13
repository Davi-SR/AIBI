# 📊 AI BI - Analista de Banco de Dados Inteligente

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)
![Agno](https://img.shields.io/badge/Agent-Agno-8A2BE2)
![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75)

Um **Agente de Business Intelligence (BI)** impulsionado por Inteligência Artificial. Com ele, os usuários podem realizar análises em formato de chat, conversando em **linguagem natural**, enquanto o agente vasculha ativamente o banco de dados via SQL e gera **Dashboards Visuais interativos**, estruturados dinamicamente na tela.

---

## 🎯 Objetivo

Eliminar o gargalo da criação tradicional de Dashboards. Através desta plataforma, as equipes de negócio e diretoria podem perguntar *"Quais foram os 5 maiores clientes do último mês? Mostre-me usando um gráfico de pizza"* e o modelo não só escreve e executa o **SQL nativo** para a base de dados, como desenha a visualização solicitada diretamente na interface de chat.

---

## ⚙️ Arquitetura do Projeto

O sistema é modular e foca em uma infraestrutura Pythônica sólida.

1. **`agent.py` | O Cérebro do BI**
   - Importa o framework **Agno** (antigo Phidata).
   - Injeta o *System Prompt* robusto (`prompt.md`), ditando limites éticos e garantindo o comportamento sênior focado em BI, sem alucinações.
   - Lê os Dicionários de Dados ("conhecimento empírico") (`knowledge.JSON`).
   - Gerencia estado e memória para suportar contexto multi-nível nas sessões através do modelo GPT.

2. **`app.py` | O Front-end de Conversação e Rendering**
   - UI do Chatbox escrita inteiramente em **Streamlit**.
   - Integra as mensagens do usuário com o cérebro `agent.py`.
   - Utiliza engenharia reversa via *Regex* para varrer a resposta textual do LLM, capturando se ele elaborou esquemas gráficos como `[BAR] -> [...]`.
   - Caso possua gráficos, o **Pandas** traduz esse output em DataFrames velozes e o **Plotly** renderiza o Dashboard lado a lado na UI.

3. **`api.py` | Camada de API Escalonável (FastAPI)** *(Opcional)*
   - Ponto de injeção em Web.
   - Fornece um endpoint `/query` POST padronizado em **FastAPI** para times externos (Móbile, Landing Pages corporativas, etc) enviarem requisições e buscarem o *RunResponse* da IA em formato programático.

---

## 🚀 Como Inicializar

Certifique-se de configurar e alimentar as variáveis de ambiente antes da inicialização.
O projeto utiliza um arquivo `.env` (oculto no rastreio) para guardar chaves sensíveis.

Crie um arquivo `.env` na raiz do projeto com:
```env
# URL de conexão válida para seu Banco de Dados (Postgres, MySQL, SQLite, etc)
DB_URL="postgresql+psycopg2://user:pass@host:5432/nomedobanco"

# Chave API da OpenAI
OPENAI_API_KEY="sk-proj-sua-chave-aqui"
```

### 1. Instalação das Dependências

Para evitar conflitos, é altamente recomendado usar pacotes gerenciados. 
Se você utiliza `pip` tradicional:
```bash
pip install -r requirements.txt
```
Se utilizar o `uv` (Altamente veloz):
```bash
uv pip install -r requirements.txt
# Ou instale o ambiente com: uv add streamlit pandas plotly agno fastapi pydantic python-dotenv
```

### 2. Subindo a Interface Gráfica (Dashboard em Chat)

Abra o terminal do projeto e utilize o motor do app Streamlit:

```bash
# Caso utilize pip puro
streamlit run app.py

# Caso utilize o uv
uv run streamlit run app.py
```

Acesse no seu navegador em `http://localhost:8501`.

### 3. (Opcional) Inicializando via API

Se o seu objetivo é testar o cérebro (`agent.py`) via requisições curl/Postman sem a UI:
```bash
uvicorn api:app --reload
```
A sua documentação **Swagger Open-API** viverá automaticamente no path: `http://127.0.0.1:8000/docs`.

---

## 📐 Estrutura de Interação Visuais (Regex Parser API)

A sua comunicação com a UI requer que o AGNO instrua o modelo a sempre devolver o indicador gráfico.

O Motor Streamlit aceita os 3 tipos de tags principais geradas por inteligência artificial sob o formato JSON Oneline:

- **[BAR] -> [{"chave":"valor"}]** (Dashboards de Barras)
- **[LINE] -> [{"chave":"valor"}]** (Progressão em Linha Mapeada)
- **[PIE] -> [{"chave":"valor"}]** (Gráficos Dimensionais de Pizza)

O **app.py** se encarrega de ler isso, higienizar e desenhar nativamente no Plotly!

---

💡 *Sistema desenvolvido prezando por resiliência de dados (Apenas Leitura no Database) e agilidade em entrega visual.*
