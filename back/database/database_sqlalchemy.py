from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from contextlib import contextmanager

# Définir la base pour les modèles ORM
Base = declarative_base()

# Modèles SQLAlchemy

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(1024), nullable=False)
    
    histories = relationship("HistoryDB", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class HistoryDB(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    
    user = relationship("UserDB", back_populates="histories")
    messages = relationship("MessageDB", back_populates="history", cascade="all, delete-orphan", order_by="MessageDB.id")

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, name='{self.name}')>"


class MessageDB(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey("history.id"), nullable=False)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relation
    history = relationship("HistoryDB", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', history_id={self.history_id})>"


# Configuration de la base de données
DATABASE_URL = "sqlite:///database/database_sqlalchemy.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Créer les tables
Base.metadata.create_all(bind=engine)


# Context manager pour la session
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Fonctions pour la table Users

def getUsers():
    """Récupère tous les utilisateurs"""
    with get_db() as db:
        users = db.query(UserDB).all()
        return [{"id": u.id, "email": u.email} for u in users]


def getUserById(id: int):
    """Récupère un utilisateur par son ID"""
    with get_db() as db:
        user = db.query(UserDB).filter(UserDB.id == id).first()
        if user:
            return {"id": user.id, "email": user.email}
        return None


def getUserByEmail(email: str):
    """Récupère un utilisateur par son email"""
    with get_db() as db:
        user = db.query(UserDB).filter(UserDB.email == email).first()
        if user:
            return {"id": user.id, "email": user.email}
        return None


def insertUser(user):
    """Insère un nouvel utilisateur"""
    with get_db() as db:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
        if existing_user:
            return {"id": existing_user.id, "email": existing_user.email}
        
        # Créer le nouvel utilisateur
        new_user = UserDB(
            email=user.email,
            hashed_password=user.hashed_password
        )
        db.add(new_user)
        db.flush()  # Pour obtenir l'ID
        return {"id": new_user.id, "email": new_user.email}


def deleteUserByid(id: int):
    """Supprime un utilisateur par son ID"""
    with get_db() as db:
        user = db.query(UserDB).filter(UserDB.id == id).first()
        if user:
            db.delete(user)
            return True
        return False


def deleteUserByEmail(email: str):
    """Supprime un utilisateur par son email"""
    with get_db() as db:
        user = db.query(UserDB).filter(UserDB.email == email).first()
        if user:
            db.delete(user)
            return True
        return False


# Fonctions pour la table History

def getHistory():
    """Récupère tout l'historique"""
    with get_db() as db:
        histories = db.query(HistoryDB).all()
        return [_history_to_dict(h) for h in histories]


def getHistoryById(id: int):
    """Récupère un historique par son ID"""
    with get_db() as db:
        history = db.query(HistoryDB).filter(HistoryDB.id == id).first()
        if history:
            return _history_to_dict(history)
        return None


def getHistoryByUserId(user_id: int):
    """Récupère tous les historiques d'un utilisateur"""
    with get_db() as db:
        histories = db.query(HistoryDB).filter(HistoryDB.user_id == user_id).all()
        return [_history_to_dict(h) for h in histories]


def insertHistory(history_item):
    """Insère un nouvel historique"""
    with get_db() as db:
        # Créer l'historique
        new_history = HistoryDB(
            user_id=history_item.user_id,
            name=history_item.name
        )
        db.add(new_history)
        db.flush()
        
        # Ajouter les messages s'il y en a
        if history_item.messages:
            for msg in history_item.messages:
                new_message = MessageDB(
                    history_id=new_history.id,
                    role=msg.role,
                    content=msg.content,
                    timestamp=msg.timestamp if hasattr(msg, 'timestamp') else datetime.utcnow()
                )
                db.add(new_message)
        
        db.flush()
        return new_history.id


def addMessageToHistory(history_id: int, message):
    """Ajoute un message à un historique"""
    with get_db() as db:
        history = db.query(HistoryDB).filter(HistoryDB.id == history_id).first()
        if history is None:
            return None
        
        # Créer le message
        message_dict = message.dict() if hasattr(message, 'dict') else message
        new_message = MessageDB(
            history_id=history_id,
            role=message_dict["role"],
            content=message_dict["content"],
            timestamp=message_dict.get("timestamp", datetime.utcnow())
        )
        db.add(new_message)
        db.flush()
        
        return _history_to_dict(history)


def deleteById(id: int):
    """Supprime un historique par son ID"""
    with get_db() as db:
        history = db.query(HistoryDB).filter(HistoryDB.id == id).first()
        if history:
            db.delete(history)
            return True
        return False


def cleanDatabase():
    """Supprime les historiques sans messages"""
    with get_db() as db:
        histories = db.query(HistoryDB).all()
        deleted_count = 0
        for history in histories:
            if len(history.messages) == 0:
                db.delete(history)
                deleted_count += 1
        return deleted_count


# Fonctions utilitaires

def _history_to_dict(history: HistoryDB):
    """Convertit un objet HistoryDB en dictionnaire"""
    return {
        "id": history.id,
        "user_id": history.user_id,
        "name": history.name,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat() if isinstance(msg.timestamp, datetime) else msg.timestamp
            }
            for msg in history.messages
        ]
    }
