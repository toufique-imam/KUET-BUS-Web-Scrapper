from flask import Flask
from flask_restful import Api,Resource,reqparse

from kuet_bus_test import get_data

app = Flask(__name__)
api = Api(app)
data =get_data()

class Bus_data(Resource):
    
    def get(self,id="bus"):
        if(id=="ALL" or id=="all"):
            return data,200
        for datac in data:
            for key in datac:
                if(key==id):
                    return datac[key],200
        return "Not Found",404

api.add_resource(Bus_data,"/data","/data/","/data/<string:id>")

if __name__ == "__main__":
    app.run()