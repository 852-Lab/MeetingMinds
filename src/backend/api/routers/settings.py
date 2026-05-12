from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import Setting
from services.crypto import encrypt, decrypt

router = APIRouter(prefix="/api/settings", tags=["settings"])

OPENAI_KEY_SETTING = "openai_api_key"

class OpenAIKeyRequest(BaseModel):
    api_key: str

@router.get("/openai-key")
def get_openai_key_status(db: Session = Depends(get_db)):
    setting = db.query(Setting).filter(Setting.key == OPENAI_KEY_SETTING).first()
    return {"configured": setting is not None}

@router.post("/openai-key")
def save_openai_key(body: OpenAIKeyRequest, db: Session = Depends(get_db)):
    if not body.api_key.startswith("sk-"):
        raise HTTPException(status_code=400, detail="Invalid OpenAI API key format")
    encrypted = encrypt(body.api_key)
    setting = db.query(Setting).filter(Setting.key == OPENAI_KEY_SETTING).first()
    if setting:
        setting.value = encrypted
    else:
        setting = Setting(key=OPENAI_KEY_SETTING, value=encrypted)
        db.add(setting)
    db.commit()
    return {"status": "saved"}

@router.delete("/openai-key")
def delete_openai_key(db: Session = Depends(get_db)):
    db.query(Setting).filter(Setting.key == OPENAI_KEY_SETTING).delete()
    db.commit()
    return {"status": "deleted"}

def get_decrypted_openai_key(db: Session) -> str | None:
    setting = db.query(Setting).filter(Setting.key == OPENAI_KEY_SETTING).first()
    if not setting:
        return None
    return decrypt(setting.value)
