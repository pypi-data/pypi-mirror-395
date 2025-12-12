#!/usr/bin/env python3
#
##################################################################################
#
#     Title : dsquasar
#    Author : Zaihua Ji, zji@ucar.edu
#      Date : 12/21/2020
#             2025-02-05 transferred to package rda_python_dsquasar from
#             https://github.com/NCAR/rda-utility-programs.git
#   Purpose : check Backup flags set in dataset.backflag and/or dsgroup.backflag of RDADB
#             to gather Web and Saved bfiles, tar them into larger (> 2GB) bfiles, and
#             back them up onto Quasar Backup Servers, at the Globus end points of
#             NCAR GDEX Quasar and/or NCAR GDEX Quasar Drdata, for Backup and/or
#             desaster recovery copies, respectively. The file tarring and backing up
#             processes are completed in utility program dsarch.
#
#    Github : https://github.com/NCAR/rda-python-dsquasar.git
#
##################################################################################
#
import os
import re
import sys
import time
from os import path as op
from time import time as tm
from rda_python_common import PgLOG
from rda_python_common import PgSIG
from rda_python_common import PgCMD
from rda_python_common import PgUtil
from rda_python_common import PgFile
from rda_python_common import PgLock
from rda_python_common import PgDBI
from rda_python_common import PgSplit

BACKMSG = {
   'B' : "Quasar Backup",
   'D' : "Quasar Backup&Drdata"
}

CINACT = 1   # create dsarch input Save/Web file lists and add backup file records
TARACT = 2   # build tarfiles (>=TARSIZE each tarfile) from the Saved/Web files in input files
CTACTS = 3   # 1|2
BCKACT = 4   # transfer multiple tarfiles (>=BCKSIZE each transfer) to Quasar backup/drdata 
TBACTS = 6   # 2|4
CBACTS = 7   # 1|2|4
CHKACT = 8   # check file sizes between db and quasar, and set status to N if different
STTACT = 16  # Check all files, backed up and ready to be backed up; and dump statistics
NBACTS = 25  # 1|8|16
PTHACT = 32  # hidden action to add leading Path Gnnn to backup files with filenames only
IDSACT = 64  # hidden action to add dsids string to bfile records for addtional dsids
MCSACT = 128  # hidden action to add MD5 checksum string to note fields of bfile records 

DSCNT = 65
DSTEP = 1000
LOGACT = PgLOG.LOGWRN
ERRACT = PgLOG.LOGERR
DTLACT = PgLOG.LOGWRN
INDENT = ''

ACTMSG = {
   CINACT : 'Create Input files',
   TARACT : 'Tar Backup files',
   CTACTS : 'Create Input&Tar backup Files',
   BCKACT : 'Transfer Globus Files',
   TBACTS : 'Tar Backup&Transfer Globus Files',
   CBACTS : 'Create Input&Tar backup&Transfer Globus Files',
   CHKACT : 'Check Backup Files',
   STTACT : 'Dump Backup Statistics',
# uncomment only as need
#   PTHACT : 'Add Gnnn Paths'
#   IDSACT : 'Add dsids Strings'
   MCSACT : 'Add MD5 CheckSum Strings'
}

BSTATS = {
   'N' : 'Input Files',
   'T' : 'Tarred Files',
   'A' : 'Backed up Files'
}

SOPT = 1
WOPT = 2
ORDERS = {}    # cache current order number for each dsid
BFILES = {}    # cache current order number for each dsid
BCKSIZE = 90*PgLOG.PGLOG['ONEGBS']  # 90GB, dsglobus transfer size
TARSIZE = 5*PgLOG.PGLOG['ONEGBS']   # 5GB, tarfile size limit
MINSIZE = PgLOG.PGLOG['TWOGBS']     # 2GB, minimal tarfile size
ONESIZE = 20*PgLOG.PGLOG['ONEGBS']  # 20GB, minimal file size to tar a single file 
TFCOUNT = 100          # if file count is greater, use MINSIZE for tar file
SUBLMTS = 2000        # file count limit for a sub-group

PGBACK = {
   'workdir' : "{}/{}/quasar_backup".format(PgLOG.PGLOG['GDEXWORK'], PgLOG.PGLOG['GDEXUSER']),
   'mproc' : 1,
   'action' : CTACTS,
   'chgdays' : 0,
   'backflag' : None,
   'actmsg' : None,
   'pstep' : 0,       # record progress step for under dscheck control
   'errcnt' : 0,
   'bckcnt' : 0,
   'maxcnt' : 10,
   'dolock' : 1,
   'doemail' : 0,
   'cmd'  : None
}

#
# main function to excecute this script
#
def main():

   global LOGACT, INDENT, ERRACT, DTLACT
   PgLOG.PGLOG['LOGFILE'] = "dsquasar.log"   # set different log file
   PgDBI.dssdb_dbname()
   bopts = option = None
   dsids = []
   sopts = {'n' : 0, 'u' : 0, 'a' : 0, 'e' : 0, 'E' : 0}  
   fcnt = 0
   argv = sys.argv[1:]
   for arg in argv:
      ms = re.match(r'^-(a|b|c|d|e|E|l|m|n|t|u|A|B|D)$', arg)
      if ms:
         arg = ms.group(1)
         if  arg == 'b':
            PgLOG.PGLOG['BCKGRND'] = 1   # processing in backgroup mode
         elif arg in sopts:
            sopts[arg] = 1
            option = None
         elif 'Acdlmt'.find(arg) > -1:
            option = arg
            if arg == 'd': bopts = []
         elif 'BD'.find(arg) > -1:
            if PGBACK['backflag']: PgLOG.pglog("-{}: Backup Flag is set to {} already".format(arg, PGBACK['backflag']), PgLOG.LGEREX)
            PGBACK['backflag'] = arg
      elif option:
         if option == 'd':
            bopts.append(arg)
         elif option == 'c':
            PGBACK['chgdays'] = int(arg)
            if PGBACK['chgdays'] < 1: PgLOG.pglog(arg +": Change Days(-c) must be > 0", PgLOG.LGWNEX)
            option = None
         elif option == 'm':
            PGBACK['mproc'] = int(arg)
            if PGBACK['mproc'] < 1: PgLOG.pglog(arg +": Multiple Processes(-m) must be > 0", PgLOG.LGWNEX)
            option = None
         elif option == 'A':
            PGBACK['action'] = int(arg)
            if PGBACK['action'] not in ACTMSG:
               PgLOG.pglog(arg + ": Invalid Action(-A) value", PgLOG.LGWNEX)
            option = None
         elif option == 'l':
            if not (arg == 'Y' or arg == 'N'): PgLOG.pglog(arg +": Lock Flag(-l) must be Y or N", PgLOG.LGWNEX)
            PGBACK['dolock'] = 1 if arg == 'Y' else 0
            option = None
         else:
            add_to_dsids(arg, dsids)
      else:
         PgLOG.pglog(arg + ": Value without leading option", PgLOG.LGWNEX)

   if not (sopts['a'] or dsids):
      print("dsquasar [-b] [(-a|-t DatasetIDs)] [-c ChangeDays] [-(e|E)] [-(B|D)] [-A ActionBits] \\")
      print("         [-l (Y|N)] [-m ProcessCount] [-n] [-u] [-d [HostName] [TryCount]")
      print("  Option -a - gather files of all datasets for Quasar Backup, or")
      print("  Option -t - specify dataset IDs to backup files, wildcard % is allowed")
      print("  Option -b - turn the background mode on; no screen display")
      print("  Option -c - change days to work with option -A 1 to rebackup changed files")
      print("  Option -d - turn the delay mode on for running as a batch job")
      print("  Option -e - send an email to specialist for statistics")
      print("  Option -E - send an email to specialist for detail statistics")
      print("  Option -B - Quasar Backup only for the provided datasets, or")
      print("  Option -D - Quasar Backup&Drdata; default to both B & D")
      print("  Option -A - Action bits, 1 - create dsarch input files; 2 - build tarfiles;")
      print("              4 - Transfer Quasar backup files; 8 - Check Backup Files;")
      print("              16 - Dump Backup Statistics; default to 3 for 1+2 actions,")
      print("              and the valid values are 1,2,3,4,6,7,8,16")
      print("  Option -l - flag to check&lock dataset before backup processes, defaults to Y")
      print("  Option -m - number of concurrent processes, defaults to 1")
      print("  Option -n - gather and show the available file counts with no backup actions")
      print("  Option -u - to clean up backup locks for provided dataset IDs")
      sys.exit(0)

   PGBACK['cmd'] = "dsquasar {}".format(' '.join(argv))
   PgLOG.cmdlog(PGBACK['cmd'])

   if sopts['u']:
      if sopts['a']: PgLOG.pglog("-u: Dataset IDs must be provided to Unlock datasets", PgLOG.LOGWRN)
      unlock_datasets(dsids)
      sys.exit(0)

   if sopts['a'] and dsids: PgLOG.pglog("-a: Option is ignored for dataset IDs provided", PgLOG.LOGWRN)
   PgFile.change_local_directory(PGBACK['workdir'], PgLOG.LGEREX)

   if sopts['e'] or sopts['E']:
      PGBACK['doemail'] = 1
      LOGACT = PgLOG.LGWNEM
      ERRACT = PgLOG.EMEROL
      INDENT = '  '
      if sopts['E']:
         DTLACT = PgLOG.LGWNEM
         PgLOG.PGLOG['EMLMAX'] = 1024

   dstart = 0 if sopts['n'] else 1
   acts = PGBACK['action']
   if acts&CHKACT:
      check_backup_action(bopts, dsids, dstart)
   elif acts&STTACT:
      dump_statistics_action(bopts, dsids)
   elif acts&PTHACT:
      add_path_action(bopts, dsids, dstart)
   elif acts&IDSACT:
      add_dsids_action(bopts, dsids, dstart)
   elif acts&MCSACT:
      add_checksum_action(bopts, dsids, dstart)
   else:
      if acts&BCKACT: dstart = globus_transfer_action(bopts, dsids, dstart)
      if acts&TARACT: dstart = build_tarfile_action(bopts, dsids, dstart)
      if acts&CINACT: dstart = create_infile_action(bopts, dsids, dstart)
      if dstart and acts&TBACTS == TBACTS: globus_transfer_action(bopts, dsids, dstart)

   if PGBACK['doemail']:
      amsg = ACTMSG[PGBACK['action']]
      bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup'
      dcnt = len(dsids)
      dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt if dcnt > 1 else 'All')
      PgLOG.set_email("{}: {} for {} Files of {}!".format(PGBACK['cmd'], amsg, bmsg, dmsg), PgLOG.EMLTOP)
      title = "dsquasar: " + amsg
      if PGBACK['bckcnt']: title += "({})".format(PGBACK['bckcnt'])
      if PGBACK['errcnt']: title += " Error({})".format(PGBACK['errcnt'])
      if PgLOG.PGLOG['DSCHECK']:
         tbl = "dscheck"
         cnd = "cindex = {}".format(PgLOG.PGLOG['DSCHECK']['cindex'])
         PgDBI.build_customized_email(tbl, "einfo", cnd, title, PgLOG.LOGWRN)
      else:
         PgLOG.pglog(title, PgLOG.LOGWRN|PgLOG.SNDEML)

   if PGBACK['pstep']: PgCMD.record_dscheck_status("D")
   PgLOG.cmdlog()
   PgLOG.pgexit(0)

#
# add given dsid to dsids; expand it if wildcard dsid is given
#
def add_to_dsids(dsid, dsids):

   if dsid.find('%') > -1:
      pgrecs = PgDBI.pgmget('dataset', 'dsid', "dsid LIKE '{}'".format(dsid))
      if pgrecs:
         for dsid in pgrecs['dsid']:
            if dsid not in dsids: dsids.append(dsid)
   else:
      dsid = PgUtil.format_dataset_id(dsid)
      if dsid not in dsids: dsids.append(dsid)

