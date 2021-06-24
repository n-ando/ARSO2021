#!/usr/bin/env python3
import openpyxl
import pprint

# col position
AUTHORS = 0
TITLE = 1
SESSION_TITLE = 2
SESSION_TYPE = 3
SESSION_CODE = 4
PAPER_TIME = 5

def channel_name(code, time):
    # set prefix from daycode
    if code == None: return ""
    if len(code) < 3: return ""
    if   code[0:2] == "Th": cname = "Day1_"
    elif code[0:2] == "Fr": cname = "Day2_"
    elif code[0:2] == "Sa": cname = "Day3_"
    else: return ""
    if code.find(".") > 0:
        (prefix, position) = code.split(".")
        poscode = F"%02d" % int(position)
        code = prefix + poscode

    return cname + time[0:2] + time[3:5] + "JST_" + code

wb = openpyxl.load_workbook('program.xlsx')

#print(type(wb))
# <class 'openpyxl.workbook.workbook.Workbook'>

#print(wb.sheetnames)
# ['sheet1', 'sheet2']
sheet = wb['Sheet1']
#print(list(sheet.values))

for p in list(sheet.values):
#    print("Authors:", p[0])
#    print("Title: ", p[1])
#    print("Session title: ", p[2])
#    print("Session type: ", p[3])
#    print("Session code: ", channel_name(p[4], p[5]))
#    print("Session time:", p[5])
#    print("-------------------------------------")
    if p[SESSION_CODE] == None or \
       p[PAPER_TIME] == None: continue
    if channel_name(p[4], p[5]) == "": continue

    desc = p[SESSION_TITLE] + " " + p[SESSION_CODE] + " (" + p[PAPER_TIME] + ")" + "\\n" + p[TITLE] + "\\n" + p[AUTHORS]
    print(channel_name(p[4], p[5]) + ":", desc)

