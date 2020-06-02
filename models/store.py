from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    store_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    items = db.relationship('ItemModel', lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def store_json(self):
        return {'name': self.name, 'items': [item.item_json() for item in self.items]}

    @classmethod
    def find_store_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
