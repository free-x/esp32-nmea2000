#! /usr/bin/env python3
import re
import sys
import os
import datetime
import getopt
import time

###generated with getPgnType.py from canboat pgns.json
PGNM_Fast=0
PGNM_Single=1
PGNM_ISO=2
PGN_MODES={

    59392: PGNM_Single,
    59904: PGNM_Single,
    60160: PGNM_Single,
    60416: PGNM_Single,
    60416: PGNM_Single,
    60416: PGNM_Single,
    60416: PGNM_Single,
    60416: PGNM_Single,
    60928: PGNM_Single,
    61184: PGNM_Single,
    61184: PGNM_Single,
    61184: PGNM_Single,
    65001: PGNM_Single,
    65002: PGNM_Single,
    65003: PGNM_Single,
    65004: PGNM_Single,
    65005: PGNM_Single,
    65006: PGNM_Single,
    65007: PGNM_Single,
    65008: PGNM_Single,
    65009: PGNM_Single,
    65010: PGNM_Single,
    65011: PGNM_Single,
    65012: PGNM_Single,
    65013: PGNM_Single,
    65014: PGNM_Single,
    65015: PGNM_Single,
    65016: PGNM_Single,
    65017: PGNM_Single,
    65018: PGNM_Single,
    65019: PGNM_Single,
    65020: PGNM_Single,
    65021: PGNM_Single,
    65022: PGNM_Single,
    65023: PGNM_Single,
    65024: PGNM_Single,
    65025: PGNM_Single,
    65026: PGNM_Single,
    65027: PGNM_Single,
    65028: PGNM_Single,
    65029: PGNM_Single,
    65030: PGNM_Single,
    65240: PGNM_ISO,
    65280: PGNM_Single,
    65284: PGNM_Single,
    65285: PGNM_Single,
    65285: PGNM_Single,
    65286: PGNM_Single,
    65286: PGNM_Single,
    65287: PGNM_Single,
    65287: PGNM_Single,
    65288: PGNM_Single,
    65289: PGNM_Single,
    65290: PGNM_Single,
    65292: PGNM_Single,
    65293: PGNM_Single,
    65293: PGNM_Single,
    65302: PGNM_Single,
    65305: PGNM_Single,
    65305: PGNM_Single,
    65305: PGNM_Single,
    65305: PGNM_Single,
    65305: PGNM_Single,
    65309: PGNM_Single,
    65312: PGNM_Single,
    65340: PGNM_Single,
    65341: PGNM_Single,
    65345: PGNM_Single,
    65350: PGNM_Single,
    65359: PGNM_Single,
    65360: PGNM_Single,
    65361: PGNM_Single,
    65371: PGNM_Single,
    65374: PGNM_Single,
    65379: PGNM_Single,
    65408: PGNM_Single,
    65409: PGNM_Single,
    65410: PGNM_Single,
    65420: PGNM_Single,
    65480: PGNM_Single,
    126208: PGNM_Fast,
    126208: PGNM_Fast,
    126208: PGNM_Fast,
    126208: PGNM_Fast,
    126208: PGNM_Fast,
    126208: PGNM_Fast,
    126208: PGNM_Fast,
    126464: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126720: PGNM_Fast,
    126983: PGNM_Fast,
    126984: PGNM_Fast,
    126985: PGNM_Fast,
    126986: PGNM_Fast,
    126987: PGNM_Fast,
    126988: PGNM_Fast,
    126992: PGNM_Single,
    126993: PGNM_Single,
    126996: PGNM_Fast,
    126998: PGNM_Fast,
    127233: PGNM_Fast,
    127237: PGNM_Fast,
    127245: PGNM_Single,
    127250: PGNM_Single,
    127251: PGNM_Single,
    127252: PGNM_Single,
    127257: PGNM_Single,
    127258: PGNM_Single,
    127488: PGNM_Single,
    127489: PGNM_Fast,
    127490: PGNM_Fast,
    127491: PGNM_Fast,
    127493: PGNM_Single,
    127494: PGNM_Fast,
    127495: PGNM_Fast,
    127496: PGNM_Fast,
    127497: PGNM_Fast,
    127498: PGNM_Fast,
    127500: PGNM_Single,
    127501: PGNM_Single,
    127502: PGNM_Single,
    127503: PGNM_Fast,
    127504: PGNM_Fast,
    127505: PGNM_Single,
    127506: PGNM_Fast,
    127507: PGNM_Fast,
    127508: PGNM_Single,
    127509: PGNM_Fast,
    127510: PGNM_Fast,
    127511: PGNM_Single,
    127512: PGNM_Single,
    127513: PGNM_Fast,
    127514: PGNM_Single,
    127744: PGNM_Single,
    127745: PGNM_Single,
    127746: PGNM_Single,
    127750: PGNM_Single,
    127751: PGNM_Single,
    128000: PGNM_Single,
    128001: PGNM_Single,
    128002: PGNM_Single,
    128003: PGNM_Single,
    128006: PGNM_Single,
    128007: PGNM_Single,
    128008: PGNM_Single,
    128259: PGNM_Single,
    128267: PGNM_Single,
    128275: PGNM_Fast,
    128520: PGNM_Fast,
    128538: PGNM_Fast,
    128768: PGNM_Single,
    128769: PGNM_Single,
    128776: PGNM_Single,
    128777: PGNM_Single,
    128778: PGNM_Single,
    128780: PGNM_Single,
    129025: PGNM_Single,
    129026: PGNM_Single,
    129027: PGNM_Single,
    129028: PGNM_Single,
    129029: PGNM_Fast,
    129033: PGNM_Single,
    129038: PGNM_Fast,
    129039: PGNM_Fast,
    129040: PGNM_Fast,
    129041: PGNM_Fast,
    129044: PGNM_Fast,
    129045: PGNM_Fast,
    129283: PGNM_Single,
    129284: PGNM_Fast,
    129285: PGNM_Fast,
    129291: PGNM_Single,
    129301: PGNM_Fast,
    129302: PGNM_Fast,
    129538: PGNM_Fast,
    129539: PGNM_Single,
    129540: PGNM_Fast,
    129541: PGNM_Fast,
    129542: PGNM_Fast,
    129545: PGNM_Fast,
    129546: PGNM_Single,
    129547: PGNM_Fast,
    129549: PGNM_Fast,
    129550: PGNM_Fast,
    129551: PGNM_Fast,
    129556: PGNM_Fast,
    129792: PGNM_Fast,
    129793: PGNM_Fast,
    129794: PGNM_Fast,
    129795: PGNM_Fast,
    129796: PGNM_Fast,
    129797: PGNM_Fast,
    129798: PGNM_Fast,
    129799: PGNM_Fast,
    129800: PGNM_Fast,
    129801: PGNM_Fast,
    129802: PGNM_Fast,
    129803: PGNM_Fast,
    129804: PGNM_Fast,
    129805: PGNM_Fast,
    129806: PGNM_Fast,
    129807: PGNM_Fast,
    129808: PGNM_Fast,
    129808: PGNM_Fast,
    129809: PGNM_Fast,
    129810: PGNM_Fast,
    130052: PGNM_Fast,
    130053: PGNM_Fast,
    130054: PGNM_Fast,
    130060: PGNM_Fast,
    130061: PGNM_Fast,
    130064: PGNM_Fast,
    130065: PGNM_Fast,
    130066: PGNM_Fast,
    130067: PGNM_Fast,
    130068: PGNM_Fast,
    130069: PGNM_Fast,
    130070: PGNM_Fast,
    130071: PGNM_Fast,
    130072: PGNM_Fast,
    130073: PGNM_Fast,
    130074: PGNM_Fast,
    130306: PGNM_Single,
    130310: PGNM_Single,
    130311: PGNM_Single,
    130312: PGNM_Single,
    130313: PGNM_Single,
    130314: PGNM_Single,
    130315: PGNM_Single,
    130316: PGNM_Single,
    130320: PGNM_Fast,
    130321: PGNM_Fast,
    130322: PGNM_Fast,
    130323: PGNM_Fast,
    130324: PGNM_Fast,
    130330: PGNM_Fast,
    130560: PGNM_Single,
    130561: PGNM_Fast,
    130562: PGNM_Fast,
    130563: PGNM_Fast,
    130564: PGNM_Fast,
    130565: PGNM_Fast,
    130566: PGNM_Fast,
    130567: PGNM_Fast,
    130569: PGNM_Fast,
    130570: PGNM_Fast,
    130571: PGNM_Fast,
    130572: PGNM_Fast,
    130573: PGNM_Fast,
    130574: PGNM_Fast,
    130576: PGNM_Single,
    130577: PGNM_Fast,
    130578: PGNM_Fast,
    130579: PGNM_Single,
    130580: PGNM_Fast,
    130581: PGNM_Fast,
    130582: PGNM_Single,
    130583: PGNM_Fast,
    130584: PGNM_Fast,
    130585: PGNM_Single,
    130586: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130816: PGNM_Fast,
    130817: PGNM_Fast,
    130817: PGNM_Fast,
    130818: PGNM_Fast,
    130819: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130820: PGNM_Fast,
    130821: PGNM_Fast,
    130821: PGNM_Fast,
    130822: PGNM_Fast,
    130823: PGNM_Fast,
    130824: PGNM_Fast,
    130824: PGNM_Fast,
    130825: PGNM_Fast,
    130827: PGNM_Fast,
    130828: PGNM_Fast,
    130831: PGNM_Fast,
    130832: PGNM_Fast,
    130833: PGNM_Fast,
    130834: PGNM_Fast,
    130835: PGNM_Fast,
    130836: PGNM_Fast,
    130836: PGNM_Fast,
    130837: PGNM_Fast,
    130837: PGNM_Fast,
    130838: PGNM_Fast,
    130839: PGNM_Fast,
    130840: PGNM_Fast,
    130842: PGNM_Fast,
    130842: PGNM_Fast,
    130842: PGNM_Fast,
    130843: PGNM_Fast,
    130843: PGNM_Fast,
    130845: PGNM_Fast,
    130845: PGNM_Fast,
    130846: PGNM_Fast,
    130846: PGNM_Fast,
    130847: PGNM_Fast,
    130850: PGNM_Fast,
    130850: PGNM_Fast,
    130850: PGNM_Fast,
    130851: PGNM_Fast,
    130856: PGNM_Fast,
    130860: PGNM_Fast,
    130880: PGNM_Fast,
    130881: PGNM_Fast,
    130944: PGNM_Fast,

    }




