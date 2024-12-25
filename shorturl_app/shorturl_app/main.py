import string
import random
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from database import SessionLocal, Base, engine
from models import URLItem

Base.metadata.create_all(bind=engine)

app = FastAPI()

class URLCreate(BaseModel):
    url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.post("/shorten")
def shorten_url(request: Request, item: URLCreate, db: Session = Depends(get_db)):
    # Генерируем уникальный short_id
    for _ in range(10):
        short_id = generate_short_id()
        existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
        if not existing:
            new_item = URLItem(short_id=short_id, full_url=str(item.url))
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            if request.url.port == 80:
                server_address = request.url.hostname
            else:
                server_address = f"{request.url.hostname}:{request.url.port}"
            return {"short_url": f"{server_address}/{short_id}"}
    raise HTTPException(status_code=500, detail="Не удалось сгенерировать короткую ссылку")

@app.get("/{short_id}")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return RedirectResponse(url=url_item.full_url)

@app.get("/stats/{short_id}")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return {
        "short_id": url_item.short_id,
        "full_url": url_item.full_url
    }

