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
# TO TIDY DATA WITH THIS KIND OF ISSUE USE THE FUNCTION FROM PANDAS: pd.melt()

d2={'Day':[5,5,6,6,7,7], 'Measure':['Presure','Temperature','Presure','Temperature','Presure','Temperature'],'Value':[0.9,25,1,28,1.1,35]}
df2=pd.DataFrame(d2)

#this dataset is also untidy since there are two variables listed in the same colunm ( if you perform an aggregation function in the colunm "Value" the result will make no sense as it has values of temperature and presure)


# TIDYING THE DATA
    # THE FUNCTION MELT
     # There are two parameters you should be aware of: id_vars and value_vars. 
     # The id_vars represent the columns of the data you do not want to melt (i.e., keep it in its current shape),
     # while the value_vars represent the columns you do wish to melt into rows. 
     # By default, if no value_vars are provided, all columns not set in the id_vars will be melted. 
     # This could save a bit of typing, depending on the number of columns that need to be melted.

#using melt to make df1 tidy
df1_tidy=pd.melt(df1,id_vars=['Name'],var_name=['Treatment'])
