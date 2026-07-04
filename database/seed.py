import os
import uuid
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base, engine, SessionLocal, User, Document, Chunk, Conversation, Message

def seed_database():
    session = SessionLocal()
    try:
        # Clear existing data
        session.query(Message).delete()
        session.query(Conversation).delete()
        session.query(Chunk).delete()
        session.query(Document).delete()
        session.query(User).delete()

        # Seed Users
        user1 = User(
            id=str(uuid.uuid4()),
            email="alice@example.com",
            password_hash="hashed_password_1",
            role="admin",
            created_at=datetime.utcnow()
        )
        user2 = User(
            id=str(uuid.uuid4()),
            email="bob@example.com",
            password_hash="hashed_password_2",
            role="member",
            created_at=datetime.utcnow()
        )

        session.add_all([user1, user2])
        session.commit()

        # Seed Documents
        document1 = Document(
            id=str(uuid.uuid4()),
            user_id=user1.id,
            filename="example.pdf",
            status="processed",
            chunk_count=5,
            created_at=datetime.utcnow()
        )
        document2 = Document(
            id=str(uuid.uuid4()),
            user_id=user2.id,
            filename="example2.docx",
            status="pending",
            chunk_count=0,
            created_at=datetime.utcnow()
        )

        session.add_all([document1, document2])
        session.commit()

        # Seed Chunks
        chunk1 = Chunk(
            id=str(uuid.uuid4()),
            document_id=document1.id,
            content="This is chunk 1 content.",
            chunk_index=0,
            embedding=[0.1] * 768
        )
        chunk2 = Chunk(
            id=str(uuid.uuid4()),
            document_id=document1.id,
            content="This is chunk 2 content.",
            chunk_index=1,
            embedding=[0.2] * 768
        )

        session.add_all([chunk1, chunk2])
        session.commit()

        # Seed Conversations
        conversation1 = Conversation(
            id=str(uuid.uuid4()),
            user_id=user1.id,
            title="First Conversation",
            created_at=datetime.utcnow()
        )
        conversation2 = Conversation(
            id=str(uuid.uuid4()),
            user_id=user2.id,
            title="Second Conversation",
            created_at=datetime.utcnow()
        )

        session.add_all([conversation1, conversation2])
        session.commit()

        # Seed Messages
        message1 = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation1.id,
            role="user",
            content="What is this document about?",
            sources=None,
            created_at=datetime.utcnow()
        )
        message2 = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation1.id,
            role="assistant",
            content="This document is about AI.",
            sources={"chunks": [chunk1.id]},
            created_at=datetime.utcnow()
        )

        session.add_all([message1, message2])
        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()