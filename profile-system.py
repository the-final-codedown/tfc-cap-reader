import falcon
import json
import os
import pymongo

# port : 8083
client = pymongo.MongoClient(
    "mongodb://" + os.getenv("DB_HOST", "localhost") + ":" + os.getenv('DB_PORT', '27017') + "/")
db = client["tfc"]
col = db["profile"]


class ProfileUpdate(object):
    def on_post(self, req, resp):
        print("post")
        result = req.media
        email = result["email"]
        model = {"_id": email}
        accounts = []
        if col.find_one({"_id": email}):
            resp.body = model
        else:
            col.insert_one({"_id":email,"_class":"fr.polytech.al.tfc.profile.model.Profile","accounts":accounts})
        print(result["email"])
        resp.body = json.dumps({'email': model['_id'], "accounts": accounts})
        resp.status = falcon.HTTP_200
        return resp

    def on_get_single(self, req, resp, email=None):
        print("get single mail")
        print(email)
        if email is not None and col.find_one({"_id":email}):
            x = col.find_one({"_id": email})
            print(x)
            resp.body = json.dumps({'email': email})
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400
        return resp

    def on_get(self, req, resp):
        print("get")
        list_doc = []
        cursor = col.find({})
        for document in cursor:
            list_doc.append(document)
        resp.body = json.dumps(list_doc)
        resp.status = falcon.HTTP_200
        return resp
    def on_put(self,req,resp):
        print("put")
        result = req.media
        print(result)
        email = {"_id":result["owner"]["email"]}
        accountId = {"accountId":result["accountId"]}
        col.update_one(email,{"$push":{"accounts":accountId}})

def setup_profile():
    app = falcon.API()

    profile_update = ProfileUpdate()
    app.add_route('/profiles', profile_update)
    app.add_route('/profiles/{email}', profile_update, suffix='single')

    return app
