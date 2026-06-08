import streamlit as st

st.set_page_config(
    page_title="Cadastro de funcionários",
    page_icon="🪪",
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

        .action-row button {
            width: 100%;
        }

        .stElementContainer  {
            width: 100%
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Cadastro de funcionários</h1>
        <p>Preencha os dados no formulário e siga para a câmera para concluir o cadastro.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "cadState" not in st.session_state:
    st.session_state.cadState = "cadastroForm"

st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

btn1, btn2 = st.columns(2)
with btn1:
    if st.button("Cadastrar funcionário"):
        st.switch_page("pages/formCadastro.py")
with btn2:
    if st.button("Bater o ponto"):
        st.switch_page("pages/ponto.py")
