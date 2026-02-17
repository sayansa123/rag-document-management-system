from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.chat import ChatSession, ChatMessage
from app.models.user import User
from app.schemas.chat import ChatMessageCreate
from app.rag.retrieval import retrieve_answer


# ============================================
# CREATE CHAT SESSION
# ============================================
def create_chat_session_helper(user: User, db: Session):
    chat_session = ChatSession(user_id=user.id)
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    return chat_session


# ============================================
# SEND CHAT MESSAGE FROM CHAT SESSION
# ============================================
def get_user_access_levels(user: User):
    if user.role == 0:
        return [0, 1, 2]  # admins can question answer from admin documents, staff documents and public documents
    if user.role == 1:
        return [1, 2]    # staffs can question answer from staff documents and public documents
    if user.role == 2:
        return [2]      # Users can question answer from public documents


def send_chat_message_helper(session_id, message: ChatMessageCreate, db: Session, current_user):
    # Verify Session Exists and belongs to user
    chat_session = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id).first()
    if not chat_session:
        raise HTTPException(status_code=404, detail='Chat session Not found or User not found')
    
    # Validate Question -> Already validated from schemas
    question = message.content.strip()
    
    # Save the user query
    user_message = ChatMessage(session_id=session_id, role=0, context=question)
    # save user message to database
    db.add(user_message)
    db.commit()

    # get allowed document access levels based on user role
    allowed_levels = get_user_access_levels(current_user)
    
    # retrieve answer using RAG
    try:
        answer = retrieve_answer(question, allowed_levels)
    except Exception as e:
        answer = f'Sorry I got an error: {str(e)}'

    # save the AI response
    ai_message = ChatMessage(session_id=session_id, role=1, context=answer)

    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    
    return ai_message


# ============================================
# GET USER'S CHAT SESSIONS
# ============================================
def get_chat_sessions_helper(user_id: int, db: Session, current_user: User):
    # Admin put a user_id
    if user_id is not None:
        if current_user.role != 0:
            raise HTTPException(status_code=403, detail="Only admin can view other users' chat session")
        target_user_id = user_id
    # default to current users' session
    else:
        target_user_id = current_user.id
    
    sessions = db.query(ChatSession).filter(ChatSession.user_id == target_user_id).order_by(ChatSession.created_at.desc()).all()
    return sessions


# ============================================
# GET CHAT HISTORY
# ============================================
def get_chat_history_helper(session_id: int, db: Session, current_user: User):
    # get that chat session
    chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not chat_session:
        raise HTTPException(status_code=404, detail='Chat Session Not found')
    
    # check access permission
    if current_user.role == 0:      # admin can see all chat messages
        pass
    else:
        if chat_session.user_id != current_user.id:
            raise HTTPException(status_code=403, detail='You can view only your chat history')
    
    # get messages
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
    return messages


# ============================================
# DELETE CHAT SESSION
# ============================================
def delete_chat_session_helper(session_id: int, db: Session, current_user: User):
    # Verify session exists
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Check permissions [not admin but want to delete others session]
    if current_user.role != 0 and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own chat sessions")
    
    # Delete all messages in the session
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    
    # Delete the session
    db.delete(session)
    db.commit()
    
    return {"message": f"Chat session {session_id} deleted successfully"}


# ============================================
# GET ALL USERS' SESSIONS (ADMIN ONLY)
# ============================================
def get_all_sessions_helper(db: Session, current_user: User):
    # Only for admin
    if current_user.role != 0:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    
    # Get all users with their sessions
    users = db.query(User).filter(User.is_deleted == False).all()
    
    result = []
    for user in users:
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == user.id
        ).order_by(
            ChatSession.created_at.desc()
        ).all()
        
        result.append({
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "session_count": len(sessions),
            "sessions": [
                {
                    "id": s.id,
                    "created_at": s.created_at,
                    "message_count": db.query(ChatMessage).filter(
                        ChatMessage.session_id == s.id
                    ).count()
                }
                for s in sessions
            ]
        })
    
    return result
