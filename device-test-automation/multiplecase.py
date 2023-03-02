import csv
import sys
from datetime import datetime
from MySQLdb import _mysql
import time
from datetime import date, timedelta


def serverReq():
    for vehicleid in vehicleids:                 # waiting until serverrequests gets sent to all the devices
        print(f"waiting until the serverrequests gets sent to the {vehicleid}")
        while (1):
            serQlist = []
            db.query(
                "SELECT * FROM serverrequests a WHERE a.VehicleID = '" + vehicleid + "' ;")
            server_result = db.store_result()
            while (1):
                serQ = server_result.fetch_row()
                if (len(serQ) < 1):
                    break
                serQlist.append(serQ)
            if (len(serQlist) < 1):
                break
            serQlist.clear()
            #  print(serQlist)

# __________ _________________ ______________ _____________________ ______________________ _________________ _____________ _______________


def TcpParser():
    #  setting the time delay and getting the start time and endtime

    time.sleep(20)
    print(f"*****testing in 'SLOWTRACKTIME' *****")
    slowtr_delay = (int(slowtrack) * int(slowupdtcount) * packet_count)
    print(
        f'wait for {slowtr_delay//60} minutes to check for packets in slow mode')
    stime = datetime.now()
    starttime = stime.strftime("%Y-%m-%d %H:%M:%S")
    #   starttime = "22-03-02 15:33:18"
    print(f'TcpParser starttime:{starttime}')
    # delaying the code from getting executed as per the desired no of packets
    time.sleep(slowtr_delay)
    etime = datetime.now()
    endtime = etime.strftime("%y-%m-%d %H:%M:%S")
    #   endtime = "22-03-02 15:43:18"
    print(f'TcpParser endTime : {endtime} \n')

    # reconnecting to the server

    try:
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")
        # connecting to the server
        print("reconnected to the server successfully")
    except:
        print("connection unsuccessful ")

    i = 0       # using i = 0 we are trying to assign pass or fail for 1st device and i = 1 for 2nd device

    # __________________________________________________________________________________________________________________

    # iterating through both devices to get packets between 2 timestamps and check if there are expected no of packets with the expected mode(fast or slow) based on which testcase passes or fails

    for vehicleid in vehicleids:
        db.query("SELECT  UID,serverTS,content FROM TcpParserMonitor a WHERE a.UID = '" + vehicleid +
                 "' AND a.serverTS > '" + str(starttime) + "' AND a.serverTS < '" + str(endtime) + "';")
        TcpParser = db.store_result()
        packetList = []
        print(f"\n'testing{vehicleid}'")
        count = 0
        while (1):
            x = TcpParser.fetch_row()
            if (len(x) < 1):
                break
            uid = x[0][0].decode()
            serverTs = x[0][1].decode()
            content = x[0][2].decode()
            op = open('multitest.txt', 'a')
            op.write(f'[{serverTs} \n {content}\n')
            op.close()

            packetList.append(content)
            data = content.split('&')
            if (data[9] == 'r,0'):
                if (data[10] == 's,0'):
                    count += 1
            else:
                if (data[9] == 's,0'):
                    count += 1

        print(f'no of packets with s,0 = {count}')
        print(packetList)

        global SLresult1           # record pass/fail values for 1st device
        global SLresult2           # record pass/fail values for 2nd device

        # __________________________________________________________________________________________________________________

        if (count == packet_count or count == packet_count - 1):
            if (i == 0):          # when i = 0 we are running test on 1st device
                SLresult1 = 'PASS'
            if (i == 1):           # when i = 1 we are running test on 2st device
                SLresult2 = 'PASS'
            op = open('multitest.txt', 'a')
            op.write(
                f"\ntesting{vehicleid} \nSLOWTRACKTIME: 'PASS'\ntotal no of packets in slow mode = {count}]\n\n")
            op.close()

            print(f'total no of packets in slow mode = {len(packetList)}')
            print(f"Testcase no {test_no} Result: 'PASS' \n")
        else:
            if (i == 0):
                SLresult1 = 'FAIL'
            if (i == 1):
                SLresult2 = 'FAIL'
            op = open('multitest.txt', 'a')
            op.write(
                f"testing{vehicleid}\nSLOWTRACKTIME: 'FAIL'\ntotal no of packets in slow mode = {count}]\n\n")
            op.close()

            print(
                f'total no of packets in slow mode = {len(packetList)} is not equal to the expected no of packets')
            print(f"Testcase no {test_no} Result: 'FAIL'\n")
        i += 1

    db.close()

