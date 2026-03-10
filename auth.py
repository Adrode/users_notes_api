from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models

# JWT config
SECRET_KEY = "AD8Afkhas!mvj73KMVEW&ASD1@D631$#8ASsdaASD612J#1@9312ASDsada"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    # bez sekretu i algorytmu praktycznie nie da się złamać JWT, więc powinny być one ukryte w aplikacji

# hashowanie hasła
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# depenedency do wyciągania tokenu z headera Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
    # zapisuje token w formie stringa, jak go nie ma to błąd 401
    # tokenUrl służy do dokumentacji Swaggera (wskazuje endpoint pod którym uzyskuje się autoryzację); przez backend nie jest to wykorzystywane

# PASSWORD
# -------------------
def hash_password(password: str) -> str:
  return pwd_context.hash(password)
    # ta funkcja hashuje przekazane hasło

def verify_password(plain: str, hashed: str) -> bool:
  return pwd_context.verify(plain, hashed)
    # ta funkcja weryfikuje plain_password z hashem
# -------------------

# USERS
# -------------------
def get_user_by_email(db: Session, email: str):
  return db.query(models.User).where(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
  user = get_user_by_email(db, email)
  if not user or not verify_password(password, user.hashed_password):
    return None
  return user
    # jeśli nie ma takiego usera lub jeśli hasło się nie zgadza to None, w innym wypadku zwraca usera
    # ta funkcja jest używana do endpointu z logowaniem
# -------------------

# JWT
# -------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
  to_encode = data.copy() # data.copy() robi się, żeby nie modyfikować oryginalnych danych z data, czyli oryginalnego słownika przekazanego w argumencie funkcji
  expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # funkcja, która tworzy token; przyjmuje data, secret_key i algorytm
    #   w data znajduje się obiekt z właściwością "sub": {"sub": email}; u mnie znajduje się to w api/auth; zamiast email może być username, id, itp.
    #   oraz do date jest wrzucany również expire, czyli czas wygaśnięcia tokena; jak wyżej
    # ta funkcja używana jest przy logowaniu
# -------------------

# CURRENT USER
# -------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = get_user_by_email(db, email)
  if user is None:
    raise credentials_exception
  return user
# -------------------