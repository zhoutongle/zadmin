#-*- coding: utf-8 -*-

import time
import Queue
import datetime
import threading

import utils
import setting
from writedebug import debug
from database import database
from diskraid import raid, disk, digiraid_lsi
#-----------------------------------
#
#-----------------------------------
UPDATERAIDMSGTHREAD = None #更新RAID信息线程
#-----------------------------------
# start thread
#-----------------------------------
def start():
    global UPDATERAIDMSGTHREAD
    try:
        if UPDATERAIDMSGTHREAD and isinstance(UPDATERAIDMSGTHREAD, UpdateRaidMsgThread) and UPDATERAIDMSGTHREAD.isAlive():
            if not UPDATERAIDMSGTHREAD._UpdateRaidMsgThread__running.isSet():
                UPDATERAIDMSGTHREAD._UpdateRaidMsgThread__running.set()
                UPDATERAIDMSGTHREAD.start()
        else:
            UPDATERAIDMSGTHREAD = UpdateRaidMsgThread('UPDATERAIDMSGTHREAD')
            UPDATERAIDMSGTHREAD.start()
    except:
        debug.write_debug(debug.LINE(),"updateraidmsgthreadclass")
#-----------------------------------
# stop thread
#-----------------------------------
def stop():
    global UPDATERAIDMSGTHREAD
    try:
        if UPDATERAIDMSGTHREAD and isinstance(UPDATERAIDMSGTHREAD, UpdateRaidMsgThread):
            if UPDATERAIDMSGTHREAD._UpdateRaidMsgThread__running.isSet():
                UPDATERAIDMSGTHREAD._UpdateRaidMsgThread__running.clear()
    except:
        debug.write_debug(debug.LINE(),"updateraidmsgthreadclass")
