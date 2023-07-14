from importlib import import_module


def import_symbol(module: str, symbol: str):
    """Helper func to get symbol (var, class, callable) 
    
    from a given module."""
    imported_module = import_module(name=module)
    return getattr(imported_module, symbol)
