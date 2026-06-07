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
st.title("Cadastro de funcionários")
st.space("small")
st.write(
    "Use a página Formulário para preencher os dados e a página Câmera para capturar o rosto."
)

if "cadState" not in st.session_state:
    st.session_state.cadState = "cadastroForm"

st.space("small")
btn1, btn2 = st.columns(2)

with btn1:
    if st.button("cadastrar um novo funcionario:"):
        st.switch_page("pages/formCadastro.py")
with btn2:
    if st.button("bater o ponto:"):
        st.switch_page("pages/ponto.py")
