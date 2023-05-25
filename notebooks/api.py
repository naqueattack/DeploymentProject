# import Flask and jsonify
from flask import Flask, jsonify, request
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy
import pickle

app = Flask(__name__)
api = Api(app)

def numFeat(X):
    return X[num_feats]

def catFeat(X):
    return X[cat_feats]

def logtransform(X):
    X['LoanAmount'] = np.log(X['LoanAmount'])
    X['TotalIncome'] = np.log(X['ApplicantIncome']+X['CoapplicantIncome'])
    X = X.drop(columns = ['ApplicantIncome','CoapplicantIncome'])
    return X
    
model = pickle.load( open( "C:/Users/Andrew/Documents/LHL/Deployment/DeploymentProject/notebooks/model.p", "rb" ) )

class Prediction(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        # getting predictions from our model.
        res = model.predict_proba(df)
        # we cannot send numpt array as a result
        return res.tolist() 
    
# assign endpoint
api.add_resource(Prediction, '/prediction')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)