import time
import serial
import threading


cmds = []
lock = threading.Lock()
condition = threading.Condition()
temperature = 0

def run_test():
    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='\\.\COM3',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
    ser.isOpen()
    while 1 :
        # get keyboard input
        inp = input(">> ")
        if inp == 'exit':
            ser.close()
            exit()
        else:
            # send the character to the device
            # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
            inp += '\r\n'
            ser.write(inp.encode('utf-8'))
            out = bytes()
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            while ser.inWaiting() > 0:
                r = ser.read(1)
                out += r
            out = out.decode('utf-8')
            if out != '':
                  print( ">>" + out, end = '')

def manipulate(type): # Turn on / Turn off aircon
    global lock
    global cmds
    lock.acquire()
    if type == 0: # turn on
        cmds.append("C/0")
    else:
        cmds.append("C/1")
    lock.release()
    


def alert():
    global condition
    condition.acquire()
    condition.notify()
    condition.release()

def run():
    global condition, lock
    global temperature, cmds
    condition.acquire()
    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='\\.\COM3',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
    ser.isOpen()
    while 1 :
        # get keyboard input
        inp = "C/2" # obtain temperature (default)
        lock.acquire()
        ##########
        if cmds:
            inp = cmds[0]
            del cmds[0]
        ##########
        lock.release()
        print("<< %s" % (inp))
        if inp == 'exit':
            ser.close()
            exit()
        else:
            # send the character to the device
            # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
            inp += '\r\n'
            ser.write(inp.encode('utf-8'))
            while 1:
                out = bytes()
                # let's wait one second before reading output (let's give device time to answer)
                while ser.inWaiting() > 0:
                    r = ser.read(1)
                    out += r
                if(not list(out)):
                    continue
                out = out.decode('utf-8')
                if out != '':
                    print( ">> ", end = '')
                    lines = out.split("\r\n")
                    for line in lines:
                        if( len(line) < 2 ):
                            continue
                        print(line)
                        if (line[0] == 'I' and line[2] == '2'):
                            print("Its degree!")
                            try:
                                temperature = float(line[4:])
                            except Exception as e:
                                print("Unknown error")
                                print(e)
                break
        #time.sleep(1)  
        condition.wait(timeout = 1)
    condition.release()


if __name__ == "__main__":
    #run()
    pass