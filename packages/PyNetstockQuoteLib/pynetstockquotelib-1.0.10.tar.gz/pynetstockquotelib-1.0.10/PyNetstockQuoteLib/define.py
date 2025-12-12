# //---------------------------------------------------------------------------
# // 即時資料
# //---------------------------------------------------------------------------
SMSG_RT = 0x01  # 即時資料主標識

# 即時資料描述映射（單主標識，無子類）
SMSG_RT_DESC = {
    SMSG_RT: "即時資料"
}

# //---------------------------------------------------------------------------
# // 五檔資料
# //---------------------------------------------------------------------------
SMSG_TWFTC = 0x05  # 五檔資料主標識

# 五檔資料描述映射（單主標識，無子類）
SMSG_TWFTC_DESC = {
    SMSG_TWFTC: "五檔資料"
}

# //---------------------------------------------------------------------------
# // 歷史資料頭尾
# //---------------------------------------------------------------------------
SMSG_NHIS = 0x07  # 歷史資料頭尾主標識

# 歷史資料頭尾描述映射（單主標識，無子類）
SMSG_NHIS_DESC = {
    SMSG_NHIS: "歷史資料頭尾"
}

# //---------------------------------------------------------------------------
# // 歷史資料
# //---------------------------------------------------------------------------
SMSG_NHISD = 0x08  # 歷史資料主標識

# 歷史資料描述映射（單主標識，無子類）
SMSG_NHISD_DESC = {
    SMSG_NHISD: "歷史資料"
}

# //---------------------------------------------------------------------------
# // 時間校正
# //---------------------------------------------------------------------------
SMSG_TS = 0x10  # 時間校正主標識

# 時間校正描述映射（單主標識，無子類）
SMSG_TS_DESC = {
    SMSG_TS: "時間校正"
}

# //---------------------------------------------------------------------------
# // 股市清盤訊息
# //---------------------------------------------------------------------------
SMSG_RSTEXC = 0x0A  # 股市清盤訊息主標識

# 股市清盤訊息描述映射（單主標識，無子類）
SMSG_RSTEXC_DESC = {
    SMSG_RSTEXC: "股市清盤訊息"
}

# //---------------------------------------------------------------------------
# // 股市交易日資訊
# //---------------------------------------------------------------------------
SMSG_EXCINFO = 0x0B  # 股市交易日資訊主標識

# 股市交易日資訊子類型
SMSG_EXCINFO_DATEI = 0x01  # 日期資訊

# 股市交易日資訊描述映射（含主標識和子類型）
SMSG_EXCINFO_DESC = {
    SMSG_EXCINFO: "股市交易日資訊（主標識）",
    SMSG_EXCINFO_DATEI: "日期資訊"
}
# //---------------------------------------------------------------------------
# // 登錄回復
# //---------------------------------------------------------------------------
SMSG_LOGIN_ECHO = 0x0E  # 登錄回復主標識

# 登錄回復子狀態碼（SMSG_LOGIN_ECHO 下屬細分狀態）
SMSGL_ACCT_ERROR = 0x01    # 帳號不存在
SMSGL_PASS_ERROR = 0x02    # 密碼錯誤
SMSGL_ACCT_EXPRD = 0x03    # 帳號過期
SMSGL_ACCT_UNUSED = 0x04   # 帳號未開通
SMSGL_ACCT_MULLOG = 0x05   # 重復登入
SMSGL_LOGIN_ERROR = 0x06   # 登入錯誤
SMSGL_LEVEL_ERROR = 0x07   # 等級錯誤
SMSGL_VERSN_ERROR = 0x08   # 版本錯誤
SMSGL_ACCT_FORBID = 0x09   # 帳號禁用
SMSGL_ACCT_OVERHD = 0x0A   # 人數過多
SMSGL_ECHO_STRING = 0x0B   # 訊息傳送
SMSGL_LOGIN_OKAY = 0x19    # 登入成功

