from fastapi import HTTPException

note_exception = HTTPException(
  status_code=404,
  detail="Not found"
)

user_id_exception = HTTPException(
  status_code=401,
  detail="Not authorized"
)