from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)


class Resource(db.Model):
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(150), nullable=False)
    resource_type = db.Column(db.String(80), nullable=False)


class EventResourceAllocation(db.Model):
    allocation_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.resource_id'), nullable=False)

    event = db.relationship('Event', backref=db.backref('allocations', cascade='all, delete-orphan'))
    resource = db.relationship('Resource', backref=db.backref('allocations', cascade='all, delete-orphan'))


