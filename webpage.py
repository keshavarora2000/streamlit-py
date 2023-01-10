import streamlit as st
import requests
import pandas as pd

st.set_page_config (
    page_title = "currencyveda Option Chain Nifty ",
    page_icon = "0",
    layout="wide"
)
st.title("Nifty Option Chain")

url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
headers ={"accept-encoding": "gzip, deflate, br",
"accept-language" : "en-US,en;q=0.9",
"referer" : "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

session = requests.Session()
request = session.get(url,headers=headers)
cookies = dict(request.cookies)
response = session.get(url,headers=headers,cookies=cookies).json()
rawdata = pd.DataFrame(response)
rawop = pd.DataFrame(rawdata['filtered']['data']).fillna(0)

def dataframe(rawop):
    data=[]
    for i in range(0,len(rawop)):
        calloi = callcoi = callvol = callLTP = callLTPchange = putLTPchange = putLTP = putvol = putcoi = putoi = 0
        stp = rawop['strikePrice'][i]
        if(rawop['CE'][i]==0):
            calloi = callcoi = callvol = callLTP = callLTPchange = 0
        else:
          calloi = rawop['CE'][i]['openInterest']
          callcoi = rawop['CE'][i]['changeinOpenInterest']
          callvol = rawop['CE'][i]['totalTradedVolume']
          callLTP = rawop['CE'][i]['lastPrice']
          callLTPchange = rawop['CE'][i]['change']
        if(rawop['PE'][i]==0):
            putoi = putcoi = putvol = putLTP = putLTPchange = 0
        else:
          putoi = rawop['PE'][i]['openInterest']
          putcoi = rawop['PE'][i]['changeinOpenInterest']
          putvol = rawop['PE'][i]['totalTradedVolume']
          putLTP = rawop['PE'][i]['lastPrice']
          putLTPchange = rawop['PE'][i]['change']

        opdata = {'CALL OI' : calloi, 'CALLCHANGE OI' : callcoi , 'CALL VOLUME' : callvol, 'CALL LTP' :callLTP, 'CALL LTP CHANGE':callLTPchange, 'STRIKE PRICE': stp,'PUT LTP CHANGE':putLTPchange, 'PUT LTP' :putLTP, 'PUT VOLUME' : putvol, 'PUT CHANGE OI' : putcoi, 'PUT OI' : putoi }
        data.append(opdata)
    optionchain = pd.DataFrame(data)
    return optionchain

optionchain = dataframe(rawop)
niftyoc = optionchain

st.dataframe(niftyoc,width=1000,height=800)
st.subheader('CALL OI VS PUT OI')
st.line_chart(niftyoc[['CALL OI','PUT OI']])
st.subheader('CALL Volume VS PUT Volume')
st.line_chart(niftyoc[['CALL VOLUME','PUT VOLUME']])