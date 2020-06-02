from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.store_json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_store_by_name(name):
            return {'message': "A store with name '{}' aslready exist.".format(name)}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while creating the store.'}, 500

        return store.store_json(), 201
          
    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted '}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.store_json() for store in StoreModel.query.all()]}
        # return {'stores': list(map(lambda x: x.stores_json(), StoreModel.query.all()))}