def logError(fmt,*args,keep=False):
    print("ERROR:" +fmt%(args),file=sys.stderr)
    if not keep:
        sys.exit(1)

def dataToSep(data,maxbytes=None):
    pd=None
    dl=int(len(data)/2)
    if maxbytes is not None and maxbytes < dl:
        dl=maxbytes
    for p in range(0,dl):
        i=2*p
        if pd is None:
            pd=data[i:i+2]
        else:
            pd+=","+data[i:i+2]
    return pd
class Format:
    F_PLAIN=0
    N_PLAIN='plain'
    F_ACT=1
    N_ACT='actisense'
    F_PASS=2
    N_PASS='pass'
    def __init__(self,name,key,merge=True):
        self.key=key
        self.name=name
        self.merge=merge

class CanFrame:
    DUMP_PAT=re.compile(r'\(([^)]*)\) *([^ ]*) *([^#]*)#(.*)')

    def __init__(self,ts,pgn,src=1,dst=255,prio=1,dev=None,hdr=None,data=None):
        self.pgn=pgn
        self.mode=PGN_MODES.get(pgn)
        self.ts=ts
        self.src=src
        self.dst=dst
        self.data=data
        self.prio=prio
        self.sequence=None
        self.frame=None
        self.len=8
        self.dev=dev
        self.hdr=hdr
        if self.mode == PGNM_Fast and data is not None and len(self.data) >= 2:
            fb=int(data[0:2],16)
            self.frame=fb & 0x1f
            self.sequence=fb >> 5
            
    def key(self):
        if self.sequence is None or self.pgn == 0:
            return None
        return f"{self.pgn}-{self.sequence}-{self.src}"
    def getFPNum(self,bytes=False):
        if self.frame != 0:
            return None
        if len(self.data) < 4:
            return None
        numbytes=int(self.data[2:4],16)
        if bytes:
            return numbytes
        frames=int((numbytes-6-1)/7)+1+1 if numbytes > 6 else 1 
        return frames
    
    def _formatTs(self):
        dt=datetime.datetime.fromtimestamp(self.ts,tz=datetime.UTC)
        return dt.strftime("%F-%T.")+dt.strftime("%f")[0:3]

    def __str__(self):
        return f"{self._formatTs()},{self.prio},{self.pgn},{self.src},{self.dst},{self.len},{dataToSep(self.data)}"
    
    def printOut(self,format:Format):
        if format.key == Format.F_PASS:
            return f"({self.ts}) {self.dev} {self.hdr}#{self.data}"
        else:
            return str(self)

    
    @classmethod
    def fromDump(cls,line):
        '''(1658058069.867835) can0 09F80103#ACAF6C20B79AAC06'''
        match=cls.DUMP_PAT.search(line)
        if match is None:
            logError("no dump pattern in line %s",line,keep=True)
            return
        ts=match[1]
        data=match[4]
        hdr=match[3]
        hdrval=int(hdr,16)
        #see candump2analyzer
        src=hdrval & 0xff
        prio=(hdrval >> 26) & 0x7
        PF=(hdrval >> 16) & 0xff
        PS=(hdrval >> 8) & 0xff
        RDP=(hdrval >> 24) & 3
        pgn=0
        if PF < 240:
            dst=PS
            pgn=(RDP << 16) + (PF << 8)
        else:
            dst=0xff
            pgn=(RDP << 16) + (PF << 8)+PS
        return CanFrame(float(ts),pgn,src=src,dst=dst,prio=prio,data=data,dev=match[2],hdr=hdr)
    
