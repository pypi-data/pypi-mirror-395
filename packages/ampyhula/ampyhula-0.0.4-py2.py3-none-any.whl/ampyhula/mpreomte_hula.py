#!/usr/bin/env python

"""
Hula的repl通讯工具

这个模块提供MPRemoteHula类，用于通过TCP链接控制Hula飞行器内部的micropython解释器

"""

import sys
import socket
import time
from collections import deque
import select

_rawdelay = None

try:
    stdout = sys.stdout.buffer
except AttributeError:
    # Python2 doesn't have buffer attr
    stdout = sys.stdout

def stdout_write_bytes(b):
    b = b.replace(b"\x04", b"")
    stdout.write(b)
    stdout.flush()

class MPRemoteHulaError(Exception):
    def __init__(self,args):
        self.args = args
        super().__init__(args)

class TCPToSerial:
    def __init__(self, ip, port,read_timeout=None):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fifo = deque()
        #self.read_timeout = read_timeout
        self.read_timeout = None
        self.size = 0
        try:
            self.__socket.connect((ip, port))
        except Exception as e:
            raise  MPRemoteHulaError("")
        
    def __del__(self):
        if self.__socket != None:
            self.__socket.close()

    def close(self):
        if self.__socket!= None:
            self.__socket.close()
            self.__socket = None

    def read(self, size=4096):
        readable, _, _ = select.select([self.__socket], [], [], 1.0)
        data = b''
        if(readable):
            data = self.__socket.recv(size)
        return data

    
    def write(self, data):
        return self.__socket.send(data)



class MPRemoteHula:
    def __init__(self,ip="192.168.100.1",port=18989,wait=0, rawdelay=0):
        global _rawdelay
        _rawdelay = rawdelay
        try:
            self.serial = TCPToSerial(ip, port, read_timeout=10)
        except Exception as e:
            self.serial = None
            print(e)

    def check_connect(self):
        if(self.serial == None):
            return False
        else:
            return True

    def close(self):
        

        self.serial.close()
    
    def read_until(self, min_num_bytes, ending, timeout=10, data_consumer=None):
        if(not self.check_connect()):
            print("Error: Not Connect hula")
            return
        data = self.serial.read(min_num_bytes)
        if data_consumer:
            data_consumer(data)
        while True:
            if data.endswith(ending):
                break
            else:
                new_data = self.serial.read(min_num_bytes)
                data = data + new_data
                if data_consumer:
                    data_consumer(new_data)
        return data

    
    def keyboard_interrupt(self):
        self.serial.write(b'\x03')

    def reset_mpy(self):
        if(not self.check_connect()):
            print("Error: Not Connect hula")
            return

        self.serial.write(b'\x03')
        time.sleep(1)
        self.serial.write(b'\x03')
        time.sleep(0.5)
        data = self.read_until(1,b'Use Ctrl-D to exit, Ctrl-E for paste mode\n>>> ')
        if not data.endswith(b'Use Ctrl-D to exit, Ctrl-E for paste mode\n>>> '):
            raise MPRemoteHulaError('could not enter raw repl')
    
    def enter_raw_repl(self):
        # Brief delay before sending RAW MODE char if requests
        if _rawdelay > 0:
            time.sleep(_rawdelay)

        if(self.serial == None):
            print("Error: Not Connect hula")
            return
        self.serial.write(b'\x05') # ctrl-E: enter raw REPL
        data = self.read_until(1, b'paste mode; Ctrl-C to cancel, Ctrl-D to finish\n')
        if data.endswith(b'paste mode; Ctrl-C to cancel, Ctrl-D to finish\n'):
            pass

        
    
    def follow(self, timeout, data_consumer=None):
        # wait for normal output
        data = self.read_until(1, b'>>>', timeout=timeout, data_consumer=data_consumer)
        if not data.endswith(b'>>>'):
            raise MPRemoteHulaError('timeout waiting for first EOF reception')
        return data[:-3]
    
    def exec_raw_no_follow(self, command):
        if isinstance(command, bytes):
            command_bytes = command
        else:
            command_bytes = bytes(command, encoding='utf8')
        # write command
        for i in range(0, len(command_bytes), 256):
            self.serial.write(command_bytes[i:min(i + 256, len(command_bytes))])
        self.serial.write(b'\x04')
        data = self.read_until(1, b'>OK\n')

        
    def exec_raw(self, command, timeout=10, data_consumer=None):
        self.exec_raw_no_follow(command);
        return self.follow(timeout, data_consumer)

    def eval(self, expression):
        ret = self.exec_('print({})'.format(expression))
        ret = ret.strip()
        return ret

    def exec_(self, command, stream_output=False):
        data_consumer = None
        if stream_output:
            data_consumer = stdout_write_bytes
        ret = self.exec_raw(command, data_consumer=data_consumer)
        if(ret.find(b'Traceback')>-1):
            index = ret.find(b'Traceback')
            ret_no_err = ret[0:index-1]
            ret_err = ret[index:]
            raise MPRemoteHulaError('exception', ret_no_err,ret_err)
        return ret

    def execfile(self, filename, stream_output=False):
        with open(filename, 'rb') as f:
            pyfile = f.read()
        return self.exec_(pyfile, stream_output=stream_output)

    def get_time(self):
        t = str(self.eval('pyb.RTC().datetime()'), encoding='utf8')[1:-1].split(', ')
        return int(t[4]) * 3600 + int(t[5]) * 60 + int(t[6])
    

    # in Python2 exec is a keyword so one must use "exec_"