#
# Check backup and file information and dump the backup statistics#
def dump_statistics_action(bopts, dsids):

   start_dsquasar_none_daemon(bopts, dsids, STTACT)

   # files ready to be backed up
   dsfiles = {'B' : {}, 'D' : {}}
   gather_dataset_files(dsfiles, dsids, False)
   dump_dataset_files(dsfiles, 'B')
   dump_dataset_files(dsfiles, 'D')
   if PGBACK['chgdays']: return   # no further checking

   # changed GDEX files ready to be backed up
   PGBACK['chgdays'] = 1
   dsfiles = {'B' : {}, 'D' : {}}
   gather_dataset_files(dsfiles, dsids, False)
   dump_dataset_files(dsfiles, 'B')
   dump_dataset_files(dsfiles, 'D')
   PGBACK['chgdays'] = 0

   # files are in input files but not tarred yet
   dsfiles = {'B' : {}, 'D' : {}}
   gather_dataset_infiles(dsfiles, dsids)
   dump_dataset_infiles(dsfiles, 'B')
   dump_dataset_infiles(dsfiles, 'D')

   # files are tarred but not backed up yet
   dsfiles = {'B' : {}, 'D' : {}}
   gather_dataset_tarfiles(dsfiles, dsids)
   dump_dataset_tarfiles(dsfiles, 'B')
   dump_dataset_tarfiles(dsfiles, 'D')

   # files backed up (including the ones got moved and deleted after backup)
   dsfiles = {'B' : {}, 'D' : {}}
   gather_dataset_bckfiles(dsfiles, dsids)
   dump_dataset_bckfiles(dsfiles, 'B')
   dump_dataset_bckfiles(dsfiles, 'D')

#
# Check the file sizes between db and backup servers, and set status to 'N' if different
#
def check_backup_action(bopts, dsids, dstart):

   dsfiles = {'B' : {}, 'D' : {}}
   fcnt = gather_dataset_bckfiles(dsfiles, dsids, False)
   if fcnt and dstart:
      start_dsquasar_none_daemon(bopts, dsids, CHKACT, fcnt)
      process_dataset_chkfiles(dsfiles, 'B')
      process_dataset_chkfiles(dsfiles, 'D')

#
# add Gnnn paths to old bfiles without ones
#
def add_path_action(bopts, dsids, dstart):

   dsfiles = {'B' : {}, 'D' : {}}
   fcnt = gather_dataset_pathfiles(dsfiles, dsids)
   if fcnt and dstart:
      start_dsquasar_none_daemon(bopts, dsids, PTHACT, fcnt)
      process_dataset_pathfiles(dsfiles, 'B')
      process_dataset_pathfiles(dsfiles, 'D')

#
# add dsids to old bfiles without ones
#
def add_dsids_action(bopts, dsids, dstart):

   dsfiles = {'B' : {}, 'D' : {}}
   fcnt = gather_dataset_dsidfiles(dsfiles, dsids)
   if fcnt and dstart:
      start_dsquasar_none_daemon(bopts, dsids, IDSACT, fcnt)
      process_dataset_dsidfiles(dsfiles, 'B')
      process_dataset_dsidfiles(dsfiles, 'D')

#
# add md5 checksums to old bfiles which miss the checksums in note field
#
def add_checksum_action(bopts, dsids, dstart):

   dsfiles = {'B' : {}, 'D' : {}}
   fcnt = gather_dataset_mcsfiles(dsfiles, dsids)
   if fcnt and dstart:
      start_dsquasar_none_daemon(bopts, dsids, MCSACT, fcnt)
      process_dataset_mcsfiles(dsfiles, 'B')
      process_dataset_mcsfiles(dsfiles, 'D')

#
# check available GDEX files to create input files
#
def create_infile_action(bopts, dsids, dstart):

   if dstart > 0: dstart = start_dsquasar_none_daemon(bopts, dsids, CINACT)

   dsfiles = {'B' : {}, 'D' : {}}
   fcnt = gather_dataset_files(dsfiles, dsids)
   if fcnt and dstart:
      backup_dataset_files(dsfiles, 'B')
      backup_dataset_files(dsfiles, 'D')

   return dstart

#
# check input files and build tar files
#
def build_tarfile_action(bopts, dsids, dstart):

   dsfiles = {'B' : {}, 'D' : {}}
   fcnt = gather_dataset_infiles(dsfiles, dsids)
   if fcnt and dstart:
      if dstart > 0: dstart = start_dsquasar_none_daemon(bopts, dsids, TARACT, fcnt)
      backup_dataset_infiles(dsfiles, 'B')
      backup_dataset_infiles(dsfiles, 'D')

   return dstart

#
# gather and transfer tar files to Globus Quasar Servers
#
def globus_transfer_action(bopts, dsids, dstart):

   dsfiles = {'B' : {}, 'D' : {}}
   fcnt = gather_dataset_tarfiles(dsfiles, dsids)
   if fcnt and dstart:
      if dstart > 0: dstart = start_dsquasar_none_daemon(bopts, dsids, BCKACT, fcnt)
      backup_dataset_tarfiles(dsfiles, 'B')
      backup_dataset_tarfiles(dsfiles, 'D')

   return dstart

#
# start none daemon and intialize dscheck counts
#
def start_dsquasar_none_daemon(bopts, dsids, act, fcnt = 0):

   acts = PGBACK['action']
   if bopts != None:
      dsid = dsids[0] if len(dsids) == 1 else ''
      if not re.match(r'^[a-z]\d{6}$', dsid): dsid = ''
      cact = ('A' if acts < 10 else '') + str(acts)
      if act == STTACT or acts&NBACTS != acts:
         PgCMD.set_one_boption('qoptions', '-l walltime=24:00:00', 1)
      PgCMD.init_dscheck(0, '', "dsquasar", dsid, cact, PGBACK['workdir'],
                         PgLOG.PGLOG['CURUID'], bopts, PgLOG.LOGWRN)
      if PGBACK['mproc'] > 1: PGBACK['mproc'] = 1
   elif PGBACK['mproc'] > 1 and acts&NBACTS == acts:
      PGBACK['mproc'] = 1

   PgSIG.start_none_daemon('dsquasar', '', PgLOG.PGLOG['CURUID'], PGBACK['mproc'], 60, 1)

   if PgLOG.PGLOG['DSCHECK']:
      if act == STTACT:
         fcnt = gather_dataset_bckfiles(None, dsids, False)
      elif act == BCKACT:
         if acts&TARACT: fcnt += 2*gather_dataset_infiles(None, dsids)
         if acts&CINACT: fcnt += 2*gather_dataset_files(None, dsids)
      else:
         if act == CINACT or act == TARACT and acts&CINACT:
            fcnt += gather_dataset_files(None, dsids)
         if acts&BCKACT: fcnt *= 2
      PgCMD.set_dscheck_fcount(fcnt, PgLOG.LGEREX)
      PgCMD.set_dscheck_dcount(0, 0, PgLOG.LGEREX)
      mstep = 100 if acts&NBACTS else 10
      pstep = int(fcnt/100)
      if pstep > mstep:
         pstep = mstep
      elif pstep < 2:
         pstep = 2
      PGBACK['pstep'] = PGBACK['pcnt'] = pstep
      PGBACK['dcnt'] = PGBACK['dsize'] = 0

   return -1

#
# set the progress counts for dscheck controlled actions
#
def set_dsquasar_progress(fcnt, fsize):

   PGBACK['dcnt'] += fcnt
   PGBACK['dsize'] += fsize
   if PGBACK['dcnt'] >= PGBACK['pcnt']:
      PgCMD.set_dscheck_dcount(PGBACK['dcnt'], PGBACK['dsize'], PgLOG.LGEREX)
      PGBACK['pcnt'] = PGBACK['dcnt'] + PGBACK['pstep']

#
# unlock locked datset for given dataset IDs
#
def unlock_datasets(dsids):

   acnt = len(dsids)
   s = 's' if acnt > 1 else ''
   PgLOG.pglog("Unlock {} Dataset{} ...".format(acnt, s), PgLOG.WARNLG)
   mcnt = 0
   for dsid in dsids:
      pgrec = PgDBI.pgget("dataset", "pid, lockhost", "dsid = '{}'".format(dsid), PgLOG.LGEREX)
      if not pgrec:
         PgLOG.pglog(dsid + ": Not exists", PgLOG.LOGERR)
      elif not pgrec['pid']:
         PgLOG.pglog(dsid + ": Not locked", PgLOG.LOGWRN)
      elif PgLock.lock_dataset(dsid, -1, PgLOG.LGEREX) > 0:
         mcnt += 1
         PgLOG.pglog("{}: Unlocked {}/{}".format(dsid, pgrec['pid'], pgrec['lockhost']), PgLOG.LOGWRN)
      elif(PgFile.check_host_down(None, pgrec['lockhost']) and
           PgLock.lock_dataset(dsid, -2, PgLOG.LGEREX) > 0):
         mcnt += 1
         PgLOG.pglog("{}: Force unlocked {}/{}".format(dsid, pgrec['pid'], pgrec['lockhost']), PgLOG.LOGWRN)
      else:
         PgLOG.pglog("{}: Unable to unlock {}/{}".format(dsid, pgrec['pid'], pgrec['lockhost']), PgLOG.LOGWRN)

   if acnt > 1: PgLOG.pglog("{} of {} Dataset{} unlocked from RDADB".format(mcnt, acnt, s), PgLOG.LOGWRN)

#
# backup bfiles onto Quasar Backup and/or Drdata endpoints for given datasets
#
def backup_dataset_files(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   dcnt = len(bfiles)
   if not dcnt: return

   amsg = ACTMSG[PGBACK['action']&CTACTS]
   bmsg = BACKMSG[backflag]
   dmsg = list(bfiles)[0] if dcnt == 1 else "{} datasets".format(dcnt)
   PgLOG.pglog("{}: {} for {} ...".format(amsg, bmsg, dmsg), PgLOG.WARNLG)

   qinfo = {'backflag' : backflag, 'bid' : current_bid(), 'dsids' : [], 'fcnt' : 0,
            'size' : 0, 'infiles' : [], 'instr' : '', 'qdsids' : [],
            'dslocks' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}

   for dsid in bfiles:
      if len(qinfo['dsids']) == DSCNT: process_one_backup_file(qinfo, True, False)
      if PGBACK['dolock'] and dsid not in qinfo['dslocks']:
         if PgLock.lock_dataset(dsid, 1, PgLOG.LOGERR) < 1: continue
         qinfo['dslocks'].append(dsid)

      fcnt = bfiles[dsid]['scount']
      if fcnt > 0:
         process_backup_files(qinfo, dsid, fcnt, bfiles[dsid]['srecs'], 'S')

      fcnt = bfiles[dsid]['wcount']
      if fcnt > 0:
         process_backup_files(qinfo, dsid, fcnt, bfiles[dsid]['wrecs'], 'W')

      if qinfo['fcnt'] == 0:  # unlock dsid for dataset backup finished
         if dsid in qinfo['dslocks']:
            PgLock.lock_dataset(dsid, 0, PgLOG.LGEREX)
            qinfo['dslocks'].remove(dsid)
         qinfo['dsids'] = []

   if qinfo['dslocks']:
      for dsid in qinfo['dslocks']:
         PgLock.lock_dataset(dsid, 0, PgLOG.LGEREX)  # unlock the locked datasets

   cmsg = 'Changed ' if PGBACK['chgdays'] else ''
   qcnt = qinfo['qcnt']
   if qcnt > 0:
      PGBACK['bckcnt'] += qcnt
      s = 's' if qcnt > 1 else ''
      fcnt = qinfo['qfcnt']
      dcnt = len(qinfo['qdsids'])
      ssize = PgUtil.format_float_value(qinfo['qsize'])
      dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "file{} for {}({}) GDEX {}files of {}".format(s, fcnt, ssize, cmsg, dmsg)
      msg = "{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg)
      PgLOG.pglog(INDENT + msg, LOGACT)

   fcnt = qinfo['fcnt']
   if fcnt > 0:
      for infile in qinfo['infiles']: PgFile.delete_local_file(infile)
      s = 's' if fcnt > 1 else ''
      ssize = PgUtil.format_float_value(qinfo['size'])
      dsids = qinfo['dsids']
      dcnt = len(dsids)
      dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
      msg = "{}: {}({}) GDEX {}file{} of {} for next {}".format(amsg, fcnt, ssize, cmsg, s, dmsg, bmsg)
      PgLOG.pglog(INDENT + msg, LOGACT)

#
# get the current bid for adding bfile
#
def current_bid():

   pgrec = PgDBI.pgget("bfile", "max(bid) mid", '', PgLOG.LGEREX)
   return (pgrec['mid'] + 1) if pgrec else 1

#
# get the current disp_order for adding bfile
#
def display_order(dsid):

   if dsid not in ORDERS:
      pgrec = PgDBI.pgget('bfile', "max(disp_order) max_order", "dsid = '{}'".format(dsid), PgLOG.LGEREX)
      ORDERS[dsid] = pgrec['max_order'] if pgrec and pgrec['max_order'] else 0

   ORDERS[dsid] += 1
   return ORDERS[dsid]

#
# backup bfiles with input files set onto Quasar Backup and/or Drdata endpoints
#
def backup_dataset_infiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   amsg = ACTMSG[TARACT]
   bmsg = BACKMSG[backflag]
   s = 's' if bcnt > 1 else ''
   PgLOG.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), PgLOG.WARNLG)

   qinfo = {'backflag' : backflag, 'bid' : 0, 'dsids' : [], 'fcnt' : 0, 'size' : 0,
            'infiles' : [], 'instr' : '', 'qdsids' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}

   for dsid in bfiles:
      if PGBACK['dolock'] and PgLock.lock_dataset(dsid, 1, PgLOG.LOGERR) < 1: continue
      for bid in bfiles[dsid]:
         qinfo['bid'] = bid
         binfo = bfiles[dsid][bid]
         for bkey in binfo: qinfo[bkey] = binfo[bkey]
         process_one_backup_file(qinfo, False)
      if PGBACK['dolock']: PgLock.lock_dataset(dsid, 0, PgLOG.LOGERR)

   qcnt = qinfo['qcnt']
   if qcnt > 0:
      PGBACK['bckcnt'] += qcnt
      s = 's' if qcnt > 1 else ''
      fcnt = qinfo['qfcnt']
      dcnt = len(qinfo['qdsids'])
      ssize = PgUtil.format_float_value(qinfo['qsize'])
      dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "file{} for {}({}) GDEX files of {}".format(s, fcnt, ssize, dmsg)
      msg = "{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg)
      PgLOG.pglog(INDENT + msg, LOGACT)

