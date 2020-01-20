import json
import os

import falcon
import pymongo

# port : 8083
client = pymongo.MongoClient(
    "mongodb://" + os.getenv("DB_HOST", "localhost") + ":" + os.getenv('MONGODB_PORT', '27017') + "/")
db = client["profiles-micro-service"]
col = db["profiles"]


class ProfileUpdate(object):
    def on_post(self, req, resp):
        result = req.media
        email = result["email"]
        model = {"_id": email}
        if col.find_one({"_id": email}):
            resp.body = model
        else:
            col.insert_one(model)
        print(result["email"])
        resp.body = json.dumps(model)
        resp.status = falcon.HTTP_200
        return resp

    def on_get(self, req, resp):
        result = req.media
        email = result["email"]
        x = col.find_one({"_id": email})
        resp.body = json.dumps(x)
        resp.status = falcon.HTTP_200
        return resp


def setup_profile():
    app = falcon.API()

    profile_update = ProfileUpdate()
    app.add_route('/profiles', profile_update)

    return app