# 登錄狀態碼描述映射（用于快速獲取中文說明，支持日志/用戶提示）
SMSGL_STATUS_DESC = {
    SMSGL_ACCT_ERROR: "帳號不存在",
    SMSGL_PASS_ERROR: "密碼錯誤",
    SMSGL_ACCT_EXPRD: "帳號過期",
    SMSGL_ACCT_UNUSED: "帳號未開通",
    SMSGL_ACCT_MULLOG: "重復登入",
    SMSGL_LOGIN_ERROR: "登入錯誤",
    SMSGL_LEVEL_ERROR: "等級錯誤",
    SMSGL_VERSN_ERROR: "版本錯誤",
    SMSGL_ACCT_FORBID: "帳號禁用",
    SMSGL_ACCT_OVERHD: "人數過多",
    SMSGL_ECHO_STRING: "訊息傳送",
    SMSGL_LOGIN_OKAY: "登入成功"
}

# //---------------------------------------------------------------------------
# // 個股資訊傳送
# //---------------------------------------------------------------------------
SMSG_STKI = 0x09  # 個股資訊傳送主標識

# 個股資訊子類型（SMSG_STKI 下屬細分類型）
SMSG_STKI_DRD = 0x02      # 除權除息庫
SMSG_STKI_STKR = 0x08     # 期貨、選擇權對應
SMSG_STKI_EXCTS = 0x0B    # 股市開收盤時間
SMSG_STKI_PRCTBL = 0x0C   # 跳動檔位
SMSG_STKI_TOPREQ = 0x0D   # 主機排名，盤中提示，潛力排行等
SMSG_STKI_QTEGRP = 0x0E   # 分類看盤索引查詢
SMSG_STKI_EXCNAME = 0x0F  # 交易所名稱
SMSG_STKI_SINFO = 0x10    # 商品基本資訊1
SMSG_STKI_SINFO2 = 0x11   # 商品基本資訊2
SMSG_STKI_D_QSID = 0x12   # 股票推薦券商資料[9-18]

# 可選：添加子類型描述映射（方便日志打印/用戶使用）
SMSG_STKI_SUBTYPE_DESC = {
    SMSG_STKI_DRD: "除權除息庫",
    SMSG_STKI_STKR: "期貨、選擇權對應",
    SMSG_STKI_EXCTS: "股市開收盤時間",
    SMSG_STKI_PRCTBL: "跳動檔位",
    SMSG_STKI_TOPREQ: "主機排名，盤中提示，潛力排行等",
    SMSG_STKI_QTEGRP: "分類看盤索引查詢",
    SMSG_STKI_EXCNAME: "交易所名稱",
    SMSG_STKI_SINFO: "商品基本資訊1",
    SMSG_STKI_SINFO2: "商品基本資訊2",
    SMSG_STKI_D_QSID: "股票推薦券商資料[9-18]"
}

# //---------------------------------------------------------------------------
# // 一般報價欄位  0 ~ 255 (SYM_FIRST ~ SYM_BASE_BEST)
# //---------------------------------------------------------------------------
# 基礎分界常量（原宏依賴的基準值，需先定義）
SYM_FIRST = 0                  # 報價欄位起始索引
SYM_BASE_BEST = 255            # 一般報價欄位結束索引（分界點）

# 核心報價欄位（1~20）
SYM_OPEN = 1                   # 開盤
SYM_HIGH = 2                   # 最高
SYM_LOW = 3                    # 最低
SYM_LAST = 4                   # 成交價
SYM_PREV = 5                   # 昨收
SYM_BID = 6                    # 買價
SYM_ASK = 7                    # 賣價
SYM_VOLUME = 8                 # 成交總張數
SYM_OPENINT = 9                # 未平倉合約數
SYM_SIZE = 10                  # 成交單量
SYM_BIDSIZE = 11               # 開出買價的量
SYM_ASKSIZE = 12               # 開出賣價的量
SYM_BIDEXCH = 13               # 出買價證交所
SYM_ASKEXCH = 14               # 出賣價證交所
SYM_TTIME = 15                 # 撮合時間
SYM_YEARHIGH = 16              # 今年最高價
SYM_YEARLOW = 17               # 今年最低價
SYM_NET = 18                   # 漲跌
SYM_NETPCT = 19                # 漲跌幅
SYM_SNOFLAG = 20               # 報價旗標

