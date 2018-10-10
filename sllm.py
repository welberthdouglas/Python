# packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

######################################
#           IMPORTING DATA
######################################

# importing raw data
# dropping the '0' colunm and indexing by date
costs = pd.read_csv('costs.csv', usecols =[1,2,3],index_col = 'date', parse_dates = True)   
installs = pd.read_csv('installs.csv', usecols = [1,2,3,4],index_col = 'date', parse_dates = True)
performance = pd.read_csv('performance.csv', usecols = [1,2,3,4],index_col = 'date', parse_dates = True)
purchases = pd.read_csv('purchases.csv', index_col = 'calendar_date', parse_dates = True)

# Replacing NaN in installs by 'Organic'
installs.fillna('Organic', inplace=True)


# importing summarized data
CPI_by_source = pd.read_csv('Visao_CPI.csv',index_col = 'date', parse_dates = True)
installs_by_source = pd.read_csv('Visao_installs.csv',index_col = 'date', parse_dates = True)
revenue_by_source = pd.read_csv('Visao_revenue.csv', index_col = 'calendar_date', parse_dates = True)
revenue_by_source_idate = pd.read_csv('Visao_revenue_2.csv', sep =' ',  parse_dates = ['install_date','purchase_date']) # this file has space as separator


# sorting index for all
 
costs = costs.sort_index()
installs = installs.sort_index()
performance = performance.sort_index()
purchases = purchases.sort_index()
CPI_by_source = CPI_by_source.sort_index()
installs_by_source = installs_by_source.sort_index()
revenue_by_source = revenue_by_source.sort_index()


# Adding how much days after installation is the purchase being made
revenue_by_source_idate['days_after_installation']=(revenue_by_source_idate['purchase_date'] - revenue_by_source_idate['install_date']).astype('timedelta64[D]')
sources=['AdYan','Adcity','Dozenads','Facebook','GenerationY','Google']
months=['nov 2015','dec 2015','jan 2016','feb 2016','mar 2016']


#####################################################################################
#               IN WHICH SOURCE THE APP HAS THE BEST PERFORMANCE?
#####################################################################################

# (revenue-cost)  performance for each source for the entire period

performance_tot={}
for i in range(len(sources)):
    rev = revenue_by_source[revenue_by_source.source == sources[i]].sum().iloc[1]
    cost = costs[costs.source == sources[i]].sum().iloc[1]
    performance_tot[sources[i]]= [rev - cost]

# (revenue - cost) performance for each source month by month

# reshaping the revenue and cost dataframe to alocate each source in a column
revenue_by_source2=pd.pivot_table(revenue_by_source,index=['calendar_date'],columns=['source'],values=['revenue'],fill_value=0) 
revenue_by_source2.columns=sources

costs2=pd.pivot_table(costs,index=['date'],columns=['source'],values=['spend'],fill_value=0) 
costs2.columns=sources

performance_m=np.zeros((6,5))
for i in range(len(sources)):
    for m in range(len(months)):
        rev = revenue_by_source2.loc[:,sources[i]][months[m]].sum()
        cost = costs2.loc[:,sources[i]][months[m]].sum() 
        performance_m[i,m] = rev - cost

# transforming the numpy array in a dataframe
performance_m=pd.DataFrame(performance_m, index=sources)
performance_m.columns=months
performance_m=performance_m.T

# ploting revenue-cost for each source monthly
performance_m.plot()


#####################################################################################
#     HOW THE REVENUE PER USER VARIES AS A FUNCION OF DSI (DAYS SINCE INSTALL)?
#####################################################################################

# revenue per user for each source (dumb way)

# FACEBOOK

days_Facebook=revenue_by_source_idate[revenue_by_source_idate.source == 'Facebook'].loc[:,['purchase','days_after_installation']]
Facebook=days_Facebook.groupby('days_after_installation').sum()
users_Facebook=(installs_by_source[installs_by_source.source=='Facebook'].sum()).loc['installs']

Facebook['revenue_user']=Facebook['purchase']/users_Facebook
Facebook['revenue_user_cum']=Facebook['revenue_user'].cumsum()
#Facebook.revenue_user.plot()

# GOOGLE
days_Google=revenue_by_source_idate[revenue_by_source_idate.source == 'Google'].loc[:,['purchase','days_after_installation']]
Google=days_Google.groupby('days_after_installation').sum()
users_Google=(installs_by_source[installs_by_source.source=='Google'].sum()).loc['installs']

Google['revenue_user']=Google['purchase']/users_Google
Google['revenue_user_cum']=Google['revenue_user'].cumsum()
#Google.revenue_user.plot()

# DOZENADS

