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

   # THE FUNCTION PIVOT_TABLE
    #Pivoting data is the opposite of melting it. While melting takes a set of columns and turns it into a single column, 
    #pivoting will create a new column for each unique value in a specified column .pivot_table() has an index parameter which
    #you can use to specify the columns that you don't want pivoted: It is similar to the id_vars parameter of pd.melt(). 
    #Two other parameters that you have to specify are columns (the name of the column you want to pivot), 
    #and values (the values to be used when the column is pivoted).

# using pivot to make df2 tidy  !!! NOT TIDY, THE PIVOT FUNCTION CREATE AN AGGREGATION IF THE INDEX (DAY IN THE EXAMPLE) HAS DUPLICATE VALUES
df2_tidy=pd.pivot_table(df2,index=['Day'],columns=['Measure'],values=['Value'])    #optional argument, aggfunc=np.mean() (by default)
df2_tidy_reset=df2_tidy.reset_index()   # to reset the index and restore the dataframe