# _____  ______________  ________________  ___________________________  ________________________  _____________  ___________  _____________


def fastmode():
    time.sleep(20)
    fastpckt = int(fastvibint)//int(fasttrack)
    print("**** testing in 'FASTTRACKTTIME' *****")
    print("required number of packets in fast mode =", fastpckt)
    fast_delay = fastpckt * 60 + 30

    fsS = datetime.now()
    fsStart = fsS.strftime("%y-%m-%d %H-%M-%S")
    # fsStart = "22-03-24 13-26-09"
    print(fsStart)
    print(f'wait for{fast_delay//60} minutes')
    time.sleep(fast_delay)
    fe = datetime.now()
    fsEnd = fe.strftime("%y-%m-%d %H-%M-%S")
    # fsEnd = "22-03-24 13-30-09"
    print(fsEnd)
    try:
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")
        # print("reconnected to the server successfully")                                 # connecting to the server
    except:
        print("connection unsuccessful ")
    i = 0

    # __________________________________________________________________________________________________________________

    for vehicleid in vehicleids:
        db.query("SELECT  UID,serverTS,content FROM TcpParserMonitor a WHERE a.UID = '" + vehicleid +
                 "' AND a.serverTS > '" + str(fsStart) + "' AND a.serverTS < '" + str(fsEnd) + "';")
        tcpresult = db.store_result()
        print(f"\n'testing{vehicleid}'")
        fsList = []
        count = 0
        while (1):
            x = tcpresult.fetch_row()
            print(x)
            if (len(x) < 1):
                break
            uid = x[0][0]
            serverTs = x[0][1].decode()
            content = x[0][2].decode()

            op = open('multitest.txt', 'a')
            op.write(f'[{serverTs} \n {content} \n')
            op.close()
            fsList.append(content)
            data = content.split('&')

            if (data[9] == 'r,0'):
                if (data[10] == 's,1'):
                    count += 1
            else:
                if (data[9] == 's,1'):
                    count += 1

        print(f'no of packets with s,1 = {count}')
        global FSresult1
        global FSresult2
        print("the number of packets found in tcpparsermonitor =", len(fsList))

       # __________________________________________________________________________________________________________________

        if (count == fastpckt - 1 or count >= fastpckt and logic2 == 0):
            if (i == 0):
                FSresult1 = 'PASS'
            if (i == 1):
                FSresult2 = 'PASS'
            op = open('multitest.txt', 'a')
            op.write(
                f"\ntesting{vehicleid}\nFASTTRACKTIME:'PASS'\ntotal no of packets in fast mode = {count}]\n\n")
            op.close()
            print(f"test case no {test_no}  Result:'PASS'")
        else:
            if (i == 0):
                FSresult1 = 'FAIL'
            if (i == 1):
                FSresult2 = 'FAIL'
            op = open('multitest.txt', 'a')
            op.write(
                f"\ntesting{vehicleid}\nFASTTRACKTIME:'FAIL'\ntotal no of packets in fast mode = {count}]\n\n")
            op.close()
            print(f"test case no {test_no}  Result: 'FAIL'")
        i += 1
    db.close()

    # after end of 1 complete test case we'll delay for 5min to enable device to go to slow mode

    time.sleep(300)
    for vehicleid in vehicleids:
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")
        db.query(
            f"INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES ('{vehicleid}','5','(SET FASTTOSLOW)');")
        db.close

