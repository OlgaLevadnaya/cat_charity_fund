from sqlalchemy import Column, String, Text

from app.core.db import ExtendedBase


class CharityProject(ExtendedBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'Проект {self.name.capitalize()}'
