import datetime
import json
from pathlib import Path
import streamlit as st
from capture.face_capture_webcam import cadastro

st.set_page_config(
    page_title="Cadastro por câmera",
    page_icon="📷",
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
        
        .stAlert {
            border-radius: 15px;
        }

        .stAlert p {
            color: #454545;
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


def save_session_state_to_file():
    data_path = Path(__file__).resolve().parent.parent / "db" / "employees.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)

    # Carregar dados existentes
    existing_data = {}
    if data_path.exists():
        with data_path.open("r", encoding="utf-8") as file:
            existing_data = json.load(file)

    # Criar novo payload com dados atualizados
    payload = {
        "id": st.session_state.id,
        "name": st.session_state.name,
        "dtNasc": (
            st.session_state.dtNasc.isoformat()
            if isinstance(st.session_state.dtNasc, datetime.date)
            else st.session_state.dtNasc
        ),
        "cargo": st.session_state.cargo,
        "tempoTrab": st.session_state.tempoTrab,
        "hrEntrada": (
            st.session_state.hrEntrada.isoformat()
            if isinstance(st.session_state.hrEntrada, datetime.time)
            else st.session_state.hrEntrada
        ),
        "hrSaida": (
            st.session_state.hrSaida.isoformat()
            if isinstance(st.session_state.hrSaida, datetime.time)
            else st.session_state.hrSaida
        ),
        "cadState": st.session_state.cadState,
    }

    # Adicionar novo funcionário sem substituir os existentes
    # Mantemos uma lista under the key 'funcionarios'
    funcionarios = existing_data.get("funcionarios", [])
    funcionarios.append(payload)
    existing_data["funcionarios"] = funcionarios

    with data_path.open("w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=2)


init_session_state()

st.markdown(
    """
    <div class="hero">
        <h1>Cadastro por câmera</h1>
        <p>Finalize o cadastro com a captura do rosto após validar os dados do formulário.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.cadState != "cadastroFoto":
    st.info("Abra o formulário, confirme os dados e volte aqui para iniciar a captura.")
    if st.button("Retornar ao formulário"):
        save_session_state_to_file()
        st.switch_page("pages/formCadastro.py")

elif st.session_state.cadState == "complete":
    st.success(
        "Cadastro finalizado. Você pode voltar ao formulário para cadastrar outra pessoa."
    )
    if st.button("novo cadastro"):
        st.session_state.cadState = "cadastroForm"
        st.session_state.id = ""
        st.session_state.name = ""
        st.session_state.dtNasc = datetime.date.today()
        st.session_state.cargo = "funcionario"
        st.session_state.tempoTrab = 0
        st.session_state.hrEntrada = datetime.time(9, 0)
        st.session_state.hrSaida = datetime.time(17, 0)
        save_session_state_to_file()
        st.switch_page("pages/formCadastro.py")

else:
    st.warning("Aguarde abrir a câmera para efetuar o cadastro.")
    st.write(f"Usuário atual: {st.session_state.id}")

    res = cadastro(st.session_state.id)
    if res:
        st.session_state.cadState = "complete"
        save_session_state_to_file()
        st.success("Cadastro concluído com sucesso.")
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("Cadastrar novo funcionário"):
                st.switch_page("pages/formCadastro.py")
        with btn2:
            if st.button("Bater ponto"):
                st.switch_page("pages/ponto.py")
                st.session_state.identState = "incompleto"
