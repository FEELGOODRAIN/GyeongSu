#!/usr/bin/env python
# coding: utf-8

# In[221]:


get_ipython().system('pip install geopandas')

import gc
import glob
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = ('C:/k_digital/Project Data')

plt.rc('font', family='Malgun Gothic')


# In[222]:


# 지하철 휠체어 리프트 보유 역 비율 분석


# In[223]:


sub = pd.read_csv(path + '/서울시 지하철 역사 노약자 장애인 편의시설 현황.csv', encoding = 'euc-kr')


# In[224]:


sub


# In[225]:


# 9호선(*단계) 를 9호선으로 수정


# In[226]:


guho = sub['호선'].str[:3] == '9호선'


# In[227]:


sub.loc[guho, '호선'] = '9호선'


# In[228]:


sub


# In[229]:


# 사용하지 않는 컬럼 제거


# In[230]:


del sub['역명']
del sub['에스컬레이터(E/S)']
del sub['수평자동보도(M/W)']
del sub['엘리베이터(E/V)']

sub


# In[231]:


# 9호선 제거
sub = sub[~sub['호선'].str.contains('9호선', na=False)]


# In[232]:


# 데이터형식 확인
sub.info()


# In[234]:


# 컬럼 명 변경
sub.rename(columns = {'휠체어리프트(W/L)':'WL'}, inplace = True)


# In[235]:


# 도입 여부만 확인하기 위해 도입 대수 1 초과 값을 1로 수정
sub['WL'][sub['WL'] > 1] = 1


# In[236]:


# 휠체어리프트 설치 역 수
sub_wl = sub['WL'].sum()
sub_wl


# In[279]:


# 호선별 설치 역 수 
wl = sub.groupby(by = '호선').sum()
wl


# In[89]:


# 지하철역 데이터 로드


# In[263]:


sta = pd.read_excel(path + '/서울교통공사 노선별 지하철역 정보.xlsx')


# In[264]:


# 사용하지 않는 컬럼 제거
del sta['전철역코드']
del sta['외부코드']
del sta['전철명명(중문)']
del sta['전철명명(일문)']
del sta['전철명명(영문)']
sta


# In[265]:


# 호선 컬럼에 '호선'이 포함된 행만 추출
sta = sta[sta['호선'].str.contains('호선', na=False)]


# In[266]:


# '인천'이 포함된 행 제거
# ~를 이용해 조건을 반대로 만듦
sta = sta[~sta['호선'].str.contains('인천', na=False)]


# In[267]:


# 9호선 제거
sta = sta[~sta['호선'].str.contains('09호선', na=False)]


# In[268]:


sta


# In[269]:


# 중복역 제거
st = sta.drop_duplicates(subset=['전철역명'])
st


# In[270]:


# 역 개수를 세기 위한 열 생성
st['count'] = 1
st


# In[278]:


# 호선별 역 수 추출
st = st.groupby(by = '호선').sum()
st


# In[277]:


# 01호선, 02호선 ... 을 1호선, 2호선으로 변경

st['호선'] = st['호선'].str[1:]
st


# In[283]:


# 호선 컬럼 기준으로 데이터프레임 결합
wlst = pd.merge(wl, st, on = '호선')
wlst


# In[289]:


wlst['per'] = round(wlst['WL'] / wlst['count'], 3) * 100
wlst


# In[292]:


wlst['ho'] = wlst.index
wlst


# In[297]:


plt.bar(wlst['ho'], wlst['per'])
plt.xlabel('호선')
plt.ylabel('설치 비율(%)')
plt.title('호선별 휠체어리프트 설치 비율')

plt.show()


# In[ ]:




