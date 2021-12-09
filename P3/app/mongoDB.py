import pymongo as pyMNG

mngClient = pyMNG.MongoClient("mongodb://localhost:27017/")
db = mngClient["si1"]
movies = db["topUK"]


def find(title=None, genre=None, year=None, actor=None):
    params = {"$and": []}

    if title:
        params["$and"].append({"title": {"$regex": str(title), "$options": "i"}})

    if genre:
        if isinstance(genre, list):
            for g in genre:
                params["$and"].append({"genres": {"$regex" : str(g), "$options" : "i"}})
        else:
            params["$and"].append({"genres": {"$regex" : str(genre), "$options" : "i"}})

    if year:
        if isinstance(year, list):
            params["$and"].append({"year": {"$in": year}})
        else:
            params["$and"].append({"year": {"$eq": year}})

    if actor:
        if isinstance(actor, list):
            for a in actor:
                params["$and"].append({"actors": {"$regex" : str(a), "$options" : "i"}})
        else:
            params["actors"] = {"$regex" : str(actor), "$options" : "i"}

    return list(movies.find(params))
