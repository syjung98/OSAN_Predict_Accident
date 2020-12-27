# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # 오산시 어린이 교통사고 위험지역 도출 

# ## 1. Data 불러오기

#12/24 GeoSeries 추가
from geoband.API import *
import pandas as pd
import folium
import json
import geopandas as gpd
from geojson import Feature, FeatureCollection, Point, dump
from geopandas import GeoSeries
from shapely.geometry import Point
import matplotlib.pyplot as plt
import pydeck as pdk
import shapely
import jenkspy
import numpy as np
plt.rc("font", family = "Malgun Gothic")
# %matplotlib inline
import warnings
warnings.filterwarnings(action='ignore') 

df1_parking=GetCompasData('SBJ_2012_001', '1', '1.오산시_주정차단속(2018~2020).csv')
df2_grid_accident=GetCompasData('SBJ_2012_001', '2', '2.오산시_어린이교통사고_격자.geojson')
df3_grid_car_enrollment=GetCompasData('SBJ_2012_001', '3', '3.오산시_차량등록현황_격자.geojson')
df4_pop=GetCompasData('SBJ_2012_001', '4', '4.오산시_연령별_거주인구격자(총인구).geojson')
df5_junior_pop=GetCompasData('SBJ_2012_001', '5', '5.오산시_연령별_거주인구격자(유소년).geojson')
df6_product_pop=GetCompasData('SBJ_2012_001', '6', '6.오산시_연령별_거주인구격자(생산가능인구).geojson')
df7_senior_pop=GetCompasData('SBJ_2012_001', '7', '7.오산시_연령별_거주인구격자(고령).geojson')
df8_floating_pop=GetCompasData('SBJ_2012_001', '8', '8.오산시_유동인구(2019).csv')
df9_protection_area=GetCompasData('SBJ_2012_001', '9', '9.오산시_어린이보호구역.csv')
df10_school=GetCompasData('SBJ_2012_001', '10', '10.오산시_학교위치정보.csv')
df11_elementary_district=GetCompasData('SBJ_2012_001', '11', '11.오산시_초등학교_통학구.geojson')
df12_middle_district=GetCompasData('SBJ_2012_001', '12', '12.오산시_중학교_학군.geojson')
df13_kinder=GetCompasData('SBJ_2012_001', '13', '13.오산시_어린이집_유치원현황.csv')
df14_weather=GetCompasData('SBJ_2012_001', '14', '14.오산시_기상데이터(2010~2019).csv')
df15_traffic_cctv=GetCompasData('SBJ_2012_001', '15', '15.오산시_무인교통단속카메라.csv')
df16_road_sign=GetCompasData('SBJ_2012_001', '16', '16.오산시_도로안전표지표준데이터.csv')
df17_crosswalk=GetCompasData('SBJ_2012_001', '17', '17.오산시_횡단보도.geojson')
df18_speed_bump=GetCompasData('SBJ_2012_001', '18', '18.오산시_과속방지턱표준데이터.csv')
df19_traffic_light=GetCompasData('SBJ_2012_001', '19', '19.오산시_신호등.geojson')
df20_cctv=GetCompasData('SBJ_2012_001', '20', '20.오산시_CCTV설치현황.csv')
df21_sidewalk=GetCompasData('SBJ_2012_001', '21', '21.오산시_인도.geojson')
df22_bus_stop=GetCompasData('SBJ_2012_001', '22', '22.오산시_버스정류장.csv')
df23_road=GetCompasData('SBJ_2012_001', '23', '23.오산시_상세도로망_LV6.geojson')
df24_traffic=GetCompasData('SBJ_2012_001', '24', '24.평일_전일,시간대별_오산시_추정교통량_Level6.csv')
df25_traffic_frequency=GetCompasData('SBJ_2012_001', '25', '25.평일_전일_오산시_혼잡빈도강도_Level6.csv')
df26_traffic_time=GetCompasData('SBJ_2012_001', '26', '26.평일_전일_오산시_혼잡시간강도_Level6.csv')
df27_building=GetCompasData('SBJ_2012_001', '27', '27.오산시_도로명주소_건물.geojson')
df28_grid_building=GetCompasData('SBJ_2012_001', '28', '28.오산시_건물연면적_격자.geojson')
df29_sports=GetCompasData('SBJ_2012_001', '29', '29.오산시_체육시설현황.csv')
df30_academy=GetCompasData('SBJ_2012_001', '30', '30.오산시_학원_및_교습소_현황.csv')
df31_le_sig=GetCompasData('SBJ_2012_001', '31', '31.오산시_법정경계(시군구).geojson')
df32_admin_emd=GetCompasData('SBJ_2012_001', '32', '32.오산시_행정경계(읍면동).geojson')
df33_legal_emd=GetCompasData('SBJ_2012_001', '33', '33.오산시_법정경계(읍면동).geojson')
df34_cadastral_map=GetCompasData('SBJ_2012_001', '34', '34.오산시_지적도.geojson')