# 補充報價欄位（22~62）
SYM_SVOLUME = 22               # 日盤成交量
SYM_TRDSTS = 23                # 2^1=試撮, 2^2=禁刪, 2^3=暫停 (20140417) 2^4=收盤(20180625)
SYM_STRSTM = 25                # 暫停/恢復時間
SYM_AVGPRC2 = 27               # 成交均價
SYM_LDATE = 28                 # 最後交易日，周月線結束日
SYM_AVGPRC = 29                # 成交均價
SYM_LOT = 30                   # 成交總筆數
SYM_BIDLOT = 31                # 總買筆數
SYM_ASKLOT = 32                # 總賣筆數
SYM_TERMHIGH = 33              # 交易歷史最高
SYM_TERMLOW = 34               # 交易歷史最低
SYM_N_LAST = 35                # 大盤指數(不含金融)
SYM_N_PREV = 36                # 大盤昨收(不含金融)
SYM_PDATE = 37                 # 交易日期
SYM_MATCHTYPE = 38             # 該筆成交是否是內外盤成交 0:外盤 1:內盤 (原名 SYM_VALUE, see SYM_SVAL)
SYM_UVALUE = 39                # 單位成交總值
SYM_BTRADE = 40                # 內盤張數
SYM_ATRADE = 41                # 外盤張數
SYM_NTRADE = 42                # 不知盤張數
SYM_CEIL = 43                  # 漲停價
SYM_FLOOR = 44                 # 跌停價
SYM_POPEN = 45                 # 昨開
SYM_PHIGH = 46                 # 昨高
SYM_PLOW = 47                  # 昨低
SYM_PVOL = 48                  # 昨量
SYM_ASSET = 49                 # 權值比重
SYM_BTL = 50                   # 總買成筆
SYM_ATL = 51                   # 總賣成筆
SYM_WARN = 52                  # 警示股與否
SYM_SETTP = 53                 # 結算價
SYM_SVAL = 54                  # 個股成交總值
SYM_BIDVOLUME = 55             # 總買量
SYM_ASKVOLUME = 56             # 總賣量
SYM_SERIAL = 57                # 傳輸序號
SYM_SEXCH = 58                 # 子股市
SYM_DATAEND = 59               # 資料結束
SYM_SECDIFF = 60               # 秒差
SYM_VOLDIFF = 61               # 量差
SYM_VDATE = 62                 # 有效日期

# 融資融券相關欄位（71~78）
SYM_K_TMB = 71                 # 融資買進
SYM_K_TMA = 72                 # 融資賣出
SYM_K_TML = 73                 # 融資余額
SYM_K_TSA = 74                 # 融券賣出
SYM_K_TSB = 75                 # 融券買進
SYM_K_TSL = 76                 # 融券余額
SYM_K_TCL = 77                 # 融資限額
SYM_K_TMC = 78                 # 資券當沖

# 機構交易相關欄位（81~86）
SYM_K_SBVOL = 81               # 自營買進
SYM_K_SSVOL = 82               # 自營賣出
SYM_K_CBVOL = 83               # 投信買進
SYM_K_CSVOL = 84               # 投信賣出
SYM_K_FBVOL = 85               # 法人買進
SYM_K_FSVOL = 86               # 法人賣出

# 股本相關欄位（90~92）
SYM_K_IQTY = 90                # 發行股數
SYM_K_BQTY = 91                # 可投資股數
SYM_K_HQTY = 92                # 持有持數

# //---------------------------------------------------------------------------
# // 最佳買賣價量
# //---------------------------------------------------------------------------

