
import time, threading, io, sys
import PyIndi
import readline
import autopa
import calibrate

from os.path import split
from util import exec

cmdName = "Meade"
telescopeName = "LX200 OpenAstroTech"
dec_offset = 15964
ra_offset = -2692
hostname = "max.local"
# hostname = "localhost"
ra_steps = "1243.6 " # 1258.6
dec_steps = "633.6 " # 628.3
port = 7624
#user = "orangepi"
ssh_cmd = "ssh max"

class OpenAstroClient(PyIndi.BaseClient):
    def __init__(self, hostname=hostname, port=port):
        super(OpenAstroClient, self).__init__()
        self.setServer(hostname,int(port))
        self.blobEvent=threading.Event()
        self.debug = True
        self._hostname = hostname
        if (not(self.connectServer())):
            raise Exception(f"No indiserver running on {hostname}:{port} - Run server in Ekos first.")
        self.telescope=self.getDevice(telescopeName)
        while not(self.telescope):
            time.sleep(0.5)
            self.log(f"Waiting for {telescopeName}")
            self.telescope=self.getDevice(telescopeName)
        if True:
            self.connect()
            self.meadeProp = self.telescope.getText(cmdName)
            while not(self.meadeProp):
                self.log(f"Waiting for '{cmdName}'")
                time.sleep(0.5)
                self.meadeProp=self.telescope.getText(cmdName)
    @property
    def debug(self):
        return self._debug
    @property
    def hostname(self):
        return self._hostname
    @debug.setter
    def debug(self, val):
        self._debug = val
    def log(self,msg,end="\n"):
        if self.debug:
            print(msg,end=end)
    def sendCommand(self,cmd):
        self.meadeResultRead = False
        self.meadeProp[0].text = cmd
        self.log(f">> Sending: {cmd}")
        self.sendNewText(self.meadeProp)
        time.sleep(0.2)
        return ("ok", "ok")
    def sendCommandAndWait(self,cmd):
        self.meadeResultRead = False
        self.meadeProp[0].text = cmd
        self.log(f">> Sending: {cmd}")
        self.sendNewText(self.meadeProp)
        while not(self.meadeResultRead):
            self.log(f"\r<<Waiting for result: {cmd}", end="")
            time.sleep(0.2)
        self.log(f"<< Received: {self.meadeResult.s} {self.meadeResult.tp.text}")
        return self.meadeResult.s,self.meadeResult.tp.text
    def newDevice(self, d):
        pass
    def newProperty(self, p):
        pass
    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        pass
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        pass
    def newText(self, tvp):
        if tvp.label == cmdName:
            self.meadeResultRead = True
            self.meadeResult = tvp
        self.log(f">> newText=>{tvp.label}={tvp.tp.text}")
        pass
    def newLight(self, lvp):
        pass
    def newMessage(self, d, m):
        pass
    def serverConnected(self):
        pass
    def serverDisconnected(self, code):
        pass
    def toggleSwitch(self, switch, index):
        for i in range(0,len(switch)):
            state = PyIndi.ISS_ON if i == index else PyIndi.ISS_OFF
            switch[i].setState(state)
        self.sendNewSwitch(switch) # send this new value to the device
    def getProp(self, device, propType, propName):
        func = None
        if propType.lower() == "switch":
            func = self.telescope.getSwitch
        elif propType.lower() == "number":
            func = self.telescope.getNumber
        elif propType.lower() == "text":
            func = self.telescope.getText
        result = None
        if func != None:
            result = func(propName)
            while not(result):
                time.sleep(0.5)
                result = func(propName)
        return result
    def connect(self):
        telescope_connect = self.getProp(self.telescope, "switch", "CONNECTION")
        if not(self.telescope.isConnected()):
            self.toggleSwitch(telescope_connect, 0)
    def disconnect(self):
        telescope_connect = self.getProp(self.telescope, "switch", "CONNECTION")
        # if the telescope device is not connected, we do connect it
        while self.telescope.isConnected():
            self.toggleSwitch(telescope_connect, 1)
        time.sleep(1)