df1_parking=pd.read_csv('1.오산시_주정차단속(2018~2020).csv')
df2_grid_accident=gpd.read_file('2.오산시_어린이교통사고_격자.geojson')
df3_grid_car_enrollment=gpd.read_file('3.오산시_차량등록현황_격자.geojson')
df4_pop=gpd.read_file('4.오산시_연령별_거주인구격자(총인구).geojson')
df5_junior_pop=gpd.read_file('5.오산시_연령별_거주인구격자(유소년).geojson')
df6_product_pop=gpd.read_file('6.오산시_연령별_거주인구격자(생산가능인구).geojson')
df7_senior_pop=gpd.read_file('7.오산시_연령별_거주인구격자(고령).geojson')
df8_floating_pop=pd.read_csv('8.오산시_유동인구(2019).csv')
df9_protection_area=pd.read_csv('9.오산시_어린이보호구역.csv')
df10_school=pd.read_csv('10.오산시_학교위치정보.csv')
df11_elementary_district=gpd.read_file('11.오산시_초등학교_통학구.geojson')
df12_middle_district=gpd.read_file('12.오산시_중학교_학군.geojson')
df13_kinder=pd.read_csv('13.오산시_어린이집_유치원현황.csv')
df14_weather=pd.read_csv('14.오산시_기상데이터(2010~2019).csv')
df15_traffic_cctv=pd.read_csv('15.오산시_무인교통단속카메라.csv')
df16_road_sign=pd.read_csv('16.오산시_도로안전표지표준데이터.csv')
df17_crosswalk=gpd.read_file('17.오산시_횡단보도.geojson')
df18_speed_bump=pd.read_csv('18.오산시_과속방지턱표준데이터.csv')
df19_traffic_light=gpd.read_file('19.오산시_신호등.geojson')
df20_cctv=pd.read_csv('20.오산시_CCTV설치현황.csv')
df21_sidewalk=gpd.read_file('21.오산시_인도.geojson')
df22_bus_stop=pd.read_csv('22.오산시_버스정류장.csv')
df23_road=gpd.read_file('23.오산시_상세도로망_LV6.geojson')
df24_traffic=pd.read_csv('24.평일_전일,시간대별_오산시_추정교통량_Level6.csv')
df25_traffic_frequency=pd.read_csv('25.평일_전일_오산시_혼잡빈도강도_Level6.csv')
df26_traffic_time=pd.read_csv('26.평일_전일_오산시_혼잡시간강도_Level6.csv')
df27_building=gpd.read_file('27.오산시_도로명주소_건물.geojson')
df28_grid_building=gpd.read_file('28.오산시_건물연면적_격자.geojson')
df29_sports=pd.read_csv('29.오산시_체육시설현황.csv')
df30_academy=pd.read_csv('30.오산시_학원_및_교습소_현황.csv')
df31_le_sig=gpd.read_file('31.오산시_법정경계(시군구).geojson')
df32_admin_emd=gpd.read_file('32.오산시_행정경계(읍면동).geojson')
df33_legal_emd=gpd.read_file('33.오산시_법정경계(읍면동).geojson')

# 좌표계 설정
df1_parking.crs = {'init':'epsg:4326'}
df2_grid_accident.crs = {'init':'epsg:4326'}
df3_grid_car_enrollment.crs = {'init':'epsg:4326'}
df4_pop.crs = {'init':'epsg:4326'}
df5_junior_pop.crs = {'init':'epsg:4326'}
df6_product_pop.crs = {'init':'epsg:4326'}
df7_senior_pop.crs = {'init':'epsg:4326'}
df8_floating_pop.crs = {'init':'epsg:4326'}
df9_protection_area.crs = {'init':'epsg:4326'}
df10_school.crs = {'init':'epsg:4326'}
df11_elementary_district.crs = {'init':'epsg:4326'}
df12_middle_district.crs = {'init':'epsg:4326'}
df13_kinder.crs = {'init':'epsg:4326'}
df14_weather.crs = {'init':'epsg:4326'}
df15_traffic_cctv.crs = {'init':'epsg:4326'}
df16_road_sign.crs = {'init':'epsg:4326'}
df17_crosswalk.crs = {'init':'epsg:4326'}
df18_speed_bump.crs = {'init':'epsg:4326'}
df19_traffic_light.crs = {'init':'epsg:4326'}
df20_cctv.crs = {'init':'epsg:4326'}
df21_sidewalk.crs = {'init':'epsg:4326'}
df22_bus_stop.crs = {'init':'epsg:4326'}
df23_road.crs = {'init':'epsg:4326'}
df24_traffic.crs = {'init':'epsg:4326'}
df25_traffic_frequency.crs = {'init':'epsg:4326'}
df26_traffic_time.crs = {'init':'epsg:4326'}
df27_building.crs = {'init':'epsg:4326'}
df28_grid_building.crs = {'init':'epsg:4326'}
df29_sports.crs = {'init':'epsg:4326'}
df30_academy.crs = {'init':'epsg:4326'}
df31_le_sig.crs = {'init':'epsg:4326'}
df32_admin_emd.crs = {'init':'epsg:4326'}
df33_legal_emd.crs = {'init':'epsg:4326'}


