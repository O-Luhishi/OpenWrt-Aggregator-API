from marshmallow import fields, Schema
from .DevicesModel import DeviceSchema
from . import db

import datetime


class RouterModel(db.Model):
    """
    Router Model
    """

    # Table Name
    __tablename__ = 'routers'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(128), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    devices = db.relationship('DeviceModel', backref='routers', lazy=True)

    # Class Constructor
    def __init__(self, data):
        """
        Class Constructor
        :param data:
        """
        self.ip_address = data.get('ip_address')
        self.status = data.get('status')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_routers():
        return RouterModel.query.all()

    @staticmethod
    def get_router_by_id(id):
        return RouterModel.query.filter_by(id=id).first()

    @staticmethod
    def get_router_by_ip(ip):
        return RouterModel.query.filter_by(ip_address=ip).first()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class RouterSchema(Schema):
    """
    Device Schema
    """
    id = fields.Int(dump_only=True)
    ip_address = fields.Str(required=True)
    status = fields.Bool(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    devices = fields.Nested(DeviceSchema, many=True)