# _____  ______________  ________________  ___________________________  ________________________  _____________  ___________  _____________


def SlowServDis():
    time.sleep(20)
    print(f"***testing in 'SLOWTRACKTTIME' ***")
    slowtr_delay = (int(slowtrack) * int(slowupdtcount) * packet_count)
    print(
        f'wait for {slowtr_delay//60} minutes to check for packets in slow mode')
    stime = datetime.now()
    starttime = stime.strftime("%Y-%m-%d %H:%M:%S")
    #   starttime = "22-03-02 15:33:18"
    print(f'positiondata starttime:{starttime}')
    # delaying the code from getting executed as per the desired no of packets
    time.sleep(slowtr_delay)
    etime = datetime.now()
    endtime = etime.strftime("%y-%m-%d %H:%M:%S")
    #   endtime = "22
    print(f'positiondata endTime : {endtime}')
    # reconnecting to the server
    try:
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")
        # connecting to the server
        print("reconnected to the server successfully")
    except:
        print("connection unsuccessful ")
    i = 0

    # __________________________________________________________________________________________________________________

    for vehicleid in vehicleids:
        db.query(
            f'SELECT * FROM positiondata a WHERE a.TruckID = "{vehicleid}"  AND a.TimeStamp> "{starttime}" AND a.TimeStamp< "{endtime}" ORDER BY a.TimeStamp DESC ;')
        positionData = db.store_result()
        print(f"\n'testing{vehicleid}")
        posList = []
        op = open('multitest.txt', 'a')
        op.write(
            '[id,Truckid,Timestamp,start,stop,latitude,longitude,speed,fuellevel,lac,ci \n')
        op.close()
        count = 0
        while (1):
            d = positionData.fetch_row()
            if (len(d) < 1):
                break
            id = d[0][0].decode()
            Truckid = d[0][1].decode()
            Timestamp = d[0][2].decode()
            start = d[0][3].decode()
            stop = d[0][4].decode()
            latitude = d[0][5].decode()
            longitude = d[0][6].decode()
            speed = d[0][7].decode()
            fuellevel = d[0][8].decode()
            lac = d[0][9].decode()
            ci = d[0][10].decode()
            posList.append(fuellevel)
            if (stop == 1):
                count += 1

            op = open('multitest.txt', 'a')
            op.write(
                f'{id}, {Truckid}, {Timestamp}, {start}, {stop}, {latitude}, {longitude}, {speed}, {fuellevel}, {lac}, {ci} \n')
            op.close()

        print(f'no of packets with stop 1 = {count}')
        global SLresult1
        global SLresult2
        print(posList)

        # __________________________________________________________________________________________________________________

        if (count == packet_count or count == packet_count - 1):
            if (i == 0):
                SLresult1 = 'PASS'
            if (i == 1):
                SLresult2 = 'PASS'
            op = open('multitest.txt', 'a')
            op.write(
                f"\ntesting{vehicleid}\nSLOWTRACKTIME: 'PASS'\ntotal no of packets in slow mode = {count}]\n\n")
            op.close()
            print(
                f'The total no of packets in slowtrack through sms is: {len(posList)}')
            print(f"Testcase no {test_no} Result: 'PASS' \n")
        else:
            if (i == 0):
                SLresult1 = 'FAIL'
            if (i == 1):
                SLresult2 = 'FAIL'
            op = open('multitest.txt', 'a')
            op.write(
                f"\ntesting{vehicleid}\nSLOWTRACKTIME: 'FAIL'\ntotal no of packets in slow mode = {count}]\n\n")
            op.close()
            print(
                f'The total no of packets in slowtrack through sms is: {len(posList)}')
            print(f"Testcase no {test_no} Result: 'FAIL' \n")
        i += 1
    db.close()


# _____  ______________  ________________  ___________________________  ________________________  _____________  ___________  _____________


