from win32com.client import Dispatch
excel = Dispatch("Excel.Application") 
excel.Visible = False
register_excel = excel.Workbooks.Open(r'C:\Users\YHU\Desktop\Matlab2Py\register_field_defaults_2p0.xml')
register_sheet = register_excel.ActiveSheet
register_name_range = register_sheet.Range("A2:A824")
register_address_range = register_sheet.Range("G2:G824")
register_address = {}
temp = []
for index in range(len(register_name_range)):
    temp.append((str(register_name_range[index]),'0x'+str(register_address_range[index])))
temp.sort()
wrong_address = []
for index in range(len(temp)-1):
    if temp[index][0] == temp[index+1][0]:
        if temp[index][1]!=temp[index+1][1]:
            wrong_address.append(temp[index])
if wrong_address:
    print wrong_address
register_address = dict(temp)
    
    
    
