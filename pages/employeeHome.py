import streamlit as st
import json
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Painel do colaborador",
    page_icon="👤",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #f7f8fc 0%, #eef2f7 100%);
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        .hero {
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            padding: 1.25rem 1.4rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 1.8rem;
            line-height: 1.15;
            color: #0f172a;
        }

        .hero p {
            margin: 0.4rem 0 0;
            color: #475569;
            font-size: 0.95rem;
        }

        .info-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }

        .label {
            color: #64748b;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.25rem;
        }

        .value {
            color: #0f172a;
            font-size: 1.05rem;
            font-weight: 700;
        }

        .hero p {
            color: #000000
        }
    </style>
    """,
    unsafe_allow_html=True,
)

user = json.loads(st.session_state.actUser)

def workStatus():
    formato = "%d/%m/%Y %H:%M:%S"
    hr_inicio = st.session_state.hrInicio
    data_hoje = datetime.now().date()
    inicio = datetime.combine(data_hoje, hr_inicio)
    
    fim = inicio + timedelta(hours=user["tempoTrab"])
    margem = timedelta(minutes=15) 
    limite_inferior_fim = fim - margem
    limite_superior_fim = fim + margem
    
    agora = datetime.now()
    
    # Exibir os tempos para conferência no console
    print(f"Início do intervalo:         {inicio.strftime(formato)}")
    print(f"Fim teórico:                 {fim.strftime(formato)}")
    print(f"Janela do 'Exatamente' (fim): {limite_inferior_fim.strftime('%H:%M:%S')} até {limite_superior_fim.strftime('%H:%M:%S')}")
    print(f"Horário atual:               {agora.strftime(formato)}")
    print("-" * 40)
    
    if agora >= limite_inferior_fim:
        return "🟢 Sua jornada de hoje está completa."
    else:
        tempo_restante = fim - agora
        if tempo_restante.total_seconds() < 0:
            return "🟢 Sua jornada de hoje está completa." # Segurança extra
            
        total_segundos = int(tempo_restante.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        horas_formatadas = f"{horas:02d}:{minutos:02d}"
        
        return f"🔴 Faltam <b>{horas_formatadas}</b> horas para o fim da jornada de hoje."

st.markdown(
    f"""
    <div class="hero">
        <h1>Olá, {user['name']}!</h1>
        <p>Confira rapidamente seu status de jornada e os horários cadastrados.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- ALTERAÇÃO AQUI: Bloco isolado para atualizar os minutos automaticamente ---
@st.fragment(run_every=10) # executa a cada 10s
def render_status():
    st.markdown(
        f"""
            <div class="hero">
                <p>{workStatus()}</p>
            </div>
        """, unsafe_allow_html=True)

render_status()
# ------------------

st.space("medium")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="label">Horário mínimo de entrada</div>
            <div class="value">{user['hrEntrada']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="label">Horário mínimo de saída</div>
            <div class="value">{user['hrSaida']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.space("xxsmall")
if (st.button("encerrar expediente:")):
    st.session_state.identState = "encerrarExpediente"
    st.switch_page("pages/ponto.py")