# 1~10檔最佳買賣價（256~316）
SYM_BESTBID1 = (SYM_BASE_BEST + 1)    # 買價1檔
SYM_BESTBID2 = (SYM_BASE_BEST + 2)    # 買價2檔
SYM_BESTBID3 = (SYM_BASE_BEST + 3)    # 買價3檔
SYM_BESTBID4 = (SYM_BASE_BEST + 4)    # 買價4檔
SYM_BESTBID5 = (SYM_BASE_BEST + 5)    # 買價5檔
SYM_BESTBIDSIZE1 = (SYM_BASE_BEST + 6)# 買量1檔
SYM_BESTBIDSIZE2 = (SYM_BASE_BEST + 7)# 買量2檔
SYM_BESTBIDSIZE3 = (SYM_BASE_BEST + 8)# 買量3檔
SYM_BESTBIDSIZE4 = (SYM_BASE_BEST + 9)# 買量4檔
SYM_BESTBIDSIZE5 = (SYM_BASE_BEST + 10)# 買量5檔
SYM_BESTASK1 = (SYM_BASE_BEST + 11)   # 賣價1檔
SYM_BESTASK2 = (SYM_BASE_BEST + 12)   # 賣價2檔
SYM_BESTASK3 = (SYM_BASE_BEST + 13)   # 賣價3檔
SYM_BESTASK4 = (SYM_BASE_BEST + 14)   # 賣價4檔
SYM_BESTASK5 = (SYM_BASE_BEST + 15)   # 賣價5檔
SYM_BESTASKSIZE1 = (SYM_BASE_BEST + 16)# 賣量1檔
SYM_BESTASKSIZE2 = (SYM_BASE_BEST + 17)# 賣量2檔
SYM_BESTASKSIZE3 = (SYM_BASE_BEST + 18)# 賣量3檔
SYM_BESTASKSIZE4 = (SYM_BASE_BEST + 19)# 賣量4檔
SYM_BESTASKSIZE5 = (SYM_BASE_BEST + 20)# 賣量5檔
SYM_BIDASKTIME = (SYM_BASE_BEST + 21) # 買賣價時間戳
SYM_BESTBID6 = (SYM_BASE_BEST + 22)   # 買價6檔
SYM_BESTBID7 = (SYM_BASE_BEST + 23)   # 買價7檔
SYM_BESTBID8 = (SYM_BASE_BEST + 24)   # 買價8檔
SYM_BESTBID9 = (SYM_BASE_BEST + 25)   # 買價9檔
SYM_BESTBID10 = (SYM_BASE_BEST + 26)  # 買價10檔
SYM_BESTBIDSIZE6 = (SYM_BASE_BEST + 27)# 買量6檔
SYM_BESTBIDSIZE7 = (SYM_BASE_BEST + 28)# 買量7檔
SYM_BESTBIDSIZE8 = (SYM_BASE_BEST + 29)# 買量8檔
SYM_BESTBIDSIZE9 = (SYM_BASE_BEST + 30)# 買量9檔
SYM_BESTBIDSIZE10 = (SYM_BASE_BEST + 31)# 買量10檔
SYM_BESTASK6 = (SYM_BASE_BEST + 32)   # 賣價6檔
SYM_BESTASK7 = (SYM_BASE_BEST + 33)   # 賣價7檔
SYM_BESTASK8 = (SYM_BASE_BEST + 34)   # 賣價8檔
SYM_BESTASK9 = (SYM_BASE_BEST + 35)   # 賣價9檔
SYM_BESTASK10 = (SYM_BASE_BEST + 36)  # 賣價10檔
SYM_BESTASKSIZE6 = (SYM_BASE_BEST + 37)# 賣量6檔
SYM_BESTASKSIZE7 = (SYM_BASE_BEST + 38)# 賣量7檔
SYM_BESTASKSIZE8 = (SYM_BASE_BEST + 39)# 賣量8檔
SYM_BESTASKSIZE9 = (SYM_BASE_BEST + 40)# 賣量9檔
SYM_BESTASKSIZE10 = (SYM_BASE_BEST + 41)# 賣量10檔

