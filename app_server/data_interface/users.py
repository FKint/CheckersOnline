from main import boto_flask


def register_user(handle, password, email):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    # TODO: hash password
    # TODO: prevent overwriting
    table.put_item(
        Item={
            "Handle": handle,
            "Email": email,
            "Password": password
        }
    )
    return None


def check_user_login(handle, password):
    dynamodb = boto_flask.resources['dynamodb']
    table = dynamodb.Table('UsersCollection')
    response = table.get_item(
        Key={
            'Handle': handle
        }
    )
    if 'Item' not in response:
        return {
                   "message": "No such user"
               }, None
    item = response['Item']
    # TODO: use password hashing (bcrypt)
    if item['Password'] != password:
        return {
                   "message": "Invalid password"
               }, None
    return None, {
        "Handle": item['Handle'],
        "Email": item['Email']
    }