#
# backup bfiles with tar files built onto Quasar Backup and/or Drdata endpoints
#
def backup_dataset_tarfiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   amsg = ACTMSG[BCKACT]
   bmsg = BACKMSG[backflag]
   s = 's' if bcnt > 1 else ''
   PgLOG.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), PgLOG.WARNLG)

   qinfo = {'backflag' : backflag, 'bids' : [], 'dsids' : [], 'fcnt' : 0, 'bcnt' : 0,
            'size' : 0, 'fromfiles' : [], 'tofiles' : [], 'qdsids' : [],
            'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}

   for bid in bfiles:
      binfo = bfiles[bid]
      for dsid in binfo['dsids']:
         if dsid not in qinfo['dsids']: qinfo['dsids'].append(dsid)
      qinfo['bcnt'] += 1
      qinfo['fcnt'] += binfo['fcnt']
      qinfo['size'] += binfo['size']
      qinfo['bids'].append(bid)
      qinfo['fromfiles'].append(binfo['fromfile'])
      qinfo['tofiles'].append(binfo['tofile'])
      if qinfo['size'] < BCKSIZE: continue
      transfer_quasar_tarfiles(qinfo)

   if qinfo['size'] > 0: transfer_quasar_tarfiles(qinfo)

   qcnt = qinfo['qcnt']
   if qcnt > 0:
      PGBACK['bckcnt'] += qcnt
      s = 's' if qcnt > 1 else ''
      fcnt = qinfo['qfcnt']
      dcnt = len(qinfo['qdsids'])
      ssize = PgUtil.format_float_value(qinfo['qsize'])
      dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "file{} for {}({}) GDEX files of {}".format(s, fcnt, ssize, dmsg)
      msg = "{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg)
      PgLOG.pglog(INDENT + msg, LOGACT)

#
# wait all child processes finish and then quit the main program
#
def quit_dsquasar(qinfo, msg = None):
   
   if PGBACK['mproc'] > 1: PgSIG.check_child(None, 0, PgLOG.LOGWRN, 1)

   if qinfo:
      if 'dslocks' in qinfo and qinfo['dslocks']:
         for dsid in qinfo['dslocks']: PgLock.lock_dataset(dsid, 0, PgLOG.LGEREX)
      qcnt = qinfo['qcnt']
      dcnt = len(qinfo['qdsids'])
      fcnt = qinfo['qfcnt']
      ssize = PgUtil.format_float_value(qinfo['qsize'])
      amsg = ACTMSG[PGBACK['action']]
      bmsg = BACKMSG[qinfo['backflag']]
      dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      msg = "Quit {}: {} {} files for {}({}) files of {}".format(amsg, qcnt, bmsg, fcnt, ssize, dmsg)
      PgLOG.pglog(msg, LOGACT)

   if PGBACK['doemail']:
      bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup'
      PgLOG.set_email("{}: Quit {} for {} Files of {}!".format(PGBACK['cmd'], amsg, bmsg, dmsg), PgLOG.EMLTOP)
      title = "dsquasar: Quit {} Error({})".format(amsg, PGBACK['errcnt'])
      if PgLOG.PGLOG['DSCHECK']:
         tbl = "dscheck"
         cnd = "cindex = {}".format(PgLOG.PGLOG['DSCHECK']['cindex'])
         PgDBI.build_customized_email(tbl, "einfo", cnd, title, PgLOG.LOGWRN)
      else:
         PgLOG.pglog(title, PgLOG.LOGWRN|PgLOG.SNDEML)

   if PGBACK['pstep']: PgCMD.record_dscheck_status("F")
   PgLOG.pgexit(0)

#
# backup one Quasar Backup or Backup&Drdata from one or multiple inputs and,
# reset the quasar backup dict
#
def process_one_backup_file(qinfo, addback, keepid = False):

   ccnt = PgSIG.check_child(None, 0, PgLOG.LOGWRN, -1) if PGBACK['mproc'] > 1 else 0
   if PgSIG.PGSIG['QUIT']: quit_dsquasar(qinfo)

   dsids = qinfo['dsids']
   dcnt = len(dsids)
   if dcnt == 0: return

   # prepare for backup one tar file
   dsid = dsids[0]
   fcnt = qinfo['fcnt']
   fsize = qinfo['size']
   bflg = qinfo['backflag']
   if addback:
      (bid, qfile) = add_backup_record(dsid, qinfo['bid'], bflg, dcnt, fcnt, fsize, dsids, qinfo['instr'])
   else:
      bid = qinfo['bid']
      qfile = qinfo['bfile']

   stat = 1
   if PGBACK['action'] > CINACT:
      s = 's' if fcnt > 1 else ''
      amsg = ACTMSG[PGBACK['action']&CTACTS]
      bmsg = BACKMSG[bflg]
      ssize = PgUtil.format_float_value(fsize)
      dmsg = dsid if dcnt == 1 else "{} datasets".format(dcnt)
      qmsg = "{}: Try {} {} file for {}({}) file{} of {}".format(amsg, qfile, bmsg, fcnt, ssize, s, dmsg)
      cmd = "dsarch {} AQ -QT {} -QF {} ".format(dsid, bflg, qfile)
      cmd += '-TO -OE -MD -IF ' + ' '.join(qinfo['infiles'])

      if ccnt > 0:
         stat = PgSIG.start_child("dsquasar_{}".format(bid), PgLOG.LOGWRN, 1)  # try to start a child process
         if stat <= 0:
            if PgSIG.PGSIG['QUIT']: quit_dsquasar(qinfo)
            sys.exit(1)   # something wrong
         elif PgSIG.PGSIG['PPID'] > 1:
            stat = PgLOG.pgsystem(cmd, ERRACT, 325)   # 256 + 64 + 4 + 1
            if stat:
               for infile in qinfo['infiles']: PgFile.delete_local_file(infile)
            elif re.search(r'file backed up to', PgLOG.PGLOG['SYSERR']):
               if PgDBI.pgdel('bfile', f"bid = {bid}"):
                  PgLOG.pglog(f"{dsid}-{qfile}: backup tarfile deleted for duplicattion", DTLACT)
               for infile in qinfo['infiles']: PgFile.delete_local_file(infile)
            sys.exit(0)  # stop child process
         else:
            PgDBI.pgdisconnect()  # disconnect database for reconnection
            PgLOG.pglog("Started a process for " + qmsg, PgLOG.LOGWRN)
      else:
         PgLOG.pglog(qmsg, PgLOG.LOGWRN)
         stat = PgLOG.pgsystem(cmd, ERRACT, 325)   # 256 + 64 + 4 + 1
         if stat:
            for infile in qinfo['infiles']: PgFile.delete_local_file(infile)
         elif re.search(r'file backed up to', PgLOG.PGLOG['SYSERR']):
            if PgDBI.pgdel('bfile', f"bid = {bid}"):
               PgLOG.pglog(f"{dsid}-{qfile}: backup tarfile deleted for duplicattion", DTLACT)
            for infile in qinfo['infiles']: PgFile.delete_local_file(infile)
         else:
            PGBACK['errcnt'] += 1
            if PGBACK['errcnt'] > PGBACK['maxcnt']: quit_dsquasar(qinfo)
            time.sleep(PgSIG.PGSIG['ETIME'])

   if stat:
      # reset qinfo after quasar backup
      qinfo['qcnt'] += 1
      qinfo['qfcnt'] += fcnt
      qinfo['qsize'] += fsize
      for dsid in dsids:
         if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)

   if addback:
      lastdsid = dsids.pop() if keepid else None         
      for dsid in dsids:  # unlock all datasets but the last one
         if dsid in qinfo['dslocks']:
            PgLock.lock_dataset(dsid, 0, PgLOG.LGEREX)
            qinfo['dslocks'].remove(dsid)
      qinfo['dsids'] = [lastdsid] if keepid else []
      qinfo['bid'] = bid + 1
      qinfo['fcnt'] = qinfo['size'] = 0
      qinfo['infiles'] = []
      qinfo['instr'] = ''

   if PGBACK['pstep']: set_dsquasar_progress((fcnt if PGBACK['action']&CINACT else 1), fsize)

