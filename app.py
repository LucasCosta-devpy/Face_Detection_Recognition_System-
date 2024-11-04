import threading
import cv2
import os
from deepface import DeepFace
from flask import Flask, Response, render_template, send_from_directory, jsonify

app = Flask(__name__)

# Variáveis globais
face_match = False
reference_img_path = "pessoa.jpg"  # Imagem de referência para comparação
reference_img = cv2.imread(reference_img_path)
attempts = 0  # Contador de tentativas
max_attempts = 2  # Número máximo de tentativas
camera_active = False  # Estado da câmera
matched_image_path = ""  # Caminho da imagem da pessoa encontrada
captured_image_path = ""  # Caminho da imagem capturada

# Lock para gerenciar o acesso à variável face_match entre threads
lock = threading.Lock()

def check_face(captured_img):
    global face_match, matched_image_path, captured_image_path
    try:
        # Verifica se a face capturada corresponde à imagem de referência
        verification_result = DeepFace.verify(captured_img, reference_img.copy())
        with lock:
            face_match = verification_result['verified']
            if face_match:
                matched_image_path = f"images/matched_face_{attempts + 1}.jpg"
                cv2.imwrite(matched_image_path, captured_img)  # Salvar imagem da pessoa encontrada
                print(f"Imagem da correspondência salva em: {matched_image_path}") 
                captured_image_path = f"images/captured_face_{attempts + 1}.jpg"
                cv2.imwrite(captured_image_path, captured_img)  # Salvar a imagem capturada
                print(f"Imagem capturada salva em: {captured_image_path}")
            else:
                print("Sem correspondência.")

    except Exception as e:
        with lock:
            face_match = False
        print(f"Erro na verificação: {e}")

def gerar_frames():
    global attempts, camera_active
    cap = cv2.VideoCapture(0)  # Usar a câmera interna
    if not cap.isOpened():
        print("Falha ao abrir a câmera.")
        return

    while camera_active:
        success, frame = cap.read()
        if not success:
            break

        # Corrigir a inversão da imagem (horizontalmente)
        frame = cv2.flip(frame, 1)

        # Converter o frame para escala de cinza
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        # Se uma face for detectada
        if len(faces) > 0 and attempts < max_attempts:
            (x, y, w, h) = faces[0]  # Considerar a primeira face detectada
            detected_face = frame[y:y+h, x:x+w]  # Capturar a face detectada
            captured_image_path = f"images/captured_face_{attempts + 1}.jpg"
            cv2.imwrite(captured_image_path, detected_face)  # Salvar a imagem capturada

            # Iniciar a verificação da face em uma nova thread
            threading.Thread(target=check_face, args=(detected_face.copy(),)).start()
            
            # Desenhar um retângulo azul ao redor da face detectada
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Humano", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Desenhar o retângulo azul em todas as faces detectadas, independentemente da correspondência
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Humano", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)  # Legenda sempre visível

        # Verifique se houve um match
        with lock:
            if face_match:
                print("Correspondência encontrada!")
            else:
                print("Tentativa: ", attempts + 1)
                if attempts >= max_attempts:
                    print("Número máximo de tentativas alcançado.")
                attempts += 1

        # Codifique o frame em JPEG para enviar para o navegador
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera')
def start_camera():
    global camera_active, attempts, face_match, matched_image_path
    camera_active = True
    attempts = 0
    face_match = False
    matched_image_path = ""  # Limpar o caminho da imagem ao reiniciar
    threading.Thread(target=gerar_frames).start()
    return "Câmera ativada!"

@app.route('/video_feed')
def video_feed():
    return Response(gerar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/images/<path:filename>')
def send_image(filename):
    return send_from_directory('images', filename)

@app.route('/status')
def status():
    global face_match, matched_image_path, captured_image_path
    with lock:
        return jsonify({
            "match": face_match, 
            "matched_image": f"/images/{os.path.basename(matched_image_path)}" if matched_image_path else "",
            "captured_image": f"/images/{os.path.basename(captured_image_path)}" if captured_image_path else ""
        })

if __name__ == "__main__":
    # Criar pasta para salvar as imagens se não existir
    os.makedirs('images', exist_ok=True)
    app.run(host='0.0.0.0', port=8080)