class MultiFrame(CanFrame):
    def __init__(self,firstFrame: CanFrame):
        super().__init__(firstFrame.ts,firstFrame.pgn,
                       src=firstFrame.src,dst=firstFrame.dst,prio=firstFrame.prio,
                       dev=firstFrame.dev,hdr=firstFrame.hdr)
        self.data=""
        self.numFrames=firstFrame.getFPNum(bytes=False)
        self.len=firstFrame.getFPNum(bytes=True)
        self.finished=False
        self.addFrame(firstFrame)
    
    def addFrame(self,frame:CanFrame):
        if self.finished:
            return False
        if frame.frame is None:
            return False
        if frame.frame == 0:
            self.data+=frame.data[4:]
        else:
            self.data+=frame.data[2:]
        if frame.frame >= (self.numFrames-1):
            self.finished=True
            return True
    
    def __str__(self):
        return f"{self._formatTs()},{self.prio},{self.pgn},{self.src},{self.dst},{self.len},{dataToSep(self.data,self.len)}"

def usage():
    print(f"usage: {sys.argv[0]} [-q] [-p pgn,pgn,...] [-w waitsec] [ -f plain|actisense] file")
    sys.exit(1)




FORMATS=[
    Format(Format.N_PLAIN,Format.F_PLAIN),
    Format(Format.N_ACT,Format.F_ACT),
    Format(Format.N_PASS,Format.F_PASS,False)
]

