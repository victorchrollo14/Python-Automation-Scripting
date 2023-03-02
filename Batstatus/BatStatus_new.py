import sys
from MySQLdb import _mysql
from datetime import datetime, timedelta



def procList(): 
    batpwrList = []
    for i in range(0,len(sortList)):
        if(i == len(sortList) - 1):
            break
        if(int(sortList[i][7]) == 1 and int(sortList[i+1][7]) == 0):
            # batpwrList.append(sortList[i])
            batpwrList.append(sortList[i+1])
            for j in range(0,len(sortList)):
                if((i+j) == len(sortList) - 1):
                    break
                if(int(sortList[i+j][7]) == 0 and int(sortList[i+j+1][7]) == 1):
                     batpwrList.append(sortList[i+j])
                    #  batpwrList.append(sortList[i+j+1])
                     break

    x = open('output.csv','a')
    for i in range(0,len(batpwrList)):
        if(i == len(batpwrList) - 1):
            break
        if(i == 0 or i%2 == 0):
            starttime = datetime.strptime(batpwrList[i][2], "%Y-%m-%d %H:%M:%S")
            endtime = datetime.strptime(sortList[i+1][2], "%Y-%m-%d %H:%M:%S")
            timediff =  endtime - starttime
            daysdiff = int(timediff.total_seconds()/(60*60*24))
            x.write(f"{batpwrList[i][1]},{batpwrList[i][3]},{batpwrList[i+1][3]},{abs(daysdiff)}\n")
    for line in batpwrList:
        print(line)
    batpwrList.clear()
    x.close()




# START OF PROGRAM

filename = sys.argv[1]
file = open(filename,'r')
filedata = file.readlines()
count = 0
sortList = []

currentTime = datetime.now()
startTime = currentTime - timedelta(days = 20)
print(f"{currentTime}\n{startTime}")

x = open('output.csv','a')
x.write(f'device id,BV previous, BV current, days-Diff\n')
x.close()


for vehicleid in filedata:
    try:
      db = _mysql.connect('savi1904.cu5bxoduqxch.us-east-1.rds.amazonaws.com','awstracker3','sensel2012','awstracker3')
    except:
        print("unable to connect to server")

    vehicleid = vehicleid.strip('\n')
    print(vehicleid,'\n')

    db.query(f"SELECT * FROM batstatus a WHERE a.vehicleid = '{vehicleid}' and  a.timestamp > '{startTime}' ORDER BY a.timestamp ;")
    results = db.store_result()
    while( 1 ):
        data = results.fetch_row()
        if(len(data) < 1):
            break
        uid    =    str(data[0][0].decode())
        deviceid =  str(data[0][1].decode())
        timestamp = str(data[0][2].decode())
        bv =        str(data[0][3].decode())
        chrger =    str(data[0][4].decode())
        dischrg =   str(data[0][5].decode())
        chrgng =    str(data[0][6].decode())
        batpwr =    str(data[0][7].decode())
        newlist = [uid,deviceid,timestamp,bv,chrger,dischrg,chrgng,batpwr]
        sortList.append(newlist)

    procList()
    sortList.clear()
    # print(sortList)



       

        

    
