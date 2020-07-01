import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
data=pd.read_csv("Companies.csv")
companynames=list(data.iloc[:,0])
links=list(data.iloc[:,1])
import numpy as np
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
    
''' Scrapping Net Sales'''

netsales_list=[]
for i in range(0,len(linkso_pl)):
    pageold=requests.get(linkso_pl[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Net Sales</td>\n.*</td>',about)
    netsales=re.findall('>[-+]?[0-9].*<',str(a))
    netsales=netsales[0][1:len(netsales[0])-1]
    if(netsales.find(',') != -1):
        b=netsales.find(',')
        netsales_list.append(float(netsales[:b]+netsales[b+1:]))
        b=-1
    else:
        netsales_list.append(float(netsales))
        
'''  The Net Sales of each company is saved in the netsales list in Crores.
     Now filtering out the companies with less than 250 cr. Net Sales.'''
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


''' Scraping debt equity Ratio '''

#links for ratio page
linkso_r=[]
for i in range(0,len(linkso)):
    a=linkso[i].find('balance-sheet')
    b=linkso[i][:a]+'ratios'+linkso[i][a+13:]
    linkso_r.append(b)
    
debtequity_ratio=[]
for i in range(0,len(linkso_r)):
    pageold=requests.get(linkso_r[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Debt Equity Ratio</td>\n.*</td>',about)
    der=re.findall('>[-+]?[0-9].*<',str(a))
    if(len(der)==0):
        der=0
    else:
        der=der[0][1:len(der[0])-1]
    debtequity_ratio.append(float(der))

#Companies with Debt Equity Ratio greater than 0.3 are filtered 

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


''' Scraping Interest Coverage Ratio '''
#links for ratio page
linkso_r=[]
for i in range(0,len(linkso)):
    a=linkso[i].find('balance-sheet')
    b=linkso[i][:a]+'ratios'+linkso[i][a+13:]
    linkso_r.append(b)

icr_list=[]
for i in range(0,len(linkso_r)): 
    pageold=requests.get(linkso_r[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Interest Cover</td>\n.*</td>',about)
    icr=re.findall('>[0-9].*<',str(a))
    icr=icr[0][1:len(icr[0])-1]
    if(len(icr)>6):
        a=icr.find(',')
        icr_list.append(float(icr[:a]+icr[a+1:]))
    else:
        icr_list.append(float(icr))


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
    
    
''' Scraping Total Income'''

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
    if(len(ti)>6):
        a=ti.find(',')
        ti_list.append(float(ti[:a]+ti[a+1:]))
    else:
        ti_list.append(float(ti))

''' Scraping Equity Share Capital'''
tot_assets=[]
current_lia=[]
noncurrent_lia=[]

for i in range(0,len(links)):
    pageold=requests.get(links[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Total Assets</td>\n.*</td>',about)
    totas=re.findall('>[0-9].*<',str(a))
    totas=totas[0][1:len(totas[0])-1]
    if(len(totas)>6):
        a=totas.find(',')
        tot_assets.append(float(totas[:a]+totas[a+1:]))
    else:
        tot_assets.append(float(totas))
    
    a=re.findall('<td>Total Non-Current Liabilities</td>\n.*</td>',about)
    totncl=re.findall('>[0-9].*<',str(a))
    totncl=totncl[0][1:len(totncl[0])-1]
    if(len(totncl)>6):
        a=totncl.find(',')
        noncurrent_lia.append(float(totncl[:a]+totncl[a+1:]))
    else:
        noncurrent_lia.append(float(totncl))
    
    a=re.findall('<td>Total Current Liabilities</td>\n.*</td>',about)
    totcl=re.findall('>[0-9].*<',str(a))
    totcl=totcl[0][1:len(totcl[0])-1]
    if(len(totcl)>6):
        a=totcl.find(',')
        current_lia.append(float(totcl[:a]+totcl[a+1:]))
    else:
        current_lia.append(float(totcl))
    
roe_list=np.array(ti_list)/(np.array(tot_assets)-np.array(current_lia)-np.array(noncurrent_lia))
roe_list=roe_list.tolist()



''' Scraping for PE'''

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
    a=re.findall('<td>Price/BV.*</td>\n.*</td>',about)
    pbv=re.findall('>[0-9].*<',str(a))
    pbv=pbv[0][1:len(pbv[0])-1]
    if(len(pbv)>6):
        a=pbv.find(',')
        pricbv.append(float(pbv[:a]+pbv[a+1:]))
    else:
        pricbv.append(float(pbv))
        
    a=re.findall('<td>Book Value.*/Share.*</td>\n.*</td>',about)
    a=a[0]
    pbvs=re.findall('>[0-9].*<',str(a))
    pbvs=pbvs[0][1:len(pbvs[0])-1]
    if(len(pbvs)>6):
        a=pbvs.find(',')
        bkvshr.append(float(pbvs[:a]+pbvs[a+1:]))
    else:
        bkvshr.append(float(pbvs))

eps_list=[]
for i in range(0,len(links_pl)):
    pageold=requests.get(links_pl[i])
    soup = BeautifulSoup(pageold.text, 'html.parser')
    about=soup.findAll('table')
    about=str(about)
    a=re.findall('<td>Basic EPS.*</td>\n.*</td>',about)
    eps=re.findall('>[0-9].*<',str(a))
    eps=eps[0][1:len(eps[0])-1]
    if(len(eps)>6):
        a=eps.find(',')
        eps_list.append(float(eps[:a]+eps[a+1:]))
    else:
        eps_list.append(float(eps))


pe=np.array(bkvshr)*np.array(pricbv)/np.array(eps_list)
pe=pe.tolist()

''' Filter PE values '''
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
    

final=list(zip(companynames,netsales_list,debtequity_ratio,icr_list,roe_list,pe))

filtered_list=pd.DataFrame(final,columns=['Company','Net Sales in cr.','Debt to Equity Ratio','Interest Coverage Ratio','Return On Equity (ROE)','P/E Ratio'])

print(filtered_list)