#
# Transfer multiple tarfiles to Quasar Backup or Backup&Drdata, and
# reset the quasar backup dict
#
def transfer_quasar_tarfiles(qinfo):

   ccnt = PgSIG.check_child(None, 0, PgLOG.LOGWRN, -1) if PGBACK['mproc'] > 1 else 0
   if PgSIG.PGSIG['QUIT']: quit_dsquasar(qinfo)

   # prepare for backup one tar file
   dsids = qinfo['dsids']
   bids = qinfo['bids']
   tofiles = qinfo['tofiles']
   fromfiles = qinfo['fromfiles']
   dcnt = len(dsids)
   bcnt = qinfo['bcnt']
   fcnt = qinfo['fcnt']
   fsize = qinfo['size']
   bflg = qinfo['backflag']

   s = 's' if bcnt > 1 else ''
   amsg = ACTMSG[BCKACT]
   bmsg = BACKMSG[bflg]
   ssize = PgUtil.format_float_value(fsize)
   dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
   fmsg = "{}({}) {} file{} of {}".format(bcnt, ssize, bmsg, s, dmsg)
   qmsg = "{}: Try {}".format(amsg, fmsg)

   if ccnt > 0:
      stat = PgSIG.start_child("dsquasar_{}".format(bids[0]), PgLOG.LOGWRN, 1)  # try to start a child process
      if stat <= 0:
         if PgSIG.PGSIG['QUIT']: quit_dsquasar(qinfo)
         sys.exit(1)   # something wrong
      elif PgSIG.PGSIG['PPID'] <= 1:
         PgDBI.pgdisconnect()  # disconnect database for reconnection
         PgLOG.pglog("Started a process for " + qmsg, PgLOG.LOGWRN)
   else:
      PgLOG.pglog(qmsg, PgLOG.LOGWRN)

   dstat = bstat = -1
   if ccnt == 0 or PgSIG.PGSIG['PPID'] > 1:
      if bflg == 'D':
         dstat = PgFile.quasar_multiple_trasnfer(tofiles, fromfiles, 'gdex-quasar-drdata', 'gdex-glade', ERRACT)
         if not dstat: PgLOG.pglog("Error Quaser Drdata for " + fmsg, ERRACT|PgLOG.LOGERR)
      bstat = PgFile.quasar_multiple_trasnfer(tofiles, fromfiles, 'gdex-quasar', 'gdex-glade', ERRACT)
      if not dstat: PgLOG.pglog("Error Quaser Backup for " + fmsg, ERRACT|PgLOG.LOGERR)
      
      if dstat == PgLOG.FINISH: dstat = PgFile.check_globus_finished(tofiles[0], 'gdex-quasar-drdata', ERRACT|PgLOG.NOWAIT)
      if bstat == PgLOG.FINISH: bstat = PgFile.check_globus_finished(tofiles[0], 'gdex-quasar', ERRACT|PgLOG.NOWAIT)
      if dstat and bstat:
         for fromfile in fromfiles:
            tarfile = PgLOG.PGLOG['DSSDATA'] + fromfile
            PgFile.delete_local_file(tarfile, PgLOG.LGEREX)
         PgLOG.pglog("{} local tarfile{} removed".format(bcnt, s), DTLACT)
         for bid in qinfo['bids']:
            PgDBI.pgexec("UPDATE bfile SET status = 'A' WHERE bid = {}".format(bid), PgLOG.LGEREX)
         PgLOG.pglog("{} backup file{} updated".format(bcnt, s), DTLACT)
      else:
         PgLOG.pglog("Backup acion is not complete and {} local tarfile{} are not removed".format(bcnt, s), PgLOG.LOGERR)
         PGBACK['errcnt'] += 1
         if PGBACK['errcnt'] > PGBACK['maxcnt']: quit_dsquasar(qinfo)
         time.sleep(PgSIG.PGSIG['ETIME'])

   if PgSIG.PGSIG['PPID'] > 1: sys.exit(0)   # stop child process

   if dstat and bstat:
      # reset qinfo after quasar backup
      qinfo['qcnt'] += bcnt
      qinfo['qfcnt'] += fcnt
      qinfo['qsize'] += fsize
      for dsid in dsids:
         if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)

   qinfo['bcnt'] = qinfo['fcnt'] = qinfo['size'] = 0
   qinfo['bids'] = []
   qinfo['dsids'] = []
   qinfo['tofiles'] = []
   qinfo['fromfiles'] = []

   if PGBACK['pstep']: set_dsquasar_progress((fcnt if PGBACK['action']&CINACT else bcnt), fsize)

#
# add a backup file record as a place holder
#
def add_backup_record(dsid, bid, bflg, dcnt, fcnt, fsize, dsids, instr):

   dorder = display_order(dsid)
   subpath = 'G{:03}'.format(int((dorder+SUBLMTS-1)/SUBLMTS))
   cmsg = '_changed' if PGBACK['chgdays'] else ''
   bfile = "{}/{}_sn{}_dn{}_fn{}{}.tar".format(subpath, dsid, bid, dcnt, fcnt, cmsg)
   record = {'dsid' : dsid, 'bfile' : bfile, 'type' : bflg, 'status' : 'N',
             'disp_order' : dorder, 'data_size' : fsize,
             'dsids' : ','.join(dsids[1:]), 'note' : instr}
   nbid = 0
   while nbid != bid:
      nbid = PgDBI.pgadd('bfile', record, PgLOG.LOGERR|PgLOG.AUTOID)
      if not nbid:
         bid = current_bid()
         bfile = "{}/{}_sn{}_dn{}_fn{}{}.tar".format(subpath, dsid, bid, dcnt, fcnt, cmsg)
         record['bfile'] = bfile
      elif nbid != bid:
         bid = nbid
         bfile = "{}/{}_sn{}_dn{}_fn{}{}.tar".format(subpath, dsid, bid, dcnt, fcnt, cmsg)
         PgDBI.pgexec("UPDATE bfile SET bfile = '{}' WHERE bid = {}".format(bfile, bid), PgLOG.LGEREX)

   return (bid, bfile)

#
# open an input file and intialize the header for given dataset ID and file type
#
def open_input_file(qinfo, dsid, ftype):

   infile = "{}_{}_{}.txt".format(dsid, ftype, qinfo['bid'])
   instr = "DS<=>{}\n{}F<:>{}T<:>SZ<:>MC<:>\n".format(dsid, ftype, ftype)
   fd = open(infile, 'w')
   fd.write(instr)
   qinfo['instr'] += "<{}>\n{}".format(infile, instr)
   qinfo['infiles'].append(infile)

   return fd

#
# build input files and backup a quasar file if accumulated enough files (>= TARSIZE)
#
def process_backup_files(qinfo, dsid, fcnt, recs, filetype):

   if dsid not in qinfo['dsids']: qinfo['dsids'].append(dsid)
   fd = None
   fcate = filetype.lower()
   tname = fcate + 'file'
   for i in range(fcnt):
      pgrec = recs[i]
      if not evaluate_file_stat(dsid, fcate, pgrec): continue
      fname = pgrec[tname]
      fsize = pgrec['data_size']
      ftype = pgrec['type']
      fcksm = pgrec['checksum']
      qinfo['fcnt'] += 1
      qinfo['size'] += fsize
      instr = "{}<:>{}<:>{}<:>{}<:>\n".format(fname, ftype, fsize, fcksm)
      if not fd: fd = open_input_file(qinfo, dsid, filetype)
      fd.write(instr)
      qinfo['instr'] += instr
      if qinfo['fcnt'] == 1:
         if qinfo['size'] < ONESIZE: continue
      elif qinfo['fcnt'] < TFCOUNT:
         if qinfo['size'] < TARSIZE: continue
      else:
         if qinfo['size'] < MINSIZE: continue
      fd.close()
      fd = None
      process_one_backup_file(qinfo, True, (fcnt-i) > 1)
   if fd: fd.close()

#
# initialize dataset backup dict structure
#
def init_backup_dict():

   return {'wcount' : 0, 'wrecs' : [], 'scount' : 0, 'srecs' : []}

#
# get all files need to be backed up for a given dataset ID
#
def get_dataset_files(dsid, dsfiles, backflag, logact = 0):

   dcnd = "dsid = '{}'".format(dsid)
   fopt = get_backup_options(dsid, dcnd)
   if not fopt:
      if logact: PgLOG.pglog(dsid + ": No data file found to backup", logact)
      return 0

   infiles = cache_dataset_infiles(dsid)
   cnts = {'B' : [0, 0], 'D' : [0, 0]}  # [cnt, size]
   bfiles = {'B' : None, 'D' : None}
   flgset = 0 if backflag == 'N' else 1
   if dsfiles:
      bfiles['B'] = init_backup_dict()
      bfiles['D'] = init_backup_dict()
   validflags = (PGBACK['backflag'] if PGBACK['backflag'] else 'BD')

   backflags = {0 : backflag}
   gcnd = dcnd + " AND pindex = 0 ORDER BY gindex"
   pgrecs = PgDBI.pgmget('dsgroup', 'gindex, backflag', gcnd, PgLOG.LGWNEX)
   if pgrecs:
      # backflag set at group level, go through groups to get backup files
      gcnt = len(pgrecs['gindex'])
      for i in range(gcnt):
         bflg = pgrecs['backflag'][i]
         gidx = pgrecs['gindex'][i]
         if bflg == 'P':
            bflg = backflag
         elif bflg != 'N':
            flgset = 1
         backflags[gidx] = bflg

   for gidx in backflags:
      bflg = backflags[gidx] 
      if validflags.find(bflg) > -1:
         gcnd = "{}index = {}".format(('t' if gidx else 'g'), gidx) 
         bt = tm()
         rcnt = get_group_files(dsid, gcnd, dcnd, bfiles[bflg], fopt, infiles, cnts[bflg])
         dt = tm() - bt
         if rcnt > 1 and dt > 29:
            rmsg = PgLOG.seconds_to_string_time(dt)
            PgLOG.pglog("{}-G{}: Found {} Files ({})".format(dsid, gidx, rcnt, rmsg), PgLOG.LOGWRN)

   fcnt = cnts['B'][0] + cnts['D'][0]
   if dsfiles:
      cmsg = 'Changed ' if PGBACK['chgdays'] else ''
      for bflg in dsfiles:
         bcnt = cnts[bflg][0]
         if bcnt > 0:
            ssize = PgUtil.format_float_value(cnts[bflg][1])
            dsfiles[bflg][dsid] = bfiles[bflg]
            bmsg = BACKMSG[bflg]
            s = 's' if bcnt > 1 else ''
            PgLOG.pglog("{}: {}({}) {}file{} found for {}".format(dsid, bcnt, ssize, cmsg, s, bmsg), DTLACT)
   
      if fcnt == 0 and logact:
         msg = '' if flgset else ", must set Backup Flag 'B' or 'D'"
         PgLOG.pglog("{}: No {}file found to backup{}".format(dsid, cmsg, msg), DTLACT)

   return fcnt

#
# get web/saved files to backup for a given group condition and file option
#
def get_group_files(dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts):

   rcnt = 0
   if PGBACK['chgdays'] > 0:
      return get_group_changed_files(dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts)
   else:
      return get_group_new_files(dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts)

#
# get new web/saved files to backup for given dataset/group info
#
def get_group_new_files(dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts):

   rcnt = 0
   if fopt&SOPT:
      cnd = dcnd
      if gcnd: cnd += ' AND ' + gcnd
      cnd += ' AND bid = 0'
      rcnt += get_group_saved_files('sfile', '*', cnd, bfiles, infiles, cnts)

   if fopt&WOPT:
      cnd = "bid = 0"
      if gcnd: cnd = gcnd + ' AND ' + cnd
      rcnt += get_group_web_files(dsid, None, '*', cnd, bfiles, infiles, cnts)

   return rcnt

#
# get changed web/saved files to re-backup for given dataset/group info
#
def get_group_changed_files(dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts):

   rcnt = 0
   PgFile.file_backup_status(None)

   if fopt&SOPT:
      cnd = 'sfile.' + dcnd
      if gcnd: cnd += ' AND sfile.' + gcnd
      tables = 'sfile join bfile on sfile.bid = bfile.bid AND sfile.date_modified > bfile.date_modified'
      rcnt += get_group_saved_files(tables, "bfile.bfile, sfile.*", cnd, bfiles, infiles, cnts)

   if fopt&WOPT:
      cnd = 'wfile.' + gcnd if gcnd else ''
      tjoin = 'join bfile on wfile.bid = bfile.bid AND wfile.date_modified > bfile.date_modified'
      rcnt += get_group_web_files(dsid, tjoin, "bfile.bfile, wfile.*", cnd, bfiles, infiles, cnts)

   return rcnt

#
# get web data files for backup
#
def get_group_web_files(dsid, tjoin, fields, cnd, bfiles, infiles, cnts):

   rcnt = 0 
   chgdays = PGBACK['chgdays']
   ifiles = infiles['W'] if infiles and infiles['W'] else None
   if tjoin:
      pgrecs = PgSplit.pgmget_wfile_join(dsid, tjoin, fields, cnd, PgLOG.LGWNEX)
   else:
      pgrecs = PgSplit.pgmget_wfile(dsid, fields, cnd, PgLOG.LGWNEX)
   cnt = len(pgrecs['wid']) if pgrecs else 0

   for i in range(cnt):
      pgrec = PgUtil.onerecord(pgrecs, i)
      if chgdays and PgFile.file_backup_status(pgrec, chgdays) > 0: continue
      if ifiles and pgrec['wfile'] in ifiles: continue
      fsize = pgrec['data_size']
      if bfiles:
         bfiles['wrecs'].append(pgrec)
         bfiles['wcount'] += 1
      cnts[0] += 1
      cnts[1] += fsize
      rcnt += 1
   return rcnt

#
# get saved data files for backup
#
def get_group_saved_files(tables, fields, cnd, bfiles, infiles, cnts):

   rcnt = 0 
   chgdays = PGBACK['chgdays']
   ifiles = infiles['S'] if infiles and infiles['S'] else None
   pgrecs = PgDBI.pgmget(tables, fields, cnd, PgLOG.LGWNEX)
   cnt = len(pgrecs['sid']) if pgrecs else 0

   for i in range(cnt):
      pgrec = PgUtil.onerecord(pgrecs, i)
      if chgdays and PgFile.file_backup_status(pgrec, chgdays) > 0: continue
      if ifiles and pgrec['sfile'] in ifiles: continue
      fsize = pgrec['data_size']
      if bfiles:
         bfiles['srecs'].append(pgrec)
         bfiles['scount'] += 1
      cnts[0] += 1
      cnts[1] += fsize
      rcnt += 1
   return rcnt