#-----------------------------------
# 更新硬RAID信息
# 更新磁盘
# 更新RAID
# 这逻辑太乱，原来的没看懂，照着改得感觉还是有问题
#-----------------------------------
def updateLsiRaid(raidnames):
    if raidnames:
        raidinfos = {}
        updatesql = []
        #磁盘信息
        lsidisks = digiraid_lsi.get_disks()
        for lsidisk in lsidisks:
            lsidisk['usr'] = '' #所在RAID
            if lsidisk['state'].find('Online') >= 0:
                usedstate = 1 #使用中
                #硬RAID时，Uuid里存放着RAID ID
                #扩容时磁盘找不到RAID信息，这块儿逻辑应该有些问题（多个RAID扩容）
                if not lsidisk.has_key('raidid'):
                    raidsql = "select Uuid,Name from Raid where state='reshape'"
                    raidids = database.selectTB([raidsql])
                    if raidids:
                        lsidisk['raidid'] = raidids[0][0]
                        lsidisk['usr'] = raidids[0][1]
                else:
                    raidsql = "select Name from Raid where Uuid='%s'" % lsidisk['raidid']
                    raidnames = database.selectTB([raidsql])
                    if raidnames:
                        lsidisk['usr'] = raidnames[0][0]
            elif lsidisk['state'].find('Offline') >= 0 or lsidisk['state'].find('Unconfigured(bad)') >= 0:
                usedstate = -2 #损坏
            elif lsidisk['state'].find('Unconfigured(good)') >= 0:
                usedstate = 2 #未使用
            elif lsidisk['state'].find('Hotspare') >= 0:
                usedstate = 3 #热备
                #全局热备
                if not lsidisk.has_key('raidid'):
                    lsidisk['usr'] = 'ALL'
            elif lsidisk['state'].find('Rebuild') >= 0:
                usedstate = 4 #重构
            if lsidisk['foreign']:
                usedstate = -1 #未激活
            #更新磁盘状态
            sql = "update Disk set Used='%s',Size='%s',Span='%s',Usr='%s',Model='%s',SN='%s' where Name='%s'" % (usedstate, lsidisk['size'], lsidisk['span'], lsidisk['usr'], lsidisk['model'], lsidisk['sn'], lsidisk['name'])
            updatesql.append(sql)
            #重构进度
            if lsidisk['state'].find('Rebuild') >= 0:
                if lsidisk.has_key('raidid'):
                    raidid = lsidisk['raidid']
                    diskname = lsidisk['name'].replace('-',':')
                    processinfo = digiraid_lsi.showprog(diskname,'disk')
                    if processinfo:
                        processinfo['state'] = 'recovery'
                        if not raidid in raidinfos:
                            raidinfos[raidid] = processinfo
        if updatesql:
            database.updateTB(updatesql)
            updatesql = []
        ####################################################################################################
        #更新RAID
        for raidname in raidnames:
            #RAID信息
            raidsql = "select uuid,name,state from Raid where name='%s' or uuid='%s'" % (raidname,raidname)
            raidmsg = database.selectTB([raidsql])
            if raidmsg:
                raidid = raidmsg[0][0]
                raidname = raidmsg[0][1]
                #查看是否有进度信息
                processinfo = digiraid_lsi.showprog(str(raidid),'raid')
                if processinfo:
                    if not raidid in raidinfos:
                        processinfo['state'] = raidmsg[0][2]
                        raidinfos[raidid] = processinfo
                else:
                    processinfo = digiraid_lsi.showprog(str(raidid),'init')
                    if processinfo:
                        processinfo['state'] = 'build'
                        raidinfos[raidid] = processinfo
                #否则直接获取
                if not raidid in raidinfos:
                    state = 'error'
                    progress = ''
                    remainingtime = ''
                    raidinfo = digiraid_lsi.get_raid_info(str(raidid))
                    if 'state' in raidinfo and raidinfo['state'] in setting.LSIRAIDSTATUS:
                        state = setting.LSIRAIDSTATUS[raidinfo['state']]
                    if 'progress' in raidinfo:
                        progress = raidinfo['progress']
                    if 'remainingtime' in raidinfo:
                        remainingtime = raidinfo['remainingtime']
                    raidinfos[raidid] = {
                        'progress': progress,
                        'remainingtime': remainingtime,
                        'state': state
                    }
                selectsql = "select Name,DiskId,ExpanderId,Used from Disk where Usr='%s'" % raidname
                diskdata = database.selectTB([selectsql])
                workdisk = []
                workdiskid = []
                sparedisk = []
                sparediskid = []
                faildisk = []
                faildiskid = []
                for lsidisk in diskdata:
                    if lsidisk[3] in ['1','4']:
                        workdisk.append(lsidisk[0])
                        workdiskid.append("%s-%s" % (lsidisk[2],lsidisk[1]))
                    elif lsidisk[3] == '3':
                        sparedisk.append(lsidisk[0])
                        sparediskid.append("%s-%s" % (lsidisk[2],lsidisk[1]))
                    elif lsidisk[3] == '-2':
                        faildisk.append(lsidisk[0])
                        faildiskid.append("%s-%s" % (lsidisk[2],lsidisk[1]))
                updatesql.append("update Raid set Progress='%s', RemainingTime='%s', State='%s', WorkingDisks='%s', FailDisks='%s', SpareDisks='%s', WorkingDisksId='%s', SpareDisksId='%s', FailDisksId='%s' where UUID='%s'" % (raidinfos[raidid]['progress'], raidinfos[raidid]['remainingtime'], raidinfos[raidid]['state'], ','.join(workdisk), ','.join(faildisk), ','.join(sparedisk), ','.join(workdiskid), ','.join(sparediskid), ','.join(faildiskid), raidid))

        if updatesql:
            database.updateTB(updatesql)
