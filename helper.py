from models import User
import json


def get_username_from_id(user_id):
    return find_user_from_id(user_id=user_id, form_json=False)["username"]


def find_user_from_id(user_id, form_json=True):
    """Find a user by their ID and return their data as a dictionary or JSON string.

    Args:
        user_id: The ID of the user to find
        form_json: If True, return the data as a JSON string. If False, return the data as a dictionary
    Returns:
        The user's data as a dictionary or JSON string
    """

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None

    user_dict = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "privilege_id": user.privilege_id
    }
    if form_json:
        return json_interpreter(user_dict, to_json=True)
    return user_dict


def json_interpreter(data=None, to_json=True):
    """Convert between JSON string and Python dictionary.

    Args:
        data: Either a dictionary to serialize or a JSON string to parse
        to_json: If True, converts dict to JSON. If False, converts JSON to dict

    Returns:
        Converted data or None if invalid input
    """
    if data is None:
        print("Warning: No data provided to convert")
        return None

    try:
        if to_json and isinstance(data, dict):
            return json.dumps(data, indent=4)
        elif not to_json and isinstance(data, str):
            return json.loads(data)
        return data
    except Exception as e:
        print(f"Error happened while converting to json: {e}")
        return None
