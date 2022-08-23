from sqlalchemy import Column, Float, Integer, String, text, TEXT, TIMESTAMP
from marshmallow import fields, ValidationError, Schema, post_load
from sqlalchemy.orm import validates
from marshmallow_sqlalchemy import SQLAlchemySchema

from . import Base


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(Float, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )
    @validates('name')
    def validate_name(self,key,value):
        assert value!='','Name cannot be empty'
        return value

    @validates('price')
    def validate_name(self, key, value):
        assert value > 0 , 'Price cannot be equal or less than 0'
        return value

    def __repr__(self) -> str:
        return "<Service(name='{}', price='{}')>".format(self.name, self.price)


class ServiceSchema(SQLAlchemySchema):
    class Meta:
        model = Service
        load_instance = True
    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String()
    price = fields.Float(required=True)
    created_on = fields.DateTime()
    modified_on = fields.DateTime()


