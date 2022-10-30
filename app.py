import streamlit as st
import requests

def getAllBookstore():
    url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
    headers = {'accept':'application/json'}
    response=requests.get(url, headers=headers)
    response=response.json()
    
    return response

def getCountyOption(items):
    optionList = []
    for item in items:
        name = item['cityName'][0:3]
        if name not in optionList:
            optionList.append(name)
    return optionList

def getDistrictOption(items, target):
    optionList = []
    for item in items:
        name = item['cityName']
        if target not in name: continue
        name.strip()
        district = name[5:]
        if len(district) == 0: continue
        if district not in optionList:
            optionList.append(district)
    return optionList

def getSpecificBookstore(items, county, districts):
    ret = []
    for item in items:
        name = item['cityName']
        if county not in name: continue
        for district in districts:
            if district not in name: continue
            ret.append(item)
    return ret

def getBookstoreInfo(items):
    ret = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])
        expander.subheader('Address')
        expander.write(item['address'])
        expander.subheader('Open Time')
        expander.write(item['openTime'])
        expander.subheader('Email')
        expander.write(item['email'])
        ret.append(expander)
    return ret
    

def app():
    bsList = getAllBookstore()

    countyOption = getCountyOption(bsList)

    st.header('特色書店地圖')
    st.metric('Total bookstore', len(bsList))
    county=st.selectbox('請選擇縣市',countyOption)
    districtOption = getDistrictOption(bsList, county)
    district=st.multiselect('請選擇區域', districtOption)
    specificBookstore = getSpecificBookstore(bsList, county, district)

    num = len(specificBookstore)
    st.write(f'總共有{num}項結果')

    specificBookstore.sort(key = lambda x:x['hitRate'], reverse = True)
    bookstoreInfo = getBookstoreInfo(specificBookstore)

if __name__ == '__main__':
    app()