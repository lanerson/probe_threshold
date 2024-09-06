import json
import os

CACHE_FILE = 'cache.json'
cache = {}
# Função para carregar cache
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

# Função para salvar cache
def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache,f,indent=4)

# Função para adicionar ao cache
def add_to_cache(_function_name, _input_data, _result):
    function_name = str(_function_name)
    input_data = str(_input_data)
    result = str(_result)
    cache = load_cache()

    if function_name not in cache:        
        cache[function_name] = {}
    
    cache[function_name][input_data] = result    
    save_cache(cache)


