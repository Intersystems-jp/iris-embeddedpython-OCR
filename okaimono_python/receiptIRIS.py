import sys
import iris
import datetime

def save(datalist):
    receipt=iris.cls("Okaimono.Receipt")._New()
    total=0
    oldstr1=""
    for str in datalist:
        #str=itemlist.rstrip('\r\n').split("\t")
        if str[0]=="storename":
            receipt.StoreName=str[1]
        elif str[0]=="datetime":
            #datetimeに変換
            okaimonodt=datetime.datetime.strptime(str[1],'%Y年%m月%d日%H:%M')
            receipt.OkaimonoDateTime=okaimonodt.strftime('%Y-%m-%d %H:%M:%S')
        elif str[0]=="discount":
            receipt.Discount=str[1]
        elif str[0]=="total_price":
            total=1
        elif (str[0]=="itemprice") and (total==1):
            receipt.TotalPrice=str[1]
            total=0
        elif str[0]=="itemname" and (str[0].find("F食料品")<0):
            item=iris.cls("Okaimono.Item")._New()
            item.Name=str[1]
            oldstr1=item.Name
        elif (str[0]=="itemprice") and (oldstr1 !="") and (oldstr1.find("F食料品")<0) :
            item.Price=str[1]
            item.Receipt=receipt
            oldstr1=""

    #print(receipt.Items.Count())
    #iris.cls("%SYSTEM.OBJ").Dump(receipt)
    #iris.cls("%SYSTEM.OBJ").Dump(receipt.Items.GetAt(1))
    st=receipt._Save()
    if st != 1:
        raise Exception(st)


## ./okaimono_python/data/*.txtを使ってIRISにデータ登録を試す場合の関数
def savefromfile(file):
    #file="C:\\WorkSpace\\EmbeddedPython-onlinelearning\\data\\txt\\OK5.txt"
    with open(file,"r", encoding='UTF-8') as f:
        datalist=f.readlines()

    f.close()

    receipt=iris.cls("Okaimono.Receipt")._New()
    total=0
    oldstr1=""
    for itemlist in datalist:
        str=itemlist.rstrip('\r\n').split("\t")
        if str[0]=="storename":
            receipt.StoreName=str[1]
        elif str[0]=="datetime":
            #datetimeに変換
            okaimonodt=datetime.datetime.strptime(str[1],'%Y年%m月%d日%H:%M')
            receipt.OkaimonoDateTime=okaimonodt.strftime('%Y-%m-%d %H:%M:%S')
        elif str[0]=="discount":
            receipt.Discount=str[1]
        elif str[0]=="total_price":
            total=1
        elif (str[0]=="itemprice") and (total==1):
            receipt.TotalPrice=str[1]
            total=0
        elif str[0]=="itemname" and (str[0].find("F食料品")<0):
            item=iris.cls("Okaimono.Item")._New()
            item.Name=str[1]
            oldstr1=item.Name
        elif (str[0]=="itemprice") and (oldstr1 !="") and (oldstr1.find("F食料品")<0) :
            item.Price=str[1]
            item.Receipt=receipt
            oldstr1=""

    #print(receipt.Items.Count())
    #iris.cls("%SYSTEM.OBJ").Dump(receipt)
    #iris.cls("%SYSTEM.OBJ").Dump(receipt.Items.GetAt(1))
    st=receipt._Save()
    if st != 1:
        raise Exception(st)