# ## 2. 분석 기초 함수

# ### 1) pydeck 사용을 위해 geometry의 Point, Multilinestring, Multipolygon을 coordinates로 바꿔주기 위한 함수 선언

# +
# 12/25 창균 추가
def POINT_to_coordinates(geo_data):
    geo_data['lat'] = geo_data['geometry'].apply(lambda coord: coord.y)
    geo_data['lon'] = geo_data['geometry'].apply(lambda coord: coord.x)
    return geo_data

# 사용 예
# df19_traffic_light = POINT_to_coordinates(df19_traffic_light)


# +
# 12/25 창균 추가
def MULTILINESTRING_to_coordinates(line_string):
    if isinstance(line_string, shapely.geometry.linestring.LineString):
        lon, lat = line_string.xy
        return [[x, y] for x, y in zip(lon, lat)]
    elif isinstance(line_string, shapely.geometry.multilinestring.MultiLineString):
        ret = []
        for i in range(len(line_string)):
            lon, lat = line_string[i].xy
            for x, y in zip(lon, lat):
                ret.append([x, y])
        return ret
    
# 사용 예
# df23_road['coordinates'] = df23_road['geometry'].apply(MULTILINESTRING_to_coordinates)
# df23_road = pd.DataFrame(df23_road) # geopanadas 가 아닌 pandas 의 데이터프레임으로 꼭 바꿔줘야 합니다.


# +
# 12/25 창균 추가
def MULTIPOLYGON_to_coordinates(x):
    lon, lat = x[0].exterior.xy
    return [[x, y] for x, y in zip(lon, lat)]

# 사용 예
# df_osan_grid['coordinates'] = df_osan_grid['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df_osan_grid = pd.DataFrame(df_osan_grid) # geopanadas 가 아닌 pandas 의 데이터프레임으로 꼭 바꿔줘야 합니다.


# -

# ### 2) 각각의 df의 lon, lat을 geometry의 point로 변환
# > 공간분석을 위해 pd.DataFrame을 gpd.GeoDataFrame으로 바꿔주는 함수

# 12/24 정민 수정사항
def location_to_point(df):
    point_df = gpd.points_from_xy(df.lon, df.lat)
    point_df = GeoSeries(point_df)
    
    col = df.columns
    
    loc_df = gpd.GeoDataFrame(df[col], geometry = point_df)
    
    return loc_df


# ### 3) 지도 그리는 함수

def drawing_Choro(df, osan_grid, title, legend):
    center=[37.1498, 127.0772]
    # 맵이 center 에 위치하고, zoom 레벨은 16로 시작하는 맵 m을 만듭니다.
    m1 = folium.Map(
        location=center,
        zoom_start=13,
        tiles='http://api.vworld.kr/req/wmts/1.0.0/26BFD173-330E-3D54-9C39-895DDD8F23B3/Base/{z}/{y}/{x}.png',
        attr='My Data Attribution'
    )

    # Choropleth 레이어를 만들고, 맵 m에 추가합니다.
    folium.Choropleth(
        geo_data=osan_grid,
        data=df,
        columns=('gid', 'time'),
        key_on='feature.properties.gid',
        legend_name = legend,
        fill_color='PuBuGn',
        line_opacity = 0.2,
    ).add_to(m1)

    # 맵 m을 출력합니다.
    m1.save("{0}.html".format(title))


# ### 4) 격자내 존재하는 좌표 개수의 합을 구하는 함수

def sjoin(grid_info,df, new_col_name, option = 'contains'):
    joined= gpd.sjoin(grid_info,df, op=option)
    result = joined.groupby('gid').size()
    result = result.to_frame().reset_index()
    grid_info=pd.merge(grid_info,result, how='outer',on='gid')
    
    grid_info = grid_info.rename(columns = {0:new_col_name})
    grid_info=grid_info.fillna(0)
    
    return grid_info


# ## 3. 목적에 맞는 데이터 전처리

# ### 기본 그리드 생성

# +
#지도에 맵핑할 격자들 만들기
# 12/25 창균 추가
df_osan_grid=df4_pop.drop('val',axis=1)

