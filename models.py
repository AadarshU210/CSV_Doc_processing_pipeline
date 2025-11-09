from db import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import JSON

class Files(Base):
    __tablename__ = "Files"

    file_id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    status = Column(String)
    result = Column(JSON, nullable = True)

