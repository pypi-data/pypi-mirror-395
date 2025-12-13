import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlmodel import Field, Session, SQLModel, create_engine, select

from dragonglass.core.config import settings
from dragonglass.core.models import Message as PydanticMessage
from dragonglass.core.models import Role, ContentPart


class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    title: str
    created_at: str
    updated_at: str
    model_config_json: str = Field(default="{}", alias="model_config")


class MessageRow(SQLModel, table=True):
    __tablename__ = "messages"
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str
    content_json: str
    created_at: str


class Database:
    """
    Manages SQLite storage using SQLModel (Pydantic + SQLAlchemy).
    Strictly handles relational data (Chat History).
    """

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or (settings.data_dir / "dg.db")
        # specific url for sqlite
        sqlite_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(sqlite_url)
        self._init_schema()

    def _init_schema(self):
        """Creates tables if they don't exist."""
        SQLModel.metadata.create_all(self.engine)

    def create_conversation(
        self, title: str | None = None, model_config: Dict[str, Any] | None = None
    ) -> str:
        """Creates a new conversation entry."""
        now = datetime.now(timezone.utc).isoformat()
        title = title or "New Chat"

        conv = Conversation(
            title=title,
            created_at=now,
            updated_at=now,
            model_config_json=json.dumps(model_config or {}),
        )

        with Session(self.engine) as session:
            session.add(conv)
            session.commit()
            session.refresh(conv)
            return conv.id

    def add_message(self, conversation_id: str, message: PydanticMessage):
        """Saves a message to the history."""
        # Convert Pydantic content parts to JSON string for storage
        content_json = json.dumps([part.model_dump() for part in message.parts])
        timestamp = message.timestamp.isoformat()

        row = MessageRow(
            conversation_id=conversation_id,
            role=message.role.value,
            content_json=content_json,
            created_at=timestamp,
        )

        with Session(self.engine) as session:
            session.add(row)

            # Update parent conversation timestamp
            statement = select(Conversation).where(Conversation.id == conversation_id)
            conv = session.exec(statement).first()
            if conv:
                conv.updated_at = timestamp
                session.add(conv)

            session.commit()

    def get_conversation_history(self, conversation_id: str) -> List[PydanticMessage]:
        """Retrieves full message history for LLM context."""
        messages = []

        with Session(self.engine) as session:
            statement = (
                select(MessageRow)
                .where(MessageRow.conversation_id == conversation_id)
                .order_by(MessageRow.created_at)
            )
            rows = session.exec(statement).all()

            for row in rows:
                try:
                    parts_data = json.loads(row.content_json)
                    parts = [ContentPart(**p) for p in parts_data]

                    messages.append(
                        PydanticMessage(
                            role=Role(row.role),
                            parts=parts,
                            timestamp=datetime.fromisoformat(row.created_at),
                        )
                    )
                except Exception:
                    continue

        return messages

    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns list of recent conversations for the generic log."""
        with Session(self.engine) as session:
            statement = (
                select(Conversation)
                .order_by(Conversation.updated_at.desc())
                .limit(limit)
            )
            # type: ignore
            results = session.exec(statement).all()
            return [c.model_dump() for c in results]

            # Global singleton


db = Database()