#
# evaluate file stat on disk/object storage and modify RDADB record if not match
#
def evaluate_file_stat(dsid, cate, pgrec):

   tname = cate + 'file'
   fname = pgrec[tname]
   chome = PgLOG.PGLOG['DECSHOME'] if cate == 's' else PgLOG.PGLOG['DSDHOME']

   if pgrec['locflag'] == 'O':
      bucket = 'gdex-decsdata' if cate == 's' else PgLOG.PGLOC['OBJCTBKT']
      ofile = PgLOG.join_paths(dsid, fname)
      info = PgFile.check_object_file(ofile, bucket, 1, ERRACT)
      if not info: return False
      lfile = "{}/{}/{}/{}".format(chome, PgLOG.PGLOG['BACKUPEP'], dsid, fname)
      PgFile.object_copy_local(lfile, ofile, bucket, ERRACT)
      cinfo = PgFile.check_local_file(lfile, 32, ERRACT)
      if not cinfo: return False
      info['checksum'] = cinfo['checksum']
      lname = 'OBS'
   else:
      lfile = "{}/{}/".format(chome, dsid)
      if cate == 's': lfile += pgrec['type'] + '/'
      lfile += fname
      info = PgFile.check_local_file(lfile, 33, ERRACT)
      if not info: return False
      lname = 'DSK'

   record = {}      
   msg = ''
   checksum = info['checksum']
   if not pgrec['checksum']:
      msg = "Checksum misses"
      record['checksum'] = checksum
      pgrec['checksum'] = ''
   elif checksum != pgrec['checksum']:
      msg = "Checksum mismatch"
      record['checksum'] = checksum

   if info['data_size'] != pgrec['data_size']:
      if msg: msg += ", "
      msg += "Size mismatch"
      record['data_size'] = info['data_size']

   difftime = PgUtil.cmptime(info['date_modified'], info['time_modified'], pgrec['date_modified'], pgrec['time_modified'])
   if difftime < 0 or msg and difftime > 0:
      if msg: msg += ", "
      msg += "Timestamp mismatch"
      record['date_modified'] = info['date_modified'] 
      record['time_modified'] = info['time_modified']

   if msg:
      msg = "{}-{}-{}: {}".format(dsid, cate.upper(), fname, msg)
      msg += "\n{}:".format(lname)
      msg += "{}/{}/{}/{}".format(checksum, info['data_size'], info['date_modified'], info['time_modified'])
      msg += "\nDBS:"
      msg += "{}/{}/{}/{}".format(pgrec['checksum'], pgrec['data_size'], pgrec['date_modified'], pgrec['time_modified'])
      PgLOG.pglog(msg, LOGACT)
      cid = cate + 'id'
      fcnd = "{} = {}".format(cid, pgrec[cid])
      if cate == 'w':
         PgSplit.pgupdt_wfile(dsid, record, fcnd, PgLOG.LGWNEX)
      else:
         PgDBI.pgupdt(tname, record, fcnd, PgLOG.LGWNEX)
      for ckey in record:
         pgrec[ckey] = record[ckey]

   return True

#
# get file backing up options (1 for saved and 2 for web, and 3 for both types)
#
def get_backup_options(dsid, dcnd):

   fopt = 0
   bcnd = "= 0" if PGBACK['chgdays'] < 1 else "> 0"
#   if PgDBI.pgget('sfile', 'sid', "{} AND bid {}".format(dcnd, bcnd), PgLOG.LGWNEX): fopt |= SOPT
   if PgSplit.pgget_wfile(dsid, 'wid', "bid " + bcnd, PgLOG.LGWNEX): fopt |= WOPT

   return fopt

#
# gather all available dataset ids to backup data files
#
def gather_dataset_files(dsfiles, dsids, unlock = True):

   fcnt = 0
   if dsids:
      for dsid in dsids:
         dcnd = "dsid = '{}'".format(dsid)
         pgrec = PgDBI.pgget("dataset", "dsid, backflag, pid", dcnd, PgLOG.LGWNEX)
         if pgrec:
            if unlock and pgrec['pid'] and PgLock.lock_dataset(dsid, 0, LOGACT) < 1: continue
            fcnt += get_dataset_files(dsid, dsfiles, pgrec['backflag'], PgLOG.LOGWRN)
   else:
      dcnd = "ORDER BY dsid"
      pgrecs = PgDBI.pgmget("dataset", "dsid, backflag, pid", dcnd, PgLOG.LGWNEX)
      dcnt = len(pgrecs['dsid']) if pgrecs else 0
      for i in range(dcnt):
         dsid = pgrecs['dsid'][i]
         if unlock and pgrecs['pid'][i] and PgLock.lock_dataset(dsid, 0, LOGACT) < 1: continue
         fcnt += get_dataset_files(dsid, dsfiles, pgrecs['backflag'][i])

   if dsfiles:
      s = 's' if fcnt > 1 else ''
      bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup' 
      cmsg = 'Changed ' if PGBACK['chgdays'] else ''
      PgLOG.pglog("{} GDEX {}file{} found ready to {}".format(fcnt, cmsg, s, bmsg), LOGACT)

   return fcnt

#
# gather all available backup file records with status N to backup
#
def gather_dataset_infiles(dsfiles, dsids):

   icnt = fcnt = cnt = 0
   bcnd = "status = 'N'"
   ocnd = " ORDER BY dsid"
   flds = "bid, dsid, bfile, type, data_size size, (scount + wcount) fcnt, dsids, note"
   if PGBACK['backflag']: bcnd += " AND type = '{}'".format(PGBACK['backflag'])
   if dsids:
      for dsid in dsids:
         dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
         pgrecs = PgDBI.pgmget("bfile", flds, dcnd, PgLOG.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            cnt = get_backup_infile(dsfiles, PgUtil.onerecord(pgrecs, i))
            if cnt:
               icnt +=1
               fcnt += cnt
   else:
      pgrecs = PgDBI.pgmget("bfile", flds, bcnd+ocnd, PgLOG.LGWNEX)
      bcnt = len(pgrecs['bid']) if pgrecs else 0
      for i in range(bcnt):
         cnt = get_backup_infile(dsfiles, PgUtil.onerecord(pgrecs, i))
         if cnt:
            icnt +=1
            fcnt += cnt

   if dsfiles:
      s = 's' if icnt > 1 else ''
      bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup' 
      PgLOG.pglog("{} input file{} found ready to {}".format(icnt, s, bmsg), LOGACT)

   return fcnt

#
# gather all available backup file records with status T to backup
#
def gather_dataset_tarfiles(dsfiles, dsids):

   tcnt = fcnt = cnt = 0
   bcnd = "status = 'T'"
   ocnd = " ORDER BY dsid"
   flds = "bid, dsid, bfile, type, data_size size, (scount + wcount) fcnt, note"
   if PGBACK['backflag']: bcnd += " AND type = '{}'".format(PGBACK['backflag'])
   if dsids:
      for dsid in dsids:
         dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
         pgrecs = PgDBI.pgmget("bfile", flds, dcnd, PgLOG.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            cnt = get_backup_tarfile(dsfiles, PgUtil.onerecord(pgrecs, i))
            if cnt:
               tcnt +=1
               fcnt += cnt
   else:
      pgrecs = PgDBI.pgmget("bfile", flds, bcnd+ocnd, PgLOG.LGWNEX)
      bcnt = len(pgrecs['bid']) if pgrecs else 0
      for i in range(bcnt):
         cnt = get_backup_tarfile(dsfiles, PgUtil.onerecord(pgrecs, i))
         if cnt:
            tcnt +=1
            fcnt += cnt

   s = 's' if tcnt > 1 else ''
   bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup' 
   PgLOG.pglog("{} tarred file{} found ready to {}".format(tcnt, s, bmsg), LOGACT)

   return fcnt

#
# get a backup file with input files set for quasar backup
#
def get_backup_infile(dsfiles, pgrec):

   ret = 1
   bfile = pgrec['bfile']
   ms = re.search(r'([a-z]\d{6})_sn(\d+)_dn(\d+)_fn(\d+)', bfile)
   if ms:
      dsid = ms.group(1)
      bid = int(ms.group(2))
      dcnt = int(ms.group(3))
      fcnt = int(ms.group(4))
      if not (dsid == pgrec['dsid'] and bid == pgrec['bid']): return 0
   else:
      dsid = pgrec['dsid']
      bid = pgrec['bid']
      fcnt = pgrec['fcnt']
      dcnt = 0
   if PGBACK['action']&CINACT: ret = fcnt
   if not dsfiles: return ret

   dsids = [dsid]
#   if not (pgrec['note'] or rebuild_file_note(pgrec, dsids)): return 0
   if not pgrec['note']:
      return PgLOG.pglog(bfile + ": Miss note for N backup file", ERRACT)

   infiles = []
   flines = []
   fd = None
   lines = pgrec['note'].split("\n")
   for line in lines:
      ms = re.match(r'^<(([a-z]\d{6})_\S+\.txt)>', line)
      if ms:
         infile = ms.group(1)
         dsid = ms.group(2)
         if dsid not in dsids: dsids.append(dsid)
         infiles.append(infile)
         if fd:
            fd.write('\n'.join(flines))
            fd.close()
            flines = []
            fd = None
         if PGBACK['action']&CTACTS and not op.isfile(infile):
            fd = open(infile, 'w')
            PgLOG.pglog("{}: Recreate missing dsarch input file in {}".format(infile, PGBACK['workdir']), DTLACT)
      elif fd and not re.match(r'^>[A-Z]{2} ', line):
         flines.append(line)

   if not infiles: return 0
   if fd:
      fd.write('\n'.join(flines))
      fd.close()

   dsid = dsids[0]
   bflg = pgrec['type']
   size = pgrec['size']
   bfiles = dsfiles[bflg]
   if dsid not in bfiles: bfiles[dsid] = {}
   bfiles[dsid][bid] = {'bfile' : bfile, 'fcnt' : fcnt, 'size' : size, 'dsids' : dsids, 'infiles' : infiles}
   return ret

#
# get a tarred backup file for quasar backup
#
def get_backup_tarfile(dsfiles, pgrec):

   ret = 1
   bfile = pgrec['bfile']
   ms = re.search(r'([a-z]\d{6})_sn(\d+)_dn(\d+)_fn(\d+)', bfile)
   if ms:
      dsid = ms.group(1)
      bid = int(ms.group(2))
      dcnt = int(ms.group(3))
      fcnt = int(ms.group(4))
      if not (dsid == pgrec['dsid'] and bid == pgrec['bid']): return 0
   else: 
      dsid = pgrec['dsid']
      bid = pgrec['bid']
      fcnt = pgrec['fcnt']
      dcnt = 0
   if PGBACK['action']&CINACT: ret = fcnt
   if not dsfiles: return ret

   dsids = [dsid]
#   if not (pgrec['note'] or rebuild_file_note(pgrec, dsids)): return 0
   if not pgrec['note']:
      return PgLOG.pglog(bfile + ": Miss note for T backup file", ERRACT)

   ftype = None
   lines = pgrec['note'].split("\n")
   for line in lines:
      ms = re.match(r'^<([a-z]\d{6})_(\w)_\d+.txt>', line)
      if ms:
         dsid = ms.group(1)
         if not ftype: ftype = ms.group(2)
         if dsid not in dsids: dsids.append(dsid)
         if len(dsids) == dcnt: break
   if not ftype: return 0

   dsid = dsids[0]
   bflg = pgrec['type']
   fromfile = get_local_globus_file(ftype, bid, dsid, bfile, bflg)
   if not fromfile: return 0
   tofile = "/{}/{}".format(dsid, bfile)
   dsfiles[bflg][bid] = {'bfile' : bfile, 'fcnt' : fcnt, 'size' : pgrec['size'],
                         'dsids' : dsids, 'tofile' : tofile, 'fromfile' : fromfile}
   return ret

#
# build fromfile name at Globus endpoint gdex-glade
#
def get_local_globus_file(ftype, bid, dsid, bfile, backflag):
   
   endpath = 'decsdata' if ftype == 'S' else 'data'
   fromfile = "/{}/gdex-quasar/{}/{}".format(endpath, dsid, op.basename(bfile))
   tarfile = PgLOG.PGLOG['DSSDATA'] + fromfile

   if PGBACK['action'] == STTACT or PgFile.check_local_file(tarfile, 0, PgLOG.LGEREX): return fromfile

   amsg = ACTMSG[BCKACT]
   bmsg = BACKMSG[backflag]
   PgLOG.pglog("{}: Miss local {} file for {}\n{}: Change file status to 'N' to recreate".format(fromfile, bmsg, amsg, bfile), DTLACT)
   PgDBI.pgexec("UPDATE bfile SET status = 'N' WHERE bid = {}".format(bid), PgLOG.LGEREX)
   return None

#
# cache the Web/Saved files in type N bfiles (included in input files) already
#
def cache_dataset_infiles(dsid):

   incnd = "status = 'N' AND (dsid = '{}' or dsids LIKE '%{}%')".format(dsid, dsid)
   pgrecs = PgDBI.pgmget('bfile', 'note', incnd, PgLOG.LGEREX)
   if not pgrecs: return None

   bckfiles = {'S' : [], 'W' : []}
   cnts = {'S' : 0, 'W' : 0}
   for note in pgrecs['note']:
      lines = note.split("\n")
      lcnt = len(lines)
      l = 0
      ftype = None
      while l < lcnt:
         line = lines[l]
         l += 1
         ms = re.match(r'^<([a-z]\d{6})_(\w)_\d+\.txt>', line)
         if ms:
            ftype = None
            l += 2
            if ms.group(1) == dsid: ftype = ms.group(2)
         elif ftype:
            n = line.find('<:>')
            bckfiles[ftype].append(line[:n])
            cnts[ftype] += 1

   fcnt = cnts['S'] + cnts['W']
   if fcnt == 0: return None

   if PGBACK['action'] == CINACT:
      s = 's' if fcnt > 1 else ''
      amsg = ACTMSG[CINACT]
      PgLOG.pglog("{}-{}: Skip {}/{} Saved/Web file{} already listed in input files".format(dsid, amsg, cnts['S'], cnts['W'], s), DTLACT)

   return bckfiles

#
# process bfiles to check sizes between db and backup servers, set status to N if different
#
def process_dataset_chkfiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   amsg = ACTMSG[CHKACT]
   bmsg = BACKMSG[backflag]
   s = 's' if bcnt > 1 else ''
   PgLOG.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), PgLOG.WARNLG)

   qinfo = {'backflag' : backflag, 'bid' : 0, 'dsid' : None, 'size' : 0, 'bfile' : None,
            'bqfiles' : {}, 'dqfiles' : {}, 'qdsids' : [], 'qcnt' : 0, 'ncnt' : 0}

   for bid in bfiles:
      qinfo['bid'] = bid
      binfo = bfiles[bid]
      if qinfo['dsid'] and binfo['dsid'] != qinfo['dsid']:
         qinfo['bqfiles'] = {}
         qinfo['dqfiles'] = {}
      for bkey in binfo: qinfo[bkey] = binfo[bkey]
      process_one_quasar_chkfile(qinfo)

   qcnt = qinfo['qcnt']
   if qcnt > 0:
      s = 's' if qcnt > 1 else ''
      ncnt = qinfo['ncnt']
      dcnt = len(qinfo['qdsids'])
      dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "for {} of {} {} file{} of {}".format(ncnt, qcnt, bmsg, s, dmsg)
      PgLOG.pglog("{}: Set status to 'N' {}".format(amsg, fmsg), LOGACT)

