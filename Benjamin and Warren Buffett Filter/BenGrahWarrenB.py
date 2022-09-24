#!/usr/bin/env python
# coding: utf-8

# # Benjamin Graham and Warren Buffett Model Stock Exchange

# ## Introduction:
# * There are about 4000 stocks which are actively traded on the stock exchanges at BSE and NSE.
# * We can extract public financial data from sites like to find which are the fundamentally strong stocks. 
# * On what stocks would the father of value investing, Benjamin Graham and Warren Buffett the most successful investors in the world make their investments on.

# ## Benjamin Graham and Warren Buffett Model:
# 1. **Step 1:** Filtering out all companies with sales less than Rs 250 cr. Companies with sales lower than this are very small companies and might not have the business stability and access to finance that is required for a safe investment. This eliminates the basic business risk.
# 2. **Step 2:** Filtering out all companies with debt to equity greater than 30%. Companies with low leverage are safer.
# 3. **Step 3:** Filtering out all companies with interest coverage ratio of less than 4. Companies with high interest coverage ratio have a highly reduced bankruptcy risk.
# 4. **Step 4:** Filtering out all companies with ROE less than 15% since they are earning less than their cost of capital. High ROE companies have a robust business model, which generates increased earnings for the company typically.
# 5. **Step 5:** Filtering out all companies with PE ratio greater than 25 since they are too expensive even for a high-quality company. This enables us to pick companies which are relatively cheaper as against their actual value. He points out that applying these filters enables us to reduce and even eliminate a lot of fundamental risks while ensuring a robust business model, strong earning potential and a good buying price.

# ## Implementation of the Model.

# In[1]:


# importing required libraries

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[2]:


# Read the data from the csv files

data=pd.read_csv("Companies.csv")
#data.head()


# ### Analysing the dataset / Data cleaning.

# In[3]:


# Checking for null values

#data.isnull().sum()


# In[4]:


#data.info()


# In[5]:


#data.describe()


# * The data looks clean and ready to be used.

# ### Extracting the links of the companies from the data.
# 
# **Note:** The data is being extracted from [Money Control Website](https://www.moneycontrol.com/)

# In[6]:


companynames=list(data.iloc[:,0])
links=list(data.iloc[:,1])

#links for old format page
linkso=[]
for i in range(0,len(links)):
    a=links[i].find('VI')
    b=links[i][:a]+links[i][a+2:]
    linkso.append(b)

#links for profit-loss page
linkso_pl=[]
for i in range(0,len(linkso)):
    a=linkso[i].find('balance-sheet')
    b=linkso[i][:a]+'profit-loss'+linkso[i][a+13:]
    linkso_pl.append(b)


# ## Implementation of Step - 1 :
# **Filtering out all companies with sales less than Rs 250 cr.**

# ### Scrapping Net Sales
# <br>
# 
# **Note:** 
# * As the details of net sales was not provided, the following banks were excluded from the file:
# > HDFC bank, ICICI bank, Indusland bank, Kotak Mahindra Bank, Yes Bank, SBI
# * As interestt cover ratio was not provided, the following were also excluded.
# > Bajaj Finserv and Infosys 
# 

# In[7]:


netsales_list=[]
for i in linkso_pl:
    i_ind = i.find('profit-loss')
    i = i[:i_ind]+'results/yearly'+i[i_ind+11:]
    pageold=requests.get(i)
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Net Sales/Income from operations</td>\n.*</td>',about)
    netsales=re.findall('>[-+]?[0-9].*<',str(a))
    netsales=netsales[0][1:len(netsales[0])-1]
    if(netsales.find(',') != -1):
        b=netsales.find(',')
        netsales_list.append(float(netsales[:b]+netsales[b+1:]))
        b=-1
    else:
        netsales_list.append(float(netsales))


# * The Net Sales of each company is saved in the netsales list in Crores.

# In[8]:


# values in cr.
#netsales_list


# #### Filtering. 
# * The companies with less than 250 cr. Net Sales are to be filtered out/removed.

# In[9]:


filtersales=[]
filtercomp=[]
filterlink=[]
filterolink=[]
for i in range(0,len(netsales_list)):
    if(netsales_list[i]<250.00):
        filtersales.append(netsales_list[i])
        filtercomp.append(companynames[i])
        filterlink.append(links[i])
        filterolink.append(linkso[i])
