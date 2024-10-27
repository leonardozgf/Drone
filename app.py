import os
import random
import shutil
from pathlib import Path

# Configurações de diretório a partir de variáveis de ambiente para flexibilidade
BASE_DIR = Path(os.getenv("BASE_DIR", "/Users/alansms/PycharmProjects/DjangoProject-Fiap/MakeSenseLocal"))
IMAGENS_RAW = BASE_DIR / "imagens_raw"
DATASET_DIR = BASE_DIR / "dataset"
IMAGES_DIR, LABELS_DIR = DATASET_DIR / "images", DATASET_DIR / "labels"
IMAGES_TRAIN, IMAGES_VAL = IMAGES_DIR / "train", IMAGES_DIR / "val"
LABELS_TRAIN, LABELS_VAL = LABELS_DIR / "train", LABELS_DIR / "val"

def criar_pasta(caminho):
    caminho.mkdir(parents=True, exist_ok=True)

def inicializar_estrutura():
    for pasta in [IMAGES_TRAIN, IMAGES_VAL, LABELS_TRAIN, LABELS_VAL]:
        criar_pasta(pasta)
    print("Estrutura de pastas criada.")

def separar_imagens(ratio_treino=0.8):
    imagens = [img for img in IMAGENS_RAW.iterdir() if img.suffix in ['.jpg', '.png']]
    random.shuffle(imagens)
    limite = int(len(imagens) * ratio_treino)
    
    for i, img in enumerate(imagens):
        destino_img = IMAGES_TRAIN if i < limite else IMAGES_VAL
        destino_label = LABELS_TRAIN if i < limite else LABELS_VAL
        shutil.copy(img, destino_img)
        gerar_label_placeholder(img.stem, destino_label)

    print("Divisão de imagens concluída.")

def gerar_label_placeholder(nome_imagem, destino_label):
    label_path = destino_label / f"{nome_imagem}.txt"
    if not label_path.exists():
        label_path.write_text("0 0.5 0.5 0.2 0.2\n")
        
def gerar_data_yaml():
    yaml_content = f"""
train: {IMAGES_TRAIN}
val: {IMAGES_VAL}

nc: 1
names: ['classe0']
"""
    (BASE_DIR / "data.yaml").write_text(yaml_content)
    print("Arquivo data.yaml criado.")

def criar_script_treinamento():
    script = f"""
from ultralytics import YOLO

modelo = YOLO('yolov8n.pt')
modelo.train(data='{BASE_DIR / "data.yaml"}', epochs=50, batch=8, imgsz=640, name='treino_modelo', project='{BASE_DIR / "runs/detect"}')
"""
    (BASE_DIR / "train_yolo.py").write_text(script)
    print("Script de treinamento criado.")

def main():
    inicializar_estrutura()
    separar_imagens()
    gerar_data_yaml()
    criar_script_treinamento()
    print("Processo completo!")

if __name__ == "__main__":
    main()
