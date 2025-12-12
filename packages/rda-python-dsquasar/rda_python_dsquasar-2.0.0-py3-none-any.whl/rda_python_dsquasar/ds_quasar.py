#!/usr/bin/env python3
#
##################################################################################
#
#     Title : ds_quasar
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
from rda_python_common.pg_cmd import PgCMD
from rda_python_common.pg_split import PgSplit

class DsQuasar(PgCMD, PgSplit):

   CINACT = 1   # create dsarch input Save/Web file lists and add backup file records
   TARACT = 2   # build tarfiles (>=self.TARSIZE each tarfile) from the Saved/Web files in input files
   CTACTS = 3   # 1|2
   BCKACT = 4   # transfer multiple tarfiles (>=self.BCKSIZE each transfer) to Quasar backup/drdata 
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

   def __init__(self):
      super().__init__()  # initialize parent class
      self.BACKMSG = {
         'B' : "Quasar Backup",
         'D' : "Quasar Backup&Drdata"
      }
      self.LOGACT = self.LOGWRN
      self.ERRACT = self.LOGERR
      self.DTLACT = self.LOGWRN
      self.INDENT = ''
      self.ACTMSG = {
         self.CINACT : 'Create Input files',
         self.TARACT : 'Tar Backup files',
         self.CTACTS : 'Create Input&Tar backup Files',
         self.BCKACT : 'Transfer Globus Files',
         self.TBACTS : 'Tar Backup&Transfer Globus Files',
         self.CBACTS : 'Create Input&Tar backup&Transfer Globus Files',
         self.CHKACT : 'Check Backup Files',
         self.STTACT : 'Dump Backup Statistics',
      # uncomment only as need
      #   self.PTHACT : 'Add Gnnn Paths'
      #   self.IDSACT : 'Add dsids Strings'
         self.MCSACT : 'Add MD5 CheckSum Strings'
      }
      self.BSTATS = {
         'N' : 'Input Files',
         'T' : 'Tarred Files',
         'A' : 'Backed up Files'
      }
      self.SOPT = 1
      self.WOPT = 2
      self.ORDERS = {}    # cache current order number for each dsid
      self.BFILES = {}    # cache current order number for each dsid
      self.BCKSIZE = 90*self.PGLOG['ONEGBS']  # 90GB, dsglobus transfer size
      self.TARSIZE = 5*self.PGLOG['ONEGBS']   # 5GB, tarfile size limit
      self.MINSIZE = self.PGLOG['TWOGBS']     # 2GB, minimal tarfile size
      self.ONESIZE = 20*self.PGLOG['ONEGBS']  # 20GB, minimal file size to tar a single file 
      self.TFCOUNT = 100          # if file count is greater, use self.MINSIZE for tar file
      self.SUBLMTS = 2000         # file count limit for a sub-group
      self.PGBACK = {
         'workdir' : "{}/{}/quasar_backup".format(self.PGLOG['GDEXWORK'], self.PGLOG['GDEXUSER']),
         'mproc' : 1,
         'action' : self.CTACTS,
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
      self.dsids = []
      self.sopts = {'n' : 0, 'u' : 0, 'a' : 0, 'e' : 0, 'E' : 0}  
      self.bopts = None
      self.dstart = 0

   # read in command line parameters
   def read_parameters(self):   
      self.PGLOG['LOGFILE'] = "dsquasar.log"   # set different log file
      self.dssdb_dbname()
      option = None
      argv = sys.argv[1:]
      for arg in argv:
         ms = re.match(r'^-(a|b|c|d|e|E|l|m|n|t|u|A|B|D)$', arg)
         if ms:
            arg = ms.group(1)
            if  arg == 'b':
               self.PGLOG['BCKGRND'] = 1   # processing in backgroup mode
            elif arg in self.sopts:
               self.sopts[arg] = 1
               option = None
            elif 'Acdlmt'.find(arg) > -1:
               option = arg
               if arg == 'd': self.bopts = []
            elif 'BD'.find(arg) > -1:
               if self.PGBACK['backflag']: self.pglog("-{}: Backup Flag is set to {} already".format(arg, self.PGBACK['backflag']), self.LGEREX)
               self.PGBACK['backflag'] = arg
         elif option:
            if option == 'd':
               self.bopts.append(arg)
            elif option == 'c':
               self.PGBACK['chgdays'] = int(arg)
               if self.PGBACK['chgdays'] < 1: self.pglog(arg +": Change Days(-c) must be > 0", self.LGWNEX)
               option = None
            elif option == 'm':
               self.PGBACK['mproc'] = int(arg)
               if self.PGBACK['mproc'] < 1: self.pglog(arg +": Multiple Processes(-m) must be > 0", self.LGWNEX)
               option = None
            elif option == 'A':
               self.PGBACK['action'] = int(arg)
               if self.PGBACK['action'] not in self.ACTMSG:
                  self.pglog(arg + ": Invalid Action(-A) value", self.LGWNEX)
               option = None
            elif option == 'l':
               if not (arg == 'Y' or arg == 'N'): self.pglog(arg +": Lock Flag(-l) must be Y or N", self.LGWNEX)
               self.PGBACK['dolock'] = 1 if arg == 'Y' else 0
               option = None
            else:
               self.add_to_dsids(arg)
         else:
            self.pglog(arg + ": Value without leading option", self.LGWNEX)
      if not (self.sopts['a'] or self.dsids):
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
      self.PGBACK['cmd'] = "dsquasar {}".format(' '.join(argv))

   # do quasar backup process
   def start_actions(self):
      self.cmdlog(self.PGBACK['cmd'])
      if self.sopts['u']:
         if self.sopts['a']: self.pglog("-u: Dataset IDs must be provided to Unlock datasets", self.LOGWRN)
         self.unlock_datasets()
         sys.exit(0)
      if self.sopts['a'] and self.dsids: self.pglog("-a: Option is ignored for dataset IDs provided", self.LOGWRN)
      self.change_local_directory(self.PGBACK['workdir'], self.LGEREX)
      if self.sopts['e'] or self.sopts['E']:
         self.PGBACK['doemail'] = 1
         self.LOGACT = self.LGWNEM
         self.ERRACT = self.EMEROL
         self.INDENT = '  '
         if self.sopts['E']:
            self.DTLACT = self.LGWNEM
            self.PGLOG['EMLMAX'] = 1024
      if self.sopts['n']: self.dstart = 1
      acts = self.PGBACK['action']
      if acts&self.CHKACT:
         self.check_backup_action()
      elif acts&self.STTACT:
         self.dump_statistics_action()
      elif acts&self.PTHACT:
         self.add_path_action()
      elif acts&self.IDSACT:
         self.add_dsids_action()
      elif acts&self.MCSACT:
         self.add_checksum_action()
      else:
         if acts&self.BCKACT: self.globus_transfer_action()
         if acts&self.TARACT: self.build_tarfile_action()
         if acts&self.CINACT: self.create_infile_action()
         if self.dstart and acts&self.TBACTS == self.TBACTS: self.globus_transfer_action()
      if self.PGBACK['doemail']:
         amsg = self.ACTMSG[self.PGBACK['action']]
         bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup'
         dcnt = len(self.dsids)
         dmsg = self.dsids[0] if dcnt == 1 else "{} datasets".format(dcnt if dcnt > 1 else 'All')
         self.set_email("{}: {} for {} Files of {}!".format(self.PGBACK['cmd'], amsg, bmsg, dmsg), self.EMLTOP)
         title = "dsquasar: " + amsg
         if self.PGBACK['bckcnt']: title += "({})".format(self.PGBACK['bckcnt'])
         if self.PGBACK['errcnt']: title += " Error({})".format(self.PGBACK['errcnt'])
         if self.PGLOG['DSCHECK']:
            tbl = "dscheck"
            cnd = "cindex = {}".format(self.PGLOG['DSCHECK']['cindex'])
            self.build_customized_email(tbl, "einfo", cnd, title, self.LOGWRN)
         else:
            self.pglog(title, self.LOGWRN|self.SNDEML)
      if self.PGBACK['pstep']: self.record_dscheck_status("D")
      self.cmdlog()
      self.pgexit(0)

   # add given dsid to self.dsids; expand it if wildcard dsid is given
   def add_to_dsids(self, dsid):
      if dsid.find('%') > -1:
         pgrecs = self.pgmget('dataset', 'dsid', "dsid LIKE '{}'".format(dsid))
         if pgrecs:
            for dsid in pgrecs['dsid']:
               if dsid not in self.dsids: self.dsids.append(dsid)
      else:
         dsid = self.format_dataset_id(dsid)
         if dsid not in self.dsids: self.dsids.append(dsid)

   # Check backup and file information and dump the backup statistics#
   def dump_statistics_action(self):   
      self.start_dsquasar_none_daemon(self.STTACT)
      # files ready to be backed up
      dsfiles = {'B' : {}, 'D' : {}}
      self.gather_dataset_files(dsfiles, False)
      self.dump_dataset_files(dsfiles, 'B')
      self.dump_dataset_files(dsfiles, 'D')
      if self.PGBACK['chgdays']: return   # no further checking
      # changed GDEX files ready to be backed up
      self.PGBACK['chgdays'] = 1
      dsfiles = {'B' : {}, 'D' : {}}
      self.gather_dataset_files(dsfiles, False)
      self.dump_dataset_files(dsfiles, 'B')
      self.dump_dataset_files(dsfiles, 'D')
      self.PGBACK['chgdays'] = 0
      # files are in input files but not tarred yet
      dsfiles = {'B' : {}, 'D' : {}}
      self.gather_dataset_infiles(dsfiles)
      self.dump_dataset_infiles(dsfiles, 'B')
      self.dump_dataset_infiles(dsfiles, 'D')
      # files are tarred but not backed up yet
      dsfiles = {'B' : {}, 'D' : {}}
      self.gather_dataset_tarfiles(dsfiles)
      self.dump_dataset_tarfiles(dsfiles, 'B')
      self.dump_dataset_tarfiles(dsfiles, 'D')   
      # files backed up (including the ones got moved and deleted after backup)
      dsfiles = {'B' : {}, 'D' : {}}
      self.gather_dataset_bckfiles(dsfiles)
      self.dump_dataset_bckfiles(dsfiles, 'B')
      self.dump_dataset_bckfiles(dsfiles, 'D')

   # Check the file sizes between db and backup servers, and set status to 'N' if different
   def check_backup_action(self):   
      dsfiles = {'B' : {}, 'D' : {}}
      fcnt = self.gather_dataset_bckfiles(dsfiles, False)
      if fcnt and self.dstart:
         self.start_dsquasar_none_daemon(self.CHKACT, fcnt)
         self.process_dataset_chkfiles(dsfiles, 'B')
         self.process_dataset_chkfiles(dsfiles, 'D')

   # add Gnnn paths to old bfiles without ones
   def add_path_action(self):
      dsfiles = {'B' : {}, 'D' : {}}
      fcnt = self.gather_dataset_pathfiles(dsfiles)
      if fcnt and self.dstart:
         self.start_dsquasar_none_daemon(self.PTHACT, fcnt)
         self.process_dataset_pathfiles(dsfiles, 'B')
         self.process_dataset_pathfiles(dsfiles, 'D')

   # add dsids to old bfiles without ones
   def add_dsids_action(self):
      dsfiles = {'B' : {}, 'D' : {}}
      fcnt = self.gather_dataset_dsidfiles(dsfiles)
      if fcnt and self.dstart:
         self.start_dsquasar_none_daemon(self.IDSACT, fcnt)
         self.process_dataset_dsidfiles(dsfiles, 'B')
         self.process_dataset_dsidfiles(dsfiles, 'D')

   # add md5 checksums to old bfiles which miss the checksums in note field
   def add_checksum_action(self):
      dsfiles = {'B' : {}, 'D' : {}}
      fcnt = self.gather_dataset_mcsfiles(dsfiles)
      if fcnt and self.dstart:
         self.start_dsquasar_none_daemon(self.MCSACT, fcnt)
         self.process_dataset_mcsfiles(dsfiles, 'B')
         self.process_dataset_mcsfiles(dsfiles, 'D')

   # check available GDEX files to create input files
   def create_infile_action(self):
      if self.dstart > 0: self.dstart = self.start_dsquasar_none_daemon(self.CINACT)
      dsfiles = {'B' : {}, 'D' : {}}
      fcnt = self.gather_dataset_files(dsfiles)
      if fcnt and self.dstart:
         self.backup_dataset_files(dsfiles, 'B')
         self.backup_dataset_files(dsfiles, 'D')

   # check input files and build tar files
   def build_tarfile_action(self):
      dsfiles = {'B' : {}, 'D' : {}}
      fcnt = self.gather_dataset_infiles(dsfiles)
      if fcnt and self.dstart:
         if self.dstart > 0: self.dstart = self.start_dsquasar_none_daemon(self.TARACT, fcnt)
         self.backup_dataset_infiles(dsfiles, 'B')
         self.backup_dataset_infiles(dsfiles, 'D')

   # gather and transfer tar files to Globus Quasar Servers
   def globus_transfer_action(self):   
      dsfiles = {'B' : {}, 'D' : {}}
      fcnt = self.gather_dataset_tarfiles(dsfiles)
      if fcnt and self.dstart:
         if self.dstart > 0: self.dstart = self.start_dsquasar_none_daemon(self.BCKACT, fcnt)
         self.backup_dataset_tarfiles(dsfiles, 'B')
         self.backup_dataset_tarfiles(dsfiles, 'D')

   # start none daemon and intialize dscheck counts
   def start_dsquasar_none_daemon(self, act, fcnt = 0):
      acts = self.PGBACK['action']
      if self.bopts != None:
         dsid = self.dsids[0] if len(self.dsids) == 1 else ''
         if not re.match(r'^[a-z]\d{6}$', dsid): dsid = ''
         cact = ('A' if acts < 10 else '') + str(acts)
         if act == self.STTACT or acts&self.NBACTS != acts:
            self.set_one_boption('qoptions', '-l walltime=24:00:00', 1)
         self.init_dscheck(0, '', "dsquasar", dsid, cact, self.PGBACK['workdir'],
                            self.PGLOG['CURUID'], self.bopts, self.LOGWRN)
         if self.PGBACK['mproc'] > 1: self.PGBACK['mproc'] = 1
      elif self.PGBACK['mproc'] > 1 and acts&self.NBACTS == acts:
         self.PGBACK['mproc'] = 1
      self.start_none_daemon('dsquasar', '', self.PGLOG['CURUID'], self.PGBACK['mproc'], 60, 1)
      if self.PGLOG['DSCHECK']:
         if act == self.STTACT:
            fcnt = self.gather_dataset_bckfiles(None, False)
         elif act == self.BCKACT:
            if acts&self.TARACT: fcnt += 2*self.gather_dataset_infiles(None)
            if acts&self.CINACT: fcnt += 2*self.gather_dataset_files(None)
         else:
            if act == self.CINACT or act == self.TARACT and acts&self.CINACT:
               fcnt += self.gather_dataset_files(None)
            if acts&self.BCKACT: fcnt *= 2
         self.set_dscheck_fcount(fcnt, self.LGEREX)
         self.set_dscheck_dcount(0, 0, self.LGEREX)
         mstep = 100 if acts&self.NBACTS else 10
         pstep = int(fcnt/100)
         if pstep > mstep:
            pstep = mstep
         elif pstep < 2:
            pstep = 2
         self.PGBACK['pstep'] = self.PGBACK['pcnt'] = pstep
         self.PGBACK['dcnt'] = self.PGBACK['dsize'] = 0
      return -1

   # set the progress counts for dscheck controlled actions
   def set_dsquasar_progress(self, fcnt, fsize):
      self.PGBACK['dcnt'] += fcnt
      self.PGBACK['dsize'] += fsize
      if self.PGBACK['dcnt'] >= self.PGBACK['pcnt']:
         self.set_dscheck_dcount(self.PGBACK['dcnt'], self.PGBACK['dsize'], self.LGEREX)
         self.PGBACK['pcnt'] = self.PGBACK['dcnt'] + self.PGBACK['pstep']

   # unlock locked datset for given dataset IDs
   def unlock_datasets(self):
      acnt = len(self.dsids)
      s = 's' if acnt > 1 else ''
      self.pglog("Unlock {} Dataset{} ...".format(acnt, s), self.WARNLG)
      mcnt = 0
      for dsid in self.dsids:
         pgrec = self.pgget("dataset", "pid, lockhost", "dsid = '{}'".format(dsid), self.LGEREX)
         if not pgrec:
            self.pglog(dsid + ": Not exists", self.LOGERR)
         elif not pgrec['pid']:
            self.pglog(dsid + ": Not locked", self.LOGWRN)
         elif self.lock_dataset(dsid, -1, self.LGEREX) > 0:
            mcnt += 1
            self.pglog("{}: Unlocked {}/{}".format(dsid, pgrec['pid'], pgrec['lockhost']), self.LOGWRN)
         elif(self.check_host_down(None, pgrec['lockhost']) and
              self.lock_dataset(dsid, -2, self.LGEREX) > 0):
            mcnt += 1
            self.pglog("{}: Force unlocked {}/{}".format(dsid, pgrec['pid'], pgrec['lockhost']), self.LOGWRN)
         else:
            self.pglog("{}: Unable to unlock {}/{}".format(dsid, pgrec['pid'], pgrec['lockhost']), self.LOGWRN)
      if acnt > 1: self.pglog("{} of {} Dataset{} unlocked from RDADB".format(mcnt, acnt, s), self.LOGWRN)

   # backup bfiles onto Quasar Backup and/or Drdata endpoints for given datasets
   def backup_dataset_files(self, dsfiles, backflag):
      bfiles = dsfiles[backflag]
      dcnt = len(bfiles)
      if not dcnt: return
      amsg = self.ACTMSG[self.PGBACK['action']&self.CTACTS]
      bmsg = self.BACKMSG[backflag]
      dmsg = list(bfiles)[0] if dcnt == 1 else "{} datasets".format(dcnt)
      self.pglog("{}: {} for {} ...".format(amsg, bmsg, dmsg), self.WARNLG)
      qinfo = {'backflag' : backflag, 'bid' : self.current_bid(), 'dsids' : [], 'fcnt' : 0,
               'size' : 0, 'infiles' : [], 'instr' : '', 'qdsids' : [],
               'dslocks' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}
      for dsid in bfiles:
         if len(qinfo['dsids']) == self.DSCNT: self.process_one_backup_file(qinfo, True, False)
         if self.PGBACK['dolock'] and dsid not in qinfo['dslocks']:
            if self.lock_dataset(dsid, 1, self.LOGERR) < 1: continue
            qinfo['dslocks'].append(dsid)
         fcnt = bfiles[dsid]['scount']
         if fcnt > 0:
            self.process_backup_files(qinfo, dsid, fcnt, bfiles[dsid]['srecs'], 'S')
         fcnt = bfiles[dsid]['wcount']
         if fcnt > 0:
            self.process_backup_files(qinfo, dsid, fcnt, bfiles[dsid]['wrecs'], 'W')
         if qinfo['fcnt'] == 0:  # unlock dsid for dataset backup finished
            if dsid in qinfo['dslocks']:
               self.lock_dataset(dsid, 0, self.LGEREX)
               qinfo['dslocks'].remove(dsid)
            qinfo['dsids'] = []
      if qinfo['dslocks']:
         for dsid in qinfo['dslocks']:
            self.lock_dataset(dsid, 0, self.LGEREX)  # unlock the locked datasets
      cmsg = 'Changed ' if self.PGBACK['chgdays'] else ''
      qcnt = qinfo['qcnt']
      if qcnt > 0:
         self.PGBACK['bckcnt'] += qcnt
         s = 's' if qcnt > 1 else ''
         fcnt = qinfo['qfcnt']
         dcnt = len(qinfo['qdsids'])
         ssize = self.format_float_value(qinfo['qsize'])
         dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         fmsg = "file{} for {}({}) GDEX {}files of {}".format(s, fcnt, ssize, cmsg, dmsg)
         msg = "{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg)
         self.pglog(self.INDENT + msg, self.LOGACT)
      fcnt = qinfo['fcnt']
      if fcnt > 0:
         for infile in qinfo['infiles']: self.delete_local_file(infile)
         s = 's' if fcnt > 1 else ''
         ssize = self.format_float_value(qinfo['size'])
         dsids = qinfo['dsids']
         dcnt = len(dsids)
         dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
         msg = "{}: {}({}) GDEX {}file{} of {} for next {}".format(amsg, fcnt, ssize, cmsg, s, dmsg, bmsg)
         self.pglog(self.INDENT + msg, self.LOGACT)

   # get the current bid for adding bfile
   def current_bid(self):
      pgrec = self.pgget("bfile", "max(bid) mid", '', self.LGEREX)
      return (pgrec['mid'] + 1) if pgrec else 1

   # get the current disp_order for adding bfile
   def display_order(self, dsid):
      if dsid not in self.ORDERS:
         pgrec = self.pgget('bfile', "max(disp_order) max_order", "dsid = '{}'".format(dsid), self.LGEREX)
         self.ORDERS[dsid] = pgrec['max_order'] if pgrec and pgrec['max_order'] else 0
      self.ORDERS[dsid] += 1
      return self.ORDERS[dsid]

   # backup bfiles with input files set onto Quasar Backup and/or Drdata endpoints
   def backup_dataset_infiles(self, dsfiles, backflag):
      bfiles = dsfiles[backflag]
      bcnt = len(bfiles)
      if not bcnt: return
      amsg = self.ACTMSG[self.TARACT]
      bmsg = self.BACKMSG[backflag]
      s = 's' if bcnt > 1 else ''
      self.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), self.WARNLG)
      qinfo = {'backflag' : backflag, 'bid' : 0, 'dsids' : [], 'fcnt' : 0, 'size' : 0,
               'infiles' : [], 'instr' : '', 'qdsids' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}
      for dsid in bfiles:
         if self.PGBACK['dolock'] and self.lock_dataset(dsid, 1, self.LOGERR) < 1: continue
         for bid in bfiles[dsid]:
            qinfo['bid'] = bid
            binfo = bfiles[dsid][bid]
            for bkey in binfo: qinfo[bkey] = binfo[bkey]
            self.process_one_backup_file(qinfo, False)
         if self.PGBACK['dolock']: self.lock_dataset(dsid, 0, self.LOGERR)
      qcnt = qinfo['qcnt']
      if qcnt > 0:
         self.PGBACK['bckcnt'] += qcnt
         s = 's' if qcnt > 1 else ''
         fcnt = qinfo['qfcnt']
         dcnt = len(qinfo['qdsids'])
         ssize = self.format_float_value(qinfo['qsize'])
         dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         fmsg = "file{} for {}({}) GDEX files of {}".format(s, fcnt, ssize, dmsg)
         msg = "{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg)
         self.pglog(self.INDENT + msg, self.LOGACT)

   # backup bfiles with tar files built onto Quasar Backup and/or Drdata endpoints
   def backup_dataset_tarfiles(self, dsfiles, backflag):
      bfiles = dsfiles[backflag]
      bcnt = len(bfiles)
      if not bcnt: return
      amsg = self.ACTMSG[self.BCKACT]
      bmsg = self.BACKMSG[backflag]
      s = 's' if bcnt > 1 else ''
      self.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), self.WARNLG)
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
         if qinfo['size'] < self.BCKSIZE: continue
         self.transfer_quasar_tarfiles(qinfo)
      if qinfo['size'] > 0: self.transfer_quasar_tarfiles(qinfo)
      qcnt = qinfo['qcnt']
      if qcnt > 0:
         self.PGBACK['bckcnt'] += qcnt
         s = 's' if qcnt > 1 else ''
         fcnt = qinfo['qfcnt']
         dcnt = len(qinfo['qdsids'])
         ssize = self.format_float_value(qinfo['qsize'])
         dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         fmsg = "file{} for {}({}) GDEX files of {}".format(s, fcnt, ssize, dmsg)
         msg = "{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg)
         self.pglog(self.INDENT + msg, self.LOGACT)

   # wait all child processes finish and then quit the main program
   def quit_dsquasar(self, qinfo, msg = None):
      if self.PGBACK['mproc'] > 1: self.check_child(None, 0, self.LOGWRN, 1)
      if qinfo:
         if 'dslocks' in qinfo and qinfo['dslocks']:
            for dsid in qinfo['dslocks']: self.lock_dataset(dsid, 0, self.LGEREX)
         qcnt = qinfo['qcnt']
         dcnt = len(qinfo['qdsids'])
         fcnt = qinfo['qfcnt']
         ssize = self.format_float_value(qinfo['qsize'])
         amsg = self.ACTMSG[self.PGBACK['action']]
         bmsg = self.BACKMSG[qinfo['backflag']]
         dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         msg = "Quit {}: {} {} files for {}({}) files of {}".format(amsg, qcnt, bmsg, fcnt, ssize, dmsg)
         self.pglog(msg, self.LOGACT)
      if self.PGBACK['doemail']:
         bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup'
         self.set_email("{}: Quit {} for {} Files of {}!".format(self.PGBACK['cmd'], amsg, bmsg, dmsg), self.EMLTOP)
         title = "dsquasar: Quit {} Error({})".format(amsg, self.PGBACK['errcnt'])
         if self.PGLOG['DSCHECK']:
            tbl = "dscheck"
            cnd = "cindex = {}".format(self.PGLOG['DSCHECK']['cindex'])
            self.build_customized_email(tbl, "einfo", cnd, title, self.LOGWRN)
         else:
            self.pglog(title, self.LOGWRN|self.SNDEML)
      if self.PGBACK['pstep']: self.record_dscheck_status("F")
      self.pgexit(0)

   # backup one Quasar Backup or Backup&Drdata from one or multiple inputs and,
   # reset the quasar backup dict
   def process_one_backup_file(self, qinfo, addback, keepid = False):
      ccnt = self.check_child(None, 0, self.LOGWRN, -1) if self.PGBACK['mproc'] > 1 else 0
      if self.PGSIG['QUIT']: self.quit_dsquasar(qinfo)
      dsids = qinfo['dsids']
      dcnt = len(dsids)
      if dcnt == 0: return
      # prepare for backup one tar file
      dsid = dsids[0]
      fcnt = qinfo['fcnt']
      fsize = qinfo['size']
      bflg = qinfo['backflag']
      if addback:
         (bid, qfile) = self.add_backup_record(dsid, qinfo['bid'], bflg, dcnt, fcnt, fsize, dsids, qinfo['instr'])
      else:
         bid = qinfo['bid']
         qfile = qinfo['bfile']
      stat = 1
      if self.PGBACK['action'] > self.CINACT:
         s = 's' if fcnt > 1 else ''
         amsg = self.ACTMSG[self.PGBACK['action']&self.CTACTS]
         bmsg = self.BACKMSG[bflg]
         ssize = self.format_float_value(fsize)
         dmsg = dsid if dcnt == 1 else "{} datasets".format(dcnt)
         qmsg = "{}: Try {} {} file for {}({}) file{} of {}".format(amsg, qfile, bmsg, fcnt, ssize, s, dmsg)
         cmd = "dsarch {} AQ -QT {} -QF {} ".format(dsid, bflg, qfile)
         cmd += '-TO -OE -MD -IF ' + ' '.join(qinfo['infiles'])
         if ccnt > 0:
            stat = self.start_child("dsquasar_{}".format(bid), self.LOGWRN, 1)  # try to start a child process
            if stat <= 0:
               if self.PGSIG['QUIT']: self.quit_dsquasar(qinfo)
               sys.exit(1)   # something wrong
            elif self.PGSIG['PPID'] > 1:
               stat = self.pgsystem(cmd, self.ERRACT, 325)   # 256 + 64 + 4 + 1
               if stat:
                  for infile in qinfo['infiles']: self.delete_local_file(infile)
               elif re.search(r'file backed up to', self.PGLOG['SYSERR']):
                  if self.pgdel('bfile', f"bid = {bid}"):
                     self.pglog(f"{dsid}-{qfile}: backup tarfile deleted for duplicattion", self.DTLACT)
                  for infile in qinfo['infiles']: self.delete_local_file(infile)
               sys.exit(0)  # stop child process
            else:
               self.pgdisconnect()  # disconnect database for reconnection
               self.pglog("Started a process for " + qmsg, self.LOGWRN)
         else:
            self.pglog(qmsg, self.LOGWRN)
            stat = self.pgsystem(cmd, self.ERRACT, 325)   # 256 + 64 + 4 + 1
            if stat:
               for infile in qinfo['infiles']: self.delete_local_file(infile)
            elif re.search(r'file backed up to', self.PGLOG['SYSERR']):
               if self.pgdel('bfile', f"bid = {bid}"):
                  self.pglog(f"{dsid}-{qfile}: backup tarfile deleted for duplicattion", self.DTLACT)
               for infile in qinfo['infiles']: self.delete_local_file(infile)
            else:
               self.PGBACK['errcnt'] += 1
               if self.PGBACK['errcnt'] > self.PGBACK['maxcnt']: self.quit_dsquasar(qinfo)
               time.sleep(self.PGSIG['ETIME'])
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
               self.lock_dataset(dsid, 0, self.LGEREX)
               qinfo['dslocks'].remove(dsid)
         qinfo['dsids'] = [lastdsid] if keepid else []
         qinfo['bid'] = bid + 1
         qinfo['fcnt'] = qinfo['size'] = 0
         qinfo['infiles'] = []
         qinfo['instr'] = ''
      if self.PGBACK['pstep']: self.set_dsquasar_progress((fcnt if self.PGBACK['action']&self.CINACT else 1), fsize)

   # Transfer multiple tarfiles to Quasar Backup or Backup&Drdata, and
   # reset the quasar backup dict
   def transfer_quasar_tarfiles(self, qinfo):
      ccnt = self.check_child(None, 0, self.LOGWRN, -1) if self.PGBACK['mproc'] > 1 else 0
      if self.PGSIG['QUIT']: self.quit_dsquasar(qinfo)
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
      amsg = self.ACTMSG[self.BCKACT]
      bmsg = self.BACKMSG[bflg]
      ssize = self.format_float_value(fsize)
      dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
      fmsg = "{}({}) {} file{} of {}".format(bcnt, ssize, bmsg, s, dmsg)
      qmsg = "{}: Try {}".format(amsg, fmsg)
      if ccnt > 0:
         stat = self.start_child("dsquasar_{}".format(bids[0]), self.LOGWRN, 1)  # try to start a child process
         if stat <= 0:
            if self.PGSIG['QUIT']: self.quit_dsquasar(qinfo)
            sys.exit(1)   # something wrong
         elif self.PGSIG['PPID'] <= 1:
            self.pgdisconnect()  # disconnect database for reconnection
            self.pglog("Started a process for " + qmsg, self.LOGWRN)
      else:
         self.pglog(qmsg, self.LOGWRN)
      dstat = bstat = -1
      if ccnt == 0 or self.PGSIG['PPID'] > 1:
         if bflg == 'D':
            dstat = self.quasar_multiple_trasnfer(tofiles, fromfiles, 'gdex-quasar-drdata', 'gdex-glade', self.ERRACT)
            if not dstat: self.pglog("Error Quaser Drdata for " + fmsg, self.ERRACT|self.LOGERR)
         bstat = self.quasar_multiple_trasnfer(tofiles, fromfiles, 'gdex-quasar', 'gdex-glade', self.ERRACT)
         if not dstat: self.pglog("Error Quaser Backup for " + fmsg, self.ERRACT|self.LOGERR)
         if dstat == self.FINISH: dstat = self.check_globus_finished(tofiles[0], 'gdex-quasar-drdata', self.ERRACT|self.NOWAIT)
         if bstat == self.FINISH: bstat = self.check_globus_finished(tofiles[0], 'gdex-quasar', self.ERRACT|self.NOWAIT)
         if dstat and bstat:
            for fromfile in fromfiles:
               tarfile = self.PGLOG['DSSDATA'] + fromfile
               self.delete_local_file(tarfile, self.LGEREX)
            self.pglog("{} local tarfile{} removed".format(bcnt, s), self.DTLACT)
            for bid in qinfo['bids']:
               self.pgexec("UPDATE bfile SET status = 'A' WHERE bid = {}".format(bid), self.LGEREX)
            self.pglog("{} backup file{} updated".format(bcnt, s), self.DTLACT)
         else:
            self.pglog("Backup acion is not complete and {} local tarfile{} are not removed".format(bcnt, s), self.LOGERR)
            self.PGBACK['errcnt'] += 1
            if self.PGBACK['errcnt'] > self.PGBACK['maxcnt']: self.quit_dsquasar(qinfo)
            time.sleep(self.PGSIG['ETIME'])
      if self.PGSIG['PPID'] > 1: sys.exit(0)   # stop child process
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
      if self.PGBACK['pstep']: self.set_dsquasar_progress((fcnt if self.PGBACK['action']&self.CINACT else bcnt), fsize)

   # add a backup file record as a place holder
   def add_backup_record(self, dsid, bid, bflg, dcnt, fcnt, fsize, dsids, instr):
      dorder = self.display_order(dsid)
      subpath = 'G{:03}'.format(int((dorder+self.SUBLMTS-1)/self.SUBLMTS))
      cmsg = '_changed' if self.PGBACK['chgdays'] else ''
      bfile = "{}/{}_sn{}_dn{}_fn{}{}.tar".format(subpath, dsid, bid, dcnt, fcnt, cmsg)
      record = {'dsid' : dsid, 'bfile' : bfile, 'type' : bflg, 'status' : 'N',
                'disp_order' : dorder, 'data_size' : fsize,
                'dsids' : ','.join(dsids[1:]), 'note' : instr}
      nbid = 0
      while nbid != bid:
         nbid = self.pgadd('bfile', record, self.LOGERR|self.AUTOID)
         if not nbid:
            bid = self.current_bid()
            bfile = "{}/{}_sn{}_dn{}_fn{}{}.tar".format(subpath, dsid, bid, dcnt, fcnt, cmsg)
            record['bfile'] = bfile
         elif nbid != bid:
            bid = nbid
            bfile = "{}/{}_sn{}_dn{}_fn{}{}.tar".format(subpath, dsid, bid, dcnt, fcnt, cmsg)
            self.pgexec("UPDATE bfile SET bfile = '{}' WHERE bid = {}".format(bfile, bid), self.LGEREX)
      return (bid, bfile)

   # open an input file and intialize the header for given dataset ID and file type
   def open_input_file(self, qinfo, dsid, ftype):
      infile = "{}_{}_{}.txt".format(dsid, ftype, qinfo['bid'])
      instr = "DS<=>{}\n{}F<:>{}T<:>SZ<:>MC<:>\n".format(dsid, ftype, ftype)
      fd = open(infile, 'w')
      fd.write(instr)
      qinfo['instr'] += "<{}>\n{}".format(infile, instr)
      qinfo['infiles'].append(infile)
      return fd

   # build input files and backup a quasar file if accumulated enough files (>= self.TARSIZE)
   def process_backup_files(self, qinfo, dsid, fcnt, recs, filetype):
      if dsid not in qinfo['dsids']: qinfo['dsids'].append(dsid)
      fd = None
      fcate = filetype.lower()
      tname = fcate + 'file'
      for i in range(fcnt):
         pgrec = recs[i]
         if not self.evaluate_file_stat(dsid, fcate, pgrec): continue
         fname = pgrec[tname]
         fsize = pgrec['data_size']
         ftype = pgrec['type']
         fcksm = pgrec['checksum']
         qinfo['fcnt'] += 1
         qinfo['size'] += fsize
         instr = "{}<:>{}<:>{}<:>{}<:>\n".format(fname, ftype, fsize, fcksm)
         if not fd: fd = self.open_input_file(qinfo, dsid, filetype)
         fd.write(instr)
         qinfo['instr'] += instr
         if qinfo['fcnt'] == 1:
            if qinfo['size'] < self.ONESIZE: continue
         elif qinfo['fcnt'] < self.TFCOUNT:
            if qinfo['size'] < self.TARSIZE: continue
         else:
            if qinfo['size'] < self.MINSIZE: continue
         fd.close()
         fd = None
         self.process_one_backup_file(qinfo, True, (fcnt-i) > 1)
      if fd: fd.close()

   # initialize dataset backup dict structure
   @staticmethod
   def init_backup_dict():   
      return {'wcount' : 0, 'wrecs' : [], 'scount' : 0, 'srecs' : []}

   # get all files need to be backed up for a given dataset ID
   def get_dataset_files(self, dsid, dsfiles, backflag, logact = 0):
      dcnd = "dsid = '{}'".format(dsid)
      fopt = self.get_backup_options(dsid, dcnd)
      if not fopt:
         if logact: self.pglog(dsid + ": No data file found to backup", logact)
         return 0
      infiles = self.cache_dataset_infiles(dsid)
      cnts = {'B' : [0, 0], 'D' : [0, 0]}  # [cnt, size]
      bfiles = {'B' : None, 'D' : None}
      flgset = 0 if backflag == 'N' else 1
      if dsfiles:
         bfiles['B'] = self.init_backup_dict()
         bfiles['D'] = self.init_backup_dict()
      validflags = (self.PGBACK['backflag'] if self.PGBACK['backflag'] else 'BD')
      backflags = {0 : backflag}
      gcnd = dcnd + " AND pindex = 0 ORDER BY gindex"
      pgrecs = self.pgmget('dsgroup', 'gindex, backflag', gcnd, self.LGWNEX)
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
            rcnt = self.get_group_files(dsid, gcnd, dcnd, bfiles[bflg], fopt, infiles, cnts[bflg])
            dt = tm() - bt
            if rcnt > 1 and dt > 29:
               rmsg = self.seconds_to_string_time(dt)
               self.pglog("{}-G{}: Found {} Files ({})".format(dsid, gidx, rcnt, rmsg), self.LOGWRN)
   
      fcnt = cnts['B'][0] + cnts['D'][0]
      if dsfiles:
         cmsg = 'Changed ' if self.PGBACK['chgdays'] else ''
         for bflg in dsfiles:
            bcnt = cnts[bflg][0]
            if bcnt > 0:
               ssize = self.format_float_value(cnts[bflg][1])
               dsfiles[bflg][dsid] = bfiles[bflg]
               bmsg = self.BACKMSG[bflg]
               s = 's' if bcnt > 1 else ''
               self.pglog("{}: {}({}) {}file{} found for {}".format(dsid, bcnt, ssize, cmsg, s, bmsg), self.DTLACT)
      
         if fcnt == 0 and logact:
            msg = '' if flgset else ", must set Backup Flag 'B' or 'D'"
            self.pglog("{}: No {}file found to backup{}".format(dsid, cmsg, msg), self.DTLACT)
   
      return fcnt

   # get web/saved files to backup for a given group condition and file option
   def get_group_files(self, dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts):
      rcnt = 0
      if self.PGBACK['chgdays'] > 0:
         return self.get_group_changed_files(dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts)
      else:
         return self.get_group_new_files(dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts)

   # get new web/saved files to backup for given dataset/group info
   def get_group_new_files(self, dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts):
      rcnt = 0
      if fopt&self.SOPT:
         cnd = dcnd
         if gcnd: cnd += ' AND ' + gcnd
         cnd += ' AND bid = 0'
         rcnt += self.get_group_saved_files('sfile', '*', cnd, bfiles, infiles, cnts)
      if fopt&self.WOPT:
         cnd = "bid = 0"
         if gcnd: cnd = gcnd + ' AND ' + cnd
         rcnt += self.get_group_web_files(dsid, None, '*', cnd, bfiles, infiles, cnts)
      return rcnt

   # get changed web/saved files to re-backup for given dataset/group info
   def get_group_changed_files(self, dsid, gcnd, dcnd, bfiles, fopt, infiles, cnts):
      rcnt = 0
      self.file_backup_status(None)
      if fopt&self.SOPT:
         cnd = 'sfile.' + dcnd
         if gcnd: cnd += ' AND sfile.' + gcnd
         tables = 'sfile join bfile on sfile.bid = bfile.bid AND sfile.date_modified > bfile.date_modified'
         rcnt += self.get_group_saved_files(tables, "bfile.bfile, sfile.*", cnd, bfiles, infiles, cnts)
      if fopt&self.WOPT:
         cnd = 'wfile.' + gcnd if gcnd else ''
         tjoin = 'join bfile on wfile.bid = bfile.bid AND wfile.date_modified > bfile.date_modified'
         rcnt += self.get_group_web_files(dsid, tjoin, "bfile.bfile, wfile.*", cnd, bfiles, infiles, cnts)
      return rcnt

   # get web data files for backup
   def get_group_web_files(self, dsid, tjoin, fields, cnd, bfiles, infiles, cnts):
      rcnt = 0 
      chgdays = self.PGBACK['chgdays']
      ifiles = infiles['W'] if infiles and infiles['W'] else None
      if tjoin:
         pgrecs = self.pgmget_wfile_join(dsid, tjoin, fields, cnd, self.LGWNEX)
      else:
         pgrecs = self.pgmget_wfile(dsid, fields, cnd, self.LGWNEX)
      cnt = len(pgrecs['wid']) if pgrecs else 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         if chgdays and self.file_backup_status(pgrec, chgdays) > 0: continue
         if ifiles and pgrec['wfile'] in ifiles: continue
         fsize = pgrec['data_size']
         if bfiles:
            bfiles['wrecs'].append(pgrec)
            bfiles['wcount'] += 1
         cnts[0] += 1
         cnts[1] += fsize
         rcnt += 1
      return rcnt

   # get saved data files for backup
   def get_group_saved_files(self, tables, fields, cnd, bfiles, infiles, cnts):
      rcnt = 0 
      chgdays = self.PGBACK['chgdays']
      ifiles = infiles['S'] if infiles and infiles['S'] else None
      pgrecs = self.pgmget(tables, fields, cnd, self.LGWNEX)
      cnt = len(pgrecs['sid']) if pgrecs else 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         if chgdays and self.file_backup_status(pgrec, chgdays) > 0: continue
         if ifiles and pgrec['sfile'] in ifiles: continue
         fsize = pgrec['data_size']
         if bfiles:
            bfiles['srecs'].append(pgrec)
            bfiles['scount'] += 1
         cnts[0] += 1
         cnts[1] += fsize
         rcnt += 1
      return rcnt

   # evaluate file stat on disk/object storage and modify RDADB record if not match
   def evaluate_file_stat(self, dsid, cate, pgrec):
      tname = cate + 'file'
      fname = pgrec[tname]
      chome = self.PGLOG['DECSHOME'] if cate == 's' else self.PGLOG['DSDHOME']
      if pgrec['locflag'] == 'O':
         bucket = 'gdex-decsdata' if cate == 's' else self.PGLOC['OBJCTBKT']
         ofile = self.join_paths(dsid, fname)
         info = self.check_object_file(ofile, bucket, 1, self.ERRACT)
         if not info: return False
         lfile = "{}/{}/{}/{}".format(chome, self.PGLOG['BACKUPEP'], dsid, fname)
         self.object_copy_local(lfile, ofile, bucket, self.ERRACT)
         cinfo = self.check_local_file(lfile, 32, self.ERRACT)
         if not cinfo: return False
         info['checksum'] = cinfo['checksum']
         lname = 'OBS'
      else:
         lfile = "{}/{}/".format(chome, dsid)
         if cate == 's': lfile += pgrec['type'] + '/'
         lfile += fname
         info = self.check_local_file(lfile, 33, self.ERRACT)
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
      difftime = self.cmptime(info['date_modified'], info['time_modified'], pgrec['date_modified'], pgrec['time_modified'])
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
         self.pglog(msg, self.LOGACT)
         cid = cate + 'id'
         fcnd = "{} = {}".format(cid, pgrec[cid])
         if cate == 'w':
            self.pgupdt_wfile(dsid, record, fcnd, self.LGWNEX)
         else:
            self.pgupdt(tname, record, fcnd, self.LGWNEX)
         for ckey in record:
            pgrec[ckey] = record[ckey]
      return True

   # get file backing up options (1 for saved and 2 for web, and 3 for both types)
   def get_backup_options(self, dsid, dcnd):
      fopt = 0
      bcnd = "= 0" if self.PGBACK['chgdays'] < 1 else "> 0"
   #   if self.pgget('sfile', 'sid', "{} AND bid {}".format(dcnd, bcnd), self.LGWNEX): fopt |= self.SOPT
      if self.pgget_wfile(dsid, 'wid', "bid " + bcnd, self.LGWNEX): fopt |= self.WOPT
      return fopt

   # gather all available dataset ids to backup data files
   def gather_dataset_files(self, dsfiles, unlock = True):
      fcnt = 0
      if self.dsids:
         for dsid in self.dsids:
            dcnd = "dsid = '{}'".format(dsid)
            pgrec = self.pgget("dataset", "dsid, backflag, pid", dcnd, self.LGWNEX)
            if pgrec:
               if unlock and pgrec['pid'] and self.lock_dataset(dsid, 0, self.LOGACT) < 1: continue
               fcnt += self.get_dataset_files(dsid, dsfiles, pgrec['backflag'], self.LOGWRN)
      else:
         dcnd = "ORDER BY dsid"
         pgrecs = self.pgmget("dataset", "dsid, backflag, pid", dcnd, self.LGWNEX)
         dcnt = len(pgrecs['dsid']) if pgrecs else 0
         for i in range(dcnt):
            dsid = pgrecs['dsid'][i]
            if unlock and pgrecs['pid'][i] and self.lock_dataset(dsid, 0, self.LOGACT) < 1: continue
            fcnt += self.get_dataset_files(dsid, dsfiles, pgrecs['backflag'][i])
      if dsfiles:
         s = 's' if fcnt > 1 else ''
         bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup' 
         cmsg = 'Changed ' if self.PGBACK['chgdays'] else ''
         self.pglog("{} GDEX {}file{} found ready to {}".format(fcnt, cmsg, s, bmsg), self.LOGACT)
      return fcnt

   # gather all available backup file records with status N to backup
   def gather_dataset_infiles(self, dsfiles):
      icnt = fcnt = cnt = 0
      bcnd = "status = 'N'"
      ocnd = " ORDER BY dsid"
      flds = "bid, dsid, bfile, type, data_size size, (scount + wcount) fcnt, dsids, note"
      if self.PGBACK['backflag']: bcnd += " AND type = '{}'".format(self.PGBACK['backflag'])
      if self.dsids:
         for dsid in self.dsids:
            dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
            pgrecs = self.pgmget("bfile", flds, dcnd, self.LGWNEX)
            bcnt = len(pgrecs['bid']) if pgrecs else 0
            for i in range(bcnt):
               cnt = self.get_backup_infile(dsfiles, self.onerecord(pgrecs, i))
               if cnt:
                  icnt +=1
                  fcnt += cnt
      else:
         pgrecs = self.pgmget("bfile", flds, bcnd+ocnd, self.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            cnt = self.get_backup_infile(dsfiles, self.onerecord(pgrecs, i))
            if cnt:
               icnt +=1
               fcnt += cnt
      if dsfiles:
         s = 's' if icnt > 1 else ''
         bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup' 
         self.pglog("{} input file{} found ready to {}".format(icnt, s, bmsg), self.LOGACT)
      return fcnt

   # gather all available backup file records with status T to backup
   #
   def gather_dataset_tarfiles(self, dsfiles):
      tcnt = fcnt = cnt = 0
      bcnd = "status = 'T'"
      ocnd = " ORDER BY dsid"
      flds = "bid, dsid, bfile, type, data_size size, (scount + wcount) fcnt, note"
      if self.PGBACK['backflag']: bcnd += " AND type = '{}'".format(self.PGBACK['backflag'])
      if self.dsids:
         for dsid in self.dsids:
            dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
            pgrecs = self.pgmget("bfile", flds, dcnd, self.LGWNEX)
            bcnt = len(pgrecs['bid']) if pgrecs else 0
            for i in range(bcnt):
               cnt = self.get_backup_tarfile(dsfiles, self.onerecord(pgrecs, i))
               if cnt:
                  tcnt +=1
                  fcnt += cnt
      else:
         pgrecs = self.pgmget("bfile", flds, bcnd+ocnd, self.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            cnt = self.get_backup_tarfile(dsfiles, self.onerecord(pgrecs, i))
            if cnt:
               tcnt +=1
               fcnt += cnt
      s = 's' if tcnt > 1 else ''
      bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup' 
      self.pglog("{} tarred file{} found ready to {}".format(tcnt, s, bmsg), self.LOGACT)
      return fcnt

   # get a backup file with input files set for quasar backup
   def get_backup_infile(self, dsfiles, pgrec):
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
      if self.PGBACK['action']&self.CINACT: ret = fcnt
      if not dsfiles: return ret
      dsids = [dsid]
   #   if not (pgrec['note'] or self.rebuild_file_note(pgrec, dsids)): return 0
      if not pgrec['note']:
         return self.pglog(bfile + ": Miss note for N backup file", self.ERRACT)
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
            if self.PGBACK['action']&self.CTACTS and not op.isfile(infile):
               fd = open(infile, 'w')
               self.pglog("{}: Recreate missing dsarch input file in {}".format(infile, self.PGBACK['workdir']), self.DTLACT)
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

   # get a tarred backup file for quasar backup
   def get_backup_tarfile(self, dsfiles, pgrec):
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
      if self.PGBACK['action']&self.CINACT: ret = fcnt
      if not dsfiles: return ret
      dsids = [dsid]
   #   if not (pgrec['note'] or self.rebuild_file_note(pgrec, dsids)): return 0
      if not pgrec['note']:
         return self.pglog(bfile + ": Miss note for T backup file", self.ERRACT)
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
      fromfile = self.get_local_globus_file(ftype, bid, dsid, bfile, bflg)
      if not fromfile: return 0
      tofile = "/{}/{}".format(dsid, bfile)
      dsfiles[bflg][bid] = {'bfile' : bfile, 'fcnt' : fcnt, 'size' : pgrec['size'],
                            'dsids' : dsids, 'tofile' : tofile, 'fromfile' : fromfile}
      return ret
   
   # build fromfile name at Globus endpoint gdex-glade
   def get_local_globus_file(self, ftype, bid, dsid, bfile, backflag):
      endpath = 'decsdata' if ftype == 'S' else 'data'
      fromfile = "/{}/gdex-quasar/{}/{}".format(endpath, dsid, op.basename(bfile))
      tarfile = self.PGLOG['DSSDATA'] + fromfile
      if self.PGBACK['action'] == self.STTACT or self.check_local_file(tarfile, 0, self.LGEREX): return fromfile
      amsg = self.ACTMSG[self.BCKACT]
      bmsg = self.BACKMSG[backflag]
      self.pglog("{}: Miss local {} file for {}\n{}: Change file status to 'N' to recreate".format(fromfile, bmsg, amsg, bfile), self.DTLACT)
      self.pgexec("UPDATE bfile SET status = 'N' WHERE bid = {}".format(bid), self.LGEREX)
      return None

   # cache the Web/Saved files in type N bfiles (included in input files) already
   def cache_dataset_infiles(self, dsid):
      incnd = "status = 'N' AND (dsid = '{}' or dsids LIKE '%{}%')".format(dsid, dsid)
      pgrecs = self.pgmget('bfile', 'note', incnd, self.LGEREX)
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
      if self.PGBACK['action'] == self.CINACT:
         s = 's' if fcnt > 1 else ''
         amsg = self.ACTMSG[self.CINACT]
         self.pglog("{}-{}: Skip {}/{} Saved/Web file{} already listed in input files".format(dsid, amsg, cnts['S'], cnts['W'], s), self.DTLACT)
      return bckfiles

   # process bfiles to check sizes between db and backup servers, set status to N if different
   def process_dataset_chkfiles(self, dsfiles, backflag):
      bfiles = dsfiles[backflag]
      bcnt = len(bfiles)
      if not bcnt: return
      amsg = self.ACTMSG[self.CHKACT]
      bmsg = self.BACKMSG[backflag]
      s = 's' if bcnt > 1 else ''
      self.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), self.WARNLG)
      qinfo = {'backflag' : backflag, 'bid' : 0, 'dsid' : None, 'size' : 0, 'bfile' : None,
               'bqfiles' : {}, 'dqfiles' : {}, 'qdsids' : [], 'qcnt' : 0, 'ncnt' : 0}
      for bid in bfiles:
         qinfo['bid'] = bid
         binfo = bfiles[bid]
         if qinfo['dsid'] and binfo['dsid'] != qinfo['dsid']:
            qinfo['bqfiles'] = {}
            qinfo['dqfiles'] = {}
         for bkey in binfo: qinfo[bkey] = binfo[bkey]
         self.process_one_quasar_chkfile(qinfo)
      qcnt = qinfo['qcnt']
      if qcnt > 0:
         s = 's' if qcnt > 1 else ''
         ncnt = qinfo['ncnt']
         dcnt = len(qinfo['qdsids'])
         dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         fmsg = "for {} of {} {} file{} of {}".format(ncnt, qcnt, bmsg, s, dmsg)
         self.pglog("{}: Set status to 'N' {}".format(amsg, fmsg), self.LOGACT)

   # check sizes between db and backup servers for one backup file, set status to N if different
   def process_one_quasar_chkfile(self, qinfo):
      if self.PGSIG['QUIT']: self.quit_dsquasar(qinfo)
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
      amsg = self.ACTMSG[self.CHKACT]
      bmsg = self.BACKMSG[bflg]
      sdsize = self.format_float_value(dsize)
      logact = self.LGEREX
      qmsg = None
      if bflg == 'D':
         endpoint = self.QPOINTS[bflg]
         qfiles = qinfo['dqfiles']
         if qpath not in qfiles: qfiles[qpath] = self.backup_glob(qpath, endpoint, 0, logact)
         info = qfiles[qpath][pfile] if qfiles[qpath] and pfile in qfiles[qpath] else None
         if not info:
            qmsg = "{}: Miss {} file {}-{}".format(amsg, bmsg, endpoint, qfile)
         elif dsize != info['data_size']:
            sqsize = self.format_float_value(info['data_size'])
            qmsg = "{}: Miss-match {} files {}({})/{}-{}({})".format(amsg, bmsg, dfile, sdsize, endpoint, qfile, sqsize)
      if not qmsg:
         endpoint = self.QPOINTS['B']
         qfiles = qinfo['bqfiles']
         if qpath not in qfiles: qfiles[qpath] = self.backup_glob(qpath, endpoint, 0, logact)
         info = qfiles[qpath][pfile] if qfiles[qpath] and pfile in qfiles[qpath] else None
         if not info:
            qmsg = "{}: Miss {} file {}-{}".format(amsg, bmsg, endpoint, qfile)
         elif dsize != info['data_size']:
            sqsize = self.format_float_value(info['data_size'])
            qmsg = "{}: Miss-match {} files {}({})/{}-{}({})".format(amsg, bmsg, dfile, sdsize, endpoint, qfile, sqsize)
      if qmsg:
         self.pglog(qmsg, self.DTLACT)
         self.pgexec("UPDATE bfile SET status = 'N' WHERE bid = {}".format(bid), logact)
         qinfo['ncnt'] += 1
      # reset qinfo after quasar backup
      qinfo['qcnt'] += 1
      if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)   
      if self.PGBACK['pstep']: self.set_dsquasar_progress(1, dsize)

   # get all available backup files records for given datasets
   def gather_dataset_bckfiles(self, dsfiles, getnote = True):
      bcnd = "status = 'A'"
      ocnd = " ORDER BY dsid"
      FLDS = ['dsid', 'size', 'bfile']
      flds = "bid, dsid, bfile, type, data_size size"
      if getnote:
         FLDS.append('fcnt')
         FLDS.append('note')
         flds += ", (scount + wcount) fcnt, note"
      if self.PGBACK['backflag']: bcnd += " AND type = '{}'".format(self.PGBACK['backflag'])
      if self.dsids:
         fcnt = 0
         for dsid in self.dsids:
            dcnd = "(dsid = '{}' OR dsids LIKE '%{}%') AND {}".format(dsid, dsid, bcnd)
            if dsfiles:
               pgrecs = self.pgmget("bfile", flds, dcnd, self.LGWNEX)
               bcnt = len(pgrecs['bid']) if pgrecs else 0
               for i in range(bcnt):
                  pgrec = self.onerecord(pgrecs, i)
                  type = pgrec['type']
                  bid = pgrec['bid']
                  if bid not in dsfiles[type]:
                     dsfiles[type][bid] = {fld : pgrec[fld] for fld in FLDS}
                     fcnt += 1
            else:
               fcnt += self.pgget("bfile", '', dcnd, self.LGWNEX)
      else:
         if dsfiles:
            pgrecs = self.pgmget("bfile", flds, bcnd+ocnd, self.LGWNEX)
            fcnt = len(pgrecs['bid']) if pgrecs else 0
            for i in range(fcnt):
               pgrec = self.onerecord(pgrecs, i)
               dsfiles[pgrec['type']][pgrec['bid']] = {fld : pgrec[fld] for fld in FLDS}
         else:
            fcnt = self.pgget("bfile", '', bcnd, self.LGWNEX)
      if dsfiles:
         s = 's' if fcnt > 1 else ''
         amsg = self.ACTMSG[self.PGBACK['action']]
         bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup'
         self.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), self.LOGACT)
      return fcnt

   # process bfiles to add leading Gnnn path onto Quasar Backup and/or Drdata endpoints
   def process_dataset_pathfiles(self, dsfiles, backflag):
      bfiles = dsfiles[backflag]
      bcnt = len(bfiles)
      if not bcnt: return
      amsg = self.ACTMSG[self.PTHACT]
      bmsg = self.BACKMSG[backflag]
      s = 's' if bcnt > 1 else ''
      self.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), self.WARNLG)
      qinfo = {'backflag' : backflag, 'bid' : 0, 'dsids' : [], 'fcnt' : 0, 'size' : 0,
               'bfile' : None, 'pfile' : None, 'qdsids' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}
      for bid in bfiles:
         qinfo['bid'] = bid
         binfo = bfiles[bid]
         for bkey in binfo: qinfo[bkey] = binfo[bkey]
         self.process_one_quasar_pathfile(qinfo)
      qcnt = qinfo['qcnt']
      if qcnt > 0:
         s = 's' if qcnt > 1 else ''
         fcnt = qinfo['qfcnt']
         dcnt = len(qinfo['qdsids'])
         ssize = self.format_float_value(qinfo['qsize'])
         dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         fmsg = "file{} for {}({}) files of {}".format(s, fcnt, ssize, dmsg)
         self.pglog("{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg), self.LOGACT)

   # backup one Quasar Backup or Backup&Drdata from one or multiple inputs and,
   # reset the quasar backup dict
   def process_one_quasar_pathfile(self, qinfo):
      ccnt = self.check_child(None, 0, self.LOGWRN, -1) if self.PGBACK['mproc'] > 1 else 0
      if self.PGSIG['QUIT']: self.quit_dsquasar(qinfo)
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
      amsg = self.ACTMSG[self.PTHACT]
      bmsg = self.BACKMSG[bflg]
      ssize = self.format_float_value(fsize)
      dmsg = dsid if dcnt == 1 else "{} datasets".format(dcnt)
      qmsg = "{}: Try {}, {} file for {}({}) file{} of {}".format(amsg, pfile, bmsg, fcnt, ssize, s, dmsg)
      if ccnt > 0:
         stat = self.start_child("dsquasar_{}".format(bid), self.LOGWRN, 1)  # try to start a child process
         if stat <= 0:
            if self.PGSIG['QUIT']: self.quit_dsquasar(qinfo)
            sys.exit(1)   # something wrong
         elif self.PGSIG['PPID'] <= 1:
            self.pgdisconnect()  # disconnect database for reconnection
            self.pglog("Started a process for " + qmsg, self.LOGWRN)
      else:
         self.pglog(qmsg, self.LOGWRN)
      logact = self.OVRIDE|self.LOGWRN
      bstat = dstat = -1
      if ccnt == 0 or self.PGSIG['PPID'] > 1:
         if bflg == 'D':
            dstat = self.move_backup_file(tofile, fromfile, 'gdex-quasar-drdata', logact)
            if not dstat: self.pglog("Error Quaser Drdata for " + qmsg, self.LOGERR)
         bstat = self.move_backup_file(tofile, fromfile, 'gdex-quasar', logact)
         if not bstat: self.pglog("Error Quaser Backup for " + qmsg, self.LOGERR)
         if dstat and bstat:
            self.pgexec("UPDATE bfile SET bfile = '{}' WHERE bid = {}".format(pfile, bid), self.LGEREX)
         else:
            self.PGBACK['errcnt'] += 1
            if self.PGBACK['errcnt'] > self.PGBACK['maxcnt']: self.quit_dsquasar(qinfo)
            time.sleep(self.PGSIG['ETIME'])
      if self.PGSIG['PPID'] > 1: sys.exit(0)   # stop child process
      if dstat and bstat:
         # reset qinfo after quasar backup
         qinfo['qcnt'] += 1
         qinfo['qfcnt'] += fcnt
         qinfo['qsize'] += fsize
         for dsid in dsids:
            if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)
      if self.PGBACK['pstep']: self.set_dsquasar_progress(1, fsize)

   # get all available backup file records without leading paths
   def gather_dataset_pathfiles(self, dsfiles):
      fcnt = 0
      bcnd = "status = 'A' AND bfile not LIKE 'G%/%.tar'"
      ocnd = " ORDER BY dsid"
      flds = "bid, dsid, bfile, type, data_size size, disp_order, (scount + wcount) fcnt, note"
      if self.PGBACK['backflag']: bcnd += " AND type = '{}'".format(self.PGBACK['backflag'])
      if self.dsids:
         for dsid in self.dsids:
            dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
            pgrecs = self.pgmget("bfile", flds, dcnd, self.LGWNEX)
            bcnt = len(pgrecs['bid']) if pgrecs else 0
            for i in range(bcnt):
               fcnt += self.get_backup_pathfile(dsfiles, self.onerecord(pgrecs, i))
      else:
         pgrecs = self.pgmget("bfile", flds, bcnd+ocnd, self.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            fcnt += self.get_backup_pathfile(dsfiles, self.onerecord(pgrecs, i))
      s = 's' if fcnt > 1 else ''
      amsg = self.ACTMSG[self.PTHACT]
      bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup'
      self.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), self.DTLACT)
      return fcnt

   # get a archived file for adding Gnnn path
   def get_backup_pathfile(self, dsfiles, pgrec):
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
      pfile = "G{:03}/{}".format(int((pgrec['disp_order']+self.SUBLMTS-1)/self.SUBLMTS), bfile)
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

   # process bfile records to add dsids string
   def process_dataset_dsidfiles(self, dsfiles, backflag):
      bfiles = dsfiles[backflag]
      bcnt = len(bfiles)
      if not bcnt: return
      amsg = self.ACTMSG[self.IDSACT]
      bmsg = self.BACKMSG[backflag]
      s = 's' if bcnt > 1 else ''
      self.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), self.WARNLG)
      qinfo = {'backflag' : backflag, 'bid' : 0, 'dsids' : [], 'fcnt' : 0, 'size' : 0,
               'qdsids' : [], 'qfcnt' : 0, 'qsize' : 0, 'qcnt' : 0}
      for bid in bfiles:
         qinfo['bid'] = bid
         binfo = bfiles[bid]
         for bkey in binfo: qinfo[bkey] = binfo[bkey]
         self.process_one_quasar_dsidfile(qinfo)
      qcnt = qinfo['qcnt']
      if qcnt > 0:
         s = 's' if qcnt > 1 else ''
         fcnt = qinfo['qfcnt']
         dcnt = len(qinfo['qdsids'])
         ssize = self.format_float_value(qinfo['qsize'])
         dmsg = qinfo['qdsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         fmsg = "file{} for {}({}) files of {}".format(s, fcnt, ssize, dmsg)
         self.pglog("{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg), self.LOGACT)

   # add dsids string to a quasar backup file record
   def process_one_quasar_dsidfile(self, qinfo):
      dsids = qinfo['dsids']
      bid = qinfo['bid']
      fcnt = qinfo['fcnt']
      fsize = qinfo['size']
      dsstr = ','.join(dsids[1:])
      stat = self.pgexec("UPDATE bfile SET dsids = '{}' WHERE bid = {}".format(dsstr, bid), self.LGEREX)
      if stat:
         # reset qinfo after quasar backup
         qinfo['qcnt'] += 1
         qinfo['qfcnt'] += fcnt
         qinfo['qsize'] += fsize
         for dsid in dsids:
            if dsid not in qinfo['qdsids']: qinfo['qdsids'].append(dsid)
      if self.PGBACK['pstep']: self.set_dsquasar_progress(1, fsize)

   # get all available backup file records without NULL dsids
   def gather_dataset_dsidfiles(self, dsfiles):
      fcnt = 0
      bcnd = "status = 'A' AND dsids IS NULL"
      ocnd = " ORDER BY dsid"
      flds = "bid, dsid, bfile, type, data_size size , disp_order, (scount + wcount) fcnt, note"
      if self.PGBACK['backflag']: bcnd += " AND type = '{}'".format(self.PGBACK['backflag'])
      if self.dsids:
         for dsid in self.dsids:
            dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
            pgrecs = self.pgmget("bfile", flds, dcnd, self.LGWNEX)
            bcnt = len(pgrecs['bid']) if pgrecs else 0
            for i in range(bcnt):
               fcnt += self.get_backup_dsidfile(dsfiles, self.onerecord(pgrecs, i))
      else:
         pgrecs = self.pgmget("bfile", flds, bcnd+ocnd, self.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            fcnt += self.get_backup_dsidfile(dsfiles, self.onerecord(pgrecs, i))
      s = 's' if fcnt > 1 else ''
      amsg = self.ACTMSG[self.IDSACT]
      bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup'
      self.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), self.DTLACT)
      return fcnt

   # get a archived file for adding dsids
   def get_backup_dsidfile(self, dsfiles, pgrec):
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

   # process bfile records to add md5 checksum strings
   def process_dataset_mcsfiles(self, dsfiles, backflag):
      bfiles = dsfiles[backflag]
      bcnt = len(bfiles)
      if not bcnt: return
      amsg = self.ACTMSG[self.MCSACT]
      bmsg = self.BACKMSG[backflag]
      s = 's' if bcnt > 1 else ''
      self.pglog("{}: {} {} file{}...".format(amsg, bcnt, bmsg, s), self.WARNLG)
      qinfo = {'dsids' : [], 'fcnt' : 0, 'mcnt' : 0, 'fsize' : 0, 'msize' : 0}
      qcnt = 0
      for bid in bfiles:
         qcnt += self.process_one_quasar_mcsfile(bid, bfiles[bid], qinfo)
      if qcnt > 0:
         s = 's' if qcnt > 1 else ''
         fcnt = qinfo['fcnt']
         mcnt = qinfo['mcnt']
         dcnt = len(qinfo['dsids'])
         fsize = self.format_float_value(qinfo['fsize'])
         msize = self.format_float_value(qinfo['msize'])
         dmsg = qinfo['dsids'][0] if dcnt == 1 else "{} datasets".format(dcnt)
         fmsg = "file{} for {}({}) of {}({}) files of {}".format(s, mcnt, msize, fcnt, fsize, dmsg)
         self.pglog("{}: {} {} {}".format(amsg, qcnt, bmsg, fmsg), self.LOGACT)

   # add a md5 checksum string to a quasar backup file record
   def process_one_quasar_mcsfile(self, bid, binfo, qinfo):
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
               pgrec = self.pgget(tname, fields, fcnd.format(dsid, type, tname, fname), self.LGWNEX)
               if (pgrec and pgrec['checksum'] and pgrec['size'] == size and 
                   self.cmptime(binfo['date'], binfo['time'], pgrec['date'], pgrec['time']) >= 0):
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
      if self.pgupdt('bfile', record, bcnd, self.LGEREX):
         qinfo['fcnt'] += binfo['fcnt']
         qinfo['fsize'] += binfo['size']
         qinfo['mcnt'] += mcnt
         qinfo['msize'] += msize
         for dsid in dsids:
            if dsid not in qinfo['dsids']: qinfo['dsids'].append(dsid)
         ret = 1
      if self.PGBACK['pstep']: self.set_dsquasar_progress(1, binfo['size'])
      return ret

   # get all available backup file records without md5 checksums
   def gather_dataset_mcsfiles(self, dsfiles):
      fcnt = 0
      bcnd = "status = 'A' AND note NOT LIKE '%<:>MC<:>%'"
      ocnd = " ORDER BY dsid"
      flds = "bid, type, data_size size, (scount + wcount) fcnt, date_modified, time_modified, note"
      if self.dsids:
         for dsid in self.dsids:
            dcnd = "dsid = '{}' AND {}".format(dsid, bcnd)
            pgrecs = self.pgmget("bfile", flds, dcnd, self.LGWNEX)
            bcnt = len(pgrecs['bid']) if pgrecs else 0
            for i in range(bcnt):
               self.get_backup_mcsfile(dsfiles, self.onerecord(pgrecs, i))
            fcnt += bcnt
      else:
         pgrecs = self.pgmget("bfile", flds, bcnd+ocnd, self.LGWNEX)
         bcnt = len(pgrecs['bid']) if pgrecs else 0
         for i in range(bcnt):
            self.get_backup_mcsfile(dsfiles, self.onerecord(pgrecs, i))
         fcnt += bcnt
      s = 's' if fcnt > 1 else ''
      amsg = self.ACTMSG[self.MCSACT]
      bmsg = self.BACKMSG[self.PGBACK['backflag']] if self.PGBACK['backflag'] else 'backup'
      self.pglog("{} {} file{} found to {}".format(fcnt, bmsg, s, amsg), self.DTLACT)
      return fcnt

   # get an archived file for adding md5 checksum
   def get_backup_mcsfile(self, dsfiles, pgrec):
      dsfiles[pgrec['type']][pgrec['bid']] = {'note' : pgrec['note'], 'fcnt' : pgrec['fcnt'], 'size' : pgrec['size'],
                                              'date' : pgrec['date_modified'], 'time' : pgrec['time_modified']}

   # rebuild missed file note 
   def rebuild_file_note(self, pgrec, dsids):
      bid = pgrec['bid']
      fields = 'file, dsid, type, data_size, checksum'
      bfiles = {dsids[0] : {'S' : [], 'W' : []}}
      pgrecs = self.pgmget('sfile', 's' + fields, "bid = {} ORDER BY dsid, sfile".format(bid), self.LGEREX)
      cnt = len(pgrecs['sfile']) if pgrecs else 0
      for i in range(cnt):
         dsid = pgrecs['dsid'][i]
         if dsid not in dsids:
            dsids.append(dsid)
            bfiles[dsid] = {'S' : [], 'W' : []}
         bfiles[dsid]['S'].append([pgrecs['sfile'][i], pgrecs['type'][i], pgrecs['data_size'][i], pgrecs['checksum'][i]])
      pgrecs = self.pgmget('wfile', 'w' + fields, "bid = {} ORDER BY dsid, wfile".format(bid), self.LGEREX)
      cnt = len(pgrecs['wfile']) if pgrecs else 0
      for i in range(cnt):
         dsid = pgrecs['dsid'][i]
         if dsid not in dsids:
            dsids.append(dsid)
            bfiles[dsid] = {'S' : [], 'W' : []}
         bfiles[dsid]['W'].append([pgrecs['wfile'][i], pgrecs['type'][i], pgrecs['data_size'][i], pgrecs['checksum'][i]])
      # create note
      note = ''
      for dsid in bfiles:
         for ftype in bfiles[dsid]:
            files = bfiles[dsid][ftype]
            if not files: continue
            note += "<{}_{}_{}.txt>\n".format(dsid, ftype, bid)
            note += "DS<=>{}\n{}F<:>{}T<:>SZ<:>MC<:>\n".format(dsid, ftype, ftype)
            for flist in files:
               note += "{}<:>{}<:>{}<:>{}<:>\n".format(flist[0], flist[1], flist[2], flist[3])
      if note:
         self.pgexec("UPDATE bfile SET note = '{}' WHERE bid = {}".format(note, bid), self.LGEREX)
         pgrec['note'] = note
         return 1
      return 0

   # dump statistics for GDEX files available to create input files
   def dump_dataset_files(self, dsfiles, backflag):
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
      cmsg = 'Changed ' if self.PGBACK['chgdays'] else ''
      bmsg = self.BACKMSG[backflag]
      if scount > 0:
         dcnt = len(sdsids)
         dmsg = sdsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
         strsize = self.format_float_value(ssize)
         msg = "{}({}) {}Saved files of {} ready for {}".format(scount, strsize, cmsg, dmsg, bmsg)
         self.pglog(self.INDENT + msg, self.LOGACT)
      if wcount > 0:
         dcnt = len(wdsids)
         dmsg = wdsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
         strsize = self.format_float_value(wsize)
         msg = "{}({}) {}Web files of {} ready for {}".format(wcount, strsize, cmsg, dmsg, bmsg)
         self.pglog(self.INDENT + msg, self.LOGACT)

   # GDEX files included in input files
   def dump_dataset_infiles(self, dsfiles, backflag):
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
      bmsg = self.BACKMSG[backflag]
      dcnt = len(dsids)
      ssize = self.format_float_value(size)
      dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
      msg = "{}({}) Input files for {} GDEX files of {} to be tarred for {}".format(bcnt, ssize, fcnt, dmsg, bmsg)
      self.pglog(self.INDENT + msg, self.LOGACT)

   # tarred GDEX files to backup
   def dump_dataset_tarfiles(self, dsfiles, backflag):
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
      ssize = self.format_float_value(size)
      bmsg = self.BACKMSG[backflag]
      dmsg = dsids[0] if dcnt == 1 else "{} datasets".format(dcnt)
      msg = "{} ({}) Tarred files for {} GDEX files of {} for {}".format(bcnt, ssize, fcnt, dmsg, bmsg)
      self.pglog(self.INDENT + msg, self.LOGACT)

   # Quasar files backed up already and file counts deleted or moved
   def dump_dataset_bckfiles(self, dsfiles, backflag):
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
         pcnt += self.count_changed_files(bid, binfo, qinfo)
         if self.PGBACK['pstep']:
            cnt += 1
            size += binfo['size']
            if cnt == self.DSTEP:
               self.set_dsquasar_progress(cnt, size)
               cnt = size = 0
      if cnt: self.set_dsquasar_progress(cnt, size)
      dscnt = len(qinfo['dsids'])
      ssize = self.format_float_value(qinfo['size'])
      bmsg = self.BACKMSG[backflag]
      dmsg = qinfo['dsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
      msg = "{} ({}) {} files for {} GDEX files of {}".format(bcnt, ssize, bmsg, qinfo['fcnt'], dmsg)
      self.pglog(self.INDENT + msg, self.LOGACT)
      indent = self.INDENT + self.INDENT
      if qinfo['ncnt'] > 0:
         dscnt = len(qinfo['ndsids'])
         dmsg = qinfo['ndsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
         msg = "{} {} files Missing Note fields of {}".format(bcnt, bmsg, dmsg)
         self.pglog(indent + msg, self.LOGACT)
      msg = "{} GDEX files Changed after {}".format(pcnt, bmsg)
      self.pglog(indent + msg, self.LOGACT)
      if pcnt == 0: return
      if qinfo['ccnt'] > 0:
         dscnt = len(qinfo['cdsids'])
         dmsg = qinfo['cdsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
         ssize = self.format_float_value(qinfo['csize'])
         msg = "{} ({}) GDEX file sizes Changed for {}".format(qinfo['ccnt'], ssize, dmsg)
         self.pglog(indent + msg, self.LOGACT)
      if qinfo['ucnt'] > 0:
         dscnt = len(qinfo['udsids'])
         dmsg = qinfo['udsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
         ssize = self.format_float_value(qinfo['usize'])
         msg = "{} ({}) GDEX files Updated & Re-done {} for {}".format(qinfo['ucnt'], ssize, bmsg, dmsg)
         self.pglog(indent + msg, self.LOGACT)
      if qinfo['dcnt'] > 0:
         dscnt = len(qinfo['ddsids'])
         dmsg = qinfo['ddsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
         ssize = self.format_float_value(qinfo['dsize'])
         msg = "{} ({}) GDEX files Got Deleted for {}".format(qinfo['dcnt'], ssize, dmsg)
         self.pglog(indent + msg, self.LOGACT)
      if qinfo['mcnt'] > 0:
         dscnt = len(qinfo['mdsids'])
         dmsg = qinfo['mdsids'][0] if dscnt == 1 else "{} datasets".format(dscnt)
         ssize = self.format_float_value(qinfo['msize'])
         msg = "{} ({}) GDEX files Moved for {}".format(qinfo['mcnt'], ssize, dmsg)
         self.pglog(indent + msg, self.LOGACT)

   # count cache the Web/Saved files in type A bfiles (archived) already
   def count_changed_files(self, bid, binfo, qinfo):
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
            pgrec = self.pgget_wfile(rinfo[1], 'bid, data_size', cnd, self.LGEREX)
         else:
            cnd = "sfile = '{}' AND dsid = '{}'".format(fname, rinfo[1])
            pgrec = self.pgget('sfile', 'bid, data_size', cnd, self.LGEREX)
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

# main function to excecute this script
def main():
   object = DsQuasar()
   object.read_parameters()
   object.start_actions()
   sys.exit(0)

# call main() to start program
if __name__ == "__main__": main()
