import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import json

st.set_page_config(
    page_title="Painel do administrador",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        .hero {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 2rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 1.75rem;
            font-weight: 700;
            color: #0f172a;
        }

        .hero p {
            margin: 0.5rem 0 0;
            color: #64748b;
            font-size: 0.95rem;
        }

        .info-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.2rem 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
            text-align: center;
        }

        .metric-val {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1;
        }

        .metric-lbl {
            font-size: 0.75rem;
            color: #64748b;
            margin-top: 0.4rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
        }
        h3 span{
            color: #000000
        }
    </style>
    """,
    unsafe_allow_html=True,
)

data_path = Path(__file__).resolve().parent.parent / "db" / "acessos.json"
data = pd.read_json(data_path)
user = json.loads(st.session_state.actUser)

st.markdown(
    f"""
    <div class="hero">
        <h1>Olá {user["name"]}</h1>
        <p>Monitore o status e os registros de acessos dos funcionários às máquinas.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        f'<div class="info-card"><div class="metric-val">{len(data)}</div><div class="metric-lbl">Total Acessos</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    corretos = len(data[data["status"] == "correto"])
    st.markdown(
        f'<div class="info-card"><div class="metric-val" style="color: #10b981;">{corretos}</div><div class="metric-lbl">Corretos</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    atrasados = len(data[data["status"] == "atrasado"])
    st.markdown(
        f'<div class="info-card"><div class="metric-val" style="color: #f59e0b;">{atrasados}</div><div class="metric-lbl">Atrasados</div></div>',
        unsafe_allow_html=True,
    )
with m4:
    negados = len(data[data["status"] == "negado"])
    st.markdown(
        f'<div class="info-card"><div class="metric-val" style="color: #ef4444;">{negados}</div><div class="metric-lbl">Negados</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Todos os Registros:")
st.dataframe(data, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Análise de Visão Geral:")
col1, col2 = st.columns(2)

# Configuração de Tema Escuro Premium para os gráficos
layout_padrao_grafico = dict(
    font=dict(
        family="Inter, Segoe UI, sans-serif", size=12, color="#f8fafc"
    ),  # Texto principal branco/claro
    paper_bgcolor="#1e293b",  # Fundo preto acinzentado do card
    plot_bgcolor="#1e293b",  # Fundo interno do gráfico
    title_font=dict(size=14, color="#ffffff", family="Inter, Segoe UI, sans-serif"),
    xaxis=dict(
        gridcolor="#334155",  # Linhas de grade sutis
        zerolinecolor="#334155",
        tickfont=dict(color="#cbd5e1"),
    ),
    yaxis=dict(
        gridcolor="#334155", zerolinecolor="#334155", tickfont=dict(color="#cbd5e1")
    ),
    legend=dict(font=dict(color="#cbd5e1")),
)

with col1:
    fig_pizza = px.pie(
        data,
        names="status",
        title="Proporção por Status de Acesso:",
        hole=0.4,
        color="status",
        color_discrete_map={
            "correto": "#10b981",
            "atrasado": "#f59e0b",
            "negado": "#ef4444",
        },
    )
    fig_pizza.update_layout(
        margin=dict(t=50, b=20, l=20, r=20), legend=dict(orientation="h", y=-0.15)
    )
    fig_pizza.update_layout(layout_padrao_grafico)
    st.plotly_chart(fig_pizza, use_container_width=True)

with col2:
    df_maq = (
        data.groupby(["access", "accessType"]).size().reset_index(name="Quantidade")
    )
    fig_barra_maq = px.bar(
        df_maq,
        x="access",
        y="Quantidade",
        color="accessType",
        title="Uso de Máquinas por Tipo",
        barmode="group",
        color_discrete_map={"entrada": "#3b82f6", "saida": "#6366f1"},
    )
    fig_barra_maq.update_layout(
        margin=dict(t=50, b=20, l=20, r=20),
        xaxis_title="Máquina",
        yaxis_title="Qtd. Acessos",
        legend=dict(orientation="h", y=-0.15),
    )
    fig_barra_maq.update_layout(layout_padrao_grafico)
    st.plotly_chart(fig_barra_maq, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