class Settings: 
    def __init__(self):
        self.dec_lower = None
        self.dec_upper = None
        self.ra_steps = None
        self.dec_steps = None
        self.dec_park = None
        self.ra_offset = None
        pass
    def save(self):
        pass
    def load(self):
        pass
    def read(self):
        if(self.dec_lower):
            return
        res = sendCommandAndWait(f"XGDLL")[1]
        # res = res.split("|")
        self.dec_lower = float(res)
        res = sendCommandAndWait(f"XGDLU")[1]
        self.dec_upper = float(res)
        self.ra_steps = float(sendCommandAndWait(f"XGR")[1])
        self.dec_steps = float(sendCommandAndWait(f"XGD")[1])
        self.dec_park = int(sendCommandAndWait(f"XGDP")[1])
        self.ra_offset = int(sendCommandAndWait(f"XGHR")[1])
    def write(self):
        pass
    def print(self):
        print(f"""DEC Limits:
    Lower: {self.dec_lower}
    Upper: {self.dec_upper}
Steps:
    RA: {self.ra_steps}
    DEC: {self.dec_steps}
Offsets:
    DEC: {self.dec_park}
    RA: {self.ra_offset}""")
        
if __name__ == '__main__':
    c = OpenAstroClient()
    s = Settings()
    cal = calibrate.Calibrate(c)
    def sendCommand(cmd):
        res = c.sendCommand(f"{cmd}#")
        print(f"# {cmd} -> {res}")
        return res
    def sendCommandAndWait(cmd):
        res = c.sendCommandAndWait(f":{cmd}#")
        print(f"# {cmd} -> {res}")
        return res
    def status():
        res = sendCommandAndWait(f"GX")[1].split(",")[0]
        return res
    def pos():
        res = sendCommandAndWait(f"GX")[1].split(",")[2:4]
        return [int(res[0]),int(res[1])]
    def print_settings():
        print("# settings")
        s.read()
        s.print()
    def shutdown():
        print("# shutdown")
        exec(f"{ssh_cmd} 'sudo shutdown now'")
    def xdf():
        print("# firmware display")
        sendCommandAndWait(f"XGHR")
        sendCommandAndWait(f"XGD")
        sendCommandAndWait(f"XGR")
    def xfr():
        print("# firmware reset")
        sendCommandAndWait("XFR")
        sendCommand(f":XSHR{ra_offset}#")
        sendCommand(f":XSD{dec_steps}#")
        sendCommand(f":XSR{ra_steps}#")
        print(f"XGD{sendCommandAndWait('XGD')[1]}\nXGR{sendCommandAndWait('XGR')[1]}")
    def reboot():
        print("# reboot")
        exec(f"{ssh_cmd} 'sudo reboot'")
    def waitFor(states):
        while True:
            res = status()
            print(res)
            if res in states:# == 'Tracking' or res == 'Parked':
                break
    def rest():
        (ra_pos,dec_pos) = pos()
        print(f"current pos: {(ra_pos,dec_pos)}")
        sendCommandAndWait(f"MXr{-ra_pos}")
        waitFor(['Tracking', 'Parked'])
        sendCommandAndWait(f"MXd{- dec_pos - dec_offset}")
        waitFor(['Tracking', 'Parked'])
    def pa():
        pa = autopa.AutoPA(c)
        pa.alignOnce()
    while True:
        print(">> Command: ", end="")
        string = input()
        if len(string) < 1:
            continue
        if string[0] == '#':
            parts = string.split()
            cmd,args = (parts[0], parts[1:])
            if cmd == '#sleep':
                time.sleep(int(args[0]))
            if cmd == '#temp':
                time.sleep(int(args[0]))
            if cmd == '#rest':
                rest()
            if cmd == '#xfr':
                xfr()
            if cmd == '#shutdown':
                shutdown()
            if cmd == '#reboot':
                reboot()
            if cmd == '#prefs':
                print_settings()
            if cmd == '#pa':
                pa()
        elif string[0] == '@':
            print(f">>> Send: {string}#")
            result = c.sendCommand(f"{string}#")
            print(f">> Result: {result}")
        else:
            result = sendCommandAndWait(string)
            print(f">> Result: {result}")
