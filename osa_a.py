from multiprocessing import Process, Queue
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from serial import Serial
import time
from os import listdir
from os.path import isfile, join
import queue as Q
import msvcrt
from scipy.signal import savgol_filter
from scipy import signal
from scipy import interpolate

#def integ_set():



def func1(queue,queueb):
    
#    ser = Serial("COM7")
    import serial.tools.list_ports
    def find_arduino(serial_number):
        for pinfo in serial.tools.list_ports.comports():
            if pinfo.serial_number == serial_number:
                return serial.Serial(pinfo.device)
        raise IOError("Could not find an arduino - is it plugged in?")
    
#    ser = find_arduino(serial_number='7')
    try:
        ser = find_arduino(serial_number='7')
    except:
        print ("err")
        ser = find_arduino(serial_number='6')
#    ser = serial.Serial('COM4')

    
    def kb():
        x=msvcrt.kbhit()
        if x:
            xxx=msvcrt.getch()
        else:
            return False
        return xxx

    
    
    
    data_buff_size = 3695     
    data = np.zeros(data_buff_size) 
    n_bytes = 7390
    n=3694
    k=0
    kk=0
    kkk=0
    data11=np.zeros(n)
    datax=np.zeros([0])
    dataxx=np.zeros([0])
#    mydata=np.zeros([8,3694])
#    mydatab=np.zeros([2,3694])
    k1=0
    xa=3
    xb=0
    k3=0
    k4=0
    
    xc=0

    
    def save_file(dmas):

        files = [f for f in listdir('data') if isfile(join('data', f))]
        hh=len(files)+1
#        hh=90
        hh1='data/'+str(hh)+'.npy'
        y22 = dmas.astype(dtype=np.float16)
        np.save(hh1, y22)
#        print "logging data for : ", time.time()-t2, " second"
#        print "saving data as : ", hh1 


    xx="b "
    ta=time.time()
    while k == 0: 
                
    #    while k==0:
        x=kb()
        try:
            if x!= False and x!='\r':
        #         try:         
                x=x.decode()
                xx=xx+x
#                print (x)
            if x!=False and x=='\r':
#                print ("aaa")
#                print (xx)
                if xx[2]== "d":        
                    print ("finish")
#                    xa=1
                    xc=0
                elif xx[2]== "s":
#                    xa=0
                    print("start")
                    xc=3

                xx="b"
        except UnicodeDecodeError:
            print ("only number are allowed")
            x=kb()
            xx="b"
        except ValueError:
            xx="b"
            print ("only number are allowed")
        except IndexError:
            xx="b"
            print ("please input number")
    #    time.sleep(0.03)



        kkk=kkk+1         
        rslt = ser.read(180000)
        data = np.fromstring(rslt, dtype=np.uint16)
        ## print "ok ", time.time()-t1
        if data[0] > 12500:
            rslt=rslt[1:-1]
            data = np.fromstring(rslt, dtype=np.uint16)
            kk=ser.read(1)
            print ("error")
        
        if np.max(data)==6000 and xc==3:
            k3=5
        if k3==5 and k4==3:
            k4=0
            k3=0
            queueb.put(dataxx)
            dataxx=np.zeros([0])
            dataxx=np.zeros([0])
        if k3==3:
            dataxx=np.append(dataxx,data)
            k4=3
        if np.max(data)==5000 and xc==3:
            k3=3
        

        datab=data[0::55]
        queue.put(datab)



        
        if xa==0:
            print ("begin data logging")
            k1=1
            datax=np.append(datax,data[0::15])
#            datax=np.append(datax,data)
            datax=np.zeros([0])
            xa=3
        if xa==1:
            k1=0
            save_file(datax)
#            print ("okkkk")
            xa=3
            
        if k1==1:
            xb=xb+1
            try:
                datax=np.append(datax,data[0::15])
#                datax=np.append(datax,data)
            except ValueError:
                pass





