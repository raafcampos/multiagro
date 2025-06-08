import json
import os

# --- Configurações Globais ---
# Você pode mudar esta variável para "en_US" ou "es_ES" para testar outros idiomas.
CURRENT_LANGUAGE = "pt_BR"
DEFAULT_FALLBACK_LANGUAGE = "en_US" # Idioma de fallback caso uma tradução não seja encontrada

# Determina o diretório do script atual e constrói o caminho para a pasta de traduções
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSLATIONS_DIR = os.path.join(BASE_DIR, "translations")

# Dicionários para armazenar as traduções carregadas
loaded_translations = {}
fallback_translations_data = {} # Renomeado para clareza

def load_language_file(lang_code):
    """Carrega um arquivo de tradução JSON para um determinado código de idioma."""
    file_path = os.path.join(TRANSLATIONS_DIR, f"{lang_code}.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"AVISO: Arquivo de tradução não encontrado: {file_path}")
    except json.JSONDecodeError:
        print(f"AVISO: Erro ao decodificar o arquivo JSON: {file_path}")
    return {}

def initialize_translations(language_to_load):
    """Carrega as traduções para o idioma especificado e o idioma de fallback."""
    global loaded_translations, fallback_translations_data, CURRENT_LANGUAGE
    
    CURRENT_LANGUAGE = language_to_load
    loaded_translations = load_language_file(CURRENT_LANGUAGE)
    
    if CURRENT_LANGUAGE != DEFAULT_FALLBACK_LANGUAGE:
        fallback_translations_data = load_language_file(DEFAULT_FALLBACK_LANGUAGE)
    else:
        # Se o idioma atual já é o de fallback, os dados de fallback são os mesmos
        fallback_translations_data = loaded_translations

def get_localized_string(key, **kwargs):
    """
    Busca uma string traduzida para uma chave específica.
    Usa CURRENT_LANGUAGE e recorre a DEFAULT_FALLBACK_LANGUAGE se necessário.
    """
    message_template = loaded_translations.get(key)

    if message_template is None:
        # Tenta no idioma de fallback
        message_template = fallback_translations_data.get(key)
        if message_template:
            print(f"AVISO: Chave '{key}' não encontrada para o idioma '{CURRENT_LANGUAGE}'. Usando tradução de fallback '{DEFAULT_FALLBACK_LANGUAGE}'.")
        else:
            # Se ainda não encontrou em nenhum dos dois
            return f"[TRADUÇÃO AUSENTE: Chave '{key}' para idioma '{CURRENT_LANGUAGE}' e fallback '{DEFAULT_FALLBACK_LANGUAGE}']"

    # Formata a mensagem se argumentos forem passados
    try:
        return message_template.format(**kwargs)
    except KeyError as e:
        print(f"AVISO: Placeholder {{{e.args[0]}}} faltando para a chave '{key}' no idioma '{CURRENT_LANGUAGE}'.")
        return message_template # Retorna a string não formatada

# --- Simulação do fluxo do chatbot ---

def start_chat():
    """Inicia a interação do chatbot."""
    print(get_localized_string("greeting"))

    user_name_prompt = get_localized_string("ask_name")
    name = input(user_name_prompt + " ")

    print(get_localized_string("welcome_user", user_name=name))

    user_query_prompt_text = get_localized_string("user_query_prompt")
    query = input(user_query_prompt_text + " ")

    print(get_localized_string("generic_response"))
    # Aqui iria a lógica de processamento da 'query'

    print(get_localized_string("goodbye"))

if __name__ == "__main__":
    initialize_translations(CURRENT_LANGUAGE) # Carrega os arquivos de tradução na inicialização

    print(f"--- Chatbot iniciado no idioma: {CURRENT_LANGUAGE} ---")
    start_chat()

    # Exemplo de como você poderia mudar o idioma e testar:
    print(f"\n--- Mudando idioma para: {DEFAULT_FALLBACK_LANGUAGE} ---")
    initialize_translations(DEFAULT_FALLBACK_LANGUAGE) # Recarrega as traduções para o novo idioma
    start_chat()

    # Exemplo de uso com uma chave que não existe em um idioma específico
    print("\n--- Testando chave ausente (deve usar fallback) ---")
    initialize_translations("es_ES") # Espanhol
    # "detailed_error" existe em en_US.json (fallback) mas não em es_ES.json
    print(get_localized_string("detailed_error", error_code="XYZ123"))

    # Testando chave que não existe em lugar nenhum
    print("\n--- Testando chave totalmente ausente ---")
    print(get_localized_string("non_existent_key"))h