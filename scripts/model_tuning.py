import models
import pandas as pd
import numpy as np
import pyspark as ps
import models
import graphlab as gl

def confusion_matrix(y_true, y_predict):
'''
    INPUT:
        - y_true: True labels
        - y_predict: Predicted labels.

    OUTPUT:
        - None: None
        
    In our case model was checked against a correct prediction equal to or above 8.
    Prints confusion matrix to screen.
    '''
    tp = fn = fp = tn = 0
    for true,pred in zip(y_true, y_predict):
        if true == 0:
            if pred == 0:
                tn +=1
            else:
                fp += 1
        else:
            if pred == 0:
                fn += 1
            else:
                tp += 1

    print "Sensitivity/Recall: ", tp/float(tp+fn)
    print "Specificity: ", tn/float(tn+fp)
    print "Precision: ", tp/float(tp+fp)
    print '\n'
    print np.array([[tp, fp],[fn, tn]])
    
def main():
    # Collect main data and side data.
    data = models.build_maindata()
    sidedata = models.build_sidedata()
    train, test = gl.recommender.util.random_split_by_user( \
            data, user_id='user_id', item_id='item_id')

    # Set hyperparameters to search across
    params = {  'target': 'rating',
            'item_data': sidedata, 
            'num_factors': [4, 6, 8],
            'nmf': [True, False],
            'regularization': [0.001, 0.0001, 0.00001, 0.000001],
            'max_iterations': [25,50] }

    # Grid search
    job = gl.grid_search.create(    (train, test),
            gl.recommender.factorization_recommender.create, params)

    job.get_best_params()
        '''
        'max_iterations': 25,
        'nmf': False,
        'num_factors': 6,
        'regularization': 0.001,
        'target': 'rating'}
        '''
    # Build model using best params
    model = gl.recommender.factorization_recommender.create( 
                                data, 
                                user_id="user_id", 
                                item_id="item_id", 
                                target="rating",
                                item_data=sidedata,
                                max_iterations=25,
                                num_factors=6,
                                regularization=0.001)

    # Check performance with confustion matrix.
    test['predict'] = model.predict(test)
    test['rating_B'] = test['rating'].apply(lambda x: 1 if x>=8 else 0)
    test['predict_B'] = test['predict'].apply(lambda x: 1 if x>=8 else 0)
    print confusion_matrix(test['rating_B'], test['predict_B'])

if __name__ == '__main__':
    main()


