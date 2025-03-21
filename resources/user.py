import sqlite3
from flask_restful import Resource, reqparse
from flask import Flask, request

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank. ")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank. ")


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "This username has already registered"},400

        user = UserModel(**data)
        UserModel.save_to_db(user)
        return {'message': 'User registered'}
