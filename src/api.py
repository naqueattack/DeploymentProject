# import Flask and jsonify
from flask import Flask, jsonify, request
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
api = Api(app)

def catFeat(X):
    cat_feats = X.dtypes[X.dtypes == 'object'].index.tolist()
    return X[cat_feats]

def numFeat(X):
    cat_feats = X.dtypes[X.dtypes == 'object'].index.tolist()
    num_feats = X.dtypes[~X.dtypes.index.isin(cat_feats)].index.tolist()
    return X[num_feats]

def logtransform(X):
    print(X)
    X['LoanAmount'] = np.log(X['LoanAmount'])
    X['TotalIncome'] = np.log(X['ApplicantIncome']+X['CoapplicantIncome'])
    X = X.drop(columns = ['ApplicantIncome','CoapplicantIncome'])
    return X

model = pickle.load( open( "C:/Users/Andrew/Documents/LHL/Deployment/DeploymentProject/notebooks/model.p", "rb" ) )

class Prediction(Resource):
    def post(self):
        # global cat_feats
        # global num_feats
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        print(df)
        
        #change numeric variables to float
        df[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']] = df[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']].astype('float')
        # getting predictions from our model.
        res = model.predict(df)
        # we cannot send numpt array as a result
        return res.tolist() 
    
    def get(self):
        return("What are you doing here? Try posting")
    
# assign endpoint
api.add_resource(Prediction, '/prediction')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)