import socket
import sys
import subprocess
import csv
import procname
import time
from datetime import datetime
import json
import urllib
import rasterio
import numpy as np
import os
import math

procname.setprocname("serverSide")

######################## VARIABLES ########################

outfile = "parsed_data.js" # Output file as a .geojson
archive_path = "archive/archive_" + str(datetime.now()) + ".csv"
radcap = 1 # Highest amount of radiation to scale color gradient
interval = 5 # Time in seconds in between scans
mapalt = 0
online = False
elevationFile = 'srtm_14_04.tif'
log = []
heatmapdata = []

#create a list of waypoints that has been visited
finishedwp = set([0, 1, 3, 4, 5, 6, 7, 8, 15, 16, 18, 19, 20, 21, 22, 30, 31, 33, 34, 35, 36, 37, 45, 46, 47, 48, 49, 50, 51, 52, 60, 61, 62, 63, 64, 65, 67, 71, 75, 76, 77, 78, 79, 80, 82, 86, 90, 91, 92, 93, 94, 95, 97, 101, 105, 106, 107, 108, 109, 110, 112, 116, 120, 121, 122, 123, 124, 125, 127, 131, 135, 136, 137, 138, 139, 140, 142, 146, 150, 151, 152, 153, 154, 155, 156, 157, 161, 166, 167, 168, 169, 170, 171, 172, 176, 181, 182, 183, 184, 185, 186, 187, 191, 196, 197, 198, 199, 200, 201, 202, 206, 211, 212, 213, 214, 215, 216, 217, 218, 219, 221, 226, 227, 228, 229, 230, 231, 232, 233, 234, 236, 237, 241, 242, 243, 244, 245, 246, 247, 251, 256, 257, 258, 259, 260, 261, 262, 266, 271, 272, 273, 274, 275, 276, 277, 281, 286, 287, 288, 289, 290, 291, 292, 301, 302, 303, 304, 305, 306, 307, 316, 317, 318, 319, 320, 321, 322, 331, 332, 333, 334, 335, 336, 337, 346, 347, 348, 349, 350, 351, 361, 362, 363, 364, 365, 366])
wpfile = "wp_data.txt"

###########################################################

def elevationOnline(lat, lng):
    apikey = "AIzaSyDvuEAYeb9xoSun0PHXVkM7oxl_sRZD2H4"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = urllib.urlopen(url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey)
    try:
        results = json.load(request).get('results')
        if 0 < len(results):
            elevation = results[0].get('elevation')
            # ELEVATION
            return elevation
        else:
            print ('HTTP GET Request failed.')
    except ValueError:
        print ('JSON decode failed: '+str(request))

def elevationOffline(lat, lng):
    global elevationFile
    coords = [(lat,lng)]
    elevation = 0
    with rasterio.open(elevationFile) as src:
        for val in src.sample(coords):
            elevation = val
        return elevation[0]
        
def countsconvert(rawcounts, absalt, mapalt, radtype):
    background = 0
    rval = 0
    newcounts = 0
    if radtype == "PRDER":
        background = 15.6
        rval = 0.66
    else:
        background = 9.6
        rval = 0.52
    newcounts = rawcounts - background
    if newcounts < 0:
        print("No radiation detected here")
        newcounts = 0
    heightaboveground = absalt - mapalt
    print("heightaboveground: " + str(heightaboveground))
    if heightaboveground < 0:
        print("Net height is negative")
        heightaboveground = 0
    conv = (newcounts * ((heightaboveground)**2) * 4 * math.pi) / rval
    return conv
        
def writeArchive(log):
    global archive_path
    script_dir = os.path.dirname(__file__)
    absolute_path = os.path.join(script_dir, archive_path)

    with open(archive_path, 'w') as outf:
        outfwriter = csv.writer(outf)
        for i in log:
            outfwriter.writerow(i)

def listen():
    global finishedwp
    global log
    global heatmapdata
    global radcap
    #create a TCP/IP socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #bind the socket to the port. SENSOR STATION IS 203!!
    #192.168.11.202
    serverflag = 0
    if (serverflag == 1):
        server_address = ('192.168.11.202',10000)
    else: 
        server_address = ('127.0.0.1',10000)

    #server_address = ('192.168.11.202',10000)
    print >>sys.stderr, 'Starting up on %s port %s...' % server_address
    sock.bind(server_address)

    #Listen for incoming connections. You can increase this but you must also allow threading.
    sock.listen(10)
    active_connections = 0
    savedata = None
    while True:
        print >>sys.stderr, 'Waiting for a connection... \n'
        connection, client_address = sock.accept()
        active_connections += 1
        try:
            while True:
                data=connection.recv(4096)
                #print("Connected!")
                #newdata = eval(data)
                if (len(data) > 1):
                
                    timeNow = str(datetime.now())
                    newdata = eval(data)
                    
                    print >>sys.stderr, 'Connection from UAS#%s on Port %s' % (newdata[0],client_address[1])
                    print("Working WP List: " + str(newdata[1]))
                    print("Finished WP: " + str(newdata[2]))
                    if (newdata[2] < 10000):                  
                      finishedwp.add(newdata[2])
                    print("Finished WP Set: " + str(finishedwp))
                    print("# of Finished: " + str(len(finishedwp))) + "/" + str(newdata[4])
                    print("At Index: " + str(newdata[3]+1) + "/" + str(newdata[1]))
                    
                    #sendall argument must be string or buffer, not a list
                    print("Sending back a message...")
                    if ((len(finishedwp)) == newdata[4]):
                      print("FINISHED!")
                      quit()
                    #sendbackmsg = [newdata[4],newdata[3]]
                    connection.sendall(str(finishedwp))
                    # Heatmap Portion
                    
                    droneID = newdata[0]
                    lat = float(newdata[5])
                    lon = float(newdata[6])
                    rawcounts = float(newdata[7])
                    absalt = float(newdata[8])
                    radtype = str(newdata[9])
                    print("droneID: " + str(droneID))
                    print("rawcounts: " + str(rawcounts))
                    print("radtype: " + str(radtype))
                    print("absalt: " + str(absalt))
              
                    if online:
                        mapalt = float(elevationOnline(lat, lon))
                    else:
                        mapalt = float(elevationOffline(lat,lon))
                    convcounts = countsconvert(rawcounts, absalt, mapalt, radtype) 
                    print("convcounts: " + str(convcounts))
                    log.append([timeNow, droneID, radtype, lat, lon, absalt, mapalt, rawcounts, convcounts])
                    heatmapdata.append([lat, lon, convcounts])
                    
                    with open(outfile, 'w') as outf:
                        radcap = 1
                        for i in range(len(heatmapdata)):
                            if heatmapdata[i][2] > radcap:
                                radcap = heatmapdata[i][2]
                        outf.write("var points = [\n")
                        for i in range(len(heatmapdata)):
                            outf.write('[{0},{1},"{2}"]'.format(heatmapdata[i][0],heatmapdata[i][1],heatmapdata[i][2]/radcap))
                            if i + 1 < len(heatmapdata):
                                outf.write(',\n')
                            else:
                                outf.write('\n')
                        outf.write('];')
                            
                    writeArchive(log)

                    with open(wpfile, 'a') as outf:
                        outf.write(str(finishedwp) + '\n')

                else:
                    break
                
        finally:
            connection.close()
        
if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
