from sklearn.datasets import make_moons
import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
from scipy.stats import ks_2samp


#------------------ gerando dados
X, Y = make_moons(n_samples=100, noise=0.2)
df = DataFrame(dict(x=X[:,0], y=X[:,1], label=Y))
Y = DataFrame(Y)

#------------------ regressão
log_reg = LogisticRegression()
log_reg.fit(df.drop('label',axis=1), df['label'])


# resposta e scores
probs = log_reg.predict_proba(df.drop('label',axis=1))
probs = probs[:, 1]
Y_decil=Y
Y_decil[1]=1-Y_decil[0]
Y_decil[2]=probs
Y_decil.columns=['contr','n_contr','score']

# definindo decis
Y_decil['decil'] = pd.qcut(Y_decil.score,10)
Y_grouped = Y_decil.groupby('decil', as_index = False)

# base agregada
agg = pd.DataFrame()
agg['score_min'] = Y_grouped.min().score
agg['score_max'] = Y_grouped.max().score
agg['n_contr'] = Y_grouped.sum().n_contr
agg['contr'] = Y_grouped.sum().contr
agg['total'] = agg.n_contr + agg.contr
agg['taxa_contr'] = (agg.contr / agg.total).apply('{0:.2%}'.format)
# ordendando
agg = (agg.sort_values(by = 'score_max', ascending = False)).reset_index(drop = True)

agg['ganho'] = (agg.contr.cumsum()/agg.contr.sum())*100
agg['lift'] = agg.ganho/((agg.total.cumsum()/agg.total.sum())*100)

d_contr=Y_decil.score[Y_decil.contr==1]
d_n_contr=Y_decil.score[Y_decil.contr==0]

KS,p_value=ks_2samp(d_contr, d_n_contr)
