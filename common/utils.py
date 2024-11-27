def check_required_fields(data, fields):
    for field in fields:
        if field not in data:
            return False
    return True
