import os
import random
import shutil

# Definição das pastas e caminhos
BASE_DIR = "/Users/alansms/PycharmProjects/DjangoProject-Fiap/MakeSenseLocal"
IMAGENS_RAW = os.path.join(BASE_DIR, "imagens_raw")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_DIR = os.path.join(DATASET_DIR, "labels")

IMAGES_TRAIN = os.path.join(IMAGES_DIR, "train")
IMAGES_VAL = os.path.join(IMAGES_DIR, "val")
LABELS_TRAIN = os.path.join(LABELS_DIR, "train")
LABELS_VAL = os.path.join(LABELS_DIR, "val")

# Função para criar as pastas necessárias
def criar_estrutura():
    pastas = [IMAGES_TRAIN, IMAGES_VAL, LABELS_TRAIN, LABELS_VAL]
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
    print("Estrutura de pastas criada com sucesso.")

# Função para dividir as imagens em treino e validação (80% treino, 20% validação)
def dividir_imagens():
    imagens = [img for img in os.listdir(IMAGENS_RAW) if img.lower().endswith(('.jpg', '.png'))]
    random.shuffle(imagens)

    limite = int(0.8 * len(imagens))
    treino = imagens[:limite]
    validacao = imagens[limite:]

    for img in treino:
        shutil.copy(os.path.join(IMAGENS_RAW, img), IMAGES_TRAIN)
        criar_label_placeholder(img, LABELS_TRAIN)

    for img in validacao:
        shutil.copy(os.path.join(IMAGENS_RAW, img), IMAGES_VAL)
        criar_label_placeholder(img, LABELS_VAL)

    print("Imagens divididas entre treino e validação.")

# Função para criar placeholders de labels, se não existirem
def criar_label_placeholder(img, destino_labels):
    nome_txt = os.path.splitext(img)[0] + ".txt"
    caminho_label = os.path.join(destino_labels, nome_txt)

    if not os.path.exists(caminho_label):
        with open(caminho_label, 'w') as f:
            f.write("0 0.5 0.5 0.2 0.2\n")  # Exemplo de label

# Função para criar o arquivo data.yaml necessário para o YOLO
def criar_data_yaml():
    data_content = f"""
train: {IMAGES_TRAIN}
val: {IMAGES_VAL}

nc: 1  # Número de classes
names: ['classe0']  # Nome das classes
"""
    with open(os.path.join(BASE_DIR, "data.yaml"), 'w') as f:
        f.write(data_content)
    print("Arquivo data.yaml criado com sucesso.")

# Função para criar o script de treinamento do YOLO
def criar_script_treinamento():
    script_content = f"""
from ultralytics import YOLO

# Carregar o modelo pré-treinado YOLOv8
model = YOLO('yolov8n.pt')

# Treinar o modelo com os dados
model.train(O 
    data='{os.path.join(BASE_DIR, "data.yaml")}',
    epochs=50,
    batch=8,
    imgsz=640,
    name='treino_modelo',
    project='{os.path.join(BASE_DIR, "runs/detect")}',
)
"""
    with open(os.path.join(BASE_DIR, "train_yolo.py"), 'w') as f:
        f.write(script_content)
    print("Script de treinamento criado com sucesso.")

# Função principal para executar todas as etapas
def main():
    criar_estrutura()
    dividir_imagens()
    criar_data_yaml()
    criar_script_treinamento()
    print("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()