from . import db
from marshmallow import fields, Schema
import datetime


class PortScanModel(db.Model):
    """
    PortScan Model
    """

    __tablename__ = 'portscanresults'

    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.Text, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.results = data.get('results')
        self.device_id = data.get('device_id')
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
    def get_all_portscans():
        return PortScanModel.query.all()

    @staticmethod
    def get_portscan_by_scan_id(id):
        return PortScanModel.query.get(id)

    @staticmethod
    def get_portscan_by_device_id(device_id):
        return db.session.query(PortScanModel).filter_by(device_id=device_id).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class PortScanSchema(Schema):
    """
    PortScan Schema
    """
    id = fields.Int(dump_only=True)
    results = fields.Str(required=True)
    device_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
