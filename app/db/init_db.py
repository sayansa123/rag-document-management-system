from app.db.session import create_database_if_not_exists, engine, Base, Local_session
from app.core.config import INITIAL_ADMIN_EMAIL, INITIAL_ADMIN_PASSWORD, INITIAL_STAFF_EMAIL, INITIAL_STAFF_PASSWORD, INITIAL_USER_EMAIL, INITIAL_USER_PASSWORD
from sqlalchemy.orm import Session
from app.models.user import User


def prepare_database():
    """Create database and tables, insert default users"""
    # Create database if not exists
    create_database_if_not_exists()
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Note: Add your default user insertion logic here if needed
    seed_initial_users()





def seed_initial_users():
    db:Session = Local_session()

    try:
        # inserting the admin details initially
        admin = db.query(User).filter(User.email == INITIAL_ADMIN_EMAIL).first()
        if not admin:
            new_admin = User(email=INITIAL_ADMIN_EMAIL, password=INITIAL_ADMIN_PASSWORD, role=0, is_deleted=False)
            db.add(new_admin)

        # inserting the staff details initially
        staff = db.query(User).filter(User.email == INITIAL_STAFF_EMAIL).first()
        if not staff:
            new_staff = User(email=INITIAL_STAFF_EMAIL, password=INITIAL_STAFF_PASSWORD, role=1, is_deleted=False)
            db.add(new_staff)

        # inserting the end_email details initially
        user = db.query(User).filter(User.email == INITIAL_USER_EMAIL).first()
        if not user:
            new_user = User(email=INITIAL_USER_EMAIL, password=INITIAL_USER_PASSWORD, role=2, is_deleted=False)
            db.add(new_user)
        
        db.commit()

    finally:
        db.close()