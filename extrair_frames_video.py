import cv2
import os

def extrair_frames(video_path, output_dir, frame_rate=30):
    """
    Extrai frames de um vídeo em um intervalo de 'frame_rate'.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Salva um frame a cada 'frame_rate' quadros
        if count % frame_rate == 0:
            frame_name = f"frame_{count}.jpg"
            cv2.imwrite(os.path.join(output_dir, frame_name), frame)

        count += 1

    cap.release()
    print(f"Frames extraídos para {output_dir}")

# Exemplo de uso
extrair_frames(
    video_path="/Users/alansms/PycharmProjects/DjangoProject-Fiap/MakeSenseLocal/video_treino/video_treino/IMG_2359.MOV",
    output_dir="/Users/alansms/PycharmProjects/DjangoProject-Fiap/MakeSenseLocal/imagens_raw",
    frame_rate=2  # Extrai um frame a cada 30 quadros
)