# //---------------------------------------------------------------------------
# 報價欄位描述映射（按功能分類，便于查詢和使用）
# //---------------------------------------------------------------------------
# 1. 核心報價欄位描述（常用基礎字段）
SYM_CORE_DESC = {
    SYM_OPEN: "開盤",
    SYM_HIGH: "最高",
    SYM_LOW: "最低",
    SYM_LAST: "成交價",
    SYM_PREV: "昨收",
    SYM_BID: "買價",
    SYM_ASK: "賣價",
    SYM_VOLUME: "成交總張數",
    SYM_OPENINT: "未平倉合約數",
    SYM_NET: "漲跌",
    SYM_NETPCT: "漲跌幅",
    SYM_YEARHIGH: "今年最高價",
    SYM_YEARLOW: "今年最低價",
    SYM_CEIL: "漲停價",
    SYM_FLOOR: "跌停價",
}

# 2. 成交量/筆數相關描述
SYM_VOLUME_DESC = {
    SYM_SIZE: "成交單量",
    SYM_BIDSIZE: "開出買價的量",
    SYM_ASKSIZE: "開出賣價的量",
    SYM_SVOLUME: "日盤成交量",
    SYM_LOT: "成交總筆數",
    SYM_BIDLOT: "總買筆數",
    SYM_ASKLOT: "總賣筆數",
    SYM_BIDVOLUME: "總買量",
    SYM_ASKVOLUME: "總賣量",
    SYM_PVOL: "昨量",
    SYM_BTRADE: "內盤張數",
    SYM_ATRADE: "外盤張數",
    SYM_NTRADE: "不知盤張數",
}

# 3. 時間/日期相關描述
SYM_TIME_DESC = {
    SYM_TTIME: "撮合時間",
    SYM_LDATE: "最後交易日/周月線結束日",
    SYM_PDATE: "交易日期",
    SYM_VDATE: "有效日期",
    SYM_STRSTM: "暫停/恢復時間",
    SYM_SECDIFF: "秒差",
    SYM_BIDASKTIME: "買賣價時間戳",
}

# 4. 融資融券相關描述
SYM_MARGIN_DESC = {
    SYM_K_TMB: "融資買進",
    SYM_K_TMA: "融資賣出",
    SYM_K_TML: "融資余額",
    SYM_K_TSA: "融券賣出",
    SYM_K_TSB: "融券買進",
    SYM_K_TSL: "融券余額",
    SYM_K_TCL: "融資限額",
    SYM_K_TMC: "資券當沖",
}

# 5. 機構交易相關描述
SYM_INSTITUTION_DESC = {
    SYM_K_SBVOL: "自營買進",
    SYM_K_SSVOL: "自營賣出",
    SYM_K_CBVOL: "投信買進",
    SYM_K_CSVOL: "投信賣出",
    SYM_K_FBVOL: "法人買進",
    SYM_K_FSVOL: "法人賣出",
}

# 6. 股本相關描述
SYM_EQUITY_DESC = {
    SYM_K_IQTY: "發行股數",
    SYM_K_BQTY: "可投資股數",
    SYM_K_HQTY: "持有持數",
}

