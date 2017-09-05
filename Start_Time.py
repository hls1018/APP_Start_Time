#!/usr/bin/env python
#-*- coding : utf-8 -*-
import subprocess
import time
import optparse
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
#import  atx

cmd_install_num = 'adb -s '
cmd_install_in = ' install '
cmd_install_dev = ' install -r '
cmd_uninstall = ' uninstall '
AM_THIS_TIME = 'ThisTime'
AM_TOTAL_TIME = 'TotalTime'
AM_WAIT_TIME = 'WaitTime'

def devicesConnectInfo():

    devicesId = []

    connResult = os.popen('adb devices').readlines()

    connDevicesInfo = connResult[1:len(connResult)-1]

    connDevicesNum = len(connDevicesInfo)


    if connDevicesNum > 0 :
        for i  in range(connDevicesNum):
            address = connDevicesInfo[i].split('\t')[0]

            if address.find('.')<0:

                devicesId.append(address)

    return devicesId


def getapk():
    apkmap = []
    path=os.getcwd()
    for parent, dirnames, filenames in os.walk(path):
        for files in filenames:
            if files.endswith('.apk'):
                apkmap.append(parent+'/'+files)
    return apkmap
def install(devicesID, appmapnamepath, package_name):
    try:
        comma = cmd_install_num + devicesID + cmd_uninstall + package_name
        os.popen(comma)
        time.sleep(7)
    except Exception:
        print 'chu cuo le '

    commands = 'adb -s ' + devicesID + '  install  ' + '"%s"' % str(appmapnamepath)
    os.popen(commands)
    time.sleep(7)

def start_activity(activiy,devicesID,g_dict):
    result = {}
    p = subprocess.Popen('adb -s '+devicesID + ' shell am start -W  {}'.format(activiy),shell=True,stdout=subprocess.PIPE)
    out,err = p.communicate()
    for line in out.splitlines():
        cmds = line.decode('utf-8').split(':')
        if len(cmds) == 2 and cmds[0] in g_dict.keys():
            result[cmds[0]] = cmds[1]
    return result


def start_cold_run(LAUNCHER_PKG_NAME,LAUNCHER_MAIN_ACTIVITY,package_name):
    #number = sys.argv[1]
    number = 10
    packagepath = getapk()
    print packagepath
    devicesInfo = devicesConnectInfo()
    devicesnum = len(devicesInfo)
    if devicesnum > 0:
        devicesID = devicesInfo[0]
    #devicesID = '063288cc00605eee'
    for iitem in range(len(packagepath)):
        g_dict = {'ThisTime': [], 'TotalTime': [], 'WaitTime': []}
        print '-------------------------loop execution ' + str(number) + '----------------------'
        print '\n\n'
        packagenames = packagepath[iitem].split('/')
        filenames=packagenames[-1].split('.apk')
        print packagenames
        for i in range(int(number)):
            print '=====================' + devicesID + '====================='
            print 'In installation'
            install(devicesID, packagepath[iitem], package_name)
            time.sleep(7)
            #print 'adb -s ' + devicesID + ' shell input keyevent 3'
            os.popen('adb -s ' + devicesID + ' shell input keyevent 3')
            print 'In startup'
            row = start_activity(LAUNCHER_MAIN_ACTIVITY,devicesID,g_dict)
            #print g_dict
            [g_dict[i].append(int(row[i])) for i in row.keys()]
            print(row)
            time.sleep(1)
            print '=====================' + 'end' + '====================='
            print '\n\n'
        df = pd.DataFrame(g_dict)
        df.to_csv(filenames[0]+'.csv')
        print(df)
        df['WaitTime'].plot(kind='bar')
        # plt.show()

if __name__ == '__main__':
   LAUNCHER_PKG_NAME =sys.argv[1]
   LAUNCHER_MAIN_ACTIVITY = sys.argv[2]
   package_name = sys.argv[3]
   start_cold_run(LAUNCHER_PKG_NAME,LAUNCHER_MAIN_ACTIVITY,package_name)