days_Dozenads=revenue_by_source_idate[revenue_by_source_idate.source == 'Dozenads'].loc[:,['purchase','days_after_installation']]
Dozenads=days_Dozenads.groupby('days_after_installation').sum()
users_Dozenads=(installs_by_source[installs_by_source.source=='Dozenads'].sum()).loc['installs']

Dozenads['revenue_user']=Dozenads['purchase']/users_Dozenads
Dozenads['revenue_user_cum']=Dozenads['revenue_user'].cumsum()
#Dozenads.revenue_user.plot()

# ADCITY

days_Adcity=revenue_by_source_idate[revenue_by_source_idate.source == 'Adcity'].loc[:,['purchase','days_after_installation']]
Adcity=days_Adcity.groupby('days_after_installation').sum()
users_Adcity=(installs_by_source[installs_by_source.source=='Adcity'].sum()).loc['installs']

Adcity['revenue_user']=Adcity['purchase']/users_Adcity
Adcity['revenue_user_cum']=Adcity['revenue_user'].cumsum()
#Adcity.revenue_user.plot()

# GENERATION Y

days_GenerationY=revenue_by_source_idate[revenue_by_source_idate.source == 'GenerationY'].loc[:,['purchase','days_after_installation']]
GenerationY=days_GenerationY.groupby('days_after_installation').sum()
users_GenerationY=(installs_by_source[installs_by_source.source=='GenerationY'].sum()).loc['installs']

GenerationY['revenue_user']=GenerationY['purchase']/users_GenerationY
GenerationY['revenue_user_cum']=GenerationY['revenue_user'].cumsum()
#GenerationY.revenue_user.plot()

# ADYAN

days_AdYan=revenue_by_source_idate[revenue_by_source_idate.source == 'AdYan'].loc[:,['purchase','days_after_installation']]
AdYan=days_AdYan.groupby('days_after_installation').sum()
users_AdYan=(installs_by_source[installs_by_source.source=='AdYan'].sum()).loc['installs']

AdYan['revenue_user']=AdYan['purchase']/users_AdYan
AdYan['revenue_user_cum']=AdYan['revenue_user'].cumsum()
#AdYan.revenue_user.plot()

revenue_per_user_cum = pd.concat([Facebook['revenue_user_cum'],Google['revenue_user_cum'],Dozenads['revenue_user_cum'],Adcity['revenue_user_cum'],GenerationY['revenue_user_cum'],AdYan['revenue_user_cum']],axis=1,keys=['Facebook','Google','Dozenads','Adcity','GenerationY','AdYan'])
revenue_per_user = pd.concat([Facebook['revenue_user'],Google['revenue_user'],Dozenads['revenue_user'],Adcity['revenue_user'],GenerationY['revenue_user'],AdYan['revenue_user']],axis=1,keys=['Facebook','Google','Dozenads','Adcity','GenerationY','AdYan'])
revenue_per_user =revenue_per_user.fillna(0)
revenue_per_user_cum =revenue_per_user_cum.fillna(method='ffill')
revenue_per_user_cum.plot()
plt.ylabel('accumulated revenue per user')
plt.savefig('accumulated revenue per user.pdf')







estimator14={}
for i in range(len(sources)):
    estimator14[sources[i]]=revenue_per_user_cum.loc[14,sources[i]]/revenue_per_user_cum[sources[i]].max()


for i in range(len(sources)):
    max[sources[i]]=revenue_per_user_cum.loc[14,sources[i]]/revenue_per_user_cum[sources[i]].max()
    
 
revenue_by_source_idate=revenue_by_source_idate.set_index('install_date')

r1=revenue_by_source_idate.loc['2015-11-01':'2015-11-14']
r1=r1[r1['days_after_installation'] <=14]
r2=revenue_by_source_idate.loc['2015-11-15':'2015-11-28']
r2=r2[r2['days_after_installation'] <=14]
r3=revenue_by_source_idate.loc['2015-11-29':'2015-12-12']
r3=r3[r3['days_after_installation'] <=14]
r4=revenue_by_source_idate.loc['2015-12-13':'2015-12-26']
r4=r4[r4['days_after_installation'] <=14]
r5=revenue_by_source_idate.loc['2015-12-27':'2015-01-09']
r5=r5[r5['days_after_installation'] <=14]
r6=revenue_by_source_idate.loc['2016-01-10':'2016-01-23']
r6=r6[r6['days_after_installation'] <=14]
r7=revenue_by_source_idate.loc['2016-01-24':'2016-02-06']
r7=r7[r7['days_after_installation'] <=14]
r8=revenue_by_source_idate.loc['2016-02-07':'2016-02-20']
r8=r8[r8['days_after_installation'] <=14]
r9=revenue_by_source_idate.loc['2016-02-21':'2016-03-05']
r9=r9[r9['days_after_installation'] <=14]
r10=revenue_by_source_idate.loc['2016-03-06':'2016-03-19']
r10=r10[r10['days_after_installation'] <=14]
r11=revenue_by_source_idate.loc['2016-03-20':'2016-03-31']
r11=r11[r11['days_after_installation'] <=14]  

    


