import streamlit as st
import pandas as pd
import plotly.express as px
import re
import json
import os

# Carrega arquivo contendo env variables (caso ainda não esteja instanciado)
from dotenv import load_dotenv
load_dotenv()

# Tenta carregar o construtor do agente
try:
    from agent import get_agent
except Exception as e:
    st.error(f"Falha ao importar o agent.py: {e}")
    get_agent = None

# Inicializa o Agente com Memória Específico desta Sessão de Usuário
if "bot_agent" not in st.session_state:
    if get_agent:
        st.session_state.bot_agent = get_agent()
    else:
        st.session_state.bot_agent = None

st.set_page_config(page_title="AI BI Dashboard", page_icon="📈", layout="wide")

st.title("📈 AI BI - Analista de Dados & Dashboards")
st.markdown("Pergunte ao agente de banco de dados e ele irá **consultar**, **analisar** e **gerar dashboards** pra você em tempo real!")

# Inicialização do estado de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem de boas-vindas do Assistant
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Olá! Eu sou seu **Analista de BI de IA**. Fui treinado para explorar seu banco de dados, montar consultas SQL seguras e gerar gráficos ricos. O que você gostaria de analisar hoje?"
    })

def render_message_content(content):
    """
    Analisa o texto retornado. Se houver um padrão como `[BAR] -> [{"chave": "valor"}]`,
    extrai os dados e tenta renderizar graficamente com Plotly via DataFrames do Pandas.
    """
    # Regex projetada para buscar o formato `[TIPO] -> [{...}]` multiline
    pattern = r'\[([A-Z]+)\]\s*->\s*(\[.*?\])'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    
    display_text = content
    chart_info = None
    
    if match:
        chart_type = match.group(1).upper()
        json_str = match.group(2)
        try:
            data = json.loads(json_str)
            if data and isinstance(data, list):
                df = pd.DataFrame(data)
                chart_info = {"type": chart_type, "df": df}
            # Removemos a notação crua do bot (JSON) para que o frontend fique limpo
            display_text = display_text.replace(match.group(0), "📊 **Visualização Renderizada no Dashboard:**")
        except Exception as e:
            st.warning(f"Erro ao parsear dados estruturados: {e}")
            
    # Renderizamos todo o conteúdo MD puro primeiro
    st.markdown(display_text)
    
    # Se encontramos e engolimos um gráfico válido, renderizamos abaixo
    if chart_info and not chart_info['df'].empty:
        df = chart_info['df']
        tipo = chart_info['type']
        
        # Pega as colunas da resposta (X = Dimensão, Y = Métrica(s))
        cols = df.columns.tolist()
        if len(cols) >= 2:
            x_col = cols[0]
            # Se vier com > 2 colunas, o Plotly entende a lista como N métricas
            y_col = cols[1] if len(cols) == 2 else cols[1:]

            try:
                # Validação de qual tipo a IA mandou usar
                if tipo in ['BAR', 'BARRA', 'BARRAS']:
                    fig = px.bar(df, x=x_col, y=y_col, text_auto=True, template="plotly_white")
                elif tipo in ['LINE', 'LINHA', 'LINHAS']:
                    fig = px.line(df, x=x_col, y=y_col, markers=True, template="plotly_white")
                elif tipo in ['PIE', 'PIZZA']:
                    fig = px.pie(df, names=x_col, values=cols[1], template="plotly_white")
                else: # Default Fallback para barras
                    fig = px.bar(df, x=x_col, y=y_col, template="plotly_white")
                
                # Ajuste de layout pro grafico não ficar achatado
                fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
                
                # Renderiza no Streamlit
                st.plotly_chart(fig, use_container_width=True)
                
                # Cria um mini painel para o usuário que quiser ver os números puros
                with st.expander("👁️ Ver Tabela Analítica (Dados Brutos)"):
                    st.dataframe(df, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Deu erro ao mandar desenhar o gráfico pro Plotly: {e}")

# Loop de Renderização das mensagens guardadas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        render_message_content(msg["content"])

# Captura Nova Entrada do Usuario
if prompt := st.chat_input("Ex: Liste os 5 produtos mais vendidos e faturamento. Mostre um [BAR]"):
    
    if not st.session_state.bot_agent:
        st.error("Agente não está carregado. Verifique o import em agent.py")
        st.stop()
        
    # Salva interacao User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Gera a Resposta via AI
    with st.chat_message("assistant"):
        with st.spinner("Conectando ao banco, extraindo consultas e gerando insights..."):
            try:
                response = st.session_state.bot_agent.run(prompt)
                
                # A dependência Agno devolve RunResponse e extraímos o contet text
                if hasattr(response, "content"):
                    assistant_text = response.content
                else:
                    assistant_text = str(response)
                    
            except Exception as e:
                assistant_text = f"🚨 Ocorreu um erro no processamento do banco: {str(e)}"
        
        # Renderização do Assistant
        render_message_content(assistant_text)
        
    # Salva Assistant State history
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
