"""Log module   

This module contains a few utility functions to parse the logs.

"""

import subprocess
import os
import logging
import re
import time
import logger


# The path of the Beyond compare 3 program
BC3 = "C:\Program Files\Beyond Compare 3\BComp.exe"


L = logger.Logger() # create logger object (put here for convieniance)
L.create_loghandler("mainLogfile.txt", 1)



def create_logdir():
    """Create a log directory"""

    log_dir = "C:/svn/ta/logs"    
    curtime = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = log_dir+"/"+curtime
    log_dirr = "\\".join(log_dir.split('/')) #c:\\svn\\ta\\logs, back slash instead of forward slash
    os.makedirs(log_dir) # Create the log directory for this run, inside log_dir

    return log_dir
    

def create_merge_log(merge_log, l_logs):

    # If the input log files do not exist, quit
    for log in l_logs:
        if not os.path.exists(log):
            print("Log file "+log+" not present. Can not create a merge file")
            return 0

    #If BC3 does not exist, quit
    if not os.path.exists(BC3):
        print("Beyond Compare 3 application is not found on the computer. Can not create a merge file")
        return 0
        
    # If a file with merge_log name already exists, create another unique merge file
    absname = os.path.splitext(merge_log)[0] #File name (including the complete path preceding it) without the extension
    ext = os.path.splitext(merge_log)[1] # File extension
    i = 1
    # Work out a file name that is not already present    
    while os.path.exists(merge_log):
        merge_log = absname+"-"+str(i)+ext
        i = i + 1
    
    # If the BC3 script exists (eg: merge2.txt, merge3.txt),
    # then create the merge file.
    if os.path.exists("merge"+str(len(l_logs))+".txt"):
        s = ""
        l_logs.reverse() #Reverse the list so that src log is first and then the sink log.
        #This is useful so that the src log appears on the left side of the merge file.
        for log in l_logs:
            s = s + " "+log
        cmd = BC3 + " @merge"+str(len(l_logs))+".txt"+s+" "+merge_log+" /closescript"
        print(cmd)
        s = subprocess.Popen(cmd)
        return os.path.basename(merge_log)
    return 0
        

    
def getTS(logfile, searchstr, startTS):
    """Get the timestamp of the string 'searchstr' in the file 'logfile'
    that occurs after startTS. It is assumed that each line in the logfile
    starts with a timestamp"""

    
    # Return 0 if the file does not exist
    try:
        fd = open(logfile)
    except IOError:
        print("ERROR: Unable to open the logfile "+ logfile)
        return 0
    
    for line in fd:
           
        ts = line.partition('>')[0] # Extract the time stamp
        line = line.partition('>')[2] # Extract the rest of the string
        ts = re.sub("(\(H\)|\(E\))",'',ts).strip() ;# Remove (H) or (E) at the front
        sec = ts[0:19] # Second
        try:
            sec = time.mktime(time.strptime(sec, "%m/%d/%Y %H:%M:%S"))
        except ValueError:
            continue
           
        msec = int(ts[20:23])/1000 # Millisecond converted to second
           
        t = sec + msec

        if (t <= startTS):
            continue
        elif (re.search(searchstr, line)):
            fd.close()
            return t
        

    fd.close()
    return 0 # Not found


def checkLogs(file, time1):
    """

    """
    time.sleep(20)
    r = checkConnTime(file, time1)
    if r[0] == 1:
        resp = r
    elif r[0] == 0:
        time.sleep(20) # Give it another 20 second, if it passes now it is a WARNING
        r = checkConnTime(file,time1)
        if r[0] == 1:
            #took longer time to connect, mark it warning, but note the connection time in the comments
            resp = [2,r[1]]
        else:
            resp = r


    run_mode = cfg.td_tree.findtext("RUN_OPTIONS/RUN_MODE", "")
    if run_mode.lower() == "manual":
        rsp = input("Did the test pass (y/n/w)?:")
        while (not((rsp.lower() == "y") or (rsp.lower() == "n") or (rsp.lower() == "w"))):
            rsp = input("Only y or Y or n or N or w or W accepted. Did the test pass (y/n/w)?:")

        if rsp.lower() == "y":
            resp[0] = 1
        elif rsp.lower() == "n":
            resp[0] = 0
        elif rsp.lower() == "w":
            resp[0] = 2
            
        comment = input("Please Comment an optional comment:")
        if comment != "":
            resp[1].append("TEST_COMMENT: "+comment)

    return resp            
   
           

