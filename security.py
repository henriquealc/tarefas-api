import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
TOKEN_EXPIRA_MINUTOS = 30
ITERACOES = 600000


def gerar_hash(senha: str) -> str:
    salt = os.urandom(16)
    derivado = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES)
    return f"{ITERACOES}${salt.hex()}${derivado.hex()}"


def verificar_senha(senha: str, senha_hash: str) -> bool:
    iteracoes, salt_hex, hash_hex = senha_hash.split("$")
    derivado = hashlib.pbkdf2_hmac(
        "sha256", senha.encode(), bytes.fromhex(salt_hex), int(iteracoes)
    )
    return hmac.compare_digest(derivado.hex(), hash_hex)


def criar_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRA_MINUTOS)
    return jwt.encode({"sub": username, "exp": expira}, SECRET_KEY, algorithm=ALGORITHM)