##################################################################
#           HOW OFTEN SHOULD WE OPTIMIZE THE CAMPAIGN?
##################################################################

# installs by source plot (dumb way)
plt.plot(installs_by_source.installs[installs_by_source.source == 'Facebook'],label='Facebook')
plt.plot(installs_by_source.installs[installs_by_source.source == 'Google'],label='Google')
plt.plot(installs_by_source.installs[installs_by_source.source == 'Dozenads'],label='Dozenads')
plt.plot(installs_by_source.installs[installs_by_source.source == 'Adcity'],label='Adcity')
plt.plot(installs_by_source.installs[installs_by_source.source == 'GenerationY'],label='GenerationY')
plt.plot(installs_by_source.installs[installs_by_source.source == 'AdYan'],label='AdYan')
plt.plot(installs_by_source.installs[installs_by_source.source == 'Other'],label='Other')
plt.ylabel('instalações')
plt.legend()
plt.xticks(rotation=90)
plt.show()

# total installs in the period
itot=installs_by_source.groupby('date').sum()
itot2=installs_by_source.installs[installs_by_source.source != 'Other'].groupby('date').sum()

#comoparison between organic and non organic installs
plt.plot(itot)
plt.plot(itot2)
plt.yscale('log')
plt.show()

# revenue per user by day for all sources 
days_total=revenue_by_source_idate.loc[:,['purchase','days_after_installation']]
total=days_total.groupby('days_after_installation').sum()
users_total=(installs_by_source.sum()).loc['installs']-(installs_by_source[installs_by_source.source=='Other'].sum()).loc['installs']

# plot
total['revenue_user']=total['purchase']/users_total
total.revenue_user.plot()



###########################################################
#                   REVENUE PER USER 
###########################################################

# aggregating data by purchase date
rev=revenue_by_source.groupby('calendar_date').sum()


inst=installs_by_source[installs_by_source.source != 'Other'].groupby('date').sum()  # excluding organic installs
inst['cumulative']=inst.installs.cumsum()

# revenue per user
rev['revenue_per_user']=rev['revenue']/inst['cumulative']
rev['revenue_per_user'].plot()

# revenue
rev['revenue'].plot()



###########################################################################
#            HOW SHOULD WE ALOCATE THE BUDGET IN THE SHORT RUN?
###########################################################################

# aggregating costs and downloads daily 
tot_costs=costs.groupby('date').sum()
tot_inst=installs_by_source.groupby('date').sum()

# plot of total costs and total downloads daily (excluding organic installs)
tot_costs.spend.plot()
tot_inst.plot()

# total costs per install
tot_costs['costperinst']=tot_costs['spend']/tot_inst['installs']
tot_costs.costperinst.plot()

# total revenue per user - cost per install
(rev['revenue_per_user']-tot_costs['costperinst']).plot()

#!!!!!       CONFERIR ISSO - NÃO PODE TER USUÁRIOS ORGANICOS AQUI
prop = installs_by_source[installs_by_source.source == 'Other'].sum()/installs_by_source['installs'].sum()

# organic installs
plt.plot(installs_by_source.installs[installs_by_source.source == 'Other'],label='Other')
plt.ylabel('instalações')
plt.legend()
plt.show()


###########################################################################
#                     IMPORTANCE OF PUBLISHER APPS
###########################################################################


# publisher apps with more installs subdivided by source

pub_app=installs[installs.source != 'Organic']#.groupby('publisher_app').count()
Facebook_pubapp=pub_app[pub_app.source == 'Facebook']
Facebook_pubapp=Facebook_pubapp.groupby('publisher_app').count()

pub_app=installs[installs.source != 'Organic']#.groupby('publisher_app').count()
AdYan_pubapp=pub_app[pub_app.source == 'AdYan']
AdYan_pubapp=AdYan_pubapp.groupby('publisher_app').count()

pub_app=installs[installs.source != 'Organic']#.groupby('publisher_app').count()
Adcity_pubapp=pub_app[pub_app.source == 'Adcity']
Adcity_pubapp=Adcity_pubapp.groupby('publisher_app').count()

pub_app=installs[installs.source != 'Organic']#.groupby('publisher_app').count()
GenerationY_pubapp=pub_app[pub_app.source == 'GenerationY']
GenerationY_pubapp=GenerationY_pubapp.groupby('publisher_app').count()

pub_app=installs[installs.source != 'Organic']#.groupby('publisher_app').count()
Dozenads_pubapp=pub_app[pub_app.source == 'Dozenads']
Dozenads_pubapp=Dozenads_pubapp.groupby('publisher_app').count()

