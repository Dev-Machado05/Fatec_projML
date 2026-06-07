import streamlit as st
from recognition.reconhecedor_lbph import identificar
import json
import time

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

if not "identState" in st.session_state:
    st.session_state.identState = "incompleto"

st.title("Ponto: (entrada/saida)")
st.caption("Clique no botão para fazer o reconhecimento facial:")

if st.session_state.identState == "erro":
    st.error("Ocorreu um erro em meio a identificação, tente novamente mais tarde...")

elif st.session_state.identState == "sucesso":
    st.success("identificação concluida, redirecionando para a próxima página...")
    time.sleep(1)
    user = json.loads(st.session_state.actUser)

    if user["cargo"] == "funcionario":
        st.switch_page("main.py")  # go to functionary page
    elif user["cargo"] == "administrador":
        st.switch_page("main.py")  # go to adm page


if st.button("iniciar reconhecimento:"):
    user = identificar()
    if user:
        st.session_state.actUser = json.dumps(user)
        st.session_state.identState = "sucesso"
    else:
        st.session_state.identState = "erro"