#
# check sizes between db and backup servers for one backup file, set status to N if different
#
def process_one_quasar_chkfile(qinfo):

   if PgSIG.PGSIG['QUIT']: quit_dsquasar(qinfo)

   # prepare for backup one tar file
   dsid = qinfo['dsid']
   bid = qinfo['bid']
   dfile = qinfo['bfile']
   dpath = op.dirname(dfile)
   qpath = "/{}/{}".format(dsid, dpath)
   qfile = "/{}/{}".format(dsid, dfile)
   pfile = op.basename(dfile)
   dsize = qinfo['size']
   bflg = qinfo['backflag']
   amsg = ACTMSG[CHKACT]
   bmsg = BACKMSG[bflg]
   sdsize = PgUtil.format_float_value(dsize)
   logact = PgLOG.LGEREX
   qmsg = None
   if bflg == 'D':
      endpoint = PgFile.QPOINTS[bflg]
      qfiles = qinfo['dqfiles']
      if qpath not in qfiles: qfiles[qpath] = PgFile.backup_glob(qpath, endpoint, 0, logact)
      info = qfiles[qpath][pfile] if qfiles[qpath] and pfile in qfiles[qpath] else None
      if not info:
         qmsg = "{}: Miss {} file {}-{}".format(amsg, bmsg, endpoint, qfile)
      elif dsize != info['data_size']:
         sqsize = PgUtil.format_float_value(info['data_size'])
         qmsg = "{}: Miss-match {} files {}({})/{}-{}({})".format(amsg, bmsg, dfile, sdsize, endpoint, qfile, sqsize)
   if not qmsg:
      endpoint = PgFile.QPOINTS['B']
      qfiles = qinfo['bqfiles']
      if qpath not in qfiles: qfiles[qpath] = PgFile.backup_glob(qpath, endpoint, 0, logact)
      info = qfiles[qpath][pfile] if qfiles[qpath] and pfile in qfiles[qpath] else None
      if not info:
         qmsg = "{}: Miss {} file {}-{}".format(amsg, bmsg, endpoint, qfile)
      elif dsize != info['data_size']:
         sqsize = PgUtil.format_float_value(info['data_size'])
         qmsg = "{}: Miss-match {} files {}({})/{}-{}({})".format(amsg, bmsg, dfile, sdsize, endpoint, qfile, sqsize)

   if qmsg:
      PgLOG.pglog(qmsg, DTLACT)
      PgDBI.pgexec("UPDATE bfile SET status = 'N' WHERE bid = {}".format(bid), logact)
      qinfo['ncnt'] += 1

   # reset qinfo after quasar backup
   qinfo['qcnt'] += 1
   if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)

   if PGBACK['pstep']: set_dsquasar_progress(1, dsize)

#
# get all available backup files records for given datasets
#
def gather_dataset_bckfiles(dsfiles, dsids, getnote = True):

   bcnd = "status = 'A'"
   ocnd = " ORDER BY dsid"
   FLDS = ['dsid', 'size', 'bfile']
   flds = "bid, dsid, bfile, type, data_size size"
   if getnote:
      FLDS.append('fcnt')
      FLDS.append('note')
      flds += ", (scount + wcount) fcnt, note"
   if PGBACK['backflag']: bcnd += " AND type = '{}'".format(PGBACK['backflag'])
   if dsids:
      fcnt = 0
      for dsid in dsids:
         dcnd = "(dsid = '{}' OR dsids LIKE '%{}%') AND {}".format(dsid, dsid, bcnd)
         if dsfiles:
            pgrecs = PgDBI.pgmget("bfile", flds, dcnd, PgLOG.LGWNEX)
            bcnt = len(pgrecs['bid']) if pgrecs else 0
            for i in range(bcnt):
               pgrec = PgUtil.onerecord(pgrecs, i)
               type = pgrec['type']
               bid = pgrec['bid']
               if bid not in dsfiles[type]:
                  dsfiles[type][bid] = {fld : pgrec[fld] for fld in FLDS}
                  fcnt += 1
         else:
            fcnt += PgDBI.pgget("bfile", '', dcnd, PgLOG.LGWNEX)

   else:
      if dsfiles:
         pgrecs = PgDBI.pgmget("bfile", flds, bcnd+ocnd, PgLOG.LGWNEX)
         fcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(fcnt):
            pgrec = PgUtil.onerecord(pgrecs, i)
            dsfiles[pgrec['type']][pgrec['bid']] = {fld : pgrec[fld] for fld in FLDS}
      else:
         fcnt = PgDBI.pgget("bfile", '', bcnd, PgLOG.LGWNEX)

   if dsfiles:
      s = 's' if fcnt > 1 else ''
      amsg = ACTMSG[PGBACK['action']]
      bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup'
      PgLOG.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), LOGACT)

   return fcnt

#
# process bfiles to add leading Gnnn path onto Quasar Backup and/or Drdata endpoints
#
def process_dataset_pathfiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   amsg = ACTMSG[PTHACT]
   bmsg = BACKMSG[backflag]
   s = 's' if bcnt > 1 else ''
   PgLOG.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), PgLOG.WARNLG)

   qinfo = {'backflag' : backflag, 'bid' : 0, 'dsids' : [], 'fcnt' : 0, 'size' : 0,
            'bfile' : None, 'pfile' : None, 'qdsids' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}

   for bid in bfiles:
      qinfo['bid'] = bid
      binfo = bfiles[bid]
      for bkey in binfo: qinfo[bkey] = binfo[bkey]
      process_one_quasar_pathfile(qinfo)

   qcnt = qinfo['qcnt']
   if qcnt > 0:
      s = 's' if qcnt > 1 else ''
      fcnt = qinfo['qfcnt']
      dcnt = len(qinfo['qdsids'])
      ssize = PgUtil.format_float_value(qinfo['qsize'])
      dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "file{} for {}({}) files of {}".format(s, fcnt, ssize, dmsg)
      PgLOG.pglog("{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg), LOGACT)

#
# backup one Quasar Backup or Backup&Drdata from one or multiple inputs and,
# reset the quasar backup dict
#
def process_one_quasar_pathfile(qinfo):

   ccnt = PgSIG.check_child(None, 0, PgLOG.LOGWRN, -1) if PGBACK['mproc'] > 1 else 0
   if PgSIG.PGSIG['QUIT']: quit_dsquasar(qinfo)

   # prepare for backup one tar file
   dsids = qinfo['dsids']
   dsid = dsids[0]
   bid = qinfo['bid']
   qfile = qinfo['bfile']
   pfile = qinfo['pfile']
   fromfile = "/{}/{}".format(dsid, qfile)
   tofile = "/{}/{}".format(dsid, pfile)
   dcnt = len(dsids)
   fcnt = qinfo['fcnt']
   fsize = qinfo['size']
   bflg = qinfo['backflag']

   s = 's' if fcnt > 1 else ''
   amsg = ACTMSG[PTHACT]
   bmsg = BACKMSG[bflg]
   ssize = PgUtil.format_float_value(fsize)
   dmsg = dsid if dcnt == 1 else "{} datasets".format(dcnt)
   qmsg = "{}: Try {}, {} file for {}({}) file{} of {}".format(amsg, pfile, bmsg, fcnt, ssize, s, dmsg)

   if ccnt > 0:
      stat = PgSIG.start_child("dsquasar_{}".format(bid), PgLOG.LOGWRN, 1)  # try to start a child process
      if stat <= 0:
         if PgSIG.PGSIG['QUIT']: quit_dsquasar(qinfo)
         sys.exit(1)   # something wrong
      elif PgSIG.PGSIG['PPID'] <= 1:
         PgDBI.pgdisconnect()  # disconnect database for reconnection
         PgLOG.pglog("Started a process for " + qmsg, PgLOG.LOGWRN)
   else:
      PgLOG.pglog(qmsg, PgLOG.LOGWRN)

   logact = PgLOG.OVRIDE|PgLOG.LOGWRN
   bstat = dstat = -1
   if ccnt == 0 or PgSIG.PGSIG['PPID'] > 1:
      if bflg == 'D':
         dstat = PgFile.move_backup_file(tofile, fromfile, 'gdex-quasar-drdata', logact)
         if not dstat: PgLOG.pglog("Error Quaser Drdata for " + qmsg, PgLOG.LOGERR)
      bstat = PgFile.move_backup_file(tofile, fromfile, 'gdex-quasar', logact)
      if not bstat: PgLOG.pglog("Error Quaser Backup for " + qmsg, PgLOG.LOGERR)
   
      if dstat and bstat:
         PgDBI.pgexec("UPDATE bfile SET bfile = '{}' WHERE bid = {}".format(pfile, bid), PgLOG.LGEREX)
      else:
         PGBACK['errcnt'] += 1
         if PGBACK['errcnt'] > PGBACK['maxcnt']: quit_dsquasar(qinfo)
         time.sleep(PgSIG.PGSIG['ETIME'])

   if PgSIG.PGSIG['PPID'] > 1: sys.exit(0)   # stop child process

   if dstat and bstat:
      # reset qinfo after quasar backup
      qinfo['qcnt'] += 1
      qinfo['qfcnt'] += fcnt
      qinfo['qsize'] += fsize
      for dsid in dsids:
         if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)

   if PGBACK['pstep']: set_dsquasar_progress(1, fsize)

