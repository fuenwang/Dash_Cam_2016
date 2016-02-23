#! /usr/bin/env python

import sys
sys.path.append('/home/Futen/Dash_Cam_2016')
import SystemParameter_For_Download as SP
import GetCircleBound
import PanoProcess
import subprocess
from multiprocessing import Pool
import numpy as np
import time
import os
import GetPanoByID
import SendEmail
number_to_do = 247
number = 0
TYPE = 'NegSource'

def DownloadList(center):   # average 42 second for one video
    pano_lst = []
    err_lst = []
    bound = GetCircleBound.GetCircleBound(center)
    for latlon in bound:
        try:
            pano_name = PanoProcess.GetPanoID(latlon)
        except:
            print 'error %f, %f'%(latlon[0],latlon[1])
            err_lst.append((latlon[0], latlon[1]))
            continue
        if pano_name != None:
            pano_lst.append((pano_name, latlon[0], latlon[1]))
    return (pano_lst, err_lst)
def Download(video_info): # (vname, lat, lon))
    #global number
    #if number >= number_to_do:
    #    return
    print '# %d'%number,video_info
    vname = video_info[0]
    latlon = (float(video_info[1]), float(video_info[2]))
    path =  SP.GetPath(vname, TYPE)# get all path

    #if path['state']['panolist'] == 'no':
    if True:
        #print vname,latlon
        result = DownloadList(latlon)
        pano_lst = result[0]
        err_lst = result[1]
        
        f = open('%s/pano_lst.txt'%path['pano_path'], 'w')
        for pano in pano_lst:
            #print pano
            s = pano[0] + '\t' + str(pano[1]) + '\t' + str(pano[2]) + '\n'
            f.write(s)
        f.close()
        f = open('%s/pano_error_lst.txt'%path['pano_path'], 'w')
        for pano in err_lst:
            #print pano
            s = str(pano[0]) + '\t' + str(pano[1]) + '\n'
            f.write(s)
        f.close()
        command = 'mv %s/pano_lst.txt %s/pano_lst_finish.txt'%(path['pano_path'], path['pano_path'])
        subprocess.call(command, shell=True)
        #number += 1
    else:
        print '%s finish'%vname

if __name__ == '__main__':
    pool = Pool(processes = 4)
    do_lst = []
    #lst = SP.GetVideoLatLon(TYPE)
    lst = SP.GetNegSourceList(LATLON=True)
    for one in lst:
        info = SP.GetPath(one[0], TYPE)
        c = 1
        try:
            f = open(info['pano_path'] + '/pano_lst_finish.txt','r')
            for line in f:
                c+=1
            f.close()
            if c<= 300:
                do_lst.append(one)
        except:
            do_lst.append(one)
    #g = ('000044','24.958109','121.224663')
    #Download(g)
    print len(do_lst)
    pool.map(Download, do_lst)
    SendEmail.SendEmail(To = 'tdk356ubuntu@gmail.com')
