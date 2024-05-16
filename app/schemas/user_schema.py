def userEntity(item) -> dict :
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "password": item["password"]
    }
    
def usersEntity(entity) -> list :
    return [userEntity(item) for item in entity]