for i in range(0,len(filtersales)):
    netsales_list.remove(filtersales[i])
    companynames.remove(filtercomp[i])
    links.remove(filterlink[i])
    linkso.remove(filterolink[i])


# ## Implementatin of Step - 2 :
# **Filtering out all companies with debt to equity greater than 30%.**

# ### Scraping debt equity Ratio

# * **Some of the data to be extracted is in old page format.**
# * **The links of the old page is stored in linkso_r list.**

# In[10]:


#links for ratio page
linkso_r=[]
for i in range(0,len(linkso)):
    a=linkso[i].find('balance-sheet')
    b=linkso[i][:a]+'ratios'+linkso[i][a+13:]
    linkso_r.append(b)
    
debtequity_ratio=[]
for i in linkso_r:
    pageold=requests.get(i)
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Total Debt/Equity.*</td>\n.*</td>',about)
    der=re.findall('>[-+]?[0-9].*<',str(a))
    if(len(der)==0):
        der=0
    else:
        der=der[0][1:len(der[0])-1]
    debtequity_ratio.append(float(der))


# In[11]:


#debtequity_ratio


# #### Companies with Debt Equity Ratio greater than 0.3 are filtered/removed.

# In[12]:


filtersales=[]  
filterder=[]
filtercomp=[]
filterlink=[]
filterolink=[]
for i in range(0,len(debtequity_ratio)):
    if(debtequity_ratio[i]>0.3):
        filterder.append(debtequity_ratio[i])
        filtercomp.append(companynames[i])
        filterlink.append(links[i])
        filterolink.append(linkso[i])
        filtersales.append(netsales_list[i])
for i in range(0,len(filterder)):
    debtequity_ratio.remove(filterder[i])
    companynames.remove(filtercomp[i])
    links.remove(filterlink[i])
    linkso.remove(filterolink[i])
    netsales_list.remove(filtersales[i])


# ## Implementation of Step - 3 :
# **Filtering out all companies with interest coverage ratio of less than 4.**
# <br>
# ### Scraping Interest Coverage Ratio.

# In[13]:


#links for ratio page
linkso_r=[]

for i in range(0,len(linkso)):
    a=linkso[i].find('balance-sheet')
    b=linkso[i][:a]+'ratios'+linkso[i][a+13:]
    linkso_r.append(b)

icr_list=[]

for i in linkso_r: 
    ind_ = i.find('ratios')
    i = i[:ind_]+'consolidated-'+i[ind_:]
    pageold=requests.get(i)
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Interest Coverage Ratios ...</td>\n.*</td>',about)
    #icr = re.findall("[^a-zA-Z:]([-+]?\d+[\.]?\d*)", str(a))
    icr=re.findall('>[-+]?[0-9].*<',str(a))
    icr=icr[0][1:len(icr[0])-1]
    if(icr.find(',') != -1):
        b=icr.find(',')
        icr_list.append(float(icr[:b]+icr[b+1:]))
        b=-1
    else:
        icr_list.append(float(icr))


# In[14]:


#icr_list


# #### Filtering out all companies with interest coverage ratio of less than 4.

# In[15]:


filtericr=[]
filtercomp=[]
filterlink=[]
filterolink=[]
filtersales=[]
filterder=[]
for i in range(0,len(icr_list)):
    if(icr_list[i]<4):
        filtericr.append(icr_list[i])
        filtercomp.append(companynames[i])
        filterlink.append(links[i])
        filterolink.append(linkso[i])
        filtersales.append(netsales_list[i])
        filterder.append(debtequity_ratio[i])
for i in range(0,len(filtericr)):
    icr_list.remove(filtericr[i])
    companynames.remove(filtercomp[i])
    links.remove(filterlink[i])
    linkso.remove(filterolink[i])   
    netsales_list.remove(filtersales[i])
    debtequity_ratio.remove(filterder[i])


# ## Implementation of Step - 4 :
# **Filtering out all companies with ROE less than 15%**

# * ROE stands for **Return on Equity.**
# * ROE is calculated by using the formula showm below.

# ![roe-return-on-equity.png](attachment:roe-return-on-equity.png)

# * Net Income can be scrapped directly from the website.
# 
# **Scraping Total Income**

# In[16]:


# links for profit loss page is stored in links_pl
links_pl=[]
for i in range(0,len(links)):
    a=links[i].find('balance-sheet')
    b=links[i][:a]+'profit-loss'+links[i][a+13:]
    links_pl.append(b)

