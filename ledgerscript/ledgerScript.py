import math
import sys
from datetime import datetime


def procOutput():
    TotHWbill = 0
    TotSWbill = 0; customerName = ''; creBal = 0; LaspayRecieved = '';LasBilRaise = '';LasHW_bildate = '';avgBillamt = 0
    opBal = 0;avgBillTout = 0;ratio1 = 0
    billFreq = '';PayFreq = "";ratio2 = ""
    TotDebtamt = 0;debitTout = 0;ratio3 = 0
    CrntTotDebtamt = 0;CrntTout = 0;ratio4 = 0
    res = 0;pes = 0
    billTimeDiff = []
    PayTimeDiff = []
    billCnt = 0
    print("inside procoutput")
    for p in range(0,len(proclist) - 1):
        # print(proclist[p][2])
        if(proclist[p][0] == "Ledger:"):
            customerName = proclist[p][1].strip()

        if(proclist[p][2] == "Closing Balance" and len(proclist[p][6]) > 1):
            creBal = float(proclist[p][6].strip())
            TotDebtamt = float(proclist[p-1][0])
            debitTout = creBal
            CrntTout = creBal
        
        if(proclist[p][2] == "Opening Balance" and len(proclist[p][5]) > 1):
                opBal = float(proclist[p][5])
                

        if "SBI OD AC" in proclist[p][2]:
                LaspayRecieved = proclist[p][6].strip()

        if "Journal" in proclist[p][3] or "SLB" in proclist[p][4] or "SR" in proclist[p][4]:
            LasBilRaise = proclist[p][5].strip()
        
        if "Journal" in proclist[p][3] or "SLB" in proclist[p][4]:
            if (len(proclist[p][5]) > 0):
                TotHWbill += float(proclist[p][5])
            LasHW_bildate = proclist[p][0].strip()

        if ("Journal" in proclist[p][3]) or ("SLB" not in proclist[p][4]) and ("Debit" not in proclist[p][5]):
            if (len(proclist[p][5]) > 0):
                TotSWbill += float(proclist[p][5])

        if(proclist[p][1] == 'Cr' and "Opening Balance" not in proclist[p][2] and "Closing Balance" not in proclist[p][2]):
            # print(proclist[p][0],proclist[p][5])
            newlist = [proclist[p][0],proclist[p][5]]
            billTimeDiff.append(newlist)
        
        if(proclist[p][3] == "Receipt" and len(proclist[p][6]) > 0):
                PayTimeDiff.append(proclist[p][0])
        
    print(PayTimeDiff)
    payDates = []
    PayUnqDates = []
    for i in range(0,len(PayTimeDiff)):
        month = PayTimeDiff[i][0:2]
        year = PayTimeDiff[i][len(PayTimeDiff[i][0])-4:]

        if(f"{month}{year}" not in payDates):
            print(f"{month}{year}")
            payDates.append(f"{month}{year}")
            PayUnqDates.append(f"{PayTimeDiff[i].strip()}")
    print(PayUnqDates) 


    if(len(PayUnqDates) >= 2):
        date_1 = PayUnqDates[0]
        date_2 = PayUnqDates[1]

        start = datetime.strptime(date_1, "%m/%d/%Y")
        end = datetime.strptime(date_2, "%m/%d/%Y")

        pes = (end.year - start.year) * 12 + (end.month - start.month)
        print('Difference between dates in months:', pes)
        
    if(pes == 1):
        PayFreq = "Monthly"
    if(pes > 1 and pes <= 3):
        PayFreq = "quaterly"
    if(pes > 3 and pes <= 6):
        PayFreq = "halfyearly"
    if(pes > 6):
        PayFreq = "yearly"


    uniqueDates = []
    UnqDates = []
    sum = 0
    for i in range(0,len(billTimeDiff)):
        month = billTimeDiff[i][0][0:2]
        year = billTimeDiff[i][0][len(billTimeDiff[i][0])-4:]
        if(f"{month}{year}" not in uniqueDates):
            # print(f"{month}{year}")
            uniqueDates.append(f"{month}{year}")
            UnqDates.append(f"{billTimeDiff[i][0].strip()}")
        if(len(billTimeDiff[i][1]) > 1):
            sum += float(billTimeDiff[i][1])
    
    if(len(UnqDates) >= 2):
        for i in range(0,len(UnqDates)):
            if(i == 2):
                break
    if(len(UnqDates) >= 2):
        date_1 = UnqDates[0]
        date_2 = UnqDates[1]

        start = datetime.strptime(date_1, "%m/%d/%Y")
        end = datetime.strptime(date_2, "%m/%d/%Y")

        res = (end.year - start.year) * 12 + (end.month - start.month)
        print('Difference between dates in months:', res)
    
    if(res == 1):
        billFreq = "Monthly"
    if(res > 1 and res <= 3):
        billFreq = "quaterly"
    if(res > 3 and res <= 6):
        billFreq = "halfyearly"
    if(res > 6):
        billFreq = "yearly"

    if(len(uniqueDates) > 1): 
        avgBillamt= int(sum/len(uniqueDates))
    if(opBal != 0 and creBal != 0):
        avgBillTout = int(creBal - opBal)
    else:
        avgBillTout = creBal
        
    if(avgBillTout != 0 and avgBillamt != 0):
        ratio1 = f"{round(avgBillamt/min(avgBillamt,avgBillTout))}:{round(avgBillTout/min(avgBillamt,avgBillTout))}"
    
    if(len(billFreq) > 1 and len(PayFreq) > 1):
        ratio2 = f"{billFreq}:{PayFreq}"
    
    if(TotDebtamt != 0 and debitTout != 0):
        ratio3 = f"{round(TotDebtamt/min(TotDebtamt,debitTout))}:{round(debitTout/min(TotDebtamt,debitTout))}"
    
    CrntTotDebtamt = TotDebtamt - opBal
    if(CrntTotDebtamt != 0 and CrntTout != 0):
        ratio4 = f"{round(CrntTotDebtamt/min(CrntTotDebtamt,CrntTout))}:{round(CrntTout/min(CrntTotDebtamt,CrntTout))}"
    
    

    print(customerName)
    print(LaspayRecieved)
    print(LasBilRaise)       
    print(creBal)
    print(TotHWbill)
    print(TotSWbill)
    print(LasHW_bildate)
    print(avgBillamt)
    print(avgBillTout)
    print(ratio1)
    print(TotDebtamt)
    print(debitTout)
    print(ratio3)
    print(CrntTotDebtamt)
    print(CrntTout)
    print(ratio4)
    print(billFreq)
    print(PayFreq)
    print(ratio2)
    op = open('ledgerOutput.csv','a')
    op.write(f"{customerName},{LaspayRecieved},{LasBilRaise},{creBal},{TotHWbill},{TotSWbill},{LasHW_bildate},{avgBillamt},{avgBillTout},{ratio1},{TotDebtamt},{debitTout},{ratio3},{CrntTotDebtamt},{CrntTout},{ratio4},{billFreq},{PayFreq},{ratio2}\n")
    op.close()