MAX_ACT=400
ACT_ESC=0x10
ACT_START=0x2
ACT_N2K=0x93
ACT_END=0x3

class ActBuffer:
    def __init__(self):
        self.buf=bytearray(MAX_ACT)
        self.sum=0
        self.idx=0
        self.clear()
    def clear(self):
        self.sum=0
        self.idx=2
        self.buf[0:2]=(ACT_ESC,ACT_START)
    def add(self,val):
        #TODO: len check?
        val=val & 0xff
        self.buf[self.idx]=val
        self.sum = (self.sum + val) & 0xff
        self.idx+=1
        if val == ACT_ESC:
            self.buf[self.idx]=ACT_ESC
            self.idx+=1
    def finalize(self):
        self.sum=self.sum % 256
        self.sum = 256 - self.sum if self.sum != 0 else 0
        self.add(self.sum)
        self.buf[self.idx]=ACT_ESC
        self.idx+=1
        self.buf[self.idx]=ACT_END
        self.idx+=1

actBuffer=ActBuffer()

def send_act(frame_like:CanFrame,quiet):
    try:
        actBuffer.clear()
        actBuffer.add(ACT_N2K)
        actBuffer.add(frame_like.len+11)
        actBuffer.add(frame_like.prio)
        pgn=frame_like.pgn
        actBuffer.add(pgn)
        pgn = pgn >> 8
        actBuffer.add(pgn)
        pgn = pgn >> 8;
        actBuffer.add(pgn)
        actBuffer.add(frame_like.dst)
        actBuffer.add(frame_like.src)
        #Time
        actBuffer.add(0)
        actBuffer.add(0)
        actBuffer.add(0)
        actBuffer.add(0)

        actBuffer.add(frame_like.len)
        for i in range(0,frame_like.len*2,2):
            actBuffer.add(int(frame_like.data[i:i+2],16))
        actBuffer.finalize()
        written=sys.stdout.buffer.write(memoryview(actBuffer.buf)[0:actBuffer.idx])
        if (written != actBuffer.idx):
            if not quiet:
                logError(f"actisense not all bytes written {written}/{actBuffer.idx} for pgn={frame_like.pgn} ts={frame_like.ts}",keep=True)
        sys.stdout.buffer.flush()
        return True
    except Exception as e:
        if not quiet:
            print(f"Error writing actisense for pgn {frame_like.pgn}, idx={actBuffer.idx}: {e}",file=sys.stderr)
        return False

