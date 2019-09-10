import pandas as pd
import numpy as np
import pandas_profiling as pp
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import make_scorer

from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import RandomForestClassifier

seed=42

data = pd.read_csv("train.csv")

#profile = data.profile_report(title='Report Case Santander')
#profile.to_file(output_file="case_santander_profiling.html")
#pickle.dump(profile,open('profile','wb'))

profile = pickle.load(open('profile', 'rb'))


def rejected_variables(profile, corr = 0.9, p_n_null = 0.0004) -> list:
    """Return a list of variable names being rejected for high 
    correlation with one of remaining variables.
    
    Args:
        threshold: correlation value which is above the threshold are rejected (Default value = 0.9)

    Returns:
        A list of rejected variables.
    """
    n_data = profile.description_set["table"]["n"]
    variable_profile = profile.description_set["variables"]
    result = []
    for col, values in variable_profile.items():
        if "correlation" in values:
            if values["correlation"] > corr:
                result.append(col)

    for col, values in variable_profile.items():
        if "distinct_count" in values:
            if values["distinct_count"] == 1:
                result.append(col)

    for col, values in variable_profile.items():
        if "n_zeros" in values:
            if values["n_zeros"]/n_data > 1 - p_n_null:
                result.append(col)
    return result

drop_variables = rejected_variables(profile)

data.drop(drop_variables, axis=1, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(data.drop('TARGET',axis=1),data['TARGET'], test_size=1/3, random_state=seed)



def avg_profit(y_true, y_pred):
    
    cm = confusion_matrix(y_true, y_pred)
    profit = cm[0][1]*(-10) + cm[1][1]*90
    return profit/cm.sum()

score_p = make_scorer(avg_profit)



clf = LogisticRegressionCV(cv=5, random_state=seed, scoring = score_p).fit(X_train, y_train)

rf = RandomForestClassifier(random_state=seed,class_weight='balanced')

param_grid = {'n_estimators' : [100,200,300],
              'max_depth' : [3,4,5]}

clf_rf = GridSearchCV(rf, param_grid=param_grid, cv=5)

clf_rf.fit(X_train, y_train)



fpr, tpr, thresholds = roc_curve(y_test, clf_rf.predict_proba(X_test)[:,1], pos_label=1)

plt.plot(fpr, tpr)
auc(fpr,tpr)
confusion_matrix(y_test, clf_rf.predict(X_test))
clf_rf.cv_results_
clf_rf.best_estimator_
clf_rf.best_score_

avg_profit(clf.predict(X_test),y_test)
score_p(clf, X_test, y_test) 

# pred # actual # profit
#   1     0        -10
#   1     1         90
#   0     1          0
#   0     0          0












y_pred = (clf.predict_proba(X_test)[:,1] >= 0.3).astype(bool)



from scipy.stats import ks_2samp
from sklearn.model_selection import GridSearchCV


def ks_stat(y, yhat):
    return ks_2samp(yhat[y==1], yhat[y!=1]).statistic

ks_scorer(clf, X_test, y_test) 


ks_scorer = make_scorer(ks_stat, needs_proba=True)

log_scorer = make_scorer(roc_auc_score, needs_proba=True, greater_is_better=False)

roc_scorer = make_scorer(log_loss, needs_proba=True)


grid = GridSearchCV(pl, param_grid=param_grid, scoring={'auc': roc_scorer, 'log': log_scorer}
    , refit='log')



score_p(clf, X_test.iloc[10:20,], y_test.iloc[20:30,])
