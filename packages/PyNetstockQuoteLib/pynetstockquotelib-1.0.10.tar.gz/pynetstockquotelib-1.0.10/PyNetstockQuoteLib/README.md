# PyNetstockQuoteLib簡介<br>

針對臺灣股期交易市場，兆源公司提供輕量級報價API模組<br>
## 功能：<br>
即時提供證券、期貨與期權市場報價，多合一接口<br>
## 特點：<br>
1. 極致化 高效，快速響應市場行情<br>
2. 輕量級，整包大小不到 200 KB<br>
適合需要高速數據獲取且對資源占用敏感的應用場景<br>


**安裝方法：pip install PyNetstockQuoteLib**<br>
申請帳號請洽公司網站：https://www.fistek.com/<br>
電話：+886-2-87717385<br>
地址：臺灣臺北市大安區106光復南路72巷73號3樓<br>

## 函數列表：<br>
**1，連接**<br>
`def Connect(Address: str, nPort: unsigned short)-> bool: ...`<br>
**2，斷開連接**<br>
`def Disconnect() -> None: ...`<br>
**3，登錄**<br>
`def Login(UserName: str, Password: str, Software: str, Version: str, Company: str, Branch: str) -> None: ...`<br>
**4，運行阻塞函數**<br>
`def Go() -> None: ...`<br>
**5，注冊報價函數**<br>
`def SubscribeToQuote(Symbol: str, Exc: int, sExc: int = -1, rlot:bool = False) -> int: ...`<br>
**6，關閉注冊報價**<br>
`def CloseSubscribe(Index: int) -> bool: ...`<br>
**7，注冊Tick函數**<br>
`def SubscribeToTick(Symbol: str, Exc: int, sExc: int = -1, rlot:bool = False) -> int: ...`<br>
**8，獲得報價**<br>
`def GetQuote(Index: int, Field: int) -> int | float: ...`<br>
**9，獲得Tick數據**<br>
`def GetTick(Index:int)-> List[Dict[str, Union[int, float]]]: ...`<br>
**10，獲得基本資料(9-16)**<br>
`def GetInfo(Exc:int, Symbol:str, Field:str, sExc:int)-> str: ...`<br>
**11，設置主動回報callback**<br>
`def SetNoticeCallback(callback: Callable[[int, int, object, int], None]) -> None: ...`<br>
**12，設置登錄回報函數**<br>
`def SetLoginCallback(callback: Callable[[int, str, int], None]) -> None: ...`<br>
**13，設置交易日資訊回報函數**<br>
`def SetExcInfoCallback(callback: Callable[[int, int], None]) -> None: ...`<br>
**14，設置基本資料更新回報函數**<br>
`def SetStkiCallback(callback: Callable[[int, int, int], None]) -> None: ...`<br>
**15，設置報價回報callback**<br>
`def SetQuoteCallback(callback: Callable[[int, int], None]) -> None: ...`<br>
**16，設置Tick回報函數**<br>
`def SetTickCallback(callback: Callable[[int], None]) -> None: ...`<br>

## 示例1：Quote.py<br>
```python
import PyNetstockQuoteLib as NsQuote

Ind = 0
Ind1 = 0
#登錄回報
def OnLogin(Type,pInfo,InfoSize):
    if(Type == NsQuote.SMSGL_LOGIN_OKAY):
        global Ind,Ind1
        print("登錄成功!")
        #登錄成功后對商品進行報價訂閱
        Ind = NsQuote.SubscribeToQuote("FITX",NsQuote.EXC_FITXN,NsQuote.EXC_FITX_T2)
        Ind1 = NsQuote.SubscribeToQuote("2330",NsQuote.EXC_STOCK)
    else:
        print("登錄失敗")        
#報價回報
def OnQuote(Index,Type):
    if(Type == 1):
        global Ind,Ind1
        if(Index == Ind):
            print("Sym:FITX,Name:" + NsQuote.GetInfo(NsQuote.EXC_FITXN,"FITX","name") +
                  "," + NsQuote.SYM_GLOBAL_DESC[NsQuote.SYM_LAST] +":" +
                  str(NsQuote.GetQuote(Index,NsQuote.SYM_LAST)) + 
                  "," + NsQuote.SYM_GLOBAL_DESC[NsQuote.SYM_VOLUME] +":" +
                  str(NsQuote.GetQuote(Index,NsQuote.SYM_VOLUME)))
        if(Index == Ind1):
            print("Sym:2330,Last:" + str(NsQuote.GetQuote(Index,NsQuote.SYM_LAST)) + 
                  ",Vol:" + str(NsQuote.GetQuote(Index,NsQuote.SYM_VOLUME)))

#啟動入口
if NsQuote.Connect():
    print("連接成功")
    NsQuote.SetLoginCallback(OnLogin)
    NsQuote.SetQuoteCallback(OnQuote)
    NsQuote.Login("xxxxx", "xxxxx")
    NsQuote.Go()
else:
    print("連接失敗")
print("Over")
```
## 示例2：Tick.py<br>
```python
import PyNetstockQuoteLib as NsQuote

indTick = 0
#登錄回報
def OnLogin(Type,pInfo,InfoSize):
    if(Type == NsQuote.SMSGL_LOGIN_OKAY):
        print("登錄成功!")
    else:
        print("登錄失敗")        
#Tick回報
def OnTick(Index):
    #獲得Tick數據,返回字典列表迭代器
    TickList = NsQuote.GetTick(Index)
    #獲得Tick總數
    Ticklen = len(TickList)
    count = 0
    #用基本資料獲取商品名稱
    print(NsQuote.GetInfo(NsQuote.EXC_FITXN,"FITX","name"))
    #顯示本次Tick信息
    print("Index:" + str(Index) + " TickCount:",str(Ticklen))
    #顯示10條數據用于測試
    for Item in TickList:
        print(Item)#Item是字典對象，實際使用時可以用Key取單元數據例如：Item["Last"]
        count = count + 1
        if (count >=10): break
#交易日資訊回報
def OnExcInfo(Type,Exc):
    if(Exc == NsQuote.EXC_FITXN):#收到對應市場交易日資訊后注冊（較為單純）
        global indTick
        indTick = NsQuote.SubscribeToTick("FITX",NsQuote.EXC_FITXN,NsQuote.EXC_FITX_T2)
#程序入口
if NsQuote.Connect():
    print("連接成功")
    NsQuote.SetLoginCallback(OnLogin)
    NsQuote.SetExcInfoCallback(OnExcInfo)
    NsQuote.SetTickCallback(OnTick)
    NsQuote.Login("xxxxx", "xxxxx")
    NsQuote.Go()
else:
    print("連接失敗")
print("Over")
```