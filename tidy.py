# How to organize a dataset so it becomes easy to analyse 
# TIDY principles:
# - Colunms represent separate variables
# - Rows represent individual observations
# - Observational units forms tables (relational)

#Examples of unTidy data
import pandas as pd

d1={'Name':['Daniel','Jane','John'],'Treatment a':['',24,12],'Treatment b':[42,27,31]}
df1=pd.DataFrame(d1)

#this dataset is untidy, there are two colunms for the variable treatment, named 'Treatment a' and 'Treatment b'

d2={'Day':[5,5,6,6,7,7], 'Measure':['Presure','Temperature','Presure','Temperature','Presure','Temperature'],'Value':[0.9,25,1,28,1.1,35]}
df2=pd.DataFrame(d2)

#this dataset is also untidy as there are two variables listed in the same colunm ( if you perform an aggregation function in the colunm "Value" the result will make no sense as it has values of temperature and presure)