# 7. 1~10檔最佳買賣價量描述
SYM_BEST_BIDASK_DESC = {
    # 買價
    SYM_BESTBID1: "買價1檔",
    SYM_BESTBID2: "買價2檔",
    SYM_BESTBID3: "買價3檔",
    SYM_BESTBID4: "買價4檔",
    SYM_BESTBID5: "買價5檔",
    SYM_BESTBID6: "買價6檔",
    SYM_BESTBID7: "買價7檔",
    SYM_BESTBID8: "買價8檔",
    SYM_BESTBID9: "買價9檔",
    SYM_BESTBID10: "買價10檔",
    # 買量
    SYM_BESTBIDSIZE1: "買量1檔",
    SYM_BESTBIDSIZE2: "買量2檔",
    SYM_BESTBIDSIZE3: "買量3檔",
    SYM_BESTBIDSIZE4: "買量4檔",
    SYM_BESTBIDSIZE5: "買量5檔",
    SYM_BESTBIDSIZE6: "買量6檔",
    SYM_BESTBIDSIZE7: "買量7檔",
    SYM_BESTBIDSIZE8: "買量8檔",
    SYM_BESTBIDSIZE9: "買量9檔",
    SYM_BESTBIDSIZE10: "買量10檔",
    # 賣價
    SYM_BESTASK1: "賣價1檔",
    SYM_BESTASK2: "賣價2檔",
    SYM_BESTASK3: "賣價3檔",
    SYM_BESTASK4: "賣價4檔",
    SYM_BESTASK5: "賣價5檔",
    SYM_BESTASK6: "賣價6檔",
    SYM_BESTASK7: "賣價7檔",
    SYM_BESTASK8: "賣價8檔",
    SYM_BESTASK9: "賣價9檔",
    SYM_BESTASK10: "賣價10檔",
    # 賣量
    SYM_BESTASKSIZE1: "賣量1檔",
    SYM_BESTASKSIZE2: "賣量2檔",
    SYM_BESTASKSIZE3: "賣量3檔",
    SYM_BESTASKSIZE4: "賣量4檔",
    SYM_BESTASKSIZE5: "賣量5檔",
    SYM_BESTASKSIZE6: "賣量6檔",
    SYM_BESTASKSIZE7: "賣量7檔",
    SYM_BESTASKSIZE8: "賣量8檔",
    SYM_BESTASKSIZE9: "賣量9檔",
    SYM_BESTASKSIZE10: "賣量10檔",
}

# 9. 其他補充欄位描述
SYM_OTHER_DESC = {
    SYM_BIDEXCH: "出買價證交所",
    SYM_ASKEXCH: "出賣價證交所",
    SYM_SNOFLAG: "報價旗標",
    SYM_TRDSTS: "交易狀態（2^1=試撮, 2^2=禁刪, 2^3=暫停, 2^4=收盤）",
    SYM_AVGPRC2: "成交均價",
    SYM_AVGPRC: "成交均價",
    SYM_TERMHIGH: "交易歷史最高",
    SYM_TERMLOW: "交易歷史最低",
    SYM_N_LAST: "大盤指數(不含金融)",
    SYM_N_PREV: "大盤昨收(不含金融)",
    SYM_MATCHTYPE: "內外盤標識（0:外盤 1:內盤）",
    SYM_UVALUE: "單位成交總值",
    SYM_POPEN: "昨開",
    SYM_PHIGH: "昨高",
    SYM_PLOW: "昨低",
    SYM_ASSET: "權值比重",
    SYM_BTL: "總買成筆",
    SYM_ATL: "總賣成筆",
    SYM_WARN: "警示股與否",
    SYM_SETTP: "結算價",
    SYM_SVAL: "個股成交總值",
    SYM_SERIAL: "傳輸序號",
    SYM_SEXCH: "子股市",
    SYM_DATAEND: "資料結束標識",
    SYM_VOLDIFF: "量差",
}

# 10. 全局統一描述映射（整合所有分類，方便一次性查詢）
SYM_GLOBAL_DESC = {}
SYM_GLOBAL_DESC.update(SYM_CORE_DESC)
SYM_GLOBAL_DESC.update(SYM_VOLUME_DESC)
SYM_GLOBAL_DESC.update(SYM_TIME_DESC)
SYM_GLOBAL_DESC.update(SYM_MARGIN_DESC)
SYM_GLOBAL_DESC.update(SYM_INSTITUTION_DESC)
SYM_GLOBAL_DESC.update(SYM_EQUITY_DESC)
SYM_GLOBAL_DESC.update(SYM_BEST_BIDASK_DESC)
SYM_GLOBAL_DESC.update(SYM_OTHER_DESC)

