# src/gemini_handler.py

import os
import time
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv

load_dotenv()
import os
import time
import json
import random
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv

load_dotenv()

# --- Configuração de Caminhos ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_PROMPTS_FILE = os.path.join(SCRIPT_DIR, '..', 'prompts_banco_imagens.json')
PROMPT_STATE_FILE = os.path.join(SCRIPT_DIR, '..', 'prompt_usage_state.json')

# --- Carregamento e Estado dos Prompts de Exemplo ---

def load_example_prompts():
    """Carrega os prompts de exemplo do arquivo JSON."""
    try:
        with open(EXAMPLE_PROMPTS_FILE, 'r', encoding='utf-8') as f:
            prompts = json.load(f)
            # Cria um dicionário para acesso rápido pelo id
            return {item['id']: item['prompt'] for item in prompts}
    except (IOError, json.JSONDecodeError) as e:
        print(f"Erro crítico: Não foi possível carregar o arquivo de prompts de exemplo '{EXAMPLE_PROMPTS_FILE}'. {e}")
        return None

EXAMPLE_PROMPTS = load_example_prompts()

def get_prompt_queue():
    """Obtém a fila de IDs de prompts não utilizados do arquivo de estado."""
    try:
        with open(PROMPT_STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
            return state.get('unused_prompt_ids', [])
    except (IOError, json.JSONDecodeError):
        # Se o arquivo não existe ou está corrompido, cria uma nova fila
        return []

def save_prompt_queue(queue):
    """Salva a fila de IDs de prompts no arquivo de estado."""
    with open(PROMPT_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'unused_prompt_ids': queue}, f, indent=4)

# --- Inicialização do Cliente Gemini ---

try:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    if not project_id or not location:
        raise ValueError("As variáveis de ambiente GOOGLE_CLOUD_PROJECT e GOOGLE_CLOUD_LOCATION devem ser definidas.")
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    print("Cliente Gemini inicializado com sucesso.")
except (ValueError, Exception) as e:
    print(f"Erro ao inicializar o cliente Gemini: {e}")
    model = None

def generate_creative_prompt(retries=3, delay=5):
    """
    Gera um prompt criativo usando um prompt de exemplo da fila.
    """
    if not model or not EXAMPLE_PROMPTS:
        print("Modelo Gemini ou prompts de exemplo não inicializados.")
        return None

    prompt_queue = get_prompt_queue()

    if not prompt_queue:
        print("Fila de prompts de exemplo vazia. Reiniciando e embaralhando...")
        prompt_queue = list(EXAMPLE_PROMPTS.keys())
        random.shuffle(prompt_queue)

    # Pega o próximo ID da fila
    example_prompt_id = prompt_queue.pop(0)
    example_prompt_text = EXAMPLE_PROMPTS.get(example_prompt_id, "um belo dia")

    # Salva o estado atualizado da fila
    save_prompt_queue(prompt_queue)

    system_instruction = (
        "You are a creative expert assistant for AI image generation. "
        "Your task is to create a new, unique, and highly descriptive prompt inspired by the user's example, but not a direct copy. "
        "Elaborate on the concept, adding details about the subject, setting, lighting, color palette, and artistic style. "
        "Produce only the new prompt text."
    )
    
    input_prompt = f"Create a new prompt inspired by this example: \n\n\"{example_prompt_text}\""

    for attempt in range(retries):
        try:
            print(f"A gerar novo prompt com Gemini, inspirado no exemplo ID: {example_prompt_id}...")
            response = model.generate_content(
                [system_instruction, input_prompt],
                generation_config={
                    "temperature": 0.9,
                    "max_output_tokens": 250
                }
            )
            if hasattr(response, 'text') and response.text:
                prompt_text = response.text.strip()
                print(f"Prompt gerado com sucesso: '{prompt_text[:70]}...'" )
                return prompt_text
            else:
                print(f"Nenhum texto gerado pela API Gemini. Motivo: {getattr(response, 'finish_reason', 'desconhecido')}")
                return None
        
        except (google_exceptions.ResourceExhausted, google_exceptions.ServiceUnavailable) as e:
            print(f"Erro recuperável: {e}. Tentativa {attempt + 1}/{retries}.")
            if attempt < retries - 1:
                time.sleep(delay)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return None

    print("Número máximo de tentativas atingido. A falhar.")
    return None
