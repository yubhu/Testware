class Chip():
    def __init__(self,name='Slingshot-D', chiprev=3.0, revlist=[1.1,2.0,3.0], register_length=8, host_port=None, simulate_i2c_calls=False):
        self.name = name
        self.chiprev = chiprev
        self.revlist = revlist
        self.register_length = register_length
        self.host_port = host_port
        self.simulate_i2c_calls = simulate_i2c_calls
        self.addresses = {}
        for item in self.revlist:
            self.addresses.update(self.fill_addresses(item))
        self.fields = {}
        for item in self.revlist:
            self.fields.update(self.fill_fields(item)) 

            
    def fill_addresses(self,revision):
        import os
        import csv
        processed = revision*10
        main_version = int(processed/10)
        minor_version = int(processed%10)
        target_file = r'C:\Users\wireless_system\Desktop\Python_bringup\code\register_field_defaults_%dp%d.csv' %(main_version,minor_version)
        file_exists = os.path.isfile(target_file)
        if not file_exists:
            print "register_field_defaults_%dp%d.xml not exists!" %(main_version,minor_version)
            return None
        csvfile = open(target_file)
        csvreader = csv.reader(csvfile)
        temp = []
        conflict_address = []
        for line in csvreader:
            if str(line[0])!='register':
                register_name_p = str(line[0]).strip()
                register_address_p = '0x' + str(line[6]).strip()
                temp.append((register_name_p,register_address_p))
        temp.sort()
        for index in range(len(temp)-1):
            if temp[index][0] == temp[index+1][0]:
                if temp[index][1]!=temp[index+1][1]:
                    conflict_address.append((temp[index],temp[index+1]))
        '''        
        if conflict_address:
            print "There is some address conflict in %dp%d.xml:" %(main_version,minor_version)
            print conflict_address
        '''
        print 'Alread set register address for Rev %dp%d chip.' %(main_version,minor_version)
        csvfile.close()
        return dict(temp)
    
    def fill_fields(self,revision):
        import os
        import csv
        import re
        pattern = re.compile(r'[0-9]+:[0-9]+:[0-9]+')
        processed = revision*10
        main_version = int(processed/10)
        minor_version = int(processed%10)
        target_file = r'C:\Users\wireless_system\Desktop\Python_bringup\code\register_field_defaults_%dp%d.csv' %(main_version,minor_version)
        file_exists = os.path.isfile(target_file)
        if not file_exists:
            print "register_field_defaults_%dp%d.xml not exists!" %(main_version,minor_version)
            return None
        csvfile = open(target_file)
        csvreader = csv.reader(csvfile)
        register_field = {}
        address_fieldbit = []
        register_fieldname_range_temp = []        
        for line in csvreader:
            if str(line[0])!='register':
                register_address_p = '0x' + str(line[6]).strip()
                field_name_processed = str(line[2]).upper().strip()
                if pattern.search(str(line[3]).strip()):
                    filed_bit_p = process_field_bit(str(line[3]).strip())
                    register_fieldbit_p = str(line[3]).strip()
                else:
                    register_fieldbit_p = str(line[3]).strip()
                address_fieldbit.append((register_address_p,register_fieldbit_p))
                if field_name_processed.endswith(']'):
                    register_fieldname_range_temp.append(field_name_processed[:-5])
                else:
                    register_fieldname_range_temp.append(field_name_processed)                
        register_field_list = zip(register_fieldname_range_temp,address_fieldbit)
        register_field_list.sort()
        conflict_field = []
        for index in range(len(register_field_list)-1):
            if register_field_list[index][0]!='RSVD':
                if register_field_list[index][0]== register_field_list[index+1][0]:
                    if register_field_list[index][1]!=register_field_list[index+1][1]:
                        conflict_field.append((register_field_list[index],register_field_list[index+1]))        
        '''
        if conflict_field:
            print "There is some conflict in field address or field bit range in %dp%d.xml:" %(main_version,minor_version)
            print conflict_field
        '''
        register_field = dict(register_field_list)
        if 'RSVD' in register_field:
            register_field.pop('RSVD')
        csvfile.close()
        return register_field
    
    def process_field_bit(input_str):
        str_processed = input_str.split(':')
        return str_processed[0]+':'+str_processed[1][2]
    