#-----------------------------------
# 更新RAID信息线程
#-----------------------------------
class UpdateRaidMsgThread(threading.Thread):
    def __init__ (self, threadname):
        try:
            threading.Thread.__init__(self, name=threadname)
            self.__running = threading.Event()
            self.__running.set()
        except:
            debug.write_debug(debug.LINE(),"updateraidmsgthreadclass")

    def run(self):
        while self.__running.isSet():
            try:
                raidnames = [] #有事件的RAID
                raidmsgs = database.selectTB(["select Name,State from Raid"])
                #判断是否有初始化，重构状态
                for raidmsg in raidmsgs:
                    if raidmsg[1] not in ['ok','alert','error']:
                        if raidmsg[0] not in raidnames:
                            raidnames.append(raidmsg[0])
                debug.write_debug(debug.LINE(), "updateraidmsgthreadclass", "***** %s" % raidnames)
                #接收事件消息
                if not raidnames:
                    while True:
                        try:
                            raidname = setting.RAIDMSGQUEUE.get(True)
                            raidnames.append(raidname)
                            if setting.RAIDMSGQUEUE.empty():
                                break
                        except Queue.Empty:
                            break
                        except:
                            debug.write_debug(debug.LINE(),"updateraidmsgthreadclass")
                            break
                else:
                    while True:
                        try:
                            raidname = setting.RAIDMSGQUEUE.get(True,20)
                            raidnames.append(raidname)
                            if setting.RAIDMSGQUEUE.empty():
                                break
                        except Queue.Empty:
                            break
                        except:
                            debug.write_debug(debug.LINE(),"updateraidmsgthreadclass")
                            break
                if raidnames:
                    #处理硬RAID
                    if setting.LSIRAID:
                        updateLsiRaid(raidnames)
                    else:#软RAID
                        process = {}
                        msg = {}
                        errname = []
                        allsql = []
                        for raidname in raidnames:
                            raiddev = raidname
                            if raiddev.find('/dev/') >= 0:
                                raidname = raidname.replace('/dev/','')
                            else:
                                raiddev = '/dev/%s' % raiddev
                            #RAID信息
                            msg = raid.getraiddetail(raiddev)
                            if not msg:
                                continue
                            #RAID状态
                            state = raid.get_raid_state(raiddev,msg['RaidLevel'])
                            if not state:
                                continue
                            #磁盘信息
                            diskids = {}
                            raiddisks = raid.asortRaidDisks(raiddev)
                            for key in raiddisks:
                                diskids[key] = ''
                                diskstr = ''
                                if raiddisks[key]:
                                    for m in raiddisks[key]:
                                        if diskstr:
                                            diskstr = "%s,'%s'" % (diskstr,m)
                                        else:
                                            diskstr = "'%s'" % m
                                    sql = "select ExpanderId,DiskId,Name,PhyId from Disk where Name in (%s)" % diskstr
                                    msgs = database.selectTB([sql])
                                    for n in msgs:
                                        tid = n[2] #磁盘名
                                        if n[0] and n[1]:
                                            tid = '%s-%s' % (n[0],n[1]) #扩展柜和盘位组合
                                        elif n[0] and n[3]:
                                            tid = '%s-%s' % (n[0],n[3]) #扩展柜和PhyId组合
                                        if diskids[key]:
                                            diskids[key] = '%s,%s' % (diskids[key],tid)
                                        else:
                                            diskids[key] = tid
                            #RAID初始化或同步进度
                            process = raid.get_raid_process(raiddev)
                            if not process:
                                process = {
                                    'rprate': '',
                                    'rptime': ''
                                }
                            #更新数据
                            sql = "update Raid set State='%s',\
                                Status='%s',\
                                Progress='%s',\
                                RemainingTime='%s',\
                                UpdateTime='%s',\
                                DiskNum='%s',\
                                WorkingDisks='%s',\
                                SpareDisks='%s',\
                                FailDisks='%s',\
                                WorkingDisksId='%s',\
                                SpareDisksId='%s',\
                                FailDisksId='%s',\
                                Size='%s',\
                                ArraySize='%s',\
                                UsedDevSize='%s' \
                                where Name='%s'"\
                                 %(state, msg['Status'], process['rprate'], process['rptime'], msg['UpdateTime'], process['rpdisknum'], ','.join(raiddisks['workingdisks']),\
                                     ','.join(raiddisks['sparedisks']), ','.join(raiddisks['faildisks']), diskids['workingdisks'], diskids['sparedisks'],\
                                     diskids['faildisks'], msg['Size'], msg['ArraySize'], msg['UsedDevSize'], raidname)
                            debug.write_debug(debug.LINE(), "updateraidmsgthreadclass", "***** %s" % sql)
                            allsql.append(sql)
                            warninglevel = '0' #正常
                            if state in ['alert','recovery']:
                                warninglevel = '1' #报警
                            if state in ['error']:
                                warninglevel = '2' #异常
                            if state in ['build','reshape']:
                                #用来标记需要扩展PV
                                setting.extendraidstatus[raidname] = 1
                                #标记当前RAID状态
                                setting.RAIDERRLIST[raidname] = state #初始化完成时的状态改变

                            #现在状态正常，在RAIDERRLIST中，异常->正常，从列表删除并记录日志
                            allchlogsql = []
                            allenlogsql = []
                            currtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                            if state in ['ok']:
                                if raidname in setting.RAIDERRLIST:
                                    monitordata = {'target':'raid', 'op':state, 'level':warninglevel, 'params':{'name':raidname}}
                                    setting.WARNINGQUEUE.put(monitordata)
                                    chlogsql = (currtime, msg['RaidLevel'], "Raid: %s %s" % (raidname, setting.CHRAIDERRSTATE[state]))
                                    enlogsql = (currtime, msg['RaidLevel'], "Raid: %s %s" % (raidname, state))
                                    allchlogsql.append(chlogsql)
                                    allenlogsql.append(enlogsql)
                                if raidname in setting.RAIDERRLIST:
                                    del setting.RAIDERRLIST[raidname]
                                #是否需要扩容
                                if raiddev in setting.extendraidstatus:
                                    pvmresizepool(raiddev)
                                    del setting.extendraidstatus[raiddev]
                            #现在状态异常，不在RAIDERRLIST中或状态改变，正常->异常、异常->异常，加入列表并记录日志
                            if state in ['error','alert','recovery']:
                                if raidname not in setting.RAIDERRLIST or setting.RAIDERRLIST[raidname] != state:
                                    setting.RAIDERRLIST[raidname] = state
                                    #报警
                                    warningdata = {'target':'raid', 'op':state, 'level':warninglevel, 'params':{'name':raidname}}
                                    setting.WARNINGQUEUE.put(warningdata)
                                    #记录日志
                                    chlogsql = (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), msg['RaidLevel'], "Raid: %s %s" % (raidname, setting.CHRAIDERRSTATE[state]))
                                    enlogsql = (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), msg['RaidLevel'], "Raid: %s %s" % (raidname, state))
                                    allchlogsql.append(chlogsql)
                                    allenlogsql.append(enlogsql)
                            #写入数据看库
                            if allchlogsql:
                                chsql = "insert into chmonitorlog(Time,level,Event) values(%s,%s,%s)"
                                database.insertDB(chsql,allchlogsql)
                            if allenlogsql:
                                ensql = "insert into enmonitorlog(Time,level,Event) values(%s,%s,%s)"
                                database.insertDB(ensql,allenlogsql)
                    #更新RAID数据库
                    if allsql:
                        database.updateTB(allsql)
                    #更新SNMP
                    setting.UPDATESNMPQUEUE.put('raid')
                    #删除fail磁盘
                    setting.FAILDISKQUEUE.put(1)
                    #告诉界面更新
                    setting.putchange()
            except:
                debug.write_debug(debug.LINE(),"updateraidmsgthreadclass")
            time.sleep(10)