# START OF PROGRAM ------------------------------------------------------------------------------------

FileName = sys.argv[1]
file = open(FileName,'r')
FileData = file.readlines()
ledList = []

for line in FileData:
    inp = line.split(',')
    ledList.append(inp)

op = open('ledgerOutput.csv','a')
op.write(f"CustomerName,LasPayRecieved,LasBilRaise,CreditBalance,TotHWbill,TotSWbill,LasHW_bildate,avgBillamt,avgBillTout,avgBill:Tout,Totdebitamt,debitTout,TotDebit:debTout,CrntDebitamt,CrntTout,CrntDebitamt:CrntTout,debitFreq,creditFreq,dbtfreq:crdtfreq\n")
op.close()
       
# print(ledList)
proclist = []
print(len(ledList))
for i in range(0,len(ledList) - 1):
    # print(ledList[i])
    if "AEROLIA" in ledList[i][0] or "AEROLIA" in ledList[i][1]:
        continue
    if(ledList[i][0] == 'Ledger:'):
        for j in range(0,len(ledList)):
            # print(ledList[i+j])
            proclist.append(ledList[i+j])
            if(i+j+1 == len(ledList) - 1):
                break
            if(ledList[i+j+1][0] == 'Ledger:'):
                break
            
        # print(proclist)
        procOutput()
        proclist.clear()
        
       
 
    