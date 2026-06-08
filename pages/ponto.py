import streamlit as st
from recognition.reconhecedor_lbph import identificar
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="Ponto",
    page_icon="⏱️",
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
            background: rgba(255, 255, 255, 0.8);
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
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if not "identState" in st.session_state:
    st.session_state.identState = "incompleto"

if (st.session_state.identState != "encerrarExpediente" and "sucessoEnc"):
    if (st.button("voltar para o inicio:")):
        st.switch_page("main.py")

st.markdown(
    """
    <div class="hero">
        <h1>Ponto: entrada e saída</h1>
        <p>Clique no botão abaixo para iniciar o reconhecimento facial.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.identState == "erro":
    st.error("Ocorreu um erro em meio a identificação, tente novamente mais tarde...")

elif st.session_state.identState == "sucesso":
    st.success("identificação concluida, redirecionando para a próxima página...")
    time.sleep(1)
    user = json.loads(st.session_state.actUser)

    if user["cargo"] == "funcionario":
        st.session_state.hrInicio = datetime.now().time()
        st.switch_page("pages/employeeHome.py")
    elif user["cargo"] == "administrador":
        st.session_state.hrInicio = datetime.now().time()
        st.switch_page("pages/admHome.py")
elif st.session_state.identState == "sucessoEnc": 
    st.success("identificação concluida, redirecionando para a próxima página...")
    st.session_state.identState = "incompleto"
    time.sleep(1)
    st.switch_page("main.py")

st.space("xxsmall")

if st.button("Iniciar reconhecimento"):
    user = identificar()
    if st.session_state.identState != "encerrarExpediente":
        if user:
            st.session_state.actUser = json.dumps(user)
            st.session_state.identState = "sucesso"
        else:
            st.session_state.identState = "erro"
    else:
        if user:
            st.session_state.identState = "sucessoEnc"
        else:
            st.session_state.identState = "erro"
