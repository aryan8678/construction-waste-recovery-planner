from sqlalchemy import Column, Integer, String, Text
from app.database.session import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), default="Inert / Structural")
    description = Column(Text, nullable=False)
    typical_waste_source = Column(Text, nullable=False)
    reuse_potential = Column(String(50), nullable=False)
    recycling_potential = Column(String(50), nullable=False)
    common_applications = Column(Text, default="[]")
    important_considerations = Column(Text, nullable=False)
