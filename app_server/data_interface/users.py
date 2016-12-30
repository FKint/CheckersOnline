from helpers.session import get_user_id, update_user_account
from application import boto_flask


def register_user(handle, password, email):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    # TODO: hash password
    # TODO: prevent overwriting
    table.put_item(
        Item={
            "Handle": handle,
            "Email": email,
            "Password": password,
            "Friends": {"AI"}
        }
    )
    return None


def get_all_user_data(handle):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    response = table.get_item(
        Key={
            'Handle': handle
        }
    )
    if 'Item' not in response:
        return None
    item = response['Item']
    return item


def extract_public_user_fields(item):
    return {
        "Handle": item['Handle'],
        "Email": item['Email'],
        "Friends": list(item['Friends']) if 'Friends' in item else []
    }


def get_public_user_account(handle):
    all_user_data = get_all_user_data(handle)
    if all_user_data is None:
        return None
    return extract_public_user_fields(get_all_user_data(handle))


def check_user_login(handle, password):
    item = get_all_user_data(handle)
    if item is None:
        return {
                   "message": "No such user"
               }, None
    # TODO: use password hashing (bcrypt)
    if item['Password'] != password:
        return {
                   "message": "Invalid password"
               }, None
    return None, extract_public_user_fields(item)


def add_friend(handle):
    user_id = get_user_id()
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    other_user = table.get_item(Key={'Handle': handle})
    print(other_user)
    if 'Item' not in other_user or other_user['Item'] is None:
        return False
    table.update_item(
        Key={'Handle': user_id},
        UpdateExpression="ADD Friends :f",
        ExpressionAttributeValues={
            ':f': {handle}
        }
    )
    update_user_account()
    return True
