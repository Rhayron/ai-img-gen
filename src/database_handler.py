# src/database_handler.py

from tinydb import TinyDB, Query
from datetime import datetime, timezone

import os

# Constrói o caminho para o ficheiro da base de dados no diretório pai (ai-img-gen)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, '..', 'prompts.json')
db = TinyDB(DB_FILE, indent=4)
Prompt = Query()

def get_next_id():
    """Obtém o próximo ID de prompt auto-incrementado."""
    if not db.all():
        return 1
    max_id = max(doc['prompt_id'] for doc in db.all())
    return max_id + 1

def add_prompt(prompt_text: str):
    """
    Adiciona um novo prompt ao banco de dados com o estado 'pending'.

    Args:
        prompt_text (str): O texto do prompt a ser adicionado.

    Returns:
        int: O ID do documento inserido.
    """
    if not prompt_text:
        print("Erro: Tentativa de adicionar um prompt vazio.")
        return None
    
    doc_id = db.insert({
        'prompt_id': get_next_id(),
        'prompt_text': prompt_text,
        'status': 'pending',
        'created_at': datetime.now(timezone.utc).isoformat(),
        'completed_at': None
    })
    print(f"Prompt adicionado ao banco de dados com ID de documento: {doc_id}")
    return doc_id

def get_pending_prompt():
    """
    Recupera o primeiro prompt pendente do banco de dados.

    Returns:
        dict: O documento do prompt pendente, ou None se não houver nenhum.
    """
    pending_prompt = db.get(Prompt.status == 'pending')
    if pending_prompt:
        print(f"Prompt pendente encontrado com ID: {pending_prompt['prompt_id']}")
    else:
        print("Nenhum prompt pendente encontrado no banco de dados.")
    return pending_prompt

def mark_prompt_completed(prompt_doc_id: int):
    """
    Atualiza o estado de um prompt para 'completed' e define o carimbo de data/hora de conclusão.

    Args:
        prompt_doc_id (int): O ID do documento do prompt a ser atualizado.
    """
    db.update(
        {
            'status': 'completed',
            'completed_at': datetime.now(timezone.utc).isoformat()
        },
        doc_ids=[prompt_doc_id]
    )
    print(f"Prompt com ID de documento {prompt_doc_id} marcado como concluído.")