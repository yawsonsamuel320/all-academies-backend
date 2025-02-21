from bson import ObjectId

def mongo_obj_to_dict(obj):
    """Convert MongoDB ObjectId to string."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {key: mongo_obj_to_dict(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [mongo_obj_to_dict(item) for item in obj]
    return obj