# but for Python3 we want to provide the nicer version "exec"
setattr(MPRemoteHula, "exec", MPRemoteHula.exec_)

def execfile(filename, ip="192.168.100.1",port=18989):
    pyb = MPRemoteHula(ip,port)
    pyb.enter_raw_repl()
    output = pyb.execfile(filename)
    stdout_write_bytes(output)
    pyb.exit_raw_repl()
    pyb.close()



def main():
    import argparse
    cmd_parser = argparse.ArgumentParser(description='Run scripts on HighHula.')

    cmd_parser.add_argument('-ip','--ip', default='192.168.100.1', help='the Hula IP address') 
    cmd_parser.add_argument('-p','--port', default=8266, help='the Hula port')
    cmd_parser.add_argument('-c', '--command', help='program passed in as string')
    cmd_parser.add_argument('-w', '--wait', default=0, type=int, help='seconds to wait for TCP Connect')
    cmd_parser.add_argument('--follow', action='store_true', help='follow the output after running the scripts [default if no scripts given]')
    cmd_parser.add_argument('files', nargs='*', help='input files')
    args = cmd_parser.parse_args()

    def execbuffer(buf):
        try:
            pyb = MPRemoteHula(args.ip, args.port, args.wait)
            pyb.enter_raw_repl()
            ret, ret_err = pyb.exec_raw(buf, timeout=None, data_consumer=stdout_write_bytes)
            pyb.exit_raw_repl()
            pyb.close()
        except MPRemoteHulaError as er:
            print(er)
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)
        if ret_err:
            stdout_write_bytes(ret_err)
            sys.exit(1)

    if args.command is not None:
        execbuffer(args.command.encode('utf-8'))

    for filename in args.files:
        with open(filename, 'rb') as f:
            pyfile = f.read()
            execbuffer(pyfile)

    if args.follow or (args.command is None and len(args.files) == 0):
        try:
            pyb = MPRemoteHula(args.ip, args.port, args.wait)
            ret, ret_err = pyb.follow(timeout=None, data_consumer=stdout_write_bytes)
            pyb.close()
        except MPRemoteHulaError as er:
            print(er)
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)
        if ret_err:
            stdout_write_bytes(ret_err)
            sys.exit(1)

if __name__ == "__main__":
    main()