#
# get all available backup file records without leading paths
#
def gather_dataset_pathfiles(dsfiles, dsids):

   fcnt = 0
   bcnd = "status = 'A' AND bfile not LIKE 'G%/%.tar'"
   ocnd = " ORDER BY dsid"
   flds = "bid, dsid, bfile, type, data_size size, disp_order, (scount + wcount) fcnt, note"
   if PGBACK['backflag']: bcnd += " AND type = '{}'".format(PGBACK['backflag'])
   if dsids:
      for dsid in dsids:
         dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
         pgrecs = PgDBI.pgmget("bfile", flds, dcnd, PgLOG.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            fcnt += get_backup_pathfile(dsfiles, PgUtil.onerecord(pgrecs, i))
   else:
      pgrecs = PgDBI.pgmget("bfile", flds, bcnd+ocnd, PgLOG.LGWNEX)
      bcnt = len(pgrecs['bid']) if pgrecs else 0
      for i in range(bcnt):
         fcnt += get_backup_pathfile(dsfiles, PgUtil.onerecord(pgrecs, i))

   s = 's' if fcnt > 1 else ''
   amsg = ACTMSG[PTHACT]
   bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup'
   PgLOG.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), DTLACT)

   return fcnt

#
# get a archived file for adding Gnnn path
#
def get_backup_pathfile(dsfiles, pgrec):

   bfile = pgrec['bfile']
   ms = re.search(r'([a-z]\d{6})_sn(\d+)_dn(\d+)_fn(\d+)', bfile)
   if ms:
      dsid = ms.group(1)
      bid = int(ms.group(2))
      dcnt = int(ms.group(3))
      fcnt = int(ms.group(4))
      if not (dsid == pgrec['dsid'] and bid == pgrec['bid']): return 0
   else: 
      dsid = pgrec['dsid']
      bid = pgrec['bid']
      fcnt = pgrec['fcnt']
      dcnt = 0
   dsids = [dsid]
   if not pgrec['note']: return 0

   pfile = "G{:03}/{}".format(int((pgrec['disp_order']+SUBLMTS-1)/SUBLMTS), bfile)

   if dcnt == 0 or dcnt > len(dsids):
      lines = pgrec['note'].split("\n")
      for line in lines:
         ms = re.match(r'^DS<=>([a-z]\d{6})', line)
         if ms:
            dsid = ms.group(1)
            if dsid not in dsids:
               dsids.append(dsid)
               if dcnt == len(dsids): break

   bflg = pgrec['type']
   dsfiles[bflg][bid] = {'dsids' : dsids, 'fcnt' : fcnt, 'size' : pgrec['size'], 'bfile' : bfile, 'pfile' : pfile}
   return 1

#
# process bfile records to add dsids string
#
def process_dataset_dsidfiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   amsg = ACTMSG[IDSACT]
   bmsg = BACKMSG[backflag]
   s = 's' if bcnt > 1 else ''
   PgLOG.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), PgLOG.WARNLG)

   qinfo = {'backflag' : backflag, 'bid' : 0, 'dsids' : [], 'fcnt' : 0, 'size' : 0,
            'qdsids' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}

   for bid in bfiles:
      qinfo['bid'] = bid
      binfo = bfiles[bid]
      for bkey in binfo: qinfo[bkey] = binfo[bkey]
      process_one_quasar_dsidfile(qinfo)

   qcnt = qinfo['qcnt']
   if qcnt > 0:
      s = 's' if qcnt > 1 else ''
      fcnt = qinfo['qfcnt']
      dcnt = len(qinfo['qdsids'])
      ssize = PgUtil.format_float_value(qinfo['qsize'])
      dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "file{} for {}({}) files of {}".format(s, fcnt, ssize, dmsg)
      PgLOG.pglog("{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg), LOGACT)

#
# add dsids string to a quasar backup file record
#
def process_one_quasar_dsidfile(qinfo):

   dsids = qinfo['dsids']
   bid = qinfo['bid']
   fcnt = qinfo['fcnt']
   fsize = qinfo['size']

   dsstr = ','.join(dsids[1:])
   stat = PgDBI.pgexec("UPDATE bfile SET dsids = '{}' WHERE bid = {}".format(dsstr, bid), PgLOG.LGEREX)

   if stat:
      # reset qinfo after quasar backup
      qinfo['qcnt'] += 1
      qinfo['qfcnt'] += fcnt
      qinfo['qsize'] += fsize
      for dsid in dsids:
         if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)

   if PGBACK['pstep']: set_dsquasar_progress(1, fsize)

#
# get all available backup file records without NULL dsids
#
def gather_dataset_dsidfiles(dsfiles, dsids):

   fcnt = 0
   bcnd = "status = 'A' AND dsids IS NULL"
   ocnd = " ORDER BY dsid"
   flds = "bid, dsid, bfile, type, data_size size , disp_order, (scount + wcount) fcnt, note"
   if PGBACK['backflag']: bcnd += " AND type = '{}'".format(PGBACK['backflag'])
   if dsids:
      for dsid in dsids:
         dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
         pgrecs = PgDBI.pgmget("bfile", flds, dcnd, PgLOG.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            fcnt += get_backup_dsidfile(dsfiles, PgUtil.onerecord(pgrecs, i))
   else:
      pgrecs = PgDBI.pgmget("bfile", flds, bcnd+ocnd, PgLOG.LGWNEX)
      bcnt = len(pgrecs['bid']) if pgrecs else 0
      for i in range(bcnt):
         fcnt += get_backup_dsidfile(dsfiles, PgUtil.onerecord(pgrecs, i))

   s = 's' if fcnt > 1 else ''
   amsg = ACTMSG[IDSACT]
   bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup'
   PgLOG.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), DTLACT)

   return fcnt

#
# get a archived file for adding dsids
#
def get_backup_dsidfile(dsfiles, pgrec):

   bfile = pgrec['bfile']
   ms = re.search(r'([a-z]\d{6})_sn(\d+)_dn(\d+)_fn(\d+)', bfile)
   if ms:
      dsid = ms.group(1)
      bid = int(ms.group(2))
      dcnt = int(ms.group(3))
      fcnt = int(ms.group(4))
      if not (dsid == pgrec['dsid'] and bid == pgrec['bid']): return 0
   else: 
      dsid = pgrec['dsid']
      bid = pgrec['bid']
      fcnt = pgrec['fcnt']
      dcnt = 0

   dsids = [dsid]
   if not pgrec['note']: return 0

   if dcnt == 0 or dcnt > len(dsids):
      lines = pgrec['note'].split("\n")
      for line in lines:
         ms = re.match(r'^DS<=>([a-z]\d{6})', line)
         if ms:
            dsid = ms.group(1)
            if dsid not in dsids:
               dsids.append(dsid)
               if dcnt == len(dsids): break

   bflg = pgrec['type']
   dsfiles[bflg][bid] = {'dsids' : dsids, 'fcnt' : fcnt, 'size' : pgrec['size']}
   return 1

