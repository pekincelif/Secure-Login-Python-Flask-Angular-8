from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank. "
                        )
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help="Every item must have store_id "
                        )
 
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.item_json()

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        # if next(filter(lambda i: i['name'] == name, items), None) is not None:
        #     return {'message': "An item with name '{}' already exist.".format(name)}, 400

        data = Item.parser.parse_args()
        if ItemModel.find_item_by_name(name):
            return {'message': "An item with name '{}' already exist.".format(name)}, 400

        try:
            new_i = ItemModel(name, **data)  # data['price'], data[store_id] equal to **data
            new_i.save_to_db()
            # ItemModel.add_new_item(new_i)
            return new_i.item_json(), 201
        except:
            return {"message": "An error occured"}, 500  # internal server error



    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message' : 'Item'}


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        up_item = ItemModel(name, data['price'], data[store_id])

        if ItemModel.find_item_by_name(name):
            try:
                up_item.save_to_db()
            except:
                return {'message': "Error occured"}, 500
        else:
            try:
                up_item.save_to_db()
            except:
                return {'message': "Error occured"}, 500
            
        return up_item.item_json(), 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        # return {'item': [item.item_json() for item in ItemModel.query.all()]}
        return {'item': list(map(lambda x: x.item_json(), ItemModel.query.all()))}