ti_list=[]
for i in range(0,len(links_pl)):
    pageold=requests.get(links_pl[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Total Revenue</td>\n.*</td>',about)
    ti=re.findall('>[0-9].*<',str(a))
    ti=ti[0][1:len(ti[0])-1]
    if(ti.find(',') != -1):
        b=ti.find(',')
        ti_list.append(float(ti[:b]+ti[b+1:]))
        b = -1
    else:
        ti_list.append(float(ti))


# * Total Net Income has been scrapped and stored in the ti_list variable.

# In[17]:


#ti_list


# **Scraping Shareholder's Equity Share Capital**

# * Total assests can be extracted directly from the website.
# * Total Liabilities is **Total Non-Current Liabilities + Total Current Liabilities.**
# * Total Non-Current Liabilities and Total Current Liabilities can be extracted from the website and later used in the formula.

# In[18]:


tot_assets=[]
current_lia=[]
noncurrent_lia=[]

for i in range(0,len(links)):
    pageold=requests.get(links[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    
    ''' Scraping Total Assests'''
    
    a=re.findall('<td>Total Assets</td>\n.*</td>',about)
    totas=re.findall('>[-+]?[0-9].*<',str(a))
    totas=totas[0][1:len(totas[0])-1]
    if(totas.find(',') != -1):
        b=totas.find(',')
        tot_assets.append(float(totas[:b]+totas[b+1:]))
        b=-1
    else:
        tot_assets.append(float(totas))
    
    ''' Scrapping Total Non- Current Liabilities.'''
    
    a=re.findall('<td>Total Non-Current Liabilities</td>\n.*</td>',about)
    totncl=re.findall('>[-+]?[0-9].*<',str(a))
    totncl=totncl[0][1:len(totncl[0])-1]
    if(totncl.find(',') != -1):
        b=totncl.find(',')
        noncurrent_lia.append(float(totncl[:b]+totncl[b+1:]))
        b = -1
    else:
        noncurrent_lia.append(float(totncl))
        
    ''' Scrapping Total Current Liabilites. '''
    
    a=re.findall('<td>Total Current Liabilities</td>\n.*</td>',about)
    totcl=re.findall('>[-+]?[0-9].*<',str(a))
    totcl=totcl[0][1:len(totcl[0])-1]
    if(totcl.find(',') != -1):
        b=totcl.find(',')
        current_lia.append(float(totcl[:b]+totcl[b+1:]))
        b=-1
    else:
        current_lia.append(float(totcl))
    


# * The Total Assets is stored in tot_assets variable.

# In[19]:


#tot_assets


# * Total Non-Current Liabilities is stored in noncurrent_lia variable

# In[20]:


#noncurrent_lia


# * Total Current Liabilities is stored in current_lia variable.

# In[21]:


#current_lia


# **Calculating ROE from the scrapped data.**

# In[22]:


# calculating Shareholder's Equity

share_equity = np.array(tot_assets)-(np.array(current_lia) + np.array(noncurrent_lia))


# In[23]:


roe_list = np.array(ti_list)/share_equity 
roe_list = roe_list.tolist()


# In[24]:


# Values are in proportion.
#roe_list


# ### Filtering ROE values.
# 
# * Filtering companies having ROE value less than 15% (0.15).

# In[25]:


filtersales=[]  
filterder=[]
filtericr=[]
filterroe=[]
filtercomp=[]
filterlink=[]
filterolink=[]
for i in range(0,len(roe_list)):
    if(roe_list[i]<0.15):
        filtersales.append(netsales_list[i])
        filterder.append(debtequity_ratio[i])
        filtericr.append(icr_list[i])
        filterroe.append(roe_list[i])
        filtercomp.append(companynames[i])
        filterlink.append(links[i])

for i in range(0,len(filterroe)):
    netsales_list.remove(filtersales[i])
    debtequity_ratio.remove(filterder[i])
    icr_list.remove(filtericr[i])
    roe_list.remove(filterroe[i])
    companynames.remove(filtercomp[i])
    links.remove(filterlink[i])


# ## Implementation of Step - 5 :
# **Filtering out all companies with PE ratio greater than 25 since they are too expensive even for a high-quality company**

# * PE stands for **Price per Earning Ratio.**
# * PE can be calculated by using the formula shown below.

# ![PE_Ratio.png](attachment:PE_Ratio.png)

# * Current Share price is not available directly from the website.
# * It can be calculated using the formula **Price per book value * Book value per Share.**

# ### Scraping for Current Share Price.

# In[26]:


# links for ratio

links_r=[]
for i in range(0,len(links)):
    a=links[i].find('balance-sheet')
    b=links[i][:a]+'ratios'+links[i][a+13:]
    links_r.append(b)

    
pricbv=[]
bkvshr=[]
for i in range(0,len(links_r)):
    pageold=requests.get(links_r[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    
    ''' Scraping for price/book-value. '''
    
    a=re.findall('<td>Price/BV.*</td>\n.*</td>',about)
    pbv=re.findall('>[-+]?[0-9].*<',str(a))
    pbv=pbv[0][1:len(pbv[0])-1]
    if(pbv.find(',') != -1):
        b=pbv.find(',')
        pricbv.append(float(pbv[:b]+pbv[b+1:]))
        b=-1
    else:
        pricbv.append(float(pbv))
        
    ''' Scraping for book-value/share. '''
    
    a=re.findall('<td>Book Value.*/Share.*</td>\n.*</td>',about)
    a=a[0]
    pbvs=re.findall('>[-+]?[0-9].*<',str(a))
    pbvs=pbvs[0][1:len(pbvs[0])-1]
    if(pbvs.find(',') != -1):
        b=pbvs.find(',')
        bkvshr.append(float(pbvs[:b]+pbvs[b+1:]))
        b=-1
    else:
        bkvshr.append(float(pbvs))


# * Price per book value is stored in the pricbv variable.

# In[27]:


#pricbv


# * Book-value per share is store in bkvshr variable.

# In[28]:


#bkvshr


# ### Scraping Earnings Per Share.

# In[29]:


eps_list=[]
for i in range(0,len(links_pl)):
    pageold=requests.get(links_pl[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Basic EPS.*</td>\n.*</td>',about)
    eps=re.findall('>[-+]?[0-9].*<',str(a))
    eps=eps[0][1:len(eps[0])-1]
    if(eps.find(',') != -1):
        b=eps.find(',')
        eps_list.append(float(eps[:b]+eps[b+1:]))
        b=-1
    else:
        eps_list.append(float(eps))


# * Earnings per share is stored in eps_list variable.

# In[30]:


#eps_list


# ### Calculating Price to Equity Ratio (PE) as per the formula.

# In[31]:


pe=np.array(bkvshr)*np.array(pricbv)/np.array(eps_list)
pe=pe.tolist()


# * PE ratio values are store in pe variable.

# In[32]:


#pe


# **Filtering out all companies with PE ratio greater than 25**

# In[33]:


''' Filtering wrt PE values '''
filtersales=[]  
filterder=[]
filtericr=[]
filterroe=[]
filterpe=[]
filtercomp=[]
filterlink=[]
filterolink=[]
for i in range(0,len(pe)):
    if(pe[i]>25):
        filtersales.append(netsales_list[i])
        filterder.append(debtequity_ratio[i])
        filtericr.append(icr_list[i])
        filterroe.append(roe_list[i])
        filterpe.append(pe[i])
        filtercomp.append(companynames[i])
        filterlink.append(links[i])

for i in range(0,len(filterpe)):
    netsales_list.remove(filtersales[i])
    debtequity_ratio.remove(filterder[i])
    icr_list.remove(filtericr[i])
    roe_list.remove(filterroe[i])
    pe.remove(filterpe[i])
    companynames.remove(filtercomp[i])
    links.remove(filterlink[i])


# ## Results:
# * The Benjamin Graham and Warren Buffer filter was implemented on the given companies to filter out the comapanies which are poor in the current stock market.

# **The final list of companies that have passed the filter is made into a dataframe.**

# In[34]:


final=list(zip(companynames,netsales_list,debtequity_ratio,icr_list,roe_list,pe))

filtered_list=pd.DataFrame(final,columns=['Company','Net Sales in cr.','Debt to Equity Ratio','Interest Coverage Ratio','Return On Equity (ROE)','P/E Ratio'])


# In[35]:


print(filtered_list)


# * Storing these companies in an excel sheet.

# In[36]:


filtered_list.to_csv('After_Filteration.csv', index=False)


# ## Note:
# * These values and filteration process is dynamic.
# * The data and values might change based on the company's performance in the stock market.
