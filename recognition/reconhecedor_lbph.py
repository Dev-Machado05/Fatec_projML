import json
import pickle
from pathlib import Path
import cv2
import time

def identificar(conf_threshold=100, max_frames=None):
    # --- Configuração de Paths e Constantes ---
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = ROOT_DIR / "db" / "employees.json"
    FACE_NAMES_PATH = ROOT_DIR / "models" / "face_names.pickle"

    # Modelos OpenCV
    detectorFace = cv2.CascadeClassifier(str(ROOT_DIR / "models" / "haarcascade_frontalface_default.xml"))
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()
    reconhecedor.read(str(ROOT_DIR / "models" / "lbph_classifier.yml"))
    
    largura, altura = 220, 220
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)

    # --- Funções Auxiliares ---
    def carregar_funcionarios():
        if not DATA_PATH.exists():
            return {}
        with DATA_PATH.open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        funcionarios = dados.get("funcionarios", [])
        return {str(funcionario.get("id")): funcionario for funcionario in funcionarios}

    def carregar_mapa_rotulos():
        if not FACE_NAMES_PATH.exists():
            return {}
        with FACE_NAMES_PATH.open("rb") as arquivo:
            face_names = pickle.load(arquivo)
        return {valor: chave for chave, valor in face_names.items()}

    # Carregar dados
    funcionarios_por_id = carregar_funcionarios()
    rotulos_por_id = carregar_mapa_rotulos()

    # --- Criar janela e posicionar em foco ---
    cv2.namedWindow("Face", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Face", cv2.WND_PROP_TOPMOST, 1.0)
    cv2.moveWindow("Face", 100, 100)

    # --- Loop Principal ---
    frames = 0
    tempo_inicio = None
    usuario_atual = None

    while True:
        conectado, imagem = camera.read()
        if not conectado:
            break

        frames += 1
        if max_frames is not None and frames > max_frames:
            break

        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(30, 30))
        
        face_reconhecida_frame = False

        for (x, y, l, a) in facesDetectadas:
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
            
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 255), 4)
            
            id_rotulo, confianca = reconhecedor.predict(imagemFace)
            id_funcionario = rotulos_por_id.get(id_rotulo)
            funcionarios = funcionarios_por_id.get(id_funcionario)
            
            nome = "Desconhecido"
            conf_val = None

            if funcionarios:
                try:
                    conf_val = float(confianca)
                except Exception:
                    conf_val = None
            
            if conf_val is not None and conf_val <= conf_threshold:
                nome = funcionarios.get("name", "Desconhecido")  # <- CORRIGIDO
                face_reconhecida_frame = True
                
                if usuario_atual == id_funcionario:
                    if tempo_inicio is None:
                        tempo_inicio = time.time()
                    elif time.time() - tempo_inicio >= 1.0:
                        camera.release()
                        cv2.destroyAllWindows()
                        return {**funcionarios, "_confidence": conf_val}
                else:
                    tempo_inicio = None
                    usuario_atual = id_funcionario
            
            cv2.putText(imagem, nome, (x, y + (a + 30)), font, 1.5, (0, 255, 255))
            cv2.putText(imagem, f"Conf: {int(confianca) if confianca else 0}", (x, y + (a + 50)), font, 1, (0, 255, 255))

        if not face_reconhecida_frame:
            tempo_inicio = None
            usuario_atual = None

        cv2.imshow("Face", imagem)
        cv2.setWindowProperty("Face", cv2.WND_PROP_TOPMOST, 1.0)
        
        key = cv2.waitKey(1)
        if key == ord('q') or cv2.getWindowProperty("Face", cv2.WND_PROP_VISIBLE) < 1:
            break

    camera.release()
    cv2.destroyAllWindows()
    return None