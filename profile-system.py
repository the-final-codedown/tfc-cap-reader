import falcon
import json
import os
import pymongo

# port : 8083
client = pymongo.MongoClient(
    "mongodb://" + os.getenv("DB_HOST", "localhost") + ":" + os.getenv('DB_PORT', '27017') + "/")
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

    def on_get_single(self, req, resp, email=None):
        print(email)
        if email is not None:
            x = col.find_one({"_id": email})
            print(x)
            resp.body = json.dumps({'email': email})
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400
        return resp

    def on_get(self, req, resp):
        list_doc = []
        cursor = col.find({})
        for document in cursor:
            list_doc.append(document)
        resp.body = json.dumps(list_doc)
        resp.status = falcon.HTTP_200
        return resp


def setup_profile():
    app = falcon.API()

    profile_update = ProfileUpdate()
    app.add_route('/profiles', profile_update)
    app.add_route('/profiles/{email}', profile_update, suffix='single')

    return app