def func2(queue,queuec):
#    from scipy.signal import savgol_filter
    
    time.sleep(0.8)
    win = pg.GraphicsWindow()
    win.setWindowTitle('Data')
    n=4000
    data22=np.zeros(n)
    global dataave
    dataave=np.zeros([505,n])
    global master
    master=np.zeros([3,700])
    
    p1 = win.addPlot()
    win.nextRow()
    p2 = win.addPlot()
    
    curvea = p1.plot(data22, pen=(0,255 ,0))
    curveb= p1.plot(data22, pen=(0,0 , 255))
    curvec= p2.plot(data22, pen=(0,0 , 255))
#    p1.setYRange(-30, 2300, padding=0)
    

    
    def update1():
        global dataave
        global master
        datx=queue.get(timeout=9)
        try:
            master=queuec.get(timeout=0.09)
        except:
            pass
        curvea.setData(datx[0::2])
        curveb.setData(datx[1::2])
        curvec.setData(master[0],master[2])
        

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update1)
    timer.start(50)
    
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()



def func3(queueb,queuec):
    def save_file(dmas):
        files = [f for f in listdir('data') if isfile(join('data', f))]
        hh=len(files)+1
        hh1='data/'+str(hh)+'.npy'
        y22 = dmas.astype(dtype=np.float)
        np.save(hh1, y22)
        
    time.sleep(0.8)
    while True:
        q=0
        try:
            data = queueb.get(timeout=4)
            q=3
        except:
            data=0
            q=0
        if q==3:
            data=data[270000:]
#            data=data[0::15]
#            data=data[20000:]
            dataa=data[0::2]
            datab=data[1::2] 
            sizea=int(dataa.shape[0]/15)
            dataa=np.mean(dataa.reshape(sizea,15),1)
            datab=np.mean(datab.reshape(sizea,15),1)
            

            datab=datab-(np.mean(datab))
            datab=savgol_filter(datab,5, 3)
            
            refa_a=dataa-(np.mean(dataa))
            refa_a=savgol_filter(refa_a,5, 3)
            
            zero_crossings = np.where(np.diff(np.sign(refa_a)))[0]
            zr=zero_crossings[0::2]
            
            ref_b=np.empty([0])
            sig_a=np.empty([0])
            zra=zr[:-1]
            zrb=zr[1:]
            for qa in range(np.shape(zra)[0]):
                beg=zra[qa]
                end=zrb[qa]
                
                dist=end-beg
                xa=np.linspace(0,(dist-1),100)
                xb=np.arange(dist)
                fa = interpolate.interp1d(xb,refa_a[beg:end])
                ref_b=np.append(ref_b,fa(xa))
                fb = interpolate.interp1d(xb,datab[beg:end])
                sig_a=np.append(sig_a,fb(xa))
#                ref_b=np.append(ref_b,signal.resample(refa_a[beg:end],180))
#                sig_a=np.append(sig_a,signal.resample(datab[beg:end],180))
                
            wavecount=zr.shape[0]
            datacount=ref_b.shape[0]
            wave=(1.0/(np.arange(datacount)+1))*(wavecount*1064)
            
            
            save_file(np.append([ref_b],[sig_a],axis=0))
            
            ref_b=np.abs(np.fft.fft(ref_b))
            sig_a=np.abs(np.fft.fft(sig_a))
            
            end=int(np.where(wave>400)[0][-1])
            begin=int(np.where(wave<2000)[0][0])
            wave=wave[begin:end]
            ref_b=ref_b[begin:end]
            sig_a=sig_a[begin:end]
            
            master=np.append([wave],[ref_b],axis=0)
            master=np.append(master,[sig_a],axis=0)
            queuec.put(master)
            print ("ok")
#            p1.plot(wave,ref_b, pen=(255,0,0))
#            p1.plot(wave,sig_a, pen=(0,255,0))
#            p2.plot(wave,ref_b, pen=(255,0,0)) 
                    

if __name__ == '__main__':
    queue=Queue()
    queueb=Queue()
    queuec=Queue()

#    queue5=Queue()
#    queue6=Queue()
    
    p1 = Process(target=func1,args=(queue,queueb,))
    p1.start()
    p2 = Process(target=func2,args=(queue,queuec,))
    p2.start()
    p3 = Process(target=func3,args=(queueb,queuec,))
    p3.start()

    
    p1.join()
    p2.join()
    p3.join()

#    p4.join()