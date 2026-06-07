import datetime
import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none
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

if (st.button("voltar ao menu inicial:")):
    st.switch_page("main.py")

st.title("Formulário de cadastro")
st.caption("Preencha os dados do funcionário antes de abrir a câmera.")

if st.session_state.cadState == "cadastroFoto":
    st.success("Dados válidos. Abrindo a página Câmera de cadastro.")

st.session_state.id = st.text_input(
    "Id/Ra", placeholder="Digite o seu RA:", value=st.session_state.id
)
st.session_state.name = st.text_input(
    "Nome:", placeholder="Digite o seu nome:", value=st.session_state.name
)
st.session_state.dtNasc = st.date_input(
    "Data Nascimento:",
    max_value=datetime.date.today(),
    value=st.session_state.dtNasc,
)
st.session_state.tempoTrab = st.number_input(
    "tempo de trabalho:",
    value=st.session_state.tempoTrab,
    min_value=0,
)
st.session_state.cargo = st.selectbox(
    "Cargo:",
    ("funcionario", "administrador"),
    index=0 if st.session_state.cargo == "funcionario" else 1,
)
st.session_state.hrEntrada = st.time_input(
    "Horario de entrada:", value=st.session_state.hrEntrada
)
st.session_state.hrSaida = st.time_input(
    "Horario de saida:", value=st.session_state.hrSaida
)

continue_btn, reset_btn = st.columns(2)

with reset_btn:
    if st.button("reset"):
        st.session_state.id = ""
        st.session_state.name = ""
        st.session_state.dtNasc = datetime.date.today()
        st.session_state.cargo = "funcionario"
        st.session_state.tempoTrab = 0
        st.session_state.hrEntrada = datetime.time(9, 0)
        st.session_state.hrSaida = datetime.time(17, 0)
        st.session_state.cadState = "cadastroForm"

with continue_btn:
    if st.button("confirmar"):
        if validate_inputs():
            st.session_state.cadState = "cadastroFoto"
            st.switch_page("pages/camCadastro.py")