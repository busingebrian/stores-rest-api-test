from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
Function that gets called when a user calls the /auth endpoint with their username & password.
    :param username: User's username in string format
    :param password: User's un-encrypted password in string format
    :return: A UserModel object if authentication was successful, none otherwise
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
    #  return None # by default python would return this if the above is not satisfied


def identity(payload):

        '''
        Function that gets called when the user has already been authenticated,
        and Flask-JWT verified their Authorization header is correct.
        :param payload: A dictionary with 'identity' key, which is the user id.
        :return: A UserModel object
        '''

        user_id = payload['identity']
        return UserModel.find_by_id(user_id)
