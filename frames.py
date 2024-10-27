from pathlib import Path
import cv2

def salvar_frames(video_path, pasta_saida, taxa_frames=30, formato='jpg'):
    """
    Extrai frames de um vídeo a cada 'taxa_frames' quadros e salva no formato especificado.
    """
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir

    cap = cv2.VideoCapture(video_path)
    contador = 0

    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            break

        # Salva o frame a cada 'taxa_frames' quadros
        if contador % taxa_frames == 0:
            nome_frame = f"frame_{contador}.{formato}"
            caminho_frame = pasta_saida / nome_frame
            cv2.imwrite(str(caminho_frame), frame)

        contador += 1

    cap.release()
    print(f"Frames salvos na pasta {pasta_saida} com sucesso.")

# Exemplo de uso
salvar_frames(
    video_path="/Users/alansms/PycharmProjects/DjangoProject-Fiap/MakeSenseLocal/video_treino/video_treino/IMG_2359.MOV",
    pasta_saida="/Users/alansms/PycharmProjects/DjangoProject-Fiap/MakeSenseLocal/imagens_raw",
    taxa_frames=2,  # Extrai um frame a cada 30 quadros
    formato='png'    # Salva os frames no formato PNG
)
