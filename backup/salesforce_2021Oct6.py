from simple_salesforce import Salesforce, SalesforceLogin
import requests
import base64
import json
import pandas as pd
from io import StringIO
import shutil
import argparse
import sys
import os
from datetime import datetime
from config import *
from simple_salesforce.exceptions import SalesforceAuthenticationFailed
import time



__author__ = 'marcel.kantor'
__date__ = '2021-07-20'



def parseArguments():

    try:
        
        parser = argparse.ArgumentParser(description='Download report data from Salesforce')        
        parser.add_argument('-s','--site', help='Enter salesforce site',required=True)
        parser.add_argument('-r','--reportId', help='Enter reportId',required=True)
        
        args = parser.parse_args()
                   
        if len(sys.argv) < 2:
            parser.print_help()
            parser.exit(1)
        
        return args
    
    except:
        #parser.print_help()
        #print('Problem @parseArguments')
        #print(sys.exc_info())
        #sys.exit(0)
        #os._exit()
        writeLog(logFile, str(sys.exc_info()))
        return



def loadLogin(site):

    try:

        loginData = json.load(open(loginConfig))

        return loginData[site]

    except:

        print('Problem @processLogin')
        writeLog(logFile, str(sys.exc_info()))
        print(sys.exc_info())
        sys.exit(1)



def getSF(username, password, security_token):
    
    try:

        sf = Salesforce(username=username, password=password, security_token=security_token)
        
        return sf
    
    except SalesforceAuthenticationFailed as e:
        print('Problem @getSF with authentication')
        #print(e.message)
        #print(e.code)
        #sys.exit(1234)
        #return 1234
        raise 

    except:
        print('Problem @getSF')
        print(sys.exc_info())
        writeLog(logFile, str(sys.exc_info()))
        sys.exit(1)



def writeLog(logFile, error):
    
    try:
        with open(logFile, 'a+') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + " ")
            f.write(sys._getframe(1).f_code.co_name + " ")            
            f.write(error + "\n")
            #f.write("\n")

    except:
        print('Problem writing to log file', )
        #return 1
        sys.exit(1)  



def main():

    try:

        myargs = parseArguments()

        if myargs is not None:

            siteRecord = loadLogin(myargs.site)

            sf = getSF(siteRecord['username'], siteRecord['password'], siteRecord['security_token'])

            response = requests.get(siteRecord['url'].format(myargs.reportId),
                      headers = sf.headers, cookies = {'sid' : sf.session_id})

            myreport = response.content.decode('utf-8')

            
            with open(myargs.reportId + '.csv', "w") as text_file:
                text_file.write(myreport)
            
            #report_df = pd.read_csv(StringIO(myreport), skipfooter=5, engine='python')
            #report_df = pd.read_csv(StringIO(myreport))
            #response.contents
            #filePath = os.path.join(outputDir, str(myargs.site) + '_ReportID_' + str(myargs.reportId) + '_' + str(datetime.today().strftime('%Y-%m-%d')) + '.csv')
            
            #report_df.to_csv(filePath,index=False)
        
    except SalesforceAuthenticationFailed as error:
        writeLog(logFile, str(sys.exc_info()))
        print(error)
        #return 1234
        sys.exit(1234)
    
    except:
        writeLog(logFile, str(sys.exc_info()))
        #print('Problem @main')
        #print(sys.exc_info())
        sys.exit(1)
        #sys.exit(main())



if __name__ == '__main__':
    main()
