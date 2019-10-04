import json
import falcon
import falcon_cors
from bson import json_util, ObjectId
from pymongo import MongoClient
from waitress import serve

cors = falcon_cors.CORS(allow_all_origins=True)

client = MongoClient('#login/password')
contacts = client.vueproject.contacts


class GetContacts:
    def on_get(self, req, resp):
        data = [{'id': str(contact['_id']),
                 'name': contact['name'],
                 'email': contact['email'],
                 'phone': contact['phone']} for contact in contacts.find()]

        data = json_util.dumps(contacts.find())
        data = json.loads(data)

        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_200


class RemoveContacts:
    def on_get(self, req, resp, cont_id):
        contacts.delete_one({'_id': ObjectId(cont_id)})
        resp.status = falcon.HTTP_200


class EditContacts:
    def update_one(self, req, resp, cont_id, email, name, phone):
        contacts.update({'id': ObjectId(cont_id)},
                        {'name': contacts[name],
                         'email': contacts[email],
                         'phone': contacts[phone]})
        resp.status = falcon.HTTP_200


class AddContacts:
    def on_post(self, req, resp):
        data = json.loads(req.stream.read())

        resp.location = contacts.save(data)
        resp.status = falcon.HTTP_200


api = falcon.API(middleware=[cors.middleware])
api.add_route('/api/contacts', GetContacts())
api.add_route('/api/contacts/add/{name}/{email}/{phone}', EditContacts())
api.add_route('api/contacts/remove/{contact_id}', RemoveContacts())

serve(api, host='127.0.0.1', port='3000')
