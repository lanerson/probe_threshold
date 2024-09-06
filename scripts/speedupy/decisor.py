from intpy import deterministic

from intpy import deterministic
from cache import load_cache

CACHE_FILE='cache.json'    

def verify(func, _args):
    args = str(_args)    
    threshold = 0.09
    try:
        with open('../probe_threshold/threshold.txt', 'r') as file:
            threshold = float(file.read())
    except FileNotFoundError as e:
        return True
    
    cache = load_cache()
    value = cache[func].get(args)
    value = value if value == None else float(value)
    if value == None or value > threshold:
        return True
    return False

def decorator(decorator=deterministic, active=False):
    def wrapper(func):
        def wrapped_func(*args, **kwargs):
            if verify(func.__name__, args):
                print(f"executando {func.__name__} com cache")
                # Aplica o decorador apenas na primeira chamada, se 'active' for True
                wrapped_func.decorated_func = decorator(func)
            else:
                print(f"executando {func.__name__} sem cache")
                # Usa a função original sem decorador
                wrapped_func.decorated_func = func

            # Chama a função correta
            return wrapped_func.decorated_func(*args, **kwargs)

        # Inicialmente, não temos uma função decorada
        wrapped_func.decorated_func = None
        return wrapped_func
    return wrapper
