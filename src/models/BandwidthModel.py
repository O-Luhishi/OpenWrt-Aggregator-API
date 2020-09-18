from . import db
from marshmallow import fields, Schema
from sqlalchemy import desc
import datetime


class BandwidthModel(db.Model):
    """
    Bandwidth Model
    """

    __tablename__ = 'bandwidth'

    id = db.Column(db.Integer, primary_key=True)
    download_speed = db.Column(db.Integer, nullable=False)
    upload_speed = db.Column(db.Integer, nullable=False)
    ping = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.download_speed = data.get('download_speed')
        self.upload_speed = data.get('upload_speed')
        self.ping = data.get('ping')
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
    def get_all_bandwidth_tests():
        return BandwidthModel.query.all()

    @staticmethod
    def get_latest_bandwidth_tests():
        return db.session.query(
            BandwidthModel.download_speed, BandwidthModel.upload_speed, BandwidthModel.ping)\
            .order_by(desc(BandwidthModel.created_at)).first()


class BandwidthSchema(Schema):
    """
    Bandwidth Schema
    """
    id = fields.Int(dump_only=True)
    download_speed = fields.Int(required=True)
    upload_speed = fields.Int(required=True)
    ping = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
