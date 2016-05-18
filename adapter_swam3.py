"""Adapter communication module.

It has functions that can start and terminate the commandserver.
It has functions to send commands to the adapter device, embedded and host,
and return responses.
"""

import subprocess
import time
import logg
import socket
import re
import sys
import traceback
import time
import os.path

#import logg

#global src_server
#global sink_server

RETRY_MAXCOUNT = 3 #Command retry max count
COMMAND_TIMEOUT_NVRAMSHOW = 5.0 #Command response timeout for nvram_show
COMMAND_TIMEOUT = 3.0 #Command response timeout for all other commands
PORT = ""

class Adapter:        
    def __init__(self, tcpport, comport, logfile, embedded_interface = "SPI", host_on_module = "0"):
        
        """Start the cmdserver task. The function does not block, and returns
    immediately after starting the server. Returns the TCPPORT that the server is listening
    on. This TCPPORT can be passed to sendnxpcmd/SendTenCmd functions to send commands to the device.
    Returns 0 if the cmdserver can not be successfully opened"""
        
        #sss_path = "C:/SS_SERVER-Release/SS_SERVER.exe"
        bc_path = "C:/svn/ta/boxcutter-1.5/boxcutter-fs.exe"
              
        #sss_path = "C:/Program Files/Sibeam/SBAM2/SS_SERVER.exe"
        sss_path = "C:\Program Files (x86)\Silicon Image\SWAM3\SWAM3.exe"

        # Gen2
        logg.L.log("Starting the ss_server task on TCPPORT "+str(tcpport)+", serial port "+comport+" and logging to file "+logfile+"...")               
        if host_on_module.upper() == "YES":
            host_on_module = "1"
        elif host_on_module.upper() == "NO":
            host_on_module = "0"
        cmd = sss_path + " server_slingshot --commport="+\
                            comport+" --portno="+str(tcpport)\
                                +" --logfilename="+logfile\
                                    +" --logsendtoclient=0"\
				    +" --logtimestamp=0"\
									+" --minimize=0"\
                                    +" --logtoconsole=0"+" --start=1"
        # In the ss_server, do not log to console. Sometimes observed OUTOFMEMORYEXCEPTION
        # that have been traced to logging to console, especially when running multiple pairs.
        # See the notes.doc for more information.
        logg.L.log("cmd: "+cmd)

        server = subprocess.Popen(cmd)
        time.sleep(10)
        i=0
        while server.poll() and (i<20):
            time.sleep(3)
            i=i+1
            
        if server.poll():
            logg.L.log("ERROR: Unable to start the ss_server")
            # Capture a screen-shot of the desktop
            sshot = logg.log_dir+"/screenshot_"+comport+".bmp"
            c = 1
            while (os.path.exists(sshot)):
                sshot = logg.log_dir+"/screenshot-"+comport+"-"+str(c)+".bmp"
                c = c + 1
            try:
                subprocess.call(bc_path+" "+sshot)
            except:
                logg.L.log(traceback.format_exc())
            raise IOError("Unable to start SS_Server")

        # Create client socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server, retry upto 80 times
        n = 80
        for i in range(0,n):
            try:
                s.connect(('localhost',int(tcpport)))
                break
            except:
                #logg.L.log("Unable to connect the client socket to the server for "+comport)
                #logg.L.log("-"*50)
                #traceback.print_exc(file=sys.stdout)
                #logg.L.log("-"*50)
                time.sleep(1)
                if i>=(n-1):
                    logg.L.log("ERROR: Unable to connect the client to the server")
                    
                    # Capture a screen-shot of the desktop
                    sshot = logg.log_dir+"/screenshot_"+comport+".bmp"
                    c = 1
                    while (os.path.exists(sshot)):
                      sshot = logg.log_dir+"/screenshot-"+comport+"-"+str(c)+".bmp"
                      c = c + 1
                    try:
                        subprocess.call(bc_path+" "+sshot)
                    except:
                        logg.L.log(traceback.format_exc())
                    raise IOError("Unable to connect the client to the server")

                else:
                    continue

        # Make it non-blocking
        s.setblocking(0)

        
        logg.L.log("Done")

        self.server = server
        self.tcpport = int(tcpport)
        self.socket = s
        
        time.sleep(2)



    def TermSrv(self):
        """Terminate the cmdserver task, given the corresponding TCPPORT"""


        try:
            self.server.terminate()
        except:
            logg.L.log(traceback.format_exc())
        
        # Wait a bit
        time.sleep(3)

            
    def SendCommand(self, cmd, mode):
        if mode == "1":
            resp = self.SendTenCmd(cmd)
            return resp
        elif mode == "0":
            resp = self.SendHostCmd(cmd)
            return resp
    
    def SendCmds(self, hostcmds, tencmds):
        """
        Synopsis:       INTEGER SendCmds(LIST OF STRING hostcmds, LIST OF STRING tencmds)

        Description:    Configures the adapter device by sending a series of host and tensilica commands.
                        After sending the commands, the device is Reset.
                        First issues a series of tensilica commands as supplied in the input list 'temcmds'.
                        Then issues a series of host commands as supplied in the input list 'hostcmds'.
                        Then performs a Reset (host command 'Reset'). The Reset command need not be
                        supplied in the list of host commands. This is automatically performed in the end,
                        after issuing all the tensilica and host commands.

        Return Value:   1 right now, could be enhanced with better checking and returning 0 in error cases

        Inputs:         1. 'hostcmds': The list of hostcommands that should be issued.
                        2. 'tencmds': The list of tensilica commands that should be issued.

        Notes:          1. Server should already be running for this command to work.
                        2. Please note that the device may not be immediately up and running after this function call
                        since the device was just Reset. The caller may need to wait for 10-15 second before
                        issuing any new commands to this device.
                        3. This function uses the 'SendTenCmd' function to issue tensilica commands, and 'SendHostCmd'
                        function to issue host commands.

        """

        for tencmd in tencmds:
            self.SendTenCmd(tencmd)
            self.Reset("1")
        for hostcmd in hostcmds:
            self.SendHostCmd(hostcmd)
            self.Reset("0")
        
        logg.L.log("Adapter Configured successfully")
        return 1

    def Reset(self, mode):
        """

        Synopsis:       INTEGER Reset(mode)

        Description:    Reset the device by issuing the host Reset command

        Return Value:   1 right now, could be enhanced with better checking and returning 0 in error cases

        Inputs:         1. None

        Notes:          1. Server should already be running for this command to work.
                        2. Please note that the device may not be immediately up and running after this function call
                        since the device was just Reset. The caller may need to wait for 10-15 second before
                        issuing any new commands to this device.
                        3. This function uses the 'SendTenCmd' function to issue tensilica commands, and 'SendHostCmd'
                        function to issue host commands.
        """
        #for Gen3, no host, reset mode = 1
        if mode == "1":
           self.SendTenCmd("Reset")
        #for Gen2, have host, reset mode = 0
        elif mode == "0":
           self.SendHostCmd("Reset")
        return 1

    def SendTenCmd(self, cmd, timeout=12.0, silent='no'):
        """
        Synopsis:       (STRING or INTEGER) SendTenCmd(STRING cmd, FLOATING NUMBER timeout)

        Description:    Issue the supplied tensilica command and return the response. The execution is synchronous.

        Return Value:   The command response is returned as a string. All the carriage returns, <TEN> prompts, <EOF> prompts
                        are removed in the response. In case of error, returns 0.

        Inputs:         1. 'cmds': The command that should be issued.
                        2. 'timeout': The time for which the function should wait for the response, before timing out
                        and returning the response (see Notes).

        Notes:          1. Server should already be running for this command to work.
                        2. If the 'timeout' parameter is not specified, a default value of 1.0 second is used.
                        3. If the command could not be transmitted (say, socket connection is broken), then the function returns 0.
                        4. If the command response contains "<EOF>" string, that is considered as a termination of the response
                        from the server. The functions returns at that point without waiting for any more data from the server, and returns
                        the string received on the socket thus far, minus the prompts and carriage returns.
                        5. If the command is "ss_server hostupgradeuart", then the presence of the string "HOST_PROGRAMMING_SUCCESSFUL"
                        or "HOST_PROGRAMMING_FAILED" is considered as the termination of the response instead of the "<EOF>" string.
                        The functions returns at that point without waiting for any more data from the server, and returns the data
                        received on the socket thus far, minus the prompts and carriage returns.
                        6. If the command is "ss_server embeddedupgrade", then the presence of the string "EMBEDDED_PROGRAMMING_SUCCESSFUL"
                        or "EMBEDDED_PROGRAMMING_FAILED" is considered as the termination of the response instead of the "<EOF>" string.
                        The functions returns at that point without waiting for any more data from the server, and returns the data
                        received on the socket thus far, minus the prompts and carriage returns.
                        7. If the command is "ss_server exit", then the function returns immediately after issuing the command,
                        without waiting for any response. This command kills the server, and no response is transmitted by the server.
                        8. If the input command is "nvram_show", a timeout value of COMMAND_TIMEOUT_NVRAMSHOW is used instead of the supplied
                        timeout value (The response to the nvram_show is long, and sometimes takes longer than 1 second).
                        9. If there is no response from the server, or if the termination string <EOF> is not present in the response,
                        the command is retried for upto 2 times (a total of 3 attempts). However, for the firmware download commands
                        (ss_server hostupgradeuart, ss_server embeddedupgrade commands) retries are not performed. The intent here is
                        that if the firmware download fails, perhaps the retry should be attempted after resetting the device, and/or
                        restarting the server. The higher-level code is expected to implement these steps.
                        10. Any commands to the ss_server (eg: ss_server version, ss_server exit, ss_server logfile=c:\test.log) should
                        be sent using this command, and not using the other "SendHostCmd" function elsewhere in this adapter module.
        """

        if re.match("I2C", PORT, re.I):
            if re.search("version", cmd) or re.search("ss_server exit", cmd) or re.search("pwr_get_mode", cmd) or re.search("pwr_set_mode", cmd):
               cmd = cmd
            else:
               cmd = cmd + " " + "i2c" ###just add "i2c" for embedded commands
        if(silent != 'yes'):
            logg.L.log("Sending \"" + cmd + "\" to the embedded on TCPPORT "+str(self.tcpport)+"...")

        if cmd == "nvram_show":
            timeout = COMMAND_TIMEOUT_NVRAMSHOW

        retry_count = 1
        do_retry = 1
        while do_retry==1 and retry_count <= RETRY_MAXCOUNT:
            if(silent != 'yes'):
                logg.L.log("attempt"+str(retry_count)+": Sending \"" + cmd + "\" to the embedded on TCPPORT "+str(self.tcpport)+"...")
            #Clear any data in the receive buffer first before issuing the command
            while 1:
                try:
                    newdata = (self.socket.recv(4096)).decode()
                except:
                    break

            t_start = time.time()
            try:
                self.socket.send(b""+cmd+"<EOF>")
            except:
                if(silent != 'yes'):
                    logg.L.log(traceback.format_exc())
                # The most common case for this exception is that the socket closed
                # This could happen if ss_Server crashed for example
                return 0

            #If the command is ss_server exit, then the socket itself is closed. So no point receiving any response
            # on the socket. Instead get out.
            if cmd == "ss_server exit":
                time.sleep(2)
                return 0

            data = ""
            while 1:
                try:
                    newdata = (self.socket.recv(4096)).decode()
                    #logg.L.log(newdata)
                    data = data + newdata
                except:
                    if re.search("ss_server hostupgradeuart",cmd):
                        time.sleep(1)
                        if (re.search("HOST_PROGRAMMING_SUCCESSFUL",data) or re.search("HOST_PROGRAMMING_FAILED",data)):
                            do_retry = 0
                            break
                        t_end = time.time()
                        #Wait a maximum of 'timeout' second
                        if t_end - t_start > timeout:
                            # The download must have failed, return 0
                            data = data.strip()
                            data = data.replace("\r", "\n") # Replace carriage return with new line
                            if(silent != 'yes'):
                                logg.L.log("Response: "+data)
                            return 0
                        
                    elif re.search("ss_server embeddedupgrade",cmd):
                        time.sleep(1)
                        if (re.search("EMBEDDED_PROGRAMMING_SUCCESSFUL",data) or re.search("EMBEDDED_PROGRAMMING_FAILED",data)):
                            do_retry = 0
                            break
                        t_end = time.time()
                        #Wait a maximum of 'timeout' second
                        if t_end - t_start > timeout:
                            # The download must have failed, return 0
                            data = data.strip()
                            data = data.replace("\r", "\n") # Replace carriage return with new line
                            if(silent != 'yes'):
                                logg.L.log("Response: "+data)
                            return 0

                    elif re.search("<EOF>",data):
                        # EOF found, get out.
                        data = re.sub("<EOF>", "", data)
                        data = re.sub("\n", "", data)
                        data = re.sub("TEN:\\\\>", "", data)
                        do_retry = 0
                        break
                    else:
                        t_end = time.time()
                        #Wait a maximum of 'timeout' second
                        if t_end - t_start > timeout:
                            do_retry = 1
                            retry_count = retry_count + 1
                            break
                    continue
        

        data = data.strip()
        data = data.replace("\r", "\n") # Replace carriage return with new line
        if(silent != 'yes'):
            logg.L.log("Response: "+data)


        return data


        

    def SendTenDlCmd(self, filename, upgrade_interface = "SPI", timeout = 1200):
        """Send the download command to tensilica, with the supplied image name.
        Used for Gen2 devices

        Synopsis:       (INTEGER) SendTenDlCmd(STRING filename, STRING upgrade_interface, FLOAT timeout)

        Description:    Perform the embedded firmware download with the supplied binary file, over the specified
                        download interface.

        Return Value:   Returns 1 if the firmware download is successful. In case of error, returns 0.

        Inputs:         1. 'filename': The binary file (the complete path on the file system) that should be
                        downloaded onto the hardware.
                        2. 'timeout': The time for which the function should wait for the response, before timing out
                        and returning the response (see Notes). If the value is not specified, a default value of 1200 second is used.

        Notes:          1. Server should already be running for this command to work.
                        2. If the 'timeout' parameter is not specified, a default value of 1.0 second is used.
                        3. If the command could not be transmitted (say, socket connection is broken), then the function returns 0.
                        4. If the command response contains "<EOF>" string, that is considered as a termination of the response
                        from the server. The functions returns at that point without waiting for any more data from the server, and returns
                        the string received on the socket thus far, minus the prompts and carriage returns.
                        5. If the command is "ss_server hostupgradeuart", then the presence of the string "HOST_PROGRAMMING_SUCCESSFUL"
                        or "HOST_PROGRAMMING_FAILED" is considered as the termination of the response instead of the "<EOF>" string.
                        The functions returns at that point without waiting for any more data from the server, and returns the data
                        received on the socket thus far, minus the prompts and carriage returns.
                        6. If the command is "ss_server embeddedupgrade", then the presence of the string "EMBEDDED_PROGRAMMING_SUCCESSFUL"
                        or "EMBEDDED_PROGRAMMING_FAILED" is considered as the termination of the response instead of the "<EOF>" string.
                        The functions returns at that point without waiting for any more data from the server, and returns the data
                        received on the socket thus far, minus the prompts and carriage returns.
                        7. If the command is "ss_server exit", then the function returns immediately after issuing the command,
                        without waiting for any response. This command kills the server, and no response is transmitted by the server.
                        8. If the input command is "nvram_show", a timeout value of COMMAND_TIMEOUT_NVRAMSHOW is used instead of the supplied
                        timeout value (The response to the nvram_show is long, and sometimes takes longer than 1 second).
                        9. If there is no response from the server, or if the termination string <EOF> is not present in the response,
                        the command is retried for upto 2 times (a total of 3 attempts). However, for the firmware download commands
                        (ss_server hostupgradeuart, ss_server embeddedupgrade commands) retries are not performed. The intent here is
                        that if the firmware download fails, perhaps the retry should be attempted after resetting the device, and/or
                        restarting the server. The higher-level code is expected to implement these steps.
                        10. Any commands to the ss_server (eg: ss_server version, ss_server exit, ss_server logfile=c:\test.log) should
                        be sent using this command, and not using the other "SendHostCmd" function elsewhere in this adapter module.





        """
            
        logg.L.log("Starting the download on the tcpport "+str(self.tcpport)+" with the file "+filename)

        #if upgrade_interface.lower() == "spi":
        cmd = "ss_server embeddedupgrade="+filename
        #elif upgrade_interface.lower() == "i2c":
            #cmd = "ss_server embeddedupgradeviahostuart="+filename
        #else:
        #logg.L.log("ERROR: Unsupported Tensilica Upgrade Interface: "+upgrade_interface)
        #return 0

        # Hold the BB in Reset before starting the download
        #resp = SendTenCmd("ht_bbreset 1")
        
        resp = self.SendTenCmd(cmd, timeout)
        time.sleep(2)
        if re.search("EMBEDDED_PROGRAMMING_SUCCESSFUL", str(resp)):
            logg.L.log("EMBEDDED_PROGRAMMING_SUCCESSFUL string found in the response. Embedded programming succeeded")
            return 1
        else:
            logg.L.log("EMBEDDED_PROGRAMMING_SUCCESSFUL string NOT found in the response. Embedded programming FAILED")
            logg.L.log("Response is "+str(resp))
            return 0


        
    def SendOdysseusDlCmd(self, filename, timeout = 300):
        """Send the download command to odysseus, with the supplied image name"""
        
        logg.L.log("Starting the odysseus software download on the tcpport "+str(self.tcpport)+" with the file "+filename)

        cmd = "ss_server hostupgradeuart="+filename
        resp = self.SendTenCmd(cmd, timeout)
        if re.search("HOST_PROGRAMMING_SUCCESSFUL", str(resp)):
            logg.L.log("HOST_PROGRAMMING_SUCCESSFUL string found in the response. Host programming succeeded")
            return 1
        else:
            logg.L.log("HOST_PROGRAMMING_SUCCESSFUL string NOT found in the response. Host programming FAILED")
            logg.L.log("Response is "+str(resp))
            return 0


       



    def ChangeSrvLog(self, newlog):
        """Change the log file that the cmdserver logs the debug messages into.
        If the a file with 'newlog' name already exists, the function adds a number
        at the end of the filename so that a file with the new name is not already present.
        Returns the name of the file that is used. Returns 0 if could not
        successfully change the log file"""

        absname = os.path.splitext(newlog)[0] #File name (including the complete path preceding it) without the extension
        ext = os.path.splitext(newlog)[1] # File extension
        i = 1

        # Work out a file name that is not already present    
        while os.path.exists(newlog):
            newlog = absname+"-"+str(i)+ext
            i = i + 1
            
        logg.L.log("Changing the log file of the server on TCPPORT "+str(self.tcpport)+" to "+newlog+"...")
        try:
            self.socket.send(b"" + "ss_server logfilename="+newlog+"<EOF>")
        except:
            logg.L.log(traceback.format_exc())
            # The most common case for this exception is that the socket closed
            # This could happen if ss_Server crashed for example
            return 0
        else:
            logg.L.log("Done")
        time.sleep(1)
        return os.path.basename(newlog)


        

    def SendSrm1(self, srm1file):
        """Send SRM1 version"""

        logg.L.log("Sending SRM1 file\"" + srm1file + "\" to the host on TCPPORT "+str(self.tcpport)+"...")
        client = subprocess.Popen("cmdclient 127.0.0.1 "+str(self.tcpport)+" -h \"srm1wr " + srm1file + "\"", stdout=subprocess.PIPE)
        resp = client.communicate()
        resp_str = resp[0].decode()
        logg.L.log(resp_str)
        return resp_str

    def SendSrm2(self, srm2file):
        """Send SRM1 version"""

        logg.L.log("Sending SRM2 file\"" + srm2file + "\" to the host on TCPPORT "+str(self.tcpport)+"...")
        client = subprocess.Popen("cmdclient 127.0.0.1 "+str(self.tcpport)+" -h \"srm2wr " + srm2file + "\"", stdout=subprocess.PIPE)
        resp = client.communicate()
        resp_str = resp[0].decode()
        logg.L.log(resp_str)
        return resp_str


    def ReadSrm(self):
        """Read SRM version"""

        logg.L.log("Read SRM from the embedded on TCPPORT "+str(self.tcpport)+"...")
        client = subprocess.Popen("cmdclient 127.0.0.1 "+str(self.tcpport)+" -e \"srmrd\"", stdout=subprocess.PIPE)
        resp = client.communicate()
        resp_str = resp[0].decode()
        logg.L.log(resp_str)
        return resp_str

    def SendHostCmd(self, cmd, timeout=3.0):
        """Send a command to the host, same as sendnxpcmd without the word nxp since there is no such processor
        in Gen2"""
        
        """Send a command to the host. Even though the function name says NXP, it also works for the ATMEL boards used in Gen2
        The function name is left as-is for backward compatibility reasons"""
        

        logg.L.log("Sending \"" + cmd + "\" to the host on TCPPORT "+str(self.tcpport)+"...")

        # In Gen2, it is version, not show_version
        if cmd == "show_version":
            cmd = "version"

        # Prepend ht_ if needed            
        if not re.match("ht_(.*)", cmd, re.IGNORECASE):
            cmd = "ht_" + cmd
        cmd = cmd+"<EOF>"
        #logg.L.log(cmd)

        if cmd == "ht_nvram_show":
            timeout = COMMAND_TIMEOUT_NVRAMSHOW

        retry_count = 1
        do_retry = 1
        while do_retry==1 and retry_count <= RETRY_MAXCOUNT:
            logg.L.log("attempt"+str(retry_count)+": Sending \"" + cmd + "\" to the host on TCPPORT "+str(self.tcpport)+"...")
            #Clear any data in the receive buffer first before issuing the command
            while 1:
                try:
                    newdata = (self.socket.recv(4096)).decode()
                except:
                    break

            t_start = time.time()
            try:
                self.socket.send(b""+cmd+"<EOF>")
            except:
                logg.L.log(traceback.format_exc())
                # The most common case for this exception is that the socket closed
                # This could happen if ss_Server crashed for example
                return 0

            data = ""
            while 1:
                try:
                    newdata = (self.socket.recv(4096)).decode()
                    #logg.L.log(newdata)
                    data = data + newdata
                except:
                    if re.search("<EOF>",data):
                        # EOF found, get out.
                        data = re.sub("<EOF>", "", data)
                        data = re.sub("\n", "", data)
                        data = re.sub("TEN:\\\\>", "", data)
                        do_retry = 0
                        break
                    else:
                        t_end = time.time()
                        #Wait a maximum of 2 second
                        if t_end - t_start > timeout:
                            do_retry = 1
                            retry_count = retry_count + 1
                            break
                    continue
        
        data = data.strip()
        data = data.replace("\r", "\n") # Replace carriage return with new line
        logg.L.log("Response: "+data)

        return data

    def ReadHostSwVer(self):
        """Determine the host software version"""

        resp = self.SendHostCmd("ht_version")
        #resp = resp.splitlines()
        if resp:
            m = re.search("Pkg: (.*), Ver: (.*), Built(.*)", resp, re.IGNORECASE)
            if m:
                return m.group(1)+" "+m.group(2)
        return ""


    def ReadTenSwVer(self):
        """Determine the tensilica software version"""

        resp = self.SendTenCmd("show_version")
        m = re.match("(.*)Pkg: (.*), Ver.: (.*) , Built: (.*)", resp, re.IGNORECASE)
        if m:
            return m.group(2)+" "+m.group(3)
        else:
            return ""

    def ReadSrvSwVer(self):
        """Determine the SS_SERVER software version"""


        resp = self.SendTenCmd("ss_server version")
        m = re.match("SS_SERVER Ver. (.*)", resp, re.IGNORECASE)
        if m:
            return m.group(1)
        else:
            return ""


    def SetAudioControl(self, val):
        """Set the audio control of the host by sending different commands depending on 
        whether the device is Gen1 device or a Gen2 device"""


        self.SendTenCmd("nvramset 0x11 "+str(val))
        

    def SetAudioMclk(self, val):
        """Set the audio MCLK of the host by sending different commands depending on 
        whether the device is Gen1 device or a Gen2 device"""


        self.SendTenCmd("nvramset 0x12 "+str(val))


    def getPackets(self,returnOpt):
        
        
        response = self.SendTenCmd("get_sper_tx_hr_stats 1", 12.0, 'yes')
        
        
        mIndex1 = response.find('mGood') + len('mGood=')
        mIndex2 = response.find('mError')	
        mGood = response[mIndex1:mIndex2]
        
        mIndex3 = response.find('mError') + len('mError=')
        mIndex4 = response.find('qGood')	
        mError = response[mIndex3:mIndex4]
        
        qIndex1 = response.find('qGood') + len('qGood=')
        qIndex2 = response.find('qError')	
        qGood = response[qIndex1:qIndex2]

        qIndex3 = response.find('qError') + len('qError=')
        qIndex4 = response.find('hGood')	
        qError = response[qIndex3:qIndex4]
        
        hIndex1 = response.find('hGood') + len('hGood=')
        hIndex2 = response.find('hError')	
        hGood = response[hIndex1:hIndex2]

        hIndex3 = response.find('hError') + len('hError=')
        hIndex4 = response.find('fGood')	
        hError = response[hIndex3:hIndex4]
        
        fIndex1 = response.find('fGood') + len('fGood=')
        fIndex2 = response.find('fError')	
        fGood = response[fIndex1:fIndex2]
        
        fIndex3 = response.find('fError') + len('fError=')
        fIndex4 = response.find('qADCGood')	
        fError = response[fIndex3:fIndex4]
        
        aIndex1 = response.find('qADCGood') + len('qADCGood=')
        aIndex2 = response.find('qADCError')	
        qADCGood = response[aIndex1:aIndex2]	
        
        aIndex3 = response.find('qADCError') + len('qADCError=')
        aIndex4 = response.find('RATE')	
        qADCError = response[aIndex3:aIndex4]	
        
        if(returnOpt == 'all'):
            return (int(mGood), int(mError), int(qGood), int(qError), int(hGood), int(hError), int(fGood), int(fError), int(qADCGood), int(qADCError))
        elif(returnOpt == 'good'):
            return (int(mGood),int(qGood),int(hGood),int(fGood),int(qADCGood))
        elif(returnOpt == 'error'):
            return (int(mError),int(qError),int(hError),int(fError),int(qADCError))
        elif(returnOpt == 'q'):
            return (int(qGood), int(qError))
        elif(returnOpt == 'h'):
            return (int(hGood), int(hError))
        elif(returnOpt == 'f'):
            return (int(fGood), int(fError))
        elif(returnOpt == 'm'):
            return (int(mGood), int(mError))
        elif(returnOpt == 'adc'):
            return (int(qADCGood), int(qADCError))
        elif(returnOpt == 'video'):
            return (int(mGood), int(mError), int(qGood), int(qError), int(hGood), int(hError), int(fGood), int(fError))
        else:
            print "No such return option!!"

    def isGen3(self):

        response = self.SendTenCmd("nvram_show", 1.0, 'yes')
        index1 = response.find('GEN3')
        isGen3Indicator = response[index1+16:index1+17]
        
        return int(isGen3Indicator)


    def apbwr(self, address, value):

        
		for i in range(0,10):
			try: 
		
				resp = self.SendTenCmd("apbwr " + address + " " + value, 12.0, 'yes')

				if (resp == 'OK'):
					return 0
				else:
					return 1
					
			except:
				
					print "******######## ERROR in apbwr_bit #######*********"
					time.sleep(5)
					if (i >= 9):
						return 1
					else:
						continue			

    def apbrd(self, address):

        response = self.SendTenCmd("apbrd " + address, 12.0, 'yes')
        return response

    def apbwr_bit(self, address, bit, value):

        
		for i in range(0,10):
			try: 

		
				response = self.SendTenCmd("apbrd " + address, 12.0, 'yes')
				
				currValue = int((int(response,0)&(1<<bit))!=0)
				
				if (currValue == value):		
					print "Bit " + str(bit) + " is already " + str(currValue)
					return 0
				else:
					if (value == 0):
						response = int(response,0)
						response &= ~(1<<bit)
						valueToWrite = hex(response)
					elif (value == 1):
						response = int(response,0)
						response |= (1<<bit)
						valueToWrite = hex(response)
				
					resp = self.SendTenCmd("apbwr " + address + " " + valueToWrite, 12.0, 'yes')
			
					if (resp == 'OK'):						
						print "Bit " + str(bit) + " of register " + address + " has been set to " + str(value)
						return 0
					else:
						return 1
						
			except:
			
				print "******######## ERROR in apbwr_bit #######*********"
				time.sleep(5)
				if (i >= 9):
					return 1
				else:
					continue
        
    def apbrd_bit(self, address, bit):

        response = self.SendTenCmd("apbrd " + address, 12.0, 'yes')
        
        currValue = int((int(response,0)&(1<<bit))!=0)

        return currValue	

    
    def nvram_update_rate(self, noRates, rate1, rate2, rate3, rate4):

        resp = self.SendTenCmd("nvram_update_gen3_ra " + str(noRates) + " " + rate1 + " " + rate2 + " " + rate3 + " " + rate4, 12.0, 'yes')
        
        
        if (resp == 'OK'):
            return 0
        else:
            return 1

    def rfregrd(self, address):

        response = self.SendTenCmd("rfregrd " + address + " 0x0", 12.0, 'yes')
        return response		

    def rfregwr(self, address, value):

        resp = self.SendTenCmd("rfregwr " + address + " " + value + " 0x0", 12.0, 'yes')

        if (resp == ''):
            return 0
        else:
            return 1

    def rfregwr_bit(self, address, bit, value):

        response = self.SendTenCmd("rfregrd " + address + " 0x0", 12.0, 'yes')
        
        currValue = int((int(response,0)&(1<<bit))!=0)
        
        if (currValue == value):		
            print "Bit " + str(bit) + " is already " + str(currValue)
        else:
            if (value == 0):
                response = int(response,0)
                response &= ~(1<<bit)
                valueToWrite = hex(response)
            elif (value == 1):
                response = int(response,0)
                response |= (1<<bit)
                valueToWrite = hex(response)
        
            resp = self.SendTenCmd("rfregwr " + address + " " + valueToWrite + " 0x0", 12.0, 'yes')
    
            if (resp == 'OK'):
                return 0
                print "Bit " + str(bit) + " of register " + address + " has been set to " + str(value)
            else:
                return 1