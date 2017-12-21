#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr
import binascii
import datetime
import time

def toDec(esa):
    if esa != "":
       out=str(int(esa,16))
       if len(out)==1:
          out="0"+out
    else:
       out=""
    return out

class urmetEasyRead(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
                      name="urmetEasyRead",
                      in_sig=[np.byte],
                      out_sig=[np.byte])

    def work(self, input_items, output_items):
        datatime = ""
        ts = time.time()
        current_time=datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%y_%H:%M:%S')
        data = binascii.hexlify(bytearray(input_items[0]))
        data = ' '.join(data[i:i+2] for i in range(0,len(data),2))
        data = data.split(" ")
        in0 = input_items[0]
        pretype = data[0] + data[1] + data[2]
        type = data[3]
        ulei = data[4] + data[5] + data[6] + data[7] + data[8]
        if str(type) == "53":
           datatime=toDec(data[12])+"-"+toDec(data[13])+"-"+toDec(data[14])+ " " + toDec(data[9]) + ":" + toDec(data[10]) + ":"+ toDec(data[11])
           unknown_data=data[15]+" "+data[16]+" "+data[17]+" "+data[18]+" "+data[19]+" "+data[20]+" "+data[21]+" "+data[22]+" "+data[23]+" "+data[24]+" "+data[25]+" "+data[26]+" "+data[27]+ " " + data[28]
        else:
           unknown_data=data[9] + " " + data[10] + " " + data[11] + " " + data[12] + " " + data[13] + " " + data[14]+" "+data[15]+" "+data[16]+" "+data[17]+" "+data[18]+" "+data[19]+" "+data[20]+" "+data[21]+" "+data[22]+" "+data[23]+" "+data[24]+" "+data[25]+" "+data[26]+" "+data[27]+ " " + data[28]
        #Print Hex
        print pretype, " ", type , " ", ulei, " ",datatime,"  ",unknown_data, "-", current_time
        hexdata= pretype+" "+type +" "+ulei+" "+datatime+"  "+unknown_data
        decimal=unknown_data.split(" ")
        decimalOut=""
        for i in range(0,len(decimal),1):
            decimal[i]=toDec(decimal[i])
            decimalOut+=" " + str(decimal[i])
        #Print Decimal
        if str(type) == "53":
           print pretype, " ", type," ", ulei, " ",datatime, " ", decimalOut, "-", current_time
        else:
           print pretype, " ", type," ", ulei, " ",datatime, " ", decimalOut, "-", current_time
        decdata=pretype+" "+type+" "+ulei+" "+datatime+" "+decimalOut
        #file maker
        filename="urmetEasyRead-"+str(type)+"-"+str(current_time)+".hack"
        file = open(filename,"w")
        file.write(hexdata+"\r\n")
        file.write(decdata+"\r\n")
        file.close()
        #domoConnector
        #filename="urmetEasyRead-"+str(type)+"-"+str(current_time)
        #file = open(filename,"w")
        #file.write(hexdata)
        #file.write(decdata)
        #file.close()
        # grc workaround
        in0 = input_items[0]
        return len(input_items[0])