#
# process bfile records to add md5 checksum strings
#
def process_dataset_mcsfiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   amsg = ACTMSG[MCSACT]
   bmsg = BACKMSG[backflag]
   s = 's' if bcnt > 1 else ''
   PgLOG.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), PgLOG.WARNLG)

   qinfo = {'dsids' : [], 'fcnt' : 0, 'mcnt' : 0, 'fsize' : 0, 'msize' : 0}

   qcnt = 0
   for bid in bfiles:
      qcnt += process_one_quasar_mcsfile(bid, bfiles[bid], qinfo)

   if qcnt > 0:
      s = 's' if qcnt > 1 else ''
      fcnt = qinfo['fcnt']
      mcnt = qinfo['mcnt']
      dcnt = len(qinfo['dsids'])
      fsize = PgUtil.format_float_value(qinfo['fsize'])
      msize = PgUtil.format_float_value(qinfo['msize'])
      dmsg = qinfo['dsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "file{} for {}({}) of {}({}) files of {}".format(s, mcnt, msize, fcnt, fsize, dmsg)
      PgLOG.pglog("{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg), LOGACT)

#
# add a md5 checksum string to a quasar backup file record
#
def process_one_quasar_mcsfile(bid, binfo, qinfo):

   fields = 'bid, data_size size, checksum, date_modified date, time_modified time'
   bcnd = "bid = {}".format(bid)
   fcnd = "dsid = '{}' AND type = '{}' AND {} = '{}' AND " + bcnd
   dsids = []
   lines = binfo['note'].split("\n")
   lcnt = len(lines)
   tname = ftype = dsid = None
   msize = mcnt = 0
   for l in range(lcnt):
      line = lines[l]
      ary = line.split('<:>')
      if len(ary) == 4:
         fname = ary[0]
         if fname == ftype:
            lines[l] += 'MC'
         else:
            type = ary[1]
            size = int(ary[2])
            pgrec = PgDBI.pgget(tname, fields, fcnd.format(dsid, type, tname, fname), PgLOG.LGWNEX)
            if (pgrec and pgrec['checksum'] and pgrec['size'] == size and 
                PgUtil.cmptime(binfo['date'], binfo['time'], pgrec['date'], pgrec['time']) >= 0):
               lines[l] += pgrec['checksum']
               mcnt += 1
               msize += size
         lines[l] += '<:>'
      else:
         ms = re.match(r'^<([a-z]\d{6})_(\w)_\d+\.txt>$', line)
         if ms:
            dsid = ms.group(1)
            ftype = ms.group(2)
            tname = ftype.lower() + 'file'
            ftype += 'F'
            if dsid not in dsids: dsids.append(dsid)

   record = {'note' : '\n'.join(lines)}
   ret = 0
   if PgDBI.pgupdt('bfile', record, bcnd, PgLOG.LGEREX):
      qinfo['fcnt'] += binfo['fcnt']
      qinfo['fsize'] += binfo['size']
      qinfo['mcnt'] += mcnt
      qinfo['msize'] += msize
      for dsid in dsids:
         if dsid not in qinfo['dsids']: qinfo['dsids'].append(dsid)
      ret = 1

   if PGBACK['pstep']: set_dsquasar_progress(1, binfo['size'])

   return ret

#
# get all available backup file records without md5 checksums
#
def gather_dataset_mcsfiles(dsfiles, dsids):

   fcnt = 0
   bcnd = "status = 'A' AND note NOT LIKE '%<:>MC<:>%'"
   ocnd = " ORDER BY dsid"
   flds = "bid, type, data_size size, (scount + wcount) fcnt, date_modified, time_modified, note"
   if dsids:
      for dsid in dsids:
         dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
         pgrecs = PgDBI.pgmget("bfile", flds, dcnd, PgLOG.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            get_backup_mcsfile(dsfiles, PgUtil.onerecord(pgrecs, i))
         fcnt += bcnt
   else:
      pgrecs = PgDBI.pgmget("bfile", flds, bcnd+ocnd, PgLOG.LGWNEX)
      bcnt = len(pgrecs['bid']) if pgrecs else 0
      for i in range(bcnt):
         get_backup_mcsfile(dsfiles, PgUtil.onerecord(pgrecs, i))
      fcnt += bcnt

   s = 's' if fcnt > 1 else ''
   amsg = ACTMSG[MCSACT]
   bmsg = BACKMSG[PGBACK['backflag']] if PGBACK['backflag'] else 'backup'
   PgLOG.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), DTLACT)

   return fcnt

#
# get an archived file for adding md5 checksum
#
def get_backup_mcsfile(dsfiles, pgrec):

   dsfiles[pgrec['type']][pgrec['bid']] = {'note' : pgrec['note'], 'fcnt' : pgrec['fcnt'], 'size' : pgrec['size'],
                                           'date' : pgrec['date_modified'], 'time' : pgrec['time_modified']}

#
# rebuild missed file note 
#
#def rebuild_file_note(pgrec, dsids):
#
#   bid = pgrec['bid']
#   fields = 'file, dsid, type, data_size, checksum'
#   bfiles = {dsids[0] : {'S' : [], 'W' : []}}
#   pgrecs = PgDBI.pgmget('sfile', 's' + fields, "bid = {} ORDER BY dsid, sfile".format(bid), PgLOG.LGEREX)
#   cnt = len(pgrecs['sfile']) if pgrecs else 0
#   for i in range(cnt):
#      dsid = pgrecs['dsid'][i]
#      if dsid not in dsids:
#         dsids.append(dsid)
#         bfiles[dsid] = {'S' : [], 'W' : []}
#      bfiles[dsid]['S'].append([pgrecs['sfile'][i], pgrecs['type'][i], pgrecs['data_size'][i], pgrecs['checksum'][i]])
#
#   pgrecs = PgDBI.pgmget('wfile', 'w' + fields, "bid = {} ORDER BY dsid, wfile".format(bid), PgLOG.LGEREX)
#   cnt = len(pgrecs['wfile']) if pgrecs else 0
#   for i in range(cnt):
#      dsid = pgrecs['dsid'][i]
#      if dsid not in dsids:
#         dsids.append(dsid)
#         bfiles[dsid] = {'S' : [], 'W' : []}
#      bfiles[dsid]['W'].append([pgrecs['wfile'][i], pgrecs['type'][i], pgrecs['data_size'][i], pgrecs['checksum'][i]])
#
#   # create note
#   note = ''
#   for dsid in bfiles:
#      for ftype in bfiles[dsid]:
#         files = bfiles[dsid][ftype]
#         if not files: continue
#         note += "<{}_{}_{}.txt>\n".format(dsid, ftype, bid)
#         note += "DS<=>{}\n{}F<:>{}T<:>SZ<:>MC<:>\n".format(dsid, ftype, ftype)
#         for flist in files:
#            note += "{}<:>{}<:>{}<:>{}<:>\n".format(flist[0], flist[1], flist[2], flist[3])
#
#   if note:
#      PgDBI.pgexec("UPDATE bfile SET note = '{}' WHERE bid = {}".format(note, bid), PgLOG.LGEREX)
#      pgrec['note'] = note
#      return 1
#
#   return 0
#


#
# dump statistics for GDEX files available to create input files
#
def dump_dataset_files(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   dcnt = len(bfiles)
   if not dcnt: return

   sdsids = []
   wdsids = []
   scount = ssize = wcount = wsize = 0
   for dsid in bfiles:
      fcnt = bfiles[dsid]['scount']
      if fcnt > 0:
         scount += fcnt
         for i in range(fcnt):
            pgrec = bfiles[dsid]['srecs'][i]
            ssize += pgrec['data_size']
         if dsid not in sdsids: sdsids.append(dsid)
      fcnt = bfiles[dsid]['wcount']
      if fcnt > 0:
         wcount += fcnt
         for i in range(fcnt):
            pgrec = bfiles[dsid]['wrecs'][i]
            wsize += pgrec['data_size']
         if dsid not in wdsids: wdsids.append(dsid)

   cmsg = 'Changed ' if PGBACK['chgdays'] else ''
   bmsg = BACKMSG[backflag]
   if scount > 0:
      dcnt = len(sdsids)
      dmsg = sdsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
      strsize = PgUtil.format_float_value(ssize)
      msg = "{}({}) {}Saved files of {} ready for {}".format(scount, strsize, cmsg, dmsg, bmsg)
      PgLOG.pglog(INDENT + msg, LOGACT)

   if wcount > 0:
      dcnt = len(wdsids)
      dmsg = wdsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
      strsize = PgUtil.format_float_value(wsize)
      msg = "{}({}) {}Web files of {} ready for {}".format(wcount, strsize, cmsg, dmsg, bmsg)
      PgLOG.pglog(INDENT + msg, LOGACT)

#
# GDEX files included in input files
#
def dump_dataset_infiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   dsids = []
   fcnt = size = bcnt = 0
   for dsid in bfiles:
      for bid in bfiles[dsid]:
         binfo = bfiles[dsid][bid]
         for dsid in binfo['dsids']:
            if dsid not in dsids: dsids.append(dsid)
         bcnt += 1
         fcnt += binfo['fcnt']
         size += binfo['size']

   bmsg = BACKMSG[backflag]
   dcnt = len(dsids)
   ssize = PgUtil.format_float_value(size)
   dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
   msg = "{}({}) Input files for {} GDEX files of {} to be tarred for {}".format(bcnt, ssize, fcnt, dmsg, bmsg)
   PgLOG.pglog(INDENT + msg, LOGACT)

#
# tarred GDEX files to backup
#
def dump_dataset_tarfiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   dsids = []
   fcnt = size = 0
   for bid in bfiles:
      binfo = bfiles[bid]
      for dsid in binfo['dsids']:
         if dsid not in dsids: dsids.append(dsid)
      fcnt += binfo['fcnt']
      size += binfo['size']

   dcnt = len(dsids)
   ssize = PgUtil.format_float_value(size)
   bmsg = BACKMSG[backflag]
   dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
   msg = "{} ({}) Tarred files for {} GDEX files of {} for {}".format(bcnt, ssize, fcnt, dmsg, bmsg)
   PgLOG.pglog(INDENT + msg, LOGACT)

#
# Quasar files backed up already and file counts deleted or moved
#
def dump_dataset_bckfiles(dsfiles, backflag):

   bfiles = dsfiles[backflag]
   bcnt = len(bfiles)
   if not bcnt: return

   dsids = []
   qinfo = {'fcnt' : 0, 'size' : 0, 'ncnt' : 0, 'ccnt' : 0, 'csize' : 0,
            'dcnt' : 0, 'dsize' : 0, 'mcnt' : 0, 'msize' : 0,
            'ucnt' : 0, 'usize' : 0, 'dsids' : [], 'ndsids' : [],
            'cdsids' : [], 'ddsids' : [], 'mdsids' : [], 'udsids' : []}
   size = cnt = pcnt = 0
   for bid in bfiles:
      binfo = bfiles[bid]
      pcnt += count_changed_files(bid, binfo, qinfo)
      if PGBACK['pstep']:
         cnt += 1
         size += binfo['size']
         if cnt == DSTEP:
            set_dsquasar_progress(cnt, size)
            cnt = size = 0
   if cnt: set_dsquasar_progress(cnt, size)

   dscnt = len(qinfo['dsids'])
   ssize = PgUtil.format_float_value(qinfo['size'])
   bmsg = BACKMSG[backflag]
   dmsg = qinfo['dsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
   msg = "{} ({}) {} files for {} GDEX files of {}".format(bcnt, ssize, bmsg, qinfo['fcnt'], dmsg)
   PgLOG.pglog(INDENT + msg, LOGACT)

   indent = INDENT + INDENT
   if qinfo['ncnt'] > 0:
      dscnt = len(qinfo['ndsids'])
      dmsg = qinfo['ndsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
      msg = "{} {} files Missing Note fields of {}".format(bcnt, bmsg, dmsg)
      PgLOG.pglog(indent + msg, LOGACT)

   msg = "{} GDEX files Changed after {}".format(pcnt, bmsg)
   PgLOG.pglog(indent + msg, LOGACT)
   if pcnt == 0: return

   if qinfo['ccnt'] > 0:
      dscnt = len(qinfo['cdsids'])
      dmsg = qinfo['cdsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
      ssize = PgUtil.format_float_value(qinfo['csize'])
      msg = "{} ({}) GDEX file sizes Changed for {}".format(qinfo['ccnt'], ssize, dmsg)
      PgLOG.pglog(indent + msg, LOGACT)

   if qinfo['ucnt'] > 0:
      dscnt = len(qinfo['udsids'])
      dmsg = qinfo['udsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
      ssize = PgUtil.format_float_value(qinfo['usize'])
      msg = "{} ({}) GDEX files Updated & Re-done {} for {}".format(qinfo['ucnt'], ssize, bmsg, dmsg)
      PgLOG.pglog(indent + msg, LOGACT)
   
   if qinfo['dcnt'] > 0:
      dscnt = len(qinfo['ddsids'])
      dmsg = qinfo['ddsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
      ssize = PgUtil.format_float_value(qinfo['dsize'])
      msg = "{} ({}) GDEX files Got Deleted for {}".format(qinfo['dcnt'], ssize, dmsg)
      PgLOG.pglog(indent + msg, LOGACT)

   if qinfo['mcnt'] > 0:
      dscnt = len(qinfo['mdsids'])
      dmsg = qinfo['mdsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
      ssize = PgUtil.format_float_value(qinfo['msize'])
      msg = "{} ({}) GDEX files Moved for {}".format(qinfo['mcnt'], ssize, dmsg)
      PgLOG.pglog(indent + msg, LOGACT)

#
# count cache the Web/Saved files in type A bfiles (archived) already
#
def count_changed_files(bid, binfo, qinfo):

   qinfo['fcnt'] += binfo['fcnt']
   qinfo['size'] += binfo['size']
   note = binfo['note']
   if not note:
      qinfo['ncnt'] += 1
      if binfo['dsid'] not in qinfo['ndsids']: qinfo['ndsids'].append(binfo['dsid'])
      return 0

   pcnt = 0
   rfiles = {}   # dict of file : array[dtype, ftype, dsid, size] 
   mfiles = {}   # dict of file : array[dtype, ftype, dsid, tfile, tdtype, tftype, tdsid]
   lines = note.split("\n")
   lcnt = len(lines)
   l = 0
   ftype = dsid = mdsid = None
   while l < lcnt:
      line = lines[l]
      l += 1
      ms = re.match(r'^<([a-z]\d{6})_(\w)_\d+\.txt>', line)
      if ms:
         dsid = ms.group(1)
         ftype = ms.group(2)
         if dsid not in qinfo['dsids']: qinfo['dsids'].append(dsid)
         l += 2
         continue
      elif dsid:
         fary = line.split('<:>')
         if len(fary) > 3:
            rary = [ftype, dsid, int(fary[2])]
            rfiles[fary[0]] = rary
            continue
         else:
            dsid = ftype = None
      
      ms = re.match(r"^>MV ([a-z]\d{6}) Type (\w) (\w+) File (\S+) To ", line)
      if ms:
         mary = [ms.group(3)[0], ms.group(1)]
         mfiles[ms.group(4)] = mary

   # gather moved, changed or deleted file info
   for fname in rfiles:
      rinfo = rfiles[fname]
      if fname in mfiles:
         minfo = mfiles[fname]
         if minfo[0] == rinfo[0] and minfo[1] == rinfo[1]:
            qinfo['mcnt'] += 1
            qinfo['msize'] += rinfo[2]
            if rinfo[1] not in qinfo['mdsids']: qinfo['mdsids'].append(rinfo[1])
            pcnt += 1
            continue

      if rinfo[0] == 'W':
         cnd = "wfile = '{}'".format(fname)
         pgrec = PgSplit.pgget_wfile(rinfo[1], 'bid, data_size', cnd, PgLOG.LGEREX)
      else:
         cnd = "sfile = '{}' AND dsid = '{}'".format(fname, rinfo[1])
         pgrec = PgDBI.pgget('sfile', 'bid, data_size', cnd, PgLOG.LGEREX)
      if not pgrec:
         # deleted file
         qinfo['dcnt'] += 1
         qinfo['dsize'] += rinfo[2]
         if rinfo[1] not in qinfo['ddsids']: qinfo['ddsids'].append(rinfo[1])
         pcnt += 1
      elif pgrec['data_size'] != rinfo[2]:
         if pgrec['bid'] == bid:   # changed file
            qinfo['ccnt'] += 1
            qinfo['csize'] += rinfo[2]
            if rinfo[1] not in qinfo['cdsids']: qinfo['cdsids'].append(rinfo[1])
         else:   # updated file
            qinfo['ucnt'] += 1
            qinfo['usize'] += rinfo[2]
            if rinfo[1] not in qinfo['udsids']: qinfo['udsids'].append(rinfo[1])
         pcnt += 1

   return pcnt

#
# call main() to start program
#
if __name__ == "__main__": main()
