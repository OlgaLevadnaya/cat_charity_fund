from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import ExtendedBase


class Donation(ExtendedBase):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return f'Пожертвование {self.full_amount}'
