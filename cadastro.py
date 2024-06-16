import os, json, atexit, copy

# Exportando funções de acesso
__all__ = ["add_cadastro", "del_cadastro", "get_cadastro_by_login", "get_cadastro_by_id_e_tipo", "login", "is_aluno", "is_professor", "is_admin"]

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
def add_cadastro(login: str, senha: str, id_usuario: int, acesso: str) -> tuple[int, None]:
    """
    Cadastra um novo usuário no sistema

    Tipos de acesso: aluno, professor, admin
    """
    if acesso not in ("aluno", "professor", "admin"):
        # Tipo de usuário inválido
        return 45, None
    
    for cadastro in _cadastros:
        if cadastro["login"] == login:
            # Login já existe
            return 46, None
        elif cadastro["id"] == id_usuario and cadastro["tipo_acesso"] == acesso:
            # ID já existe para esse tipo de usuário
            return 47, None
    
    novo_cadastro = {
        "login": login,
        "senha": senha,
        "id": id_usuario if acesso != "admin" else -1, # admin é único e possui ID -1
        "tipo_acesso": acesso
    }
    _cadastros.append(novo_cadastro)

    return 0, None

def del_cadastro(login: str) -> tuple[int, None]:
    """
    Remove um usuário do sistema pelo seu login
    """
    for i, cadastro in enumerate(_cadastros):
        if cadastro["login"] == login and cadastro["tipo_acesso"] != "admin":
            del _cadastros[i]
            return 0, None

    # Login não encontrado
    return 49, None

def get_cadastro_by_login(login: str) -> tuple[int, dict]:
    """
    Retorna o cadastro de um usuário pelo seu login
    """
    for cadastro in _cadastros:
        if cadastro["login"] == login:
            return 0, copy.deepcopy(cadastro)

    # Login não encontrado
    return 49, None # type: ignore

def get_cadastro_by_id_e_tipo(id_usuario: int, acesso: str) -> tuple[int, dict]:
    """
    Retorna o cadastro de um usuário pelo seu ID e tipo de acesso
    """
    for cadastro in _cadastros:
        if cadastro["id"] == id_usuario and cadastro["tipo_acesso"] == acesso:
            return 0, copy.deepcopy(cadastro)

    # ID + tipo de aceso não encontrado
    return 48, None # type: ignore

def login(login: str, senha: str) -> tuple[int, int]:
    """
    Verifica o login de um usuário
    
    Retorna o ID do usuário (-1 se for admin), ou None + erro se não encontrado
    """
    for cadastro in _cadastros:
        if cadastro["login"] == login:
            if cadastro["senha"] == senha:
                # Login bem sucedido
                return 0, cadastro["id"]
            else:
                # Senha incorreta
                return 50, None # type: ignore
    
    # Login não encontrado
    return 49, None # type: ignore

def is_aluno(login: str) -> tuple[int, bool]:
    """
    Retorna se o usuário é um aluno
    """
    for cadastro in _cadastros:
        if cadastro["login"] == login:
            return 0, cadastro["tipo_acesso"] == "aluno"

    # Login não encontrado
    return 49, None # type: ignore

def is_professor(login: str) -> tuple[int, bool]:
    """
    Retorna se o usuário é um professor
    """
    for cadastro in _cadastros:
        if cadastro["login"] == login:
            return 0, cadastro["tipo_acesso"] == "professor"

    # Login não encontrado
    return 49, None # type: ignore

def is_admin(login: str) -> tuple[int, bool]:
    """
    Retorna se o usuário é um admin
    """
    for cadastro in _cadastros:
        if cadastro["login"] == login:
            return 0, cadastro["tipo_acesso"] == "admin"

    # Login não encontrado
    return 49, None # type: ignore

# Setup
# Popula lista
_read_cadastros()

# Salva lista ao final da execução
atexit.register(_write_cadastros)
