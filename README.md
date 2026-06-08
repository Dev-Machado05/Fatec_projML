# Fatec_projML — Reconhecimento Facial (FATEC)

Fatec_projML é um sistema de reconhecimento facial em Python que utiliza OpenCV (LBPH). O sistema permite:
- Cadastro de colaboradores
- Captura de imagens via webcam
- Treinamento de modelos (LBPH / Eigen / Fisher)
- Reconhecimento em tempo real e registro de presença

### 1. Pré-requisitos

- Python 3.10+ instalado
- Webcam funcional
- Recomenda-se criar um ambiente virtual

### 2. Clonar o repositório

```bash
git clone https://github.com/Dev-Machado05/Fatec_projML.git
cd Fatec_projML
```

### 3. Criar e ativar ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install opencv-python opencv-contrib-python numpy pillow streamlit pandas plotly
```

### 5. Estrutura recomendada de pastas

```
Fatec_projML/
├── capture/                # scripts de captura (webcam)
├── recognition/            # treinamento e reconhecimento
├── utils/                  # utilitários (resize, helpers)
├── pages/                  # páginas Streamlit
├── dataset/
├── dataset_full/
├── db/                     # dados (db/employees.json)
├── models/                 # artefatos treinados + cascades
└── main.py                 # entrypoint (mantido na raiz)
```

### 6. Preparar diretórios e arquivos necessários

- Garanta que existam: `dataset/`, `dataset_full/`, `db/`, `models/`.
- Coloque o cascade e os artefatos treinados em `models/` (recomendado):
  - `models/haarcascade_frontalface_default.xml`
  - `models/lbph_classifier.yml` (após treino)
  - `models/face_names.pickle` (após treino)

### 7. execução do projeto

- Execute a aplicação principal com o comando:

```bash
streamlit run main.py
```

- Acesse a página de cadastro (`Formulário`) e preencha os dados.
- Ele irá mudar para a `Câmera` para capturar o rosto e gravar as imagens (as imagens são gravadas em `dataset/` e `dataset_full/` já os dados do furmulário em `db/`).

### 8. Observações sobre caminhos e imports

- Os módulos em `recognition/` e `capture/` procuram artefatos com base na raiz do projeto. Se você mover arquivos, atualize `ROOT_DIR` ou os imports conforme necessário.
- Ao mover um arquivo Python para uma subpasta, atualize imports. Exemplo:

```py
# antes (arquivo na raiz)
from helper_functions import resize_video

# depois (arquivo em utils/)
from utils.helper_functions import resize_video
```

### 9. Problemas comuns e soluções

- `cv2.face` não encontrado: instale `opencv-contrib-python`.
- Erro ao abrir webcam: verifique permissões e se outro app está usando a câmera.
- Modelos não encontrados: coloque `.yml`, `face_names.pickle` e o cascade em `models/` ou ajuste `ROOT_DIR`.

### 10. Testes rápidos

- Verifique imports básicos:

```bash
python -c "import capture.face_capture_webcam; import recognition.reconhecedor_lbph; import utils.helper_functions"
```

- Rode Streamlit e teste o fluxo `Ponto` para validar integração.