# checking for packets when fastserverupdt is disabled
def fastServDis():
    fastpckt = int(fastvibint)//int(fasttrack)
    print("******testing in 'FASTTRACKTTIME' ******")
    print("required number of packets in fast mode =", fastpckt)

    fast_delay = fastpckt * 60 + 30
    time.sleep(20)
    fsS = datetime.now()
    fsStart = fsS.strftime("%y-%m-%d %H-%M-%S")
    # fsStart = "22-03-04 17-05-31"
    print(f'positiondata starttime:{fsStart}')
    time.sleep(fast_delay)
    fe = datetime.now()
    fsEnd = fe.strftime("%y-%m-%d %H-%M-%S")
    # fsEnd = "22-03-04 17-08-31"
    print(f'positiondata end time:{fsEnd}')
    try:
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")
        # connecting to the server
        print("reconnected to the server successfully")
    except:
        print("connection unsuccessful ")
    i = 0

    # __________________________________________________________________________________________________________________

    for vehicleid in vehicleids:
        db.query(
            f'SELECT * FROM positiondata a WHERE a.TruckID = "{vehicleid}"  AND a.TimeStamp> "{fsStart}" AND a.TimeStamp< "{fsEnd}" ORDER BY a.TimeStamp DESC ;')
        positionData = db.store_result()
        print(f"\n'testing{vehicleid}'")
        posList = []
        op = open('multitest.txt', 'a')
        op.write(
            ' \n[id,Truckid,Timestamp,start,stop,latitude,longitude,speed,fuellevel,lac,ci \n')
        op.close()
        count = 0
        while (1):
            d = positionData.fetch_row()
            if (len(d) < 1):
                break
            id = d[0][0].decode()
            Truckid = d[0][1].decode()
            Timestamp = d[0][2].decode()
            start = d[0][3].decode()
            stop = d[0][4].decode()
            latitude = d[0][5].decode()
            longitude = d[0][6].decode()
            speed = d[0][7].decode()
            fuellevel = d[0][8].decode()
            lac = d[0][9].decode()
            ci = d[0][10].decode()

            op = open('multitest.txt', 'a')
            op.write(
                f'{id}, {Truckid}, {Timestamp}, {start}, {stop}, {latitude}, {longitude}, {speed}, {fuellevel}, {lac}, {ci} \n')
            op.close()

            if (stop == 0):
                count += 1
            posList.append(fuellevel)

        # __________________________________________________________________________________________________________________

        print(posList)
        print(f"total no of packets in fastmode through sms:{count} \n")
        print(f'no of packets with stop 0 = {count}')
        global FSresult1
        global FSresult2
        if (count >= fastpckt or count == fastpckt - 1 and logic2 == 0):
            if (i == 0):
                FSresult1 = 'PASS'
            if (i == 1):
                FSresult2 = "PASS"
            op = open('multitest.txt', 'a')
            op.write(
                f"\ntesting{vehicleid}\nFASTTRACKTIME:'PASS'\ntotal no of packets in fast mode = {count}]\n\n")
            op.close()
            print(f"test case no {test_no} Result: 'PASS' ")

        else:
            if (i == 0):
                FSresult1 = 'FAIL'
            if (i == 1):
                FSresult2 = "FAIL"
            op = open('multitest.txt', 'a')
            op.write(
                f"\ntesting{vehicleid}\nFASTTRACKTIME: 'FAIL'\ntotal no of packets in fast mode = {count}]\n\n")
            op.close()
            print(f"test case no {test_no} Result: 'FAIL' ")
        i += 1
    db.close()

    # after end of 1 complete test case we'll delay for 5min to enable device to go to slow mode
    time.sleep(300)
    for vehicleid in vehicleids:
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")
        db.query(
            f"INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES ('{vehicleid}','5','(SET FASTTOSLOW)');")
        db.close


# _____  ______________  ________________  ___________________________  ________________________  _____________  ___________  _____________