pub_app=installs[installs.source != 'Organic']#.groupby('publisher_app').count()
Google_pubapp=pub_app[pub_app.source == 'Google']
Google_pubapp=Google_pubapp.groupby('publisher_app').count()

# publisher apps with more installs overall

pub_app_tot=installs[installs.source != 'Organic'].groupby('publisher_app').count()
pub_app_tot=pub_app_tot.sort_values(['source'],ascending=False)
pub_app_tot.head(20)[1:].plot(marker='.')

installs[installs.source == 'Organic']['publisher_app'].unique()


###########################################################################
#                             EXTRA PLOTS
###########################################################################

# extra plots made in a dumb way

# IMPRESSIONS
plt.plot(performance.impressions[performance.source == 'Facebook'],label='Facebook')
plt.plot(performance.impressions[performance.source == 'Google'],label='Google')
plt.plot(performance.impressions[performance.source == 'Dozenads'],label='Dozenads')
plt.plot(performance.impressions[performance.source == 'Adcity'],label='Adcity')
plt.plot(performance.impressions[performance.source == 'GenerationY'],label='GenerationY')
plt.plot(performance.impressions[performance.source == 'AdYan'],label='AdYan')
plt.legend()
plt.ylabel('impressões')
plt.show()


# CLICKS
plt.plot(performance.clicks[performance.source == 'Facebook'],label='Facebook')
plt.plot(performance.clicks[performance.source == 'Google'],label='Google')
plt.plot(performance.clicks[performance.source == 'Dozenads'],label='Dozenads')
plt.plot(performance.clicks[performance.source == 'Adcity'],label='Adcity')
plt.plot(performance.clicks[performance.source == 'GenerationY'],label='GenerationY')
plt.plot(performance.clicks[performance.source == 'AdYan'],label='AdYan')
plt.ylabel('clicks')
plt.legend()
plt.show()



# CLICKS / IMPRESSIONS
# calculating the ratio between clicks and impressions
performance['ratio'] = (performance.clicks/performance.impressions)*1000

plt.plot(performance.ratio[performance.source == 'Facebook'],label='Facebook')
plt.plot(performance.ratio[performance.source == 'Google'],label='Google')
plt.plot(performance.ratio[performance.source == 'Dozenads'],label='Dozenads')
plt.plot(performance.ratio[performance.source == 'Adcity'],label='Adcity')
plt.plot(performance.ratio[performance.source == 'GenerationY'],label='GenerationY')
plt.plot(performance.ratio[performance.source == 'AdYan'],label='AdYan')
plt.ylabel('clicks por impressão')
plt.legend()
plt.show()


# REVENUE
plt.plot(revenue_by_source.revenue[revenue_by_source.source == 'Facebook'],label='Facebook')
plt.plot(revenue_by_source.revenue[revenue_by_source.source == 'Google'],label='Google')
plt.plot(revenue_by_source.revenue[revenue_by_source.source == 'Dozenads'],label='Dozenads')
plt.plot(revenue_by_source.revenue[revenue_by_source.source == 'Adcity'],label='Adcity')
plt.plot(revenue_by_source.revenue[revenue_by_source.source == 'GenerationY'],label='GenerationY')
plt.plot(revenue_by_source.revenue[revenue_by_source.source == 'AdYan'],label='AdYan')
plt.ylabel('revenue')
plt.legend()
plt.show()

# CPI
plt.plot(CPI_by_source.cpi[CPI_by_source.source == 'Facebook'],label='Facebook')
plt.plot(CPI_by_source.cpi[CPI_by_source.source == 'Google'],label='Google')
plt.plot(CPI_by_source.cpi[CPI_by_source.source == 'Dozenads'],label='Dozenads')
plt.plot(CPI_by_source.cpi[CPI_by_source.source == 'Adcity'],label='Adcity')
plt.plot(CPI_by_source.cpi[CPI_by_source.source == 'GenerationY'],label='GenerationY')
plt.plot(CPI_by_source.cpi[CPI_by_source.source == 'AdYan'],label='AdYan')
plt.ylabel('Custo por download')
plt.legend()

# COSTS
plt.plot(costs.spend[costs.source == 'Facebook'],label='Facebook')
plt.plot(costs.spend[costs.source == 'Google'],label='Google')
plt.plot(costs.spend[costs.source == 'Dozenads'],label='Dozenads')
plt.plot(costs.spend[costs.source == 'Adcity'],label='Adcity')
plt.plot(costs.spend[costs.source == 'GenerationY'],label='GenerationY')
plt.plot(costs.spend[costs.source == 'AdYan'],label='AdYan')
plt.ylabel('custo')
plt.legend()
plt.show()
