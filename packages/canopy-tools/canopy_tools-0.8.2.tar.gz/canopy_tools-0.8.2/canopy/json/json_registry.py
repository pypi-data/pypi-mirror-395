json_function_registry = {}

def register_json(func):
    """
    Decorator to register a function in the json_function_registry.
    """
    key = func.__name__
    if key in json_function_registry:
        raise KeyError(f"Function {key} already registered.")
    else:
        json_function_registry[key] = func
    return func

def get_json_function(json_config):
    """
    Get the appropriate function from the registry based on the json_config.
    """
    function_name = f"{json_config['figure']}"
    if function_name in json_function_registry:
        return json_function_registry[function_name]
    else:
        raise ValueError(f"No registered function for {function_name}")