# geometry to coordinates
df_osan_grid['coordinates'] = df_osan_grid['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df_osan_grid = pd.DataFrame(df_osan_grid)

df_osan_grid.head(5)
# -

# ### df1 오산시 주정차 단속

# +
#df1 오산시 주정차 단속
# 12/25 창균 추가
df1_parking.columns=['date','parking_location','admin_area','school_zone',
                 'lon','lat','parking_type']

#스쿨존에 해당하면 1 아니면 0
df1_parking.loc[df1_parking['school_zone']=='N','school_zone']=0
df1_parking.loc[df1_parking['school_zone']=='Y','school_zone']=1

# 오산시 유탑유블레스 남측 좌표 삽입 (널 처리)
df1_parking["lon"].fillna(127.072291, inplace = True)
df1_parking["lat"].fillna(37.141363, inplace = True)

df1_parking = location_to_point(df1_parking)
df1_parking.head()
# -

# ### df4 인구, df5 유소년 인구, df6 생산가능인구, df7 노인 인구 - 인구수 변수 이름 변경 및 널처리

# +
#나중에 비율 구할때 써야됨
#val값에 null은 측정이 안된 곳이기에 0으로 처리해줌-SY
# 12/25 창균 추가
df4_pop=df4_pop.rename(columns={'val':'pop_val'})
df4_pop=df4_pop.fillna(0)
# geometry to coordinates
df4_pop['coordinates'] = df4_pop['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df4_pop = pd.DataFrame(df4_pop)

df5_junior_pop=df5_junior_pop.rename(columns={'val':'junior_val'})
df5_junior_pop=df5_junior_pop.fillna(0)
# geometry to coordinates
df5_junior_pop['coordinates'] = df5_junior_pop['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df5_junior_pop = pd.DataFrame(df5_junior_pop)

df6_product_pop=df6_product_pop.rename(columns={'val':'product_val'})
df6_product_pop=df6_product_pop.fillna(0)
# geometry to coordinates
df6_product_pop['coordinates'] = df6_product_pop['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df6_product_pop = pd.DataFrame(df6_product_pop)

df7_senior_pop=df7_senior_pop.rename(columns={'val':'senior_val'})
df7_senior_pop=df7_senior_pop.fillna(0)
# geometry to coordinates
df7_senior_pop['coordinates'] = df7_senior_pop['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df7_senior_pop = pd.DataFrame(df7_senior_pop)

# +
# 정민 수정사항(12/21)
# 오산시 격자별 유소년 인구수/총 인구수 데이터 전처리
df_junior_ratio_pop = df5_junior_pop.merge(df4_pop, on ='gid')
df_junior_ratio_pop = df_junior_ratio_pop.drop(['geometry_x', 'coordinates_x'], axis = 1)
df_junior_ratio_pop.columns = ['gid', 'junior_val', 'pop_val', 'geometry', 'coordinates']

# 비율 컬럼 생성
df_junior_ratio_pop['junior_ratio'] = df_junior_ratio_pop['junior_val']/df_junior_ratio_pop['pop_val'] * 100
df_junior_ratio_pop['junior_ratio'].value_counts()
df_junior_ratio_pop=df_junior_ratio_pop.fillna(0)

# geometry to coordinates
df_junior_ratio_pop['coordinates'] = df_junior_ratio_pop['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df_junior_ratio_pop = pd.DataFrame(df_junior_ratio_pop)

df_junior_ratio_pop
# -

# 주니어 인구비율 분포확인
# %matplotlib inline
df_junior_ratio_pop["junior_ratio"].plot(xlabel = "gid", ylabel = "junior population ratio to total population")

# ### df8 유동인구

# +
#합치는 코드 있어서 한번만 돌려야됨
# location_to_point 함수에서 위도 경도를 point로 가져오려면 각 df의 특성에 맞는 이름인 df_lat, df_lon가 아니라 lat, lon으로 정해준다.
#유동인구
df_col_list=list(df8_floating_pop)
df_col_list_all=df_col_list[3:]
df_col_list_14_20=df_col_list[17:23]
#모든 시간대 유동인구
df8_floating_pop['all']=df8_floating_pop[df_col_list_all].sum(axis=1)
#사고가 가장 많이 일어나는 14~20
df8_floating_pop['14_20']=df8_floating_pop[df_col_list_14_20].sum(axis=1)
df8_floating_pop=df8_floating_pop.rename(columns={'STD_YM':'YM','lon':'lon','lat':'lat'})
#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df8_floating_pop = location_to_point(df8_floating_pop)

df8_floating_pop
# -

# ### df9 어린이 보호구역

# +
#어린이 보호구역
df9_protection_area.columns=['protection_type','protection_name','protection_cctv',
                         'protection_cctv_count','width','lon','lat']
#cctv 있으면 1 없으면 0
df9_protection_area.loc[df9_protection_area['protection_cctv']=='N','protection_cctv']=0
df9_protection_area.loc[df9_protection_area['protection_cctv']=='Y','protection_cctv']=1

# object typecasting to int
df9_protection_area['protection_cctv'] = df9_protection_area['protection_cctv'].astype('int')

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df9_protection_area = location_to_point(df9_protection_area)

df9_protection_area
# -

# ### df10 학교 위치정보

# +
# 학교 위치정보
# 중학교와 고등학교는 비대상으로 drop 처리
a=df10_school.loc[df10_school['학교구분'].isin(['고등학교','중학교'])].index
df10_school=df10_school.drop(a)
df10_school.columns=['school_type','school_name','lon','lat']
df10_school = df10_school.reset_index(drop=True)

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df10_school = location_to_point(df10_school)

df10_school
# -

# ### df11 초등학교 통학구

# +
# 초등학교 통학구
#type이 0이면 단독 통학구 1이면 다중 통학구로 예상됨
df11_elementary_district.columns=['ed_objectid','district_id','ed_name','ed_type','geometry']
df11_elementary_district['coordinates'] = df11_elementary_district['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df11_elementary_district = pd.DataFrame(df11_elementary_district)

# object typecasting to int
df11_elementary_district['ed_type'] = df11_elementary_district['ed_type'].astype('int')
df11_elementary_district.head()
# -

# ### df13 어린이집 유치원 현황

# +
# 어린이집 유치원현황
df13_kinder=df13_kinder.drop('시설타입',axis=1)
df13_kinder.columns=['kinder_type','kinder_name','lon','lat']

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df13_kinder = location_to_point(df13_kinder)

df13_kinder
# -

# ### df15 무인교통 단속 카메라

# +
#무인교통 단속 카메라
df15_traffic_cctv=df15_traffic_cctv.drop(['도로노선방향','단속구분'],axis=1)
df15_traffic_cctv.columns=['tc_road_name','tc_location_name','lon','lat']

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df15_traffic_cctv = location_to_point(df15_traffic_cctv)

df15_traffic_cctv
# -

# ### df16 도로안전표지 표준 데이터

# +
#도로안전표지 표준데이터
df16_road_sign.columns=['road_sign_num','road_sign_type','lon','lat']

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df16_road_sign = location_to_point(df16_road_sign)

df16_road_sign
# -

# ### df17 횡단보도

#횡단보도
## 창균 추가 수정 (12.22)
df17_crosswalk.columns=['crosswalk_objectid','geometry']
df17_crosswalk

# ### df18 과속방지턱 표준데이터

# +
#과속방지턱표준데이터
df18_speed_bump.columns=['bump_road_name','bump_location_name','bump_height','bump_width',
                   'bump_length','bump_sep','bump_continue','lon','lat']
#과속방지턱 보차분리여부,연속형 여부 0,1로 변환
df18_speed_bump.loc[df18_speed_bump['bump_sep']=='N','bump_sep']=0
df18_speed_bump.loc[df18_speed_bump['bump_sep']=='Y','bump_sep']=1
df18_speed_bump.loc[df18_speed_bump['bump_continue']=='N','bump_continue']=0
df18_speed_bump.loc[df18_speed_bump['bump_continue']=='Y','bump_continue']=1

# object typecasting to int
df18_speed_bump['bump_sep'] = df18_speed_bump['bump_sep'].astype('int')
df18_speed_bump['bump_continue'] = df18_speed_bump['bump_continue'].astype('int')

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df18_speed_bump = location_to_point(df18_speed_bump)

df18_speed_bump
# -

# ### df19 신호등

# +
#신호등
## 창균 추가 수정 (12.22)
## 창균 추가 수정 (12/25)
df19_traffic_light.columns=['traffic_light_objectid','geometry']

# geometry to coordinates
df19_traffic_light = POINT_to_coordinates(df19_traffic_light)
# df19_traffic_light = pd.DataFrame(df19_traffic_light)

df19_traffic_light
# -

# ### df20 cctv

# +
#cctv
# location_to_point 함수에서 위도 경도를 point로 가져오려면 각 df의 특성에 맞는 이름인 df_lat, df_lon가 아니라 lat, lon으로 정해준다.
# cctv_type A: 방범 B:도시공원 C:어린이보호 D:차량방범
df20_cctv.columns=['cctv_type','cctv_road_name','lat','lon']
#cctv_lat,lon에서 중복적으로 결측값이 나와서 drop, road_name도 null값 nan으로 처리-SY
df20_cctv=df20_cctv.drop([500,567],axis=0)
df20_cctv=df20_cctv.fillna('NaN')

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df20_cctv = location_to_point(df20_cctv)

df20_cctv
# -

# ### df21 인도

# +
#인도
df21_sidewalk=df21_sidewalk.drop('QUAL',axis=1)
df21_sidewalk.columns=['sidewalk_id','sidewalk_bicycle',
                  'sidewalk_type','geometry']
#자전거 도로유무 BYC001이 있고 나머지가 없음
df21_sidewalk.loc[df21_sidewalk['sidewalk_bicycle']=='BYC001','sidewalk_bicycle']=1
df21_sidewalk.loc[df21_sidewalk['sidewalk_bicycle']=='BYC002','sidewalk_bicycle']=0

# object typecasting to int
df21_sidewalk['sidewalk_bicycle'] = df21_sidewalk['sidewalk_bicycle'].astype('int')

# geometry to coordinates
df21_sidewalk['coordinates'] = df21_sidewalk['geometry'].apply(MULTILINESTRING_to_coordinates)
# df21_sidewalk = pd.DataFrame(df21_sidewalk)

df21_sidewalk
# -

# ### df22 버스 정류장

# +
# 버스 정류장
# location_to_point 함수에서 위도 경도를 point로 가져오려면 각 df의 특성에 맞는 이름인 df_lat, df_lon가 아니라 lat, lon으로 정해준다.
## 창균 추가 수정 (12.22)
df22_bus_stop.columns=['bus_stop_id','bus_stop_name','lon','lat']

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df22_bus_stop = location_to_point(df22_bus_stop)

df22_bus_stop
# -

# ### df23 상세 도로망

# +
#상세도로망
#road_name null값 nan으로 처리-SY
# 고속도로 제거
df23_road=df23_road[df23_road['road_rank'].isin(['103','105','106','107'])]
# 불필요한 컬럼 제거
df23_road=df23_road.drop('facil_name',axis=1)
# 널값 처리
df23_road=df23_road.fillna('NaN')

# object typecasting to int
df23_road = df23_road.apply(pd.to_numeric, errors = 'ignore')
# 뒤에 교통량 분석을 위해 id는 str으로 타입 캐스팅
df23_road['link_id'] = df23_road['link_id'].astype(str)

# geometry to coordinates
df23_road['coordinates'] = df23_road['geometry'].apply(MULTILINESTRING_to_coordinates)
# df23_road = pd.DataFrame(df23_road)

df23_road
# -

# ### df24 평일 시간대별 추정 교통량

# +
#평일 시간대별 추정교통량
# road_name null값 nan으로 처리-SY
# 고속도로 제외한 값 삽입
df24_traffic=df24_traffic[df24_traffic['도로등급'].isin(['103','105','106','107'])]
# 필요없는 컬럼 삭제
df24_traffic=df24_traffic.drop(['평일주말','시도명','시군구명'],axis=1)
# 널값 NaN 처리
df24_traffic=df24_traffic.fillna('NaN')

df24_traffic.columns=['link_id','road_rank','link_length','road_name',
               'emd_name','time','all_traffic','car_traffic',
                'bus_traffic','freight_car_traffic']
#traffic의 time column에서 dtype이 통일이 되어 있지 않아 str로 통일함-SY
df24_traffic['time']=df24_traffic['time'].apply(str)

df24_traffic
# -

# ### df25 평일 혼잡빈도강도

# 평일 혼잡빈도강도
#road_name null값 nan으로 처리-SY
df25_traffic_frequency=df25_traffic_frequency[df25_traffic_frequency['도로등급'].isin(['103','105','106','107'])]
df25_traffic_frequency=df25_traffic_frequency.drop(['시도명','시군구명','평일주말','시간적범위'],axis=1)
df25_traffic_frequency=df25_traffic_frequency.fillna('NaN')
df25_traffic_frequency.columns=['link_id','road_rank','link_length','road_name',
                          'emd_name','frequency']
df25_traffic_frequency['link_id'] = df25_traffic_frequency['link_id'].astype(str)
df25_traffic_frequency

# ### df26 평일 혼잡시간강도

#평일 혼잡시간강도
#road_name null값 nan으로 처리-SY
df26_traffic_time=df26_traffic_time[df26_traffic_time['도로등급'].isin(['103','105','106','107'])]
df26_traffic_time=df26_traffic_time.drop(['시도명','시군구명','평일주말','시간적범위'],axis=1)
df26_traffic_time=df26_traffic_time.fillna('NaN')
df26_traffic_time.columns=['link_id','road_rank','link_length','road_name',
                          'emd_name','time']
df26_traffic_time['link_id'] = df26_traffic_time['link_id'].astype(str)
df26_traffic_time

# ### df27 도로명주소 건물

# +
# 창균 수정 (12/26)
#건물
# 불필요한 컬럼 삭제
df27_building=df27_building.drop(['UND_FLO_CO','GRO_FLO_CO','BULD_NM_DC','BULD_NM'],axis=1)

# object typecasting to int
df27_building = df27_building.apply(pd.to_numeric, errors = 'ignore')

df27_building['coordinates'] = df27_building['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df27_building = pd.DataFrame(df27_building)

df27_building
# -

# ### df28 격자별 건물 연면적

# +
# 창균 수정 (12/26)
#격자별 건물연면적
#val값의 null은 측정이 안된 값이라 0으로 처리-SY
df28_grid_building.columns=['gid','grid_building_val','geometry']
df28_grid_building=df28_grid_building.fillna(0)

# geometry to coordinates
df28_grid_building['coordinates'] = df28_grid_building['geometry'].apply(MULTIPOLYGON_to_coordinates)
# df28_grid_building = pd.DataFrame(df28_grid_building)

df28_grid_building
# -

# ### df29 체육시설

# +
#체육시설
df29_sports.columns=['sports_type','lon','lat']

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df29_sports = location_to_point(df29_sports)

df29_sports
# -

# ### df30 학원 교습소

# +
#학원,교습소
df30_academy=df30_academy.drop('교습과정명',axis=1)
df30_academy.columns=['academy_type','lon','lat']
df30_academy=df30_academy.fillna('NaN')

#lat, lon to point & pd.DataFrame to gpd.GeodataFrame
df30_academy = location_to_point(df30_academy)

df30_academy
# -

# # 4. 분석을 위한 추가 처리

# ## 1) 격차별 데이터

#각 격자에 교통사고 횟수 concat
df_osan_grid_info=pd.concat([df_osan_grid,df2_grid_accident['accident_cnt']],axis=1)
#각 격자에 거주인구수 concat
df_osan_grid_info=pd.concat([df_osan_grid_info,df4_pop['pop_val']],axis=1)
#각 격자에 유소년 거주인구수 concat
df_osan_grid_info=pd.concat([df_osan_grid_info,df5_junior_pop['junior_val']],axis=1)
#각 격자에 건물 면적 concat
df_osan_grid_info=pd.concat([df_osan_grid_info,df28_grid_building['grid_building_val']],axis=1)
df_osan_grid_info

# ## 2) 교통량 분석

# +
# 14~20시에 해당하는 교통량과 상세도로망의 데이터 merge
df_traffic_1420=df24_traffic[df24_traffic['time'].isin(['14','15','16','17,''18','19'])]
df_traffic_road = []
for i in df23_road['link_id']:
    df_traffic_road.append([i,sum(df_traffic_1420[df_traffic_1420['link_id'].apply(str).str.contains(i)]['all_traffic']),
                         sum(df_traffic_1420[df_traffic_1420['link_id'].apply(str).str.contains(i)]['freight_car_traffic'])])
    
df_traffic_road=pd.DataFrame(df_traffic_road)
df_traffic_road.columns=['link_id','all_traffic','freight_car_traffic']

#road_info에 모든 도로의 교통량,시간복잡도,빈도복잡도의 데이터를 merge한다
df_road_info=pd.merge(df23_road,df_traffic_road,on='link_id')
df_road_info
# -

# ## 3) 평일시간복잡도

# +
# 평일시간복잡도와 상세도로망 merge
df_traffic_time_road = []
for i in df23_road['link_id']:
    df_traffic_time_road.append([i,sum(df26_traffic_time[df26_traffic_time['link_id'].apply(str).str.contains(i)]['time'])])
    
df_traffic_time_road=pd.DataFrame(df_traffic_time_road)
df_traffic_time_road.columns=['link_id','time']
# road_info에 시간복잡도 merge
df_road_info=pd.merge(df_road_info,df_traffic_time_road,on='link_id')
df_road_info
# -

# ## 4) 평일빈도복잡도

# +
# 평일빈도복잡도와 상세도로망 merge
df25_traffic_frequency_road = []
for i in df23_road['link_id']:
    df25_traffic_frequency_road.append([i,sum(df25_traffic_frequency[df25_traffic_frequency['link_id'].apply(str).str.contains(i)]['frequency'])])
    
df25_traffic_frequency_road=pd.DataFrame(df25_traffic_frequency_road)
df25_traffic_frequency_road.columns=['link_id','frequency']
#road_info에 빈도복잡도 merge
df_road_info=pd.merge(df_road_info,df25_traffic_frequency_road,on='link_id')
df_road_info

# +
layer = pdk.Layer(
    'ScatterplotLayer',
    df16_road_sign,
    get_position=['lon', 'lat'],
    get_radius=15,
    get_fill_color=[180, 0, 200, 140],
    pickable=True,
    auto_highlight=True
    )

center=[127.0772,37.1498]
view_state = pdk.ViewState( 
    longitude=center[0], 
    latitude=center[1], 
    zoom=10
) 
r2 = pdk.Deck(layers=[layer], initial_view_state=view_state,
             map_style='mapbox://styles/mapbox/outdoors-v11',
             mapbox_key = "pk.eyJ1IjoicmVib3JuMTk5OCIsImEiOiJja2oyZGppZ24wdHJ1MnRtaHU5dm92cnV0In0.8sNxBdHqt8JccQZB-oe3Cg"
            )

r2.to_html()
# -

# # Link 정보 취합 및 시각화

# ### df23_road 분포

# +
df23_road['N_road_width'] = df23_road['width'] / df23_road['width'].max()
layer_1 = pdk.Layer(
    'PathLayer',
    df23_road,
    get_path='coordinates',
    get_width='width * 10',
    get_color='[255, 120, 255* N_road_width]',
    pickable=True,
    auto_highlight=True
)

layer_2 = pdk.Layer(
    'ScatterplotLayer',
    df16_road_sign,
    get_position=['lon', 'lat'],
    get_radius=8,
    get_fill_color=[180, 0, 200, 140],
    pickable=True,
    auto_highlight=True
    )

center=[127.0772,37.1498]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=13)

r = pdk.Deck(layers=[layer_1, layer_2], initial_view_state=view_state,
             map_style='mapbox://styles/mapbox/outdoors-v11',
             mapbox_key = "pk.eyJ1IjoicmVib3JuMTk5OCIsImEiOiJja2oyZGppZ24wdHJ1MnRtaHU5dm92cnV0In0.8sNxBdHqt8JccQZB-oe3Cg"
            )

r.to_html()

# +
df23_road['N_road_width'] = df23_road['width'] / df23_road['width'].max()
layer_1 = pdk.Layer(
    'PathLayer',
    df23_road,
    get_path='coordinates',
    get_width='width * 10',
    get_color='[255, 120, 255* N_road_width]',
    pickable=True,
    auto_highlight=True
)

layer_2 = pdk.Layer(
    'ScatterplotLayer',
    df16_road_sign,
    get_position=['lon', 'lat'],
    get_radius=8,
    get_fill_color=[180, 0, 200, 140],
    pickable=True,
    auto_highlight=True
    )

layer_2 = pdk.Layer(
    'ScatterplotLayer',
    df10_school,
    get_position=['lon', 'lat'],
    get_radius=16,
    get_fill_color=[180, 0, 200, 140],
    pickable=True,
    auto_highlight=True
    )

center=[127.0772,37.1498]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=13)

r = pdk.Deck(layers=[layer_1, layer_2], initial_view_state=view_state,
             map_style='mapbox://styles/mapbox/outdoors-v11',
             mapbox_key = "pk.eyJ1IjoicmVib3JuMTk5OCIsImEiOiJja2oyZGppZ24wdHJ1MnRtaHU5dm92cnV0In0.8sNxBdHqt8JccQZB-oe3Cg"
            )

r.to_html()

# +
df = df24_traffic
df['N_total_traffic'] = df['all_traffic'] / df['all_traffic'].max()
layer = pdk.Layer( 'PathLayer', 
                  df, 
                  get_path='link_id', 
                  get_width='N_total_traffic*10', 
                  get_color='[255, 255 * N_total_traffic, 120]', 
                  pickable=True, auto_highlight=True 
                 ) 

center=[127.0772,37.1498]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=13)

r = pdk.Deck(layers=[layer], initial_view_state=view_state,
             map_style='mapbox://styles/mapbox/outdoors-v11',
             mapbox_key = "pk.eyJ1IjoicmVib3JuMTk5OCIsImEiOiJja2oyZGppZ24wdHJ1MnRtaHU5dm92cnV0In0.8sNxBdHqt8JccQZB-oe3Cg"
            )

r.to_html()

# +
layer = pdk.Layer('PathLayer', 
                  df, 
                  get_path='link_id', 
                  get_width='N_total_traffic*10', 
                  get_color='[255, 255 * N_total_traffic, 120]', 
                  pickable=True, auto_highlight=True 
                 ) 

center=[127.0772,37.1498]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=13)

r = pdk.Deck(layers=[layer], initial_view_state=view_state,
             map_style='mapbox://styles/mapbox/outdoors-v11',
             mapbox_key = "pk.eyJ1IjoicmVib3JuMTk5OCIsImEiOiJja2oyZGppZ24wdHJ1MnRtaHU5dm92cnV0In0.8sNxBdHqt8JccQZB-oe3Cg"
            )

r.to_html()

# +
# buffer_road = gpd.GeoDataFrame({'geometry': df23_road.buffer(1000)})
# origin_ = df_osan_grid.groupby(['gid']).apply(lambda gr : gr.area.sum())

# ax = df_osan_grid.plot(column="gid", figsize=(8,8), alpha=0.8, legend=True)
# df23_road.plot(ax=ax, marker='v', color='black', label='Firestation')
# buffer_road.boundary.plot(ax=ax, color='red')
# ax.set_title("df23_road buffer", fontsize=20)
# ax.set_axis_off()
# plt.show()

# print(origin_)

# +
grid_info_ = df_osan_grid

grid_info_ = grid_info_.join(df2_grid_accident, how = 'left', lsuffix = '', rsuffix = '_r')
grid_info_.drop(['gid_r', 'geometry_r'], axis = 1, inplace = True)

grid_info_ = sjoin(grid_info_, df1_parking, 'pk_vio_val')
grid_info_ = sjoin(grid_info_, df22_bus_stop, 'bus_stop_val')
grid_info_ = sjoin(grid_info_, df17_crosswalk, 'crosswalk_val')
grid_info_ = sjoin(grid_info_, df21_sidewalk, 'sidewalk_val')

grid_info_
# -

grid_info_.describe()

# +
polygon_layer = pdk.Layer(
    'PolygonLayer',
    grid_info_,
    stroked=False,
    # processes the data as a flat longitude-latitude pair
    get_polygon="coordinates",
    get_fill_color = '[180 * accident_cnt, 0, 200, 140]',
    pickable=True,
    auto_highlight=True
    )

layer = pdk.Layer(
    'ScatterplotLayer',
    df10_school,
    get_position=['lon', 'lat'],
    get_radius=15,
    get_fill_color=[180, 0, 200, 140],
    pickable=True,
    auto_highlight=True
    )

center=[127.0772,37.1498]
view_state = pdk.ViewState(
    longitude=center[0],
    latitude=center[1],
    zoom=13)

r = pdk.Deck(layers=[polygon_layer, layer], initial_view_state=view_state,
             map_style='mapbox://styles/mapbox/outdoors-v11',
             mapbox_key = "pk.eyJ1IjoicmVib3JuMTk5OCIsImEiOiJja2oyZGppZ24wdHJ1MnRtaHU5dm92cnV0In0.8sNxBdHqt8JccQZB-oe3Cg"
            )

r.to_html()
# -


