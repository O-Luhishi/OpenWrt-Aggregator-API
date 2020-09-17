from marshmallow import fields, Schema
from .PortScanModel import PortScanSchema
from . import db

import datetime


class DeviceModel(db.Model):
    """
    Device Model
    """

    # Table Name
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    mac_address = db.Column(db.String(128), unique=True, nullable=False)
    ip_address = db.Column(db.String(128), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    portscan_results = db.relationship('PortScanModel', backref='devices', lazy=True)

    # Class Constructor
    def __init__(self, data):
        """
        Class Constructor
        :param data:
        """
        self.name = data.get('name')
        self.mac_address = data.get('mac_address')
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
    def get_all_devices():
        return DeviceModel.query.all()

    @staticmethod
    def get_device(id):
        return DeviceModel.query.get(id)

    @staticmethod
    def get_device_by_ip(ip):
        return DeviceModel.query.filter_by(ip_address=ip).first()

    @staticmethod
    def get_ip_address_by_device_id(id):
        return db.session.query(DeviceModel.ip_address).filter_by(id=id).first()

    @staticmethod
    def get_device_name_by_device_id(id):
        return db.session.query(DeviceModel.name).filter_by(id=id).first()

    @staticmethod
    def get_mac_address_by_id(id):
        return db.session.query(DeviceModel.mac_address).filter_by(id=id).first()

    @staticmethod
    def get_mac_address_by_ip(ip):
        return db.session.query(DeviceModel.mac_address).filter_by(ip_address=ip).first()

    def __repr__(self):
        return '{}'.format(self.id)


class DeviceSchema(Schema):
    """
    Device Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    mac_address = fields.Str(required=True)
    ip_address = fields.Str(required=True)
    status = fields.Bool(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    portscan_results = fields.Nested(PortScanSchema, many=True)
