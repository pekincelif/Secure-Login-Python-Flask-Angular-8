from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    # user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user

def identify(payload):
    id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(id)
