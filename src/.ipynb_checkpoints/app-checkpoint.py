# import Flask and jsonify
from flask import Flask, jsonify, request
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy
import pickle
import json

app = Flask(__name__)
api = Api(app)

num_feats = ['Total_Income_Log', 'Loan_Amount_Log', 'Loan_Amount_Term']
cat_feats = ['Gender',
             'Married',
             'Dependents',
             'Education',
             'Self_Employed',
             'Property_Area']

def numFeat(data):
    return data[num_feats]

def catFeat(data):
    return data[cat_feats]
    
model = pickle.load( open( "model2.p", "rb" ) )


class Scoring(Resource):
    def post(self):
        json_data = request.get_json()
        data = json.loads(json_data)
        df = pd.DataFrame.from_dict(data)
        
        print(df)
        # getting predictions from our model.
        # it is much simpler because we used pipelines during development
        res = model.predict(df)
        print(res)
        # we cannot send numpt array as a result
        return res.tolist() 


# assign endpoint
api.add_resource(Scoring, '/scoring')

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)