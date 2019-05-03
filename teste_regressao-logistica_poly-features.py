from sklearn.datasets import make_moons
import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
#import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
#from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
#sns.set(style="white")

#------------------ gerando dados
X, y = make_moons(n_samples=10000, noise=0.2)
df = DataFrame(dict(x=X[:,0], y=X[:,1], label=y))

# scatter plot, dots colored by class value
colors = {0:'red', 1:'blue'}
fig, ax = plt.subplots()
grouped = df.groupby('label')
for key, group in grouped:
    group.plot(ax=ax, kind='scatter', x='x', y='y', label=key, color=colors[key],s=1)
plt.show()


#------------------ regressão logistica

log_reg = LogisticRegression()
log_reg.fit(df.drop('label',axis=1), df['label'])


# AUC
probs = log_reg.predict_proba(df.drop('label',axis=1))
probs = probs[:, 1]
roc_auc_score(df['label'], probs)


#----------------- ploting decision boundary

#creating grid
xx, yy = np.mgrid[-3:3:.01, -3:3:.01]
grid = np.c_[xx.ravel(), yy.ravel()]
probs = log_reg.predict_proba(grid)[:, 1].reshape(xx.shape)


#ploting linear decision boundary
f, ax = plt.subplots(figsize=(8, 6))
ax.contour(xx, yy, probs, levels=[.5], cmap="Greys", vmin=0, vmax=.6)

ax.scatter(X[100:,0], X[100:, 1], c=y[100:], s=1,
           cmap="RdBu", vmin=-.2, vmax=1.2, linewidth=1)

ax.set(aspect="equal",
       xlim=(-2, 3), ylim=(-1.5, 2),
       xlabel="$X_1$", ylabel="$X_2$")


#------------------- regressão logistica with polynomial features

# gerando polynomial features
poly_features = PolynomialFeatures(degree=3, include_bias=False)
X_poly = poly_features.fit_transform(X)
df_poly=DataFrame(X_poly)

# regressão
log_reg_poly = LogisticRegression()
log_reg_poly.fit(X_poly, y)

#AUC
probs = log_reg_poly.predict_proba(X_poly)
probs = probs[:, 1]
roc_auc_score(y, probs)

#----------------- ploting decision boundary

#creating grid
xx, yy = np.mgrid[-3:3:.01, -3:3:.01]
X_2=DataFrame(dict(x=xx.ravel(), y=yy.ravel()))
X_poly = poly_features.fit_transform(X_2)
probs = log_reg_poly.predict_proba(X_poly)[:, 1].reshape(xx.shape)


#ploting nomlinear decision boundary

f, ax = plt.subplots(figsize=(8, 6))
ax.contour(xx, yy, probs, levels=[.5], cmap="Greys", vmin=0, vmax=.6)

ax.scatter(X[100:,0], X[100:, 1], c=y[100:], s=1,
           cmap="RdBu", vmin=-.2, vmax=1.2, linewidth=1)

ax.set(aspect="equal",
       xlim=(-2, 3), ylim=(-1.5, 2),
       xlabel="$X_1$", ylabel="$X_2$")
