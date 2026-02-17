from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.core.security import create_access_token


# ============================================
# REGISTRATION -> PUBLIC USER
# ============================================
def register_user(user, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = User(email=user.email, password=user.password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ============================================
# LOGIN -> ALL ROLES
# ============================================
def login_user(user, db: Session):
    existing_user = db.query(User).filter(User.email == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail='Invalid email')
    if existing_user.is_deleted:
        raise HTTPException(status_code=403, detail='Account has been deactivated')
    if not user.password == existing_user.password:
        raise HTTPException(status_code=401, detail='Invalid Password')
    
    token_data = {
        'user_id': existing_user.id,
        'email': existing_user.email,
        'role': existing_user.role
    }
    token = create_access_token(data=token_data)

    return {
        'access_token': token,
        'token_type': 'bearer'
    }