# starting vibrations
def startVib():
    vib_deviceID = "INST34210"     # device that controls vibrations
    print("starting vibrations")

    try:
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")
        # connecting to the server
        print("reconnected to the server successfully \n")
    except:
        print("connection unsuccessful ")

    if (int(slowserverupdt) == 1):
        for vehicleid in vehicleids:                 # enabling slowserverupdt when disabled
            db.query(
                f"INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES ('{vehicleid}','5','(SET SLOWSERVERUPDT 0)');")

            # sending cmd to on the fan
    db.query(
        f"INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES ('{vib_deviceID}','5','(SET IMMON 1)');")
    db.close()
    print(f"vibrations started:{datetime.now()}")
    op = open('multitest.txt', "a")
    op.write(f"vibration start:{datetime.now()}\n")
    op.close()

    # _______________________________________________________________________________________________________________________________

    if (int(anglediffthd) > 0):                 # testing for 2nd logic in testcase 8 and 9
        time.sleep(int(slowvibinterval) + 120)
        # subtracting 2 min from current time
        qtime = datetime.now() - timedelta(hours=0, minutes=2)
        qtime.strftime('%H:%M %p')
        db = _mysql.connect
        ("Hostname", "dbusername", "password", "dbname")

        # checking in tcpparser monitor when fastserver update is enabled

        if (int(fastserverupdt) == 0):
            for vehicleid in vehicleids:
                count = 0
                op = open('multitest.txt', "a")
                db.query(
                    f'SELECT UID,serverTS,content FROM TcpParserMonitor a WHERE a.UID="{vehicleid}"  AND a.ServerTS>"{qtime}";')
                # checking for packets in fastmode
                res = db.store_result()
                while (1):
                    r = res.fetch_row()
                    if (len(r) < 1):
                        break
                    uid = r[0][0].decode()
                    serverts = r[0][1].decode()
                    content = r[0][2].decode()
                    op.write(f'{content}')
                    data = content.split('&')
                    # checking whether s,1 is present in content packets
                    if (data[9] == 'r,0'):
                        if (data[10] == 's,1'):
                            count += 1                          # count increases when we find s,1 packet
                    else:
                        if (data[9] == 's,1'):
                            count += 1
                print(count)
                if (count > 0):
                    # if we find any packet in fast mode then logic 2 fails else passes
                    logic2 = 1
                    op.write(
                        f"device alerted in 1st logic in  {vehicleid} \nfast packets count = {count}\n*_____*__________*________\n\n")
                else:
                    op.write(
                        f"logic 2 passed in {vehicleid} \nfast packets count = {count}\n*_____*__________*________\n\n")
                op.close()
        # __________________________________________________________________________________________________________________

        # checking in postiondata when fastserverupdt is disabled
        else:
            for vehicleid in vehicleids:
                count = 0
                op = open('multitest.txt', "a")
                db = _mysql.connect(
                    "Hostname", "dbusername", "password", "dbname")
                db.query(
                    f'SELECT * FROM positiondata a WHERE a.TruckID="{vehicleid}"  AND a.TimeStamp>"{qtime}";')
                positionData = db.store_result()
                while (1):
                    d = positionData.fetch_row()
                    if (len(d) < 1):
                        break
                    id = d[0][0].decode()
                    Truckid = d[0][1].decode()
                    Timestamp = d[0][2].decode()
                    start = d[0][3].decode()
                    stop = d[0][4].decode()
                    latitude = d[0][5].decode()
                    longitude = d[0][6].decode()
                    speed = d[0][7].decode()
                    fuellevel = d[0][8].decode()
                    lac = d[0][9].decode()
                    ci = d[0][10].decode()
                    op.write(
                        f'{id}, {Truckid}, {Timestamp}, {start}, {stop}, {latitude}, {longitude}, {speed}, {fuellevel}, {lac}, {ci} \n')

                    if (stop == 0):
                        count += 1
                if (count > 0):
                    # if we find any packet in fast mode then logic 2 fails else passes
                    op.write(
                        f"device alerted in 1st logic in  {vehicleid} \nfast packets count = {count}\n *_____*__________*________\n\n")
                else:
                    op.write(
                        f"logic 2 passed in {vehicleid} \nfast packets count = {count}\n*_____*__________*________\n\n")
                op.close()
        # total vibration of slwvibintbi +  120 seconds
        time.sleep(int(slwvibintbi) - (int(slowvibinterval) + 60))

    else:
        time.sleep(int(slowvibinterval) + 180)

    db = _mysql.connect("Hostname", "dbusername", "password", "dbname")

    db.query(
        f"INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES ('{vib_deviceID}','5','(SET IMMON 0)');")
    # off the fan
    print(f"vibrations ended:{datetime.now()}")
    op = open('multitest.txt', "a")
    op.write(f"vibration endtime:{datetime.now()}\n")
    op.close()

    db.close()

