# src/main.py

import os
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro.env
# Isto deve ser feito antes de importar os nossos manipuladores
load_dotenv()

from gemini_handler import generate_creative_prompt
from database_handler import add_prompt, get_pending_prompt, mark_prompt_completed
# from fooocus_handler import generate_image_from_prompt # Comentado
from imagefx_handler import generate_image_with_imagefx # Adicionado

# --- Configuração ---
# Diretório para guardar as imagens geradas
# Constrói o caminho para o diretório de imagens no diretório pai (ai-img-gen)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', 'images')
# Número de novos prompts a gerar em cada execução
NUM_PROMPTS_TO_GENERATE = 5
# Número de imagens a gerar a partir de prompts pendentes em cada execução
NUM_IMAGES_TO_CREATE = 5

# Carrega o cookie de autenticação a partir das variáveis de ambiente
# Certifique-se de que tem um ficheiro .env na raiz do projeto com:
# GOOGLE_LABS_COOKIE="O_SEU_COOKIE_AQUI"
GOOGLE_LABS_COOKIE = os.getenv("GOOGLE_LABS_COOKIE")

def setup_directories():
    """Garante que o diretório de saída de imagens exista."""
    if not os.path.exists(IMAGE_OUTPUT_DIR):
        os.makedirs(IMAGE_OUTPUT_DIR)
        print(f"Diretório '{IMAGE_OUTPUT_DIR}' criado.")

def populate_prompts():
    """Gera novos prompts e adiciona-os ao banco de dados."""
    print("\n--- FASE 1: POPULAÇÃO DE PROMPTS ---")
    generated_count = 0
    for i in range(NUM_PROMPTS_TO_GENERATE):
        print(f"\nA tentar gerar prompt {i + 1}/{NUM_PROMPTS_TO_GENERATE}...")
        prompt_text = generate_creative_prompt()
        if prompt_text:
            add_prompt(prompt_text)
            generated_count += 1
    print(f"\nFase de população de prompts concluída. {generated_count} novos prompts adicionados.")

def process_pending_prompts():
    """Processa prompts pendentes para gerar imagens."""
    print("\n--- FASE 2: CRIAÇÃO DE IMAGENS ---")

    if not GOOGLE_LABS_COOKIE:
        print("\nERRO: A variável de ambiente GOOGLE_LABS_COOKIE não está definida.")
        print("Por favor, crie um ficheiro .env na raiz do projeto e adicione a seguinte linha:")
        print('GOOGLE_LABS_COOKIE="O_SEU_COOKIE_AQUI"')
        return

    processed_count = 0
    for i in range(NUM_IMAGES_TO_CREATE):
        print(f"\nA tentar processar imagem {i + 1}/{NUM_IMAGES_TO_CREATE}...")
        pending_prompt = get_pending_prompt()

        if not pending_prompt:
            print("Não há mais prompts pendentes para processar.")
            break

        prompt_text = pending_prompt['prompt_text']
        prompt_doc_id = pending_prompt.doc_id
        
        # Chama o novo handler para gerar a imagem com a imageFX-api
        generated_image_paths = generate_image_with_imagefx(prompt_text, GOOGLE_LABS_COOKIE)

        if generated_image_paths:
            # A imagem já foi guardada pelo handler.
            # Apenas marcamos o prompt como concluído.
            mark_prompt_completed(prompt_doc_id)
            processed_count += 1
            # Opcional: pode-se fazer algo com o caminho da imagem, como guardar no banco de dados.
            # Por agora, apenas imprimimos a confirmação que já é feita pelo handler.
        else:
            print(f"A geração de imagem falhou para o prompt: '{prompt_text}'")


    print(f"\nFase de criação de imagens concluída. {processed_count} novas imagens geradas.")

if __name__ == "__main__":
    print("Iniciando o Pipeline de Arte com IA...")
    setup_directories()
    populate_prompts()
    process_pending_prompts()
    print("\nPipeline concluído.")
