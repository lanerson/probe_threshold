import inspect
import time
import sys

from functools import wraps

from parser_params import get_params
from environment import init_env
from logger.log import debug
from speedupy.cache import add_to_cache

g_argsp_m, g_argsp_M, g_argsp_s, g_argsp_no_cache, g_argsp_hash = get_params()

print(g_argsp_m)

print(g_argsp_no_cache)

print(g_argsp_hash)

if g_argsp_m == None and not g_argsp_no_cache:
    print("Error: enter the \"-h\" parameter on the command line after \"python script.py\" to see usage instructions")
    sys.exit()

if g_argsp_no_cache:
    #On the decorator "initialize_intpy", "user_script_path" is declared
    #to maintain compatibility
    def initialize_intpy(user_script_path):
        def decorator(f):
            def execution(*method_args, **method_kwargs):
                f(*method_args, **method_kwargs)
            return execution
        return decorator


    def deterministic(f):
        return f
else:
    init_env()
    from data_access import get_cache_data, create_entry, salvarNovosDadosBanco
    from function_graph import create_experiment_function_graph, get_source_code_executed

    g_user_script_graph = None

    def _initialize_cache(user_script_path):
        global g_user_script_graph
        g_user_script_graph = create_experiment_function_graph(user_script_path)

    def initialize_intpy(user_script_path):
        def decorator(f):
            def execution(*method_args, **method_kwargs):
                _initialize_cache(user_script_path)
                f(*method_args, **method_kwargs)
                if g_argsp_m != ['v01x']:
                    _salvarCache()
            return execution
        return decorator


    def deterministic(f):
        return _method_call(f) if _is_method(f) else _function_call(f)


    def _get_cache(func, args):        
        fun_source = get_source_code_executed(func, g_user_script_graph)
        return get_cache_data(func.__name__, args, fun_source, g_argsp_m)


    def _cache_exists(cache):
        return cache is not None


    def _cache_data(func, fun_args, fun_return, elapsed_time):
        debug("starting caching data for {0}({1})".format(func.__name__, fun_args))
        start = time.perf_counter()
        fun_source = get_source_code_executed(func, g_user_script_graph)
        create_entry(func.__name__, fun_args, fun_return, fun_source, g_argsp_m)
        end = time.perf_counter()
        debug("caching {0} took {1}".format(func.__name__, end - start))


    def _execute_func(f, self, *method_args, **method_kwargs):
        start = time.perf_counter()
        result_value = f(self, *method_args, **method_kwargs) if self is not None else f(*method_args, **method_kwargs)
        end = time.perf_counter()

        elapsed_time = end - start

        debug("{0} took {1} to run".format(f.__name__, elapsed_time))

        return result_value, elapsed_time


    def _method_call(f):
        @wraps(f)
        def wrapper(self, *method_args, **method_kwargs):
            debug("calling {0}".format(f.__name__))
            c = _get_cache(f, method_args)
            if not _cache_exists(c):

                debug("cache miss for {0}({1})".format(f.__name__, *method_args))
                return_value, elapsed_time = _execute_func(f, self, *method_args, **method_kwargs)
                _cache_data(f, method_args, return_value, elapsed_time)
                add_to_cache(f.__name__,method_args,elapsed_time) # Modificação para o decisor
                return return_value
            else:
                debug("cache hit for {0}({1})".format(f.__name__, *method_args))
                
                return c
        
        return wrapper


    def _function_call(f):
        @wraps(f)
        def wrapper(*method_args, **method_kwargs):
            debug("calling {0}".format(f.__name__))
            c = _get_cache(f, method_args)
            if not _cache_exists(c):
                debug("cache miss for {0}({1})".format(f.__name__, *method_args))
                return_value, elapsed_time = _execute_func(f, *method_args, **method_kwargs)
                _cache_data(f, method_args, return_value, elapsed_time)
                add_to_cache(f.__name__,method_args,elapsed_time) # Modificação para o decisor
                return return_value
            else:
                debug("cache hit for {0}({1})".format(f.__name__, *method_args))
                # print("será que ela que tamo buscando?", c, '\n')
                return c

        return wrapper


    # obs
    def _is_method(f):
        args = inspect.getfullargspec(f).args
        return bool(args and args[0] == 'self')


    def _salvarCache():
        salvarNovosDadosBanco(g_argsp_m)
