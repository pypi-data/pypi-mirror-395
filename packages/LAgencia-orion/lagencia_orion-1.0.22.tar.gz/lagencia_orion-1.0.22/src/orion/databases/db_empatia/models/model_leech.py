from sqlalchemy import Column, DateTime, Integer, String

from databases.config_db_empatia import BaseEmpatia


class UpdateCodes(BaseEmpatia):
    __tablename__ = "update_codes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, nullable=False)
    status = Column(String(15), nullable=False)
    website = Column(String(10), nullable=False)
    date = Column(DateTime, nullable=False)
