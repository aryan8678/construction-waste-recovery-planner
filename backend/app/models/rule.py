from sqlalchemy import Column, Integer, String, Text
from app.database.session import Base

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_id = Column(String(20), unique=True, nullable=False, index=True)
    material = Column(String(100), nullable=False, index=True)
    pathway = Column(String(100), nullable=False)
    priority = Column(Integer, nullable=False)
    conditions_description = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    applications = Column(Text, default="[]")
    alternatives = Column(Text, default="[]")
