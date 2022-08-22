from sqlalchemy import Column, Integer, text, TEXT, TIMESTAMP
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy.orm import relationship

from . import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    description=Column(TEXT,nullable=True)
    status = Column(TEXT,nullable=True)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self) -> str:
        return "<Order(id='{}', created_on='{}')>".format(self.id, self.created_on)

class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True

    id = fields.Integer()
    description = fields.String()
    status = fields.String()
    created_on = fields.DateTime()
    modified_on = fields.DateTime()