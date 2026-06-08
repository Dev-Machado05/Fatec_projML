import json
import pickle
from pathlib import Path

import cv2

def identificar(conf_threshold=100, max_frames=None):
    # ROOT_DIR aponta para a raiz do projeto (um nível acima desta pasta)
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = ROOT_DIR / "db" / "employees.json"
    FACE_NAMES_PATH = ROOT_DIR / "models" / "face_names.pickle"

    detectorFace = cv2.CascadeClassifier(str(ROOT_DIR / "models" / "haarcascade_frontalface_default.xml"))
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()
    reconhecedor.read(str(ROOT_DIR / "models" / "lbph_classifier.yml"))
    largura, altura = 220, 220
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)


    def carregar_funcionarios():
        if not DATA_PATH.exists():
            return {}

        with DATA_PATH.open(encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        funcionarios = dados.get("funcionarios", [])
        # retorna mapa id -> dict completo do funcionário
        return {str(funcionario.get("id")): funcionario for funcionario in funcionarios}


    def carregar_mapa_rotulos():
        if not FACE_NAMES_PATH.exists():
            return {}

        with FACE_NAMES_PATH.open("rb") as arquivo:
            face_names = pickle.load(arquivo)

        return {valor: chave for chave, valor in face_names.items()}


    funcionarios_por_id = carregar_funcionarios()
    rotulos_por_id = carregar_mapa_rotulos()

    frames = 0

    while True:
        conectado, imagem = camera.read()
        if not conectado:
            break

        frames += 1
        if max_frames is not None and frames > max_frames:
            break

        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(30,30))
        for (x, y, l, a) in facesDetectadas:
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)
            id_rotulo, confianca = reconhecedor.predict(imagemFace)
            id_funcionario = rotulos_por_id.get(id_rotulo)
            funcionario = funcionarios_por_id.get(id_funcionario)
            nome = funcionario.get("name", "Desconhecido") if funcionario else "Desconhecido"
            cv2.putText(imagem, nome, (x,y +(a+30)), font, 2, (0,0,255))
            cv2.putText(imagem, str(confianca), (x,y + (a+50)), font, 1, (0,0,255))

            # LBPH: menor valor de 'confianca' significa melhor correspondencia
            try:
                conf_val = float(confianca)
            except Exception:
                conf_val = None

            if funcionario and conf_val is not None and conf_val <= conf_threshold:
                camera.release()
                cv2.destroyAllWindows()
                # retornar o registro completo do funcionário e a confiança
                return {**funcionario, "_confidence": conf_val}

        cv2.imshow("Face", imagem)
        key = cv2.waitKey(1)
        if key == ord('q') or cv2.getWindowProperty("Face", cv2.WND_PROP_VISIBLE) < 1:
            break

    camera.release()
    cv2.destroyAllWindows()