# _________________________________________________________________________________________________________________________________


filename = sys.argv[1]
csv_file = open(filename, 'r')
csv_reader = csv.reader(csv_file)
# ADDING TESTING DEVICE ID
vehicleids = ["33770", "35663"]
packet_count = 1
lines = []
# Writing the testcaseNo to the output file
op = open('multitest.txt', 'a')
op.write(
    f'################### {date.today()}  ##############################\n')
op.close()
for line in csv_file:
    if (len(line) < 100):
        inp = line.split(",")
        # assigning the configuration names to each values respectively
        test_no = inp[0]
        model = inp[1]
        accl = inp[2]
        slowtrack = inp[3]
        slowupdtcount = inp[4]
        slowmodestandby = inp[5]
        slowvibinterval = inp[6]
        slowmotioncount = inp[7]
        tampintto = inp[8]
        slwvibintbi = inp[9]
        slwmotioncnbi = inp[10]
        tmp1inttobi = inp[11]
        fasttrack = inp[12]
        fastmodestandby = inp[13]
        fastvibint = inp[14]
        fastmotioncount = inp[15]
        theftslowtrack = inp[16]
        slowserverupdt = inp[17]
        fastserverupdt = inp[18]
        theftserverupdt = inp[19]
        slowsmsupdt = inp[20]
        fastsmsupdt = inp[21]
        theftsmsupdt = inp[22]
        sgnspgsupdt = inp[23]
        anglediffthd = inp[24]
        geofencetype1 = inp[25]
        geofencetype2 = inp[26]

        try:
            # connecting to the server
            db = _mysql.connect("Hostname", "dbusername", "password", "dbname")
        except:
            print("connection unsuccessful ")

        logic2 = 0
        print(f"###starting test case {test_no} ####")
        if (int(anglediffthd) == 0):
            continue

        # Writing the testcaseNo to the output file
        op = open('multitest.txt', 'a')
        op.write(f'Test case {test_no} \n')
        op.close()

        # __________________________________________________________________________________________________________________

        # passing all the configuration to the server
        for vehicleid in vehicleids:
            db.query("INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES('" + vehicleid + "','5','(SET MODEL " + str(model) +
                     ", SET ACCL " + str(accl) + " , SET SLOWTRACKTIME " + str(slowtrack) + ",SET SLOWUPDTCOUNT " + str(slowupdtcount) + ")');")

            db.query("INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES('" + vehicleid + "','5','(SET SLOWMODESTANDBY " + str(slowmodestandby) +
                     ",SET SLOWVIBINTERVAL " + str(slowvibinterval) + ",SET SLOWMOTIONCOUNT " + str(slowmotioncount) + ",SET TAMPINTTO " + str(tampintto) + ")');")

            db.query("INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES('" + vehicleid + "','5','(SET SLWVIBINTTBI " + str(slwvibintbi) +
                     ", SET SLWMOTIONCNTBI " + str(slwmotioncnbi) + " , SET TMP1INTTOBI " + str(tmp1inttobi) + ",SET FASTTRACKTIME " + str(fasttrack) + ")');")

            db.query("INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES('" + vehicleid + "','5','(SET FASTMODESTANDBY " + str(fastmodestandby) +
                     ",SET FASTVIBINTERVAL " + str(fastvibint) + ",SET FASTMOTIONCOUNT " + str(fastmotioncount) + ",SET THEFTSLOWTRACKTIME " + str(theftslowtrack) + ")');")

            db.query("INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES('" + vehicleid + "','5','(SET SLOWSERVERUPDT " +
                     str(slowserverupdt) + ", SET FASTSERVERUPDT " + str(fastserverupdt) + " , SET THEFTSERVERUPDT " + str(theftserverupdt) + ")');")

            db.query("INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES('" + vehicleid + "','5','(SET SLOWSMSUPDT " +
                     str(slowsmsupdt) + ",SET FASTSMSUPDT " + str(fastsmsupdt) + ",SET THEFTSMSUPDT " + str(theftsmsupdt) + ")');")

            db.query("INSERT INTO serverrequests(vehicleid,requestno,requestmsg) VALUES('" + vehicleid + "','5','(SET SGNGPRSUPDT " + str(sgnspgsupdt) +
                     ", SET ANGLEDIFFTHD " + str(anglediffthd) + " , SET GEOFENCETYPE1 " + str(geofencetype1) + ",SET GEOFENCETYPE2 " + str(geofencetype2) + ")');")

        # end of sending the configuration to the server
        print("configurations inserted into serverrequests")

        # __________________________________________________________________________________________________________________

        # looping inside serverrequest until serverrequests gets sent to device
        serverReq()
        print("server request sent to the device successfully\n")
        # closing the connection to the server to avoid lost connection error caused by time.sleep()
        db.close()
        print("disconnected from server ")

        # if(int(slowserverupdt) == 0):      # getting the packets from TcpParserMonitor (slowmode)
        #     TcpParser()

        # if(int(slowserverupdt) == 1):      # getting the packets from positiondata when serverupdt is disabled(slowmode)
        #     SlowServDis()

        startVib()                   # introduces vibrations that enables fastmode

        if (int(fastserverupdt) == 0):       # checking for packets in TcpParserMonitor(fast mode)
            fastmode()

        # checking for packets in positiondata when serverupdt is disabled(fastmode)
        if (int(fastserverupdt) == 1):
            fastServDis()

        # __________________________________________________________________________________________________________________

        for veh in range(len(vehicleids)):
            if (veh == 0):
                # IF SLOWMODE AND FASTMODE PASSES THEN WHOLE TEST CASE PASSES
                if (SLresult1 == 'PASS' and FSresult1 == "PASS"):
                    print(f'testcase{test_no}: "PASS"')
                    op = open('multitest.txt', 'a')
                    op.write(
                        f'[{vehicleids[veh]}\ntestcase{test_no}: "PASS" ]\n\n')
                    op.close()
                else:
                    print(f'testcase{test_no}: "FAIL"')
                    op = open('multitest.txt', 'a')
                    op.write(
                        f'[{vehicleids[veh]}\ntestcase{test_no}: "FAIL"]\n\n')
                    op.close()
            if (veh == 1):
                # IF SLOWMODE AND FASTMODE PASSES THEN WHOLE TEST CASE PASSES
                if (SLresult2 == 'PASS' and FSresult2 == "PASS"):
                    print(f'testcase{test_no}: "PASS"')
                    op = open('multitest.txt', 'a')
                    op.write(
                        f'[{vehicleids[veh]}\ntestcase{test_no}: "PASS"]\n\n_______________________________________________________________________________________"\n\n')
                    op.close()
                else:
                    print(f'testcase{test_no}: "FAIL"')
                    op = open('multitest.txt', 'a')
                    op.write(
                        f'[{vehicleids[veh]}\ntestcase{test_no}: "FAIL"]\n\n _____________________________________________________________________________________________"\n\n')
                    op.close()

        print("\n")
        print("-*-" * 10, "\n")

        #   if(int(test_no) == 4):
        #       break
