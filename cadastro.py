import os, json, atexit

# Exportando funções de acesso
__all__ = []

# Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")
_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "cadastros.json")

# [
#     {
#         "login": str,
#         "senha": str,
#         "id": int,
#         "tipo_acesso": str
#     },
#     ...
# ]
_cadastros: list[dict] = []

# Funções internas
def _read_cadastros() -> None:
    global _cadastros

    if not os.path.exists(_JSON_FILE_PATH):
        _write_cadastros()
        return

    try:
        with open(_JSON_FILE_PATH, 'r') as file:
            _cadastros = json.load(file)
    except Exception as e:
        print(f"Erro de I/O em _read_cadastros: {e}")

def _write_cadastros() -> None:
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    try:
        with open(_JSON_FILE_PATH, 'w') as file:
            json.dump(_cadastros, file, indent=2)
    except Exception as e:
        print(f"Erro de I/O em _write_cadastros: {e}")

# Funções de acesso
# TODO

# Setup
# Popula lista
_read_cadastros()

# Salva lista ao final da execução
atexit.register(_write_cadastros)
