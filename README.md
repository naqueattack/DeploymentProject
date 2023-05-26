# Mini-project IV

### [Assignment](assignment.md)

## Project/Goals
Goal of the project is to train a model and successfully deploy to AWS in the cloud

## Hypothesis
I expect the following to be related to higher loan application acceptance
Lower Dependents
Higher Education
Non-Self Employed
Higher Income (and coapplicant income)
Suburban > Urban > Rural due to correlation with income
Lower loan amounts
Longer loan terms
Present credit history

First I'll take a look at correlations between numeric variables and y variable. For nominal/categorical I can take a look at boxplots to get an idea of whether there is a difference or not.

## EDA 
There is a lot of EDA to cover, but the most interesting tidbits are the following:

-High class imbalance between loan acceptance and loan denial
-Income is fairly tightly packed with numerous outliers
-Men were overrepresented in the dataset
-Graduates were directionally more likely to be accepted for a loan. Self-employedness had no impact
-Loan status followed the direction I predicted for housing location
-Those without credit history had almost no chance of being approved for a loan
-Income and loan amount / length were only very weakly correlated with loan acceptance

There are too many images to showcase here without bloating the file, so I'd point you to notebooks/instructions for full EDA

## Process
The below process was done using a pipeline and this is the order:

## Oversampling & Splitting
#### Step 1: Oversampled the data at a rate of 0.8 to 1 to help correct imbalance without copying too much. This improved the models quite a bit
#### Step 2: Shuffled the data before splitting
#### Step 3: Split data into test train (80% split)

## Categorical Features
#### Step 1: Impute missing values
##### 1. Used the most frequent value in these cases I didn't find a good connection to be able to predict them
#### Step 2: One hot encoding
#### Step 3: PCA

## Numeric Features
#### Step 1: Impute missing values
##### 1. Used the mean for LoanAmount
##### 2. Used 360 (most common) for Loan_Amount_Term
##### 3. Filled credit history with 0's as if we don't have it, we can assume we don't have their credit history
#### Step 2: Log transformation of variables
##### 1. Log transformed LoanAmount
##### 2. Log transformed combination of income variables (dropped originals)
### Step 3. Kept K Best numeric variables

## Modeling
#### Model 1: XGBoost
#### Model 2: RandomForestClassifier

##### Both models were trained using RandomGridSearch. The exact specifications can be found below:

XGBOOST - param_grid = {"preprocessing__cat_transform__pca__n_components": [2],
                  "preprocessing__num_transform__selection__k": [4],
                  "model__max_depth":[8],
                  "model__min_child_weight":[1],
                  "model__n_estimators":[750],
                  "model__reg_lambda":[3],
                  "model__reg_alpha":[0],
                  "model__learning_rate":[.3]
             }

RandomForest - param_grid = {"preprocessing__cat_transform__pca__n_components": [2],
                   "preprocessing__num_transform__selection__k": [4],
                   "model__max_depth":[12],
                   "model__n_estimators":[250],
                   "model__bootstrap":[True],
                   "model__min_samples_leaf":[1],
                   "model__class_weight":[None]
              }
              
![Pipeline image](https://github.com/naqueattack/DeploymentProject/blob/master/images/Pipeline.PNG?raw=true)

## Results/Demo
Both models were similar in accuracy, though XGBoost did outperform RandomForest. In the end for production I used randomforest as I was unable to succesfully load XGBoost model in the cloud. This is a future endeavor as the accuracy difference is about 2%.

Confusion Matrix RandomForest:

![Confusion Matrix](https://github.com/naqueattack/DeploymentProject/blob/master/images/Confusion.PNG?raw=true)

Random Forest:
Accuracy: 78%
Precision: 77%
Recall: 81%

XGBoost:
Accuracy: 80%
Precision: 77%
Recall: 85%


The model does about equally well on both classes thanks to oversampling, but unfortunately a bit worse on class 0 (loan denied) which is probably the class we'd want to make sure to get.

The demo can be pulled using the training file in notebooks. This can be modified and it returns a 0 for loan denied and 1 for loan accepted.

## Challenges 
Uploading to the cloud proved incredibly difficult as pieces of my pipeline didn't behave as I thought they would and this caused hours of debugging. 

For that matter, putting things into a pipeline does save time on the backend, but being new to it, it takes a lot of time on the front end to get things working

## Future Goals
It would be good to work more with the features on feature engineering and try other models