def checkConnTime(file, time1):
   """Determine the connection time by looking for the occurrance of the
   string "baseband video UNMUTE" in the specified input file that occurs AFTER time1.
   If there is more than one occurrance "baseband video UNMUTE", that's reported also."""

   s = []
   
   time2 = getTS(file, "baseband video UNMUTE", time1)
   if (not time2):
       s.append("TEST_COMMENT: Unable to connect")
       res = 0
   elif (time2 <= time1):
       s.append("TEST_COMMENT: Time taken for connection: <=0 second")
       res = 0
   else:
       # Verify that there is no other "baseband video UNMUTE" after time2. If there is another
       # "baseband video UNMUTE" after time2 (say at time3), it indicates that the connection was
       # first created at time2, and then was disconnected and reconnected at time3.
       # That's a bug, and the test should be marked FAILED.
       count = 0
       while time2:
           count = count+1
           time_last = time2
           time2 = getTS(file, "baseband video UNMUTE", time_last)
           
       if count>1:
           s.append("TEST_COMMENT: "+str(count)+" occurrances of \"baseband video UNMUTE\" detected")
           res = 1
       else:
           res = 1

       # Verify there are no disconnects after the last "baseband video UNMUTE"
       time_disc = getTS(file, "Disconnect", time_last)
       if time_disc:
           s.append("TEST_COMMENT: There is a Disconnect AFTER the last \"baseband video UNMUTE\". Test FAILED")
           res = 0
       else:
           s.append("CONNECTION_TIME: %.2f"%(time_last - time1))
           s.append("TEST_COMMENT: Time taken for connection: %.2f"%(time_last - time1) + " second")
   
   return [res,s]


def checkLog(file, str, time1):
   """Look for the first occurance of the string str in the logfile file
   that occurs AFTER time1.
   """

   time2 = getTS(file, str, time1)

   if (not time2):
       return 0
   elif (time2 <= time1):
       return 0
   else:
       # Verify that there is no other str after time2. If there is another
       # str after time2 (say at time3), it indicates that the connection was
       # first created at time2, and then was disconnected and reconnected at time3.
       # That's a bug, and the test should be marked FAILED.
       time3 = getTS(file, str, time2)
       if time3:
           print("TEST_COMMENT: More than one occurrance of "+str+" detected")
           return 0

       return 1


def searchLog( file, token, T1, T2):
    """ return a list with each element: 
            0 if token not found in filename file.
            timestamp if token found in format of MM/DD/YYYY HH:MM:SS:MMM as a string
            ROGER - currently returning zero if error!!! Is this what we want?

        file - input arg - string - filename of log file to be searched.
        token - input arg - list of strings - message to search for in log
        T1 - input arg - list of strings in format of MM/DD/YYYY HH:MM:SS:MMM - Start searching from this specified time.
                                                                Null string means start from beginning of log file.
        T2 - input arg - list of strings in format of MM/DD/YYYY HH:MM:SS:MMM - End searching at this specified time.
                                                                Null string means stop searching at end of log file.

        Action Items:
        1. check for valid T1 and T2 format
        2. if log file doesn't begin with datetimestamp, then do what? skip processing of that line???
    """
   
    f = open(file, "r")
    try:
        f = open(file, "r")
    except IOError:
        print("ERROR: Unable to open the debug logfile "+ file)
        return 0

    # error check arguments
    if (type(token) != list):
        print("ERROR: argument token is not a list!")
        return 0
    elif (type(T1) != list):
        print("ERROR: argument "+T1+" is not a list!")
        return 0
    elif (type(T2) != list):
        print("ERROR: argument "+T2+" is not a list!")
        return 0

    # error check arguments
    numTokens = len(token)
    if ((numTokens != len(T1)) or (numTokens != len(T2))):
        print("ERROR: number of arguments in lists token, T1, and T2 are not the same!")
        return 0    

    # process first token in the list
    iToken = 0;

    retList = []; # return value is a list of timestamps
    for i in range(numTokens):
        retList.append('')

    # log processing ends when the last line of the log file has been reached or all tokens have been found    
    for line in f:
        # process line by line
        ts = line.partition('>')[0] # Extract the time stamp. In general for P4, it will be line[0:23]

        if (ts < T1[iToken]):
            continue

        if ((T2[iToken] != '') and (ts > T2[iToken])):
            # done searching since debug log datetimestamp is beyond end of T2 datetimestamp search criteria
            f.close()
            return retList
 
        line = line.partition('>')[2] # Extract the rest of the string
        
        if (line.find(token[iToken]) != -1):
            retList[iToken] = ts
            iToken = iToken + 1
            if (iToken > (numTokens-1)):
                f.close()
                return retList
    f.close()
    
    return retList






