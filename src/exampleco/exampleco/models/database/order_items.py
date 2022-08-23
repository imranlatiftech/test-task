from sqlalchemy import Column, Integer, text, TEXT, TIMESTAMP, ForeignKey
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy.orm import relationship

from . import Base

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    description=Column(TEXT,nullable=True)
    order_id=Column(Integer,ForeignKey('orders.id',ondelete='CASCADE'))
    service_id=Column(Integer,ForeignKey('services.id'))
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )


    def __repr__(self) -> str:
        return "<OrderItem(id='{}',order_id='{}',service_id='{}',created_on='{}')>".format(self.id,self.order_id,self.service_id,self.created_on)

class OrderItemSchema(SQLAlchemySchema):
    class Meta:
        model = OrderItem
        load_instance = True

    id = fields.Integer()
    description = fields.String()
    order_id = fields.Integer()
    service_id = fields.Integer()
    created_on = fields.DateTime()
    modified_on = fields.DateTime()