# 證券
EXC_STOCK = 1
EXC_STOCK_T1 = 1    # 上柜
EXC_STOCK_T4 = 4    # 興柜
# 金融期貨
EXC_FITX = 2
EXC_FITX_T2 = 2     # 非個股期貨
EXC_FITX_T3 = 3     # 選擇權
EXC_FITX_T5 = 5     # 非個股期貨復式
EXC_FITX_T6 = 6     # 個股期貨
EXC_FITX_T7 = 7     # 個股期貨復式
# 金融期貨夜盤
EXC_FITXN = 12
EXC_FITXN_T2 = 2     # 非個股期貨夜盤
EXC_FITXN_T3 = 3     # 選擇權夜盤
EXC_FITXN_T5 = 5     # 非個股期貨復式夜盤
EXC_FITXN_T6 = 6     # 個股期貨夜盤
EXC_FITXN_T7 = 7     # 個股期貨復式夜盤

# //---------------------------------------------------------------------------
# // 市場類型（證券/金融期貨）常量定義
# //---------------------------------------------------------------------------
# 證券相關
EXC_STOCK = 1                  # 證券主類型
EXC_STOCK_T1 = 1               # 上柜（證券細分類型）
EXC_STOCK_T4 = 4               # 興柜（證券細分類型）

# 金融期貨相關（日盤）
EXC_FITX = 2                   # 金融期貨主類型（日盤）
EXC_FITX_T2 = 2                # 非個股期貨（金融期貨日盤細分）
EXC_FITX_T3 = 3                # 選擇權（金融期貨日盤細分）
EXC_FITX_T5 = 5                # 非個股期貨復式（金融期貨日盤細分）
EXC_FITX_T6 = 6                # 個股期貨（金融期貨日盤細分）
EXC_FITX_T7 = 7                # 個股期貨復式（金融期貨日盤細分）

# 金融期貨相關（夜盤）
EXC_FITXN = 12                 # 金融期貨主類型（夜盤）
EXC_FITXN_T2 = 2               # 非個股期貨夜盤（金融期貨夜盤細分）
EXC_FITXN_T3 = 3               # 選擇權夜盤（金融期貨夜盤細分）
EXC_FITXN_T5 = 5               # 非個股期貨復式夜盤（金融期貨夜盤細分）
EXC_FITXN_T6 = 6               # 個股期貨夜盤（金融期貨夜盤細分）
EXC_FITXN_T7 = 7               # 個股期貨復式夜盤（金融期貨夜盤細分）

# //---------------------------------------------------------------------------
# // 市場類型統一描述映射（唯一字典：STOCK_EXC_DESC）
# // 格式：{代碼: "完整描述（含主類型+細分類型）"}
# //---------------------------------------------------------------------------
STOCK_EXC_DESC = {
    # 證券主類型+細分類型
    EXC_STOCK: "證券",
    EXC_STOCK_T1: "上柜",
    EXC_STOCK_T4: "興柜",
    
    # 金融期貨（日盤）主類型+細分類型
    EXC_FITX: "金融期貨（日盤）",
    EXC_FITX_T2: "非個股期貨",
    EXC_FITX_T3: "選擇權",
    EXC_FITX_T5: "非個股期貨復式",
    EXC_FITX_T6: "個股期貨",
    EXC_FITX_T7: "個股期貨復式",
    
    # 金融期貨（夜盤）主類型+細分類型
    EXC_FITXN: "金融期貨（夜盤）",
    EXC_FITXN_T2: "非個股期貨夜盤",
    EXC_FITXN_T3: "選擇權夜盤",
    EXC_FITXN_T5: "非個股期貨復式夜盤",
    EXC_FITXN_T6: "個股期貨夜盤",
    EXC_FITXN_T7: "個股期貨復式夜盤"
}