class Counters:
    C_OK=1
    C_FAIL=2
    C_FRAME=3
    TITLES={
        C_OK:'OK',
        C_FAIL:'FAIL',
        C_FRAME:'FRAMES'
    }
    def __init__(self):
        self.counters={}
        for i in self.TITLES.keys():
            self.counters[i]=0
    def add(self,idx:int):
        if idx not in self.TITLES.keys():
            return
        self.counters[idx]+=1
    def __str__(self):
        rt=None
        for i in self.TITLES.keys():
            v=f"{self.TITLES[i]}:{self.counters[i]}"
            if rt is None:
                rt=v
            else:
                rt+=","+v
        return rt

def writeOut(frame:CanFrame,format:Format,quiet:bool,counters:Counters):
    rt=False
    if format.key == Format.F_ACT:
        rt= send_act(frame,quiet)
    else:
        print(frame.printOut(format))
        rt=True
    counters.add(Counters.C_OK if rt else Counters.C_FAIL)
    return rt

def findFormat(name:str)->Format:
    for f in FORMATS:
        if f.name == name:
            return f
    return None

if __name__ == '__main__':
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hp:qw:f:")
    except getopt.GetoptError as e:
        logError(e)
    pgnlist=[]
    quiet=False
    delay=0.0
    format=findFormat(Format.N_PLAIN)
    for o,a in opts:
        if o == '-h':
            usage()
        elif o == '-q':
            quiet=True
        elif o == '-p':
            pgns=(int(x) for x in a.split(","))
            pgnlist.extend(pgns)
        elif o == '-w':
            delay=float(a)
        elif o == '-f':
            format=findFormat(a)
            if format is None:
                logError(f"invalid format {a}, allowed {','.join(x.name for x in FORMATS)}")
    if len(args) < 1:
        usage()
    hasFilter=len(pgnlist) > 0
    if not quiet and hasFilter:
        print(f"PGNs: {','.join(str(x) for x in pgnlist)}",file=sys.stderr)
    counters=Counters()
    with open (args[0],"r") as fh:
        buffer={}
        lnr=0
        for line in fh:
            lnr+=1
            frame=CanFrame.fromDump(line)
            if hasFilter and not frame.pgn in pgnlist:
                continue
            counters.add(Counters.C_FRAME)
            if frame.sequence is None or not format.merge:
                writeOut(frame,format,quiet,counters=counters)
                if delay > 0:
                    time.sleep(delay)
            else:
                key=frame.key()
                mf=buffer.get(key)
                mustDelete=False
                if mf is None:
                    if frame.frame != 0:
                        if not quiet:
                            print(f"floating multi frame in line {lnr}: {frame}",file=sys.stderr)
                        continue
                    mf=MultiFrame(frame)
                    if not mf.finished:
                        buffer[key]=mf
                else:
                    mf.addFrame(frame)
                    mustDelete=True
                if mf.finished:
                    writeOut(mf,format,quiet,counters=counters)
                    if mustDelete:
                        del buffer[key]
                    if delay > 0:
                        time.sleep(delay)
    if not quiet:
        print(f"STATISTICS: {counters}",file=sys.stderr)
        