import datetime
import streamlit as st

st.set_page_config(
    page_title="Formulário de cadastro",
    page_icon="📝",
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

        .form-card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }

        .stHorizontalBlock .stElementContainer {
            width: 100%
        } 

        label[data-testid="stWidgetLabel"] p {
            color: #000000 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def init_session_state():
    defaults = {
        "cadState": "cadastroForm",
        "id": "",
        "name": "",
        "dtNasc": datetime.date.today(),
        "cargo": "funcionario",
        "tempoTrab": 0,
        "hrEntrada": datetime.time(9, 0),
        "hrSaida": datetime.time(17, 0),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def validate_inputs():
    required_texts = [
        ("id", st.session_state.id),
        ("name", st.session_state.name),
    ]

    for label, value in required_texts:
        if not isinstance(value, str) or value.strip() == "":
            st.error(f"Campo '{label}' não pode estar vazio.")
            return False

    if not isinstance(st.session_state.dtNasc, datetime.date):
        st.error("Data de nascimento inválida.")
        return False

    if not isinstance(st.session_state.hrEntrada, datetime.time) or not isinstance(
        st.session_state.hrSaida, datetime.time
    ):
        st.error("Horário de entrada/saída inválido.")
        return False

    if not isinstance(st.session_state.tempoTrab, int):
        st.error("Tempo de trabalho inválido.")
        return False

    return True


init_session_state()

if st.button("Voltar ao menu inicial"):
    st.switch_page("main.py")

st.markdown(
    """
    <div class="hero">
        <h1>Formulário de cadastro</h1>
        <p>Preencha os dados do funcionário antes de abrir a câmera.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.cadState == "cadastroFoto":
    st.success("Dados válidos. Abrindo a página Câmera de cadastro.")

col1, col2 = st.columns(2)

with col1:
    st.session_state.id = st.text_input(
        "Id/Ra", placeholder="Digite o seu RA:", value=st.session_state.id
    )
    st.session_state.dtNasc = st.date_input(
        "Data de nascimento",
        max_value=datetime.date.today(),
        value=st.session_state.dtNasc,
    )
    st.session_state.hrEntrada = st.time_input(
        "Horário de entrada", value=st.session_state.hrEntrada
    )

with col2:
    st.session_state.name = st.text_input(
        "Nome", placeholder="Digite o seu nome:", value=st.session_state.name
    )
    st.session_state.tempoTrab = st.number_input(
        "Tempo de trabalho (horas)",
        value=st.session_state.tempoTrab,
        min_value=0,
    )
    st.session_state.hrSaida = st.time_input(
        "Horário de saída", value=st.session_state.hrSaida
    )

st.session_state.cargo = st.selectbox(
    "Cargo",
    ("funcionario", "administrador"),
    index=0 if st.session_state.cargo == "funcionario" else 1,
)

st.space("xxsmall")

continue_btn, reset_btn = st.columns(2)

with reset_btn:
    if st.button("Limpar formulário"):
        st.session_state.id = ""
        st.session_state.name = ""
        st.session_state.dtNasc = datetime.date.today()
        st.session_state.cargo = "funcionario"
        st.session_state.tempoTrab = 0
        st.session_state.hrEntrada = datetime.time(9, 0)
        st.session_state.hrSaida = datetime.time(17, 0)
        st.session_state.cadState = "cadastroForm"

with continue_btn:
    if st.button("Continuar"):
        if validate_inputs():
            st.session_state.cadState = "cadastroFoto"
            st.switch_page("pages/camCadastro.py")