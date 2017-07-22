import time
import serial
import threading

cmds = []
lock = threading.Lock()
condition = threading.Condition()
temperature = 0
temperature_prev = 0

MODE_AI = True
MARGINAL_TEMPERATURE_OFF = 27.0
MARGINAL_TEMPARATURE_ON = 27.5
IS_AC_TURNED_ON = False


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
                  # print( ">>" + out, end = '')
                  # print(">>" + out + "")
                pass

def manipulate(type): # Turn on / Turn off aircon
    global lock
    global cmds
    global IS_AC_TURNED_ON
    lock.acquire()
    if type == 0: # turn on
        cmds.append("C/0")
        IS_AC_TURNED_ON = True
    else:
        cmds.append("C/1")
        IS_AC_TURNED_ON = False
    lock.release()
    


def alert():
    global condition
    condition.acquire()
    condition.notify()
    condition.release()

def run():
    global condition, lock
    global temperature, cmds
    global IS_AC_TURNED_ON
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
    # Initialize the air condition by turning it on by ICCHOI
    manipulate(0)
    IS_AC_TURNED_ON = True

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
        #print("<< %s" % (inp))
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
                    # print( ">> ", end = '')
                    # print(">>" + out + "")
                    lines = out.split("\r\n")
                    for line in lines:
                        if( len(line) < 2 ):
                            continue
                        # print(line)
                        if (line[0] == 'I' and line[2] == '2'):
                            #print("Its degree!")
                            try:
                                temperature_prev = temperature
                                temperature = float(line[4:])
                                print(temperature)
                                # for AI mode
                                if MODE_AI:
                                    # by ICCHOI
                                    if abs(temperature_prev - temperature) < 0.25:
                                        if temperature >= MARGINAL_TEMPARATURE_ON and IS_AC_TURNED_ON == False:
                                            print('The AC has been turned ON by AI')
                                            manipulate(0)
                                        elif temperature <= MARGINAL_TEMPERATURE_OFF and IS_AC_TURNED_ON == True:
                                            print( 'The AC has been turned OFF by AI')
                                            manipulate(1)
                                    else:
                                        print('The thermometer returned an invalid temperature')

                            except Exception as e:
                                print("Unknown error")
                                # print(e)
                                pass
                break
        #time.sleep(1)  
        condition.wait(timeout = 1)
    condition.release()


if __name__ == "__main__":
    #run()
    pass