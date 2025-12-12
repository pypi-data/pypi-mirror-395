###############################################################################
#
#     Title : pg_check.py
#    Author : Zaihua Ji,  zji@ucar.edu
#      Date : 08/26/2020
#             2025-02-10 transferred to package rda_python_dscheck from
#             https://github.com/NCAR/rda-shared-libraries.git
#             2025-12-04 convert to class PgOPT
#   Purpose : python library module for for holding some global variables and
#             functions for dscheck utility
#
#    Github : https://github.com/NCAR/rda-python-dscheck.git
#
###############################################################################
#
import os
import re
import time
from rda_python_common.pg_cmd import PgCMD
from rda_python_common.pg_opt import PgOPT

class PgCheck(PgOPT, PgCMD):

   def __init__(self):
      super().__init__()  # initialize parent class
      self.LOOP = 0
      self.PLIMITS = {}
      self.DWHOSTS = {}     # hosts are down
      self.RUNPIDS = {}
      self.SHELLS = {}      # shell names used by specialists
      # define initially the needed option values
      self.OPTS.update({
         'PC' : [0x0004, 'ProcessCheck',    1],
         'AC' : [0x0008, 'AddCheck',        1],
         'GD' : [0x0010, 'GetDaemon',       0],
         'SD' : [0x0020, 'SetDaemon',       1],
         'GC' : [0x0040, 'GetCheck',        0],
         'DL' : [0x0080, 'Delete',          1],
         'UL' : [0x0100, 'UnLockCheck',     1],
         'EC' : [0x0200, 'EmailCheck',      0],
         'IC' : [0x0400, 'InterruptCheck',  1],
         'CH' : [0x1000, 'CheckHost',       0],
         'SO' : [0x1000, 'SetOptions',      1],      
         'AW' : [0, 'AnyWhere',      0],
         'BG' : [0, 'BackGround',    0],
         'CP' : [0, 'CheckPending',  0],
         'CS' : [0, 'CheckStatus',   0],
         'FI' : [0, 'ForceInterrrupt', 0],
         'FO' : [0, 'FormatOutput',  0],
         'LO' : [0, 'LogOn',         0],
         'MD' : [0, 'PgDataset',     3],
         'NC' : [0, 'NoCommand',     0],
         'ND' : [0, 'NewDaemon',     0],
         'NT' : [0, 'NoTrim',        0],
         'WR' : [0, 'WithdsRqst',    0],
         'WU' : [0, 'WithdsUpdt',    0],
         'DM' : [1, 'DaemonMode',    1],  # for action PC, start|quit|logon|logoff
         'DV' : [1, 'Divider',       1],  # default to <:>
         'ES' : [1, 'EqualSign',     1],  # default to <=>
         'FN' : [1, 'FieldNames',     0],
         'LH' : [1, 'LocalHost',      0,  ''],
         'MT' : [1, 'MaxrunTime',     0],
         'OF' : [1, 'OutputFile',     0],
         'ON' : [1, 'OrderNames',     0],
         'AO' : [1, 'ActOption',      1],  # default to <!>
         'WI' : [1, 'WaitInterval',   1],
         'AN' : [2, 'ActionName',     0],
         'AV' : [2, 'ArgumentVector', 0],
         'AX' : [2, 'ArgumenteXtra',  0],
         'CC' : [2, 'CarbonCopy',     0],
         'CD' : [2, 'CheckDate',    256],
         'CI' : [2, 'CheckIndex',    16],
         'CM' : [2, 'Command',        1],
         'CT' : [2, 'CheckTime',     32],
         'DB' : [2, 'Debug',          0],
         'DC' : [2, 'DoneCount',     17],
         'DF' : [2, 'DownFlags',      1],
         'DI' : [2, 'DaemonIndex',   16],
         'DS' : [2, 'Dataset',        1],
         'ER' : [2, 'ERrormessage',   0],
         'EV' : [2, 'Environments',   1],
         'FC' : [2, 'FileCount',     17],
         'HN' : [2, 'HostName',       1],
         'IF' : [2, 'InputFile',      0],
         'MC' : [2, 'MaxCount',      17],
         'MH' : [2, 'MatchHost',      1],
         'MO' : [2, 'Modules',        1],
         'PI' : [2, 'ParentIndex',   17],
         'PL' : [2, 'ProcessLimit',  17],
         'PO' : [2, 'Priority',      17],
         'PQ' : [2, 'PBSQueue',       0],
         'QS' : [2, 'QSubOptions',    0],
         'SN' : [2, 'Specialist',     1],
         'ST' : [2, 'Status',         0],
         'SZ' : [2, 'DataSize',      16],
         'TC' : [2, 'TryCount',      17],
         'WD' : [2, 'WorkDir',        0],
      })
      self.ALIAS.update({
         'AN' : ['Action'],
         'BG' : ['b'],
         'CF' : ['Confirmation', 'ConfirmAction'],
         'CM' : ['CommandName'],
         'DL' : ['RM', 'Remove'],
         'DS' : ['Dsid', 'DatasetID'],
         'DV' : ['Delimiter', 'Separater'],
         'EV' : ['Envs'],
         'GZ' : ['GMT', 'GreenwichZone', 'UTC'],
         'MC' : ['MaximumCount', 'MaxTryCount'],
         'MH' : ['MatchHostname'],
         'NC' : ['NoRemoteCommand'],
         'MO' : ['Mods'],
         'PI' : ['ParentCheckIndex'],
         'QS' : ['PBSOptions'],
         'SO' : ['SetBatchOptions'],
         'SZ' : ['Size', "ProcSize"],
         'UL' : ['UnLock'],
         'WD' : ["WorkDirectory"],
         'WR' : ["WithRequest"],
         'WU' : ["WithUpdate"],
      })
      self.TBLHASH['dscheck'] = {
        #SHORTNM KEYS DBFIELD
         'C' : ['CI', "cindex",         0],
         'O' : ['CM', "command",        1],
         'V' : ['AV', "argv",           1],
         'T' : ['DS', "dsid",           1],
         'A' : ['AN', "action",         1],
         'U' : ['ST', "status",         1],
         'P' : ['PQ', "pbsqueue",       1],
         'R' : ['PI', "pindex",         0],
         'B' : ['DF', "dflags",         0],
         'F' : ['FC', "fcount",         0],
         'J' : ['DC', "dcount",         0],
         'K' : ['TC', "tcount",         0],
         'L' : ['MC', "mcount",         0],
         'Z' : ['SZ', "size",           0],
         'D' : ['CD', "date",           1],
         'Y' : ['CT', "time",           1],
         'H' : ['HN', "hostname",       1],
         'N' : ['SN', "specialist",     1],
         'W' : ['WD', "workdir",        1],
         'M' : ['MO', "modules",        1],
         'I' : ['EV', "environments",   1],
         'Q' : ['QS', "qoptions",       1],
         'X' : ['AX', "argextra",      -1],
         'E' : ['ER', "errmsg",        -1],
      }
      self.TBLHASH['dsdaemon'] = {
        #SHORTNM KEYS DBFIELD
         'I' : ['DI', "dindex",         0],
         'C' : ['CM', "command",        1],
         'H' : ['HN', "hostname",       1],
         'M' : ['MH', "matchhost",      1],
         'S' : ['SN', "specialist",     1],
         'P' : ['PL', "proclimit",      0],
         'O' : ['PO', "priority",       0],
      }
      self.CHKHOST = {
         'curhost' : self.get_host(1),
         'chkhost' : None,
         'hostcond' : None,
         'isbatch' : 0
      }
      self.PGOPT['dscheck']   = "COVTUPFJDNW"            # default
      self.PGOPT['chkall']    = "COVTAUPRBFJKLZDYHNWMIQXE"   # default to all   
      self.PGOPT['dsdaemon']  = "ICHQSPO"                 # default to all
      self.PGOPT['waitlimit'] = 280      # limit of C and P request checks at a time
      self.PGOPT['totallimit'] = 380     # maximum number of checks can be started on PBS
      self.PBSQUEUES = {'rda' : None, 'htc' : 'casper@casper-pbs'}
      self.PBSTIMES = {'default' : 21600, 'rda' : self.PGLOG['PBSTIME'], 'htc' : 86400}
      #self.DOPTHOSTS = {'rda-work' : None, 'PBS' : ['!subconv -Q']}
      self.DOPTHOSTS = {'rda-work' : None, 'PBS' : None, 'cron' : None}
      self.DSLMTS = {}
      self.EMLMTS = {}

   # get the maximum running time for batch processes
   def max_batch_time(self, qname):
      if self.CHKHOST['curhost'] == self.PGLOG['PBSNAME']:
         if not (qname and qname in self.PBSTIMES): qname = 'default'
         return self.PBSTIMES[qname]
      else:
         return 0

   # check if enough information entered on command line and/or input file
   # for given action(s)
   def check_dscheck_options(self, cact, aname):
      errmsg = [
         "Option -DM(-DaemonMode) works with Action -PC(-ProcessCheck) only",
         "Do not specify Check Index for Daemon Mode",
         "Miss check index per Info option -CI(-CheckIndex)",
         "Need Machine Hostname per -HN for new daemon control",
         "Need Application command name per -CM for new daemon control",
         "Must be {} to process Checks in daemon mode".format(self.PGLOG['GDEXUSER']),
         "Miss Command information per Info option -CM(-Command)",
      ]
      erridx = -1
      self.set_uid(aname)
      if 'CI' in self.params: self.validate_checks()
      if 'DS' in self.params: self.validate_datasets()
      if 'DM' in self.params:
         if cact != "PC":
            erridx = 0
         elif self.PGLOG['CURUID'] != self.PGLOG['GDEXUSER']:
            erridx = 5
         elif 'CI' in self.params:
            erridx = 1
      elif cact == "DL":
         if not ('CI' in self.params or 'DI' in self.params): erridx = 2
      elif cact == 'SD':
         self.validate_daemons()
         if 'SD' in self.params:
            if 'HN' not in self.params:
               erridx = 3
            elif 'CM' not in self.params:
               erridx = 4
      elif cact == "AC":
         if 'CM' not in self.params:
            erridx = 6
      elif 'CI' not in self.params and (cact == "IC" or cact == "UL" and 'LL' not in self.params):
         erridx = 2
      if erridx >= 0: self.action_error(errmsg[erridx], cact)
      if cact == "PC" or cact == 'UL':
         if self.PGLOG['CURUID'] != self.params['LN']:
            self.action_error("{}: cannot process Checks as {}".format(self.PGLOG['CURUID'], self.params['LN']), cact)
         if 'LH' in self.params:
            chkhost = self.get_short_host(self.params['LH'])
            if not chkhost: chkhost = self.get_host(1)
            self.CHKHOST['chkhost'] = self.CHKHOST['curhost'] = chkhost
            if self.valid_batch_host(chkhost):
               self.reset_batch_host(chkhost)
               self.CHKHOST['isbatch'] = 1
               self.CHKHOST['hostcond'] = "IN ('{}', '{}')".format(chkhost, self.PGLOG['HOSTNAME'])
            else:
               if self.pgcmp(chkhost, self.PGLOG['HOSTNAME'], 1):
                  self.action_error("{}: Cannot handle checks on {}".format(self.PGLOG['HOSTNAME'], chkhost), cact)
               self.CHKHOST['hostcond'] = "= '{}'".format(chkhost)
      if 'DM' in self.params:
         if self.PGLOG['self.CHKHOSTS'] and self.PGLOG['self.CHKHOSTS'].find(self.PGLOG['HOSTNAME']) < 0:
            self.action_error("Daemon mode can only be started on '{}'".format(self.PGLOG['self.CHKHOSTS']), cact)
         if re.match(r'^(start|begin)$', self.params['DM'], re.I):
            if not ('NC' in self.params or 'LH' in self.params): self.params['NC'] = 1 
            wtime = self.params['WI'] if 'WI' in self.params else 0
            mtime = self.params['MT'] if 'MT' in self.params else 0
            logon = self.params['LO'] if 'LO' in self.params else 0
            self.start_daemon(aname, self.PGLOG['CURUID'], 1, wtime, logon, 0, mtime)
         else:
            self.signal_daemon(self.params['DM'], aname, self.params['LN'])
      else:
         if cact == "PC":
            self.validate_single_process(aname, self.params['LN'], self.argv_to_string())
         elif cact == "SO":
            plimit = self.params['PL'][0] if 'PL' in self.params and self.params['PL'][0] > 0 else 1
            self.validate_multiple_process(aname, plimit, self.params['LN'], self.argv_to_string())
         wtime = self.params['WI'] if 'WI' in self.params else 30
         logon = self.params['LO'] if 'LO' in self.params else 1
         self.start_none_daemon(aname, cact, self.params['LN'], 1, wtime, logon)
         if not ('CI' in self.params or 'DS' in self.params or self.params['LN'] == self.PGLOG['GDEXUSER']):
            self.set_default_value("SN", self.params['LN'])
      # minimal wait interval in seconds for next check
      self.PGOPT['minlimit'] = self.params['WI'] = self.PGSIG['WTIME']

   # process counts of hosts in dsdaemon control records for given command and specialist
   def get_process_limits(self, cmd, specialist, logact = 0):
      ckey = "{}-{}".format(cmd, specialist)
      if ckey in self.PLIMITS: return self.PLIMITS[ckey]
      cnd = "command = '{}' AND specialist = '{}'".format(cmd, specialist)
      if self.CHKHOST['chkhost']:
         ecnd = " AND hostname = '{}'".format(self.CHKHOST['chkhost'])
         hstr = " for " + self.CHKHOST['chkhost']
      else:
         ecnd = " ORDER by priority, hostname"
         hstr = ""
      pgrecs = self.pgmget("dsdaemon", "hostname, bqueues, matchhost, proclimit, priority", cnd + ecnd, logact)
      if not pgrecs and self.pgget("dsdaemon", "", cnd, logact) == 0:
         pgrecs = self.pgmget("dsdaemon", "hostname, matchhost, proclimit, priority",
                               "command = 'ALL' AND specialist = '{}'{}".format(specialist, ecnd), logact)
      cnt = (len(pgrecs['hostname']) if pgrecs else 0)
      if cnt == 0:
         self.PLIMITS[ckey] = 0
         return 0
      j = 0
      self.PLIMITS[ckey] = {'host' : [], 'priority' : [], 'acnt' : [], 'match' : [], 'pcnd' : []}
      for i in range(cnt):
         if pgrecs['proclimit'][i] <= 0: continue
         host = pgrecs['hostname'][i]
         self.PLIMITS[ckey]['host'].append(host)
         self.PLIMITS[ckey]['priority'].append(pgrecs['priority'][i])
         self.PLIMITS[ckey]['acnt'].append(pgrecs['proclimit'][i])
         self.PLIMITS[ckey]['match'].append(pgrecs['matchhost'][i])
         self.PLIMITS[ckey]['pcnd'].append("{} AND pid > 0 AND lockhost = '{}'".format(cnd, host))
      if not self.PLIMITS[ckey]['host']: self.PLIMITS[ckey] = 0
      return self.PLIMITS[ckey]

   # find a available host name to process a dscheck record
   def get_process_host(self, limits, hosts, cmd, act, logact = 0):
      cnt = len(limits['host'])
      for i in range(cnt):
         host = limits['host'][i]
         if host in self.DWHOSTS: continue     # the host is down
         if limits['acnt'][i] > self.pgget("dscheck", "", limits['pcnd'][i], logact):
            if cmd == 'dsrqst' and act == 'PR':
               mflag = 'G'
            else:
               mflag = limits['match'][i]
            if self.check_process_host(hosts, host, mflag): return i
      return -1

   # reset the cached process limits
   def reset_process_limits(self):   
      if self.LOOP%3 == 0:
         self.PLIMITS = {}   # clean the cache for available processes on hosts
      if self.LOOP%10 == 0:
         self.DWHOSTS = {}
         self.set_pbs_host(None, 1)
      self.LOOP += 1

   # start dschecks
   def start_dschecks(self, cnd, logact = 0):
      rcnt = 0
      self.check_dscheck_locks(cnd, logact)
      self.email_dschecks(cnd, logact)
      self.purge_dschecks(cnd, logact)
      if 'NC' in self.params: return 0 
      if self.CHKHOST['isbatch'] and 'CP' in self.params: self.check_dscheck_pends(cnd, logact)
      self.reset_process_limits()
      if self.CHKHOST['isbatch']: rcnt = self.pgget("dscheck", "", "lockhost = '{}' AND pid > 0".format(self.PGLOG['PBSNAME']), logact)
      cnd += "pid = 0 AND status <> 'D' AND einfo IS NULL AND (qoptions IS NULL OR LEFT(qoptions, 1) != '!') ORDER by hostname DESC, cindex"
      pgrecs = self.pgmget("dscheck", "*", cnd, logact)
      cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      pcnt = 0
      for i in range(cnt):
         if (pcnt + rcnt) > self.PGOPT['totallimit']: break
         pgrec = self.onerecord(pgrecs, i)
         if(pgrec['fcount'] and pgrec['dcount'] >= pgrec['fcount'] or
            pgrec['tcount'] and pgrec['tcount'] >= pgrec['mcount'] or
            pgrec['pindex'] and self.pgget("dscheck", "", "cindex = {} AND status <> 'D'".format(pgrec['pindex']), logact)):
            continue
         if pgrec['dflags'] and self.check_storage_dflags(pgrec['dflags'], pgrec, logact): continue
         ret = self.start_one_dscheck(pgrec, logact)
         if ret > 0: pcnt += ret
      if cnt > 1: self.pglog("{} of {} DSCHECK records started on {}".format(pcnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)
      return pcnt

   #  check long locked dschecks and unlock them if the processes are dead
   def check_dscheck_locks(self, cnd, logact = 0):
      ltime = int(time.time())
      lochost = self.PGLOG['HOSTNAME']
      cnd += "pid > 0 AND "
      dtime = ltime - self.PGSIG['DTIME']
      ctime = ltime - self.PGSIG['CTIME']
      rtime = ltime - self.PGSIG['RTIME']
      cnd += "chktime > 0 AND (chktime < {} OR chktime < {} AND lockhost {} OR chktime < {} AND lockhost = 'rda_config')".format(ctime, dtime, self.CHKHOST['hostcond'], rtime)
      pgrecs = self.pgmget("dscheck", "*", cnd, logact)
      cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      lcnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         lmsg = "{}({}) at {} on {}".format(pgrec['lockhost'], pgrec['pid'], self.current_datetime(), self.PGLOG['HOSTNAME'])
         cidx = pgrec['cindex']
         if self.CHKHOST['chkhost'] or pgrec['lockhost'] == lochost:
            spid = "{}{}".format(pgrec['lockhost'], pgrec['pid'])
            if spid not in self.RUNPIDS and self.lock_dscheck(cidx, 0) > 0:
               self.pglog("CHK{}: unlocked {}".format(cidx, lmsg), self.LOGWRN)
               lcnt += 1
            else:
               self.update_dscheck_time(pgrec, ltime, logact)
         elif not pgrec['lockhost'] or pgrec['lockhost'] == 'rda_config':
            record = {'pid' : 0, 'lockhost' : ''}
            if self.pgupdt("dscheck", record, "cindex = {} AND pid = {}".format(cidx, pgrec['pid']), logact):
               self.pglog("CHK{}: unlocked {}".format(cidx, lmsg), self.LOGWRN)
               lcnt += 1
         elif (logact&self.EMEROL) == self.EMEROL:
            self.pglog("Chk{}: time NOT updated for {} of {}".format(cidx, self.dscheck_runtime(pgrec['chktime'], ltime), lmsg), logact)   
      if cnt > 0: 
         s = 's' if cnt > 1 else ''
         self.pglog("{} of {} DSCHECK record{} unlocked on {}".format(lcnt, cnt, s, self.PGLOG['HOSTNAME']), self.WARNLG)
      self.RUNPIDS = {}

   #  check long pending dschecks and kill them
   def check_dscheck_pends(self, cnd, logact = 0):
      ltime = int(time.time()) - self.PGSIG['RTIME']
      cnd += "pid > 0 AND "
      cnd += "lockhost {} AND status = 'P' AND subtime > 0 AND subtime < {}".format(self.CHKHOST['hostcond'], ltime)
      pgrecs = self.pgmget("dscheck", "pid", cnd, logact)
      cnt = (len(pgrecs['pid']) if pgrecs else 0)
      pcnt = 0
      for i in range(cnt):
         pid = pgrecs['pid'][i]
         info = self.get_pbs_info(pid, 0, logact)
         if info and info['State'] == 'Q':
            self.pgsystem("rdakill -h {} -p {}".format(self.PGLOG['PBSNAME'], pid), self.LOGWRN, 5)
            pcnt += 1
      if cnt > 0:
         s = 's' if cnt > 1 else ''
         self.pglog("{} of {} Pending DSCHECK record{} stopped on {}".format(pcnt, cnt, s, self.PGLOG['HOSTNAME']), self.WARNLG)

   # update dscheck time in case in pending status or
   # the command does not updateupdates not on time by itself
   def update_dscheck_time(self, pgrec, ltime, logact = 0):
      record = {'chktime' : ltime}
      if(self.CHKHOST['chkhost'] and self.CHKHOST['chkhost'] == self.PGLOG['PBSNAME']
         and pgrec['lockhost'] == self.PGLOG['PBSNAME']):
         info = self.get_pbs_info(pgrec['pid'], 0, logact)
         if info:
            stat = info['State']
            if stat != pgrec['status']: record['status'] = stat
      else:
         if pgrec['lockhost'] != self.PGLOG['HOSTNAME']: return    # connot update dscheck time
         if self.check_host_pid(pgrec['lockhost'], pgrec['pid']):
            if pgrec['status'] != "R": record['status'] = "R"
         else:
            if pgrec['status'] == "R": record['status'] = "F"
      if pgrec['stttime']:
         if pgrec['command'] == "dsrqst" and pgrec['oindex']:
            (record['fcount'], record['dcount'], record['size']) = self.get_dsrqst_counts(pgrec, logact)
   
      elif 'status' in record and record['status'] == 'R':
         record['stttime'] = ltime
      cnd = "cindex = {} AND pid = {}".format(pgrec['cindex'], pgrec['pid'])
      if self.pgget("dscheck", "", "{} AND chktime = {}".format(cnd, pgrec['chktime']), logact):
         # update only the chktime is not changed yet
         self.pgupdt("dscheck", record, cnd, logact)

   # return a running time string for given start and end times of the process
   def dscheck_runtime(self, start, end = None):
      stime = ''
      if start:
         if not end: end = int(time.time())
         rtime = (end - start)
         if rtime >= 60:
            stime = self.seconds_to_string_time(rtime)
      return stime

   #  check dschecks and purge them if done already
   def purge_dschecks(self, cnd, logact = 0):
      cnd += "pid = 0 AND einfo IS NULL"
      pgrecs = self.pgmget("dscheck", "*", cnd, logact)
      cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      ctime = int(time.time()) - self.PGSIG['CTIME']
      dcnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         if(pgrec['status'] == "D" or
            pgrec['status'] == "R" and pgrec['chktime'] < ctime or
            pgrec['fcount'] and pgrec['dcount'] >= pgrec['fcount'] or
            pgrec['tcount'] and pgrec['tcount'] >= pgrec['mcount']):
            if self.lock_dscheck(pgrec['cindex'], 1) <= 0: continue
            dcnt += self.delete_dscheck(pgrec, None, logact)
      if dcnt and cnt > 1: self.pglog("{} of {} DSCHECK records purged on {}".format(dcnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   #  check dschecks and send saved email
   def email_dschecks(self, cnd, logact = 0):
      emlact = self.LOGWRN|self.FRCLOG
      if logact and (logact&self.EMEROL) == self.EMEROL: emlact |= self.EMEROL
      cnd += "pid = 0 AND einfo IS NOT NULL"
      pgrecs = self.pgmget("dscheck", "cindex", cnd, logact)
      cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      ecnt = 0
      for i in range(cnt):
         cidx = pgrecs['cindex'][i]
         if self.lock_dscheck(cidx, 1) <= 0: continue
         pgrec = self.pgget("dscheck", "*", "cindex = {}".format(cidx), logact)
         einfo = pgrec['einfo'] if pgrec else None
         if einfo:
            if pgrec['dflags'] and pgrec['tcount'] and pgrec['tcount'] < pgrec['mcount']:
               msgary = self.check_storage_dflags(pgrec['dflags'], pgrec, logact)
               if msgary:
                  einfo = "The Check will be resubmitted after the down storage Up again:\n{}\n{}".format("\n".join(msgary), einfo)
            sent = 1 if(self.send_customized_email("Chk{}".format(cidx), einfo, emlact) and
                    self.pgexec("UPDATE dscheck set einfo = NULL WHERE cindex = {}".format(cidx), logact)) else -1
         else:
            sent = 0
         self.lock_dscheck(cidx, 0)
         if sent == -1: break
         ecnt += sent
      if ecnt and cnt > 1: self.pglog("{} of {} DSCHECK emails sent on {}".format(ecnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   # start a dscheck job for given dscheck record
   def start_one_dscheck(self, pgrec, logact = 0):
      cidx = pgrec['cindex']
      specialist = pgrec['specialist']
      host = self.CHKHOST['chkhost']
      dlimit = self.get_system_down_limit(host, logact)
      if dlimit < 0:
         self.lock_dscheck(cidx, 0)
         return 0
      limits = self.get_process_limits(pgrec['command'], specialist, logact)
      if not limits:
         if pgrec['hostname'] and (logact&self.EMEROL) == self.EMEROL:
            host = self.get_host(1)
            if self.check_process_host(pgrec['hostname'], host, 'I'):
               self.pglog("Chk{}: {} is not configured properly to run on {} for {}".format(cidx, pgrec['command'], host, specialist), logact)
         return 0
      lidx = self.get_process_host(limits, pgrec['hostname'], pgrec['command'], pgrec['action'], logact)
      if lidx < 0 or self.skip_dscheck_record(pgrec, host, logact): return 0
      cmd = "pgstart_{} ".format(specialist) if self.PGLOG['CURUID'] == self.PGLOG['GDEXUSER'] else ""
      if not self.pgcmp(host, self.PGLOG['PBSNAME'], 1):
         if self.reach_dataset_limit(pgrec): return 0
         cmd += self.get_specialist_shell(specialist) + 'qsub '
         options = self.get_pbs_options(pgrec, dlimit, logact)
         if options:
            cmd += options
         elif pgrec['status'] == 'E':
            return 0
         bstr = " in {} Queue {} ".format(self.PGLOG['PBSNAME'], pgrec['pbsqueue'])
      else:
         bstr = ""
         cmd += "rdasub -bg "
      if pgrec['workdir']:
         if pgrec['workdir'].find('$') > -1:
            cmd += "-cwd '{}' ".format(pgrec['workdir'])
         else:
            cmd += "-cwd {} ".format(pgrec['workdir'])
      else:
         cmd += "-cwd '$HOME' "
      chkcmd = pgrec['command']
      cmd += "-cmd " + chkcmd
      if pgrec['argv']:
         argv = pgrec['argv']
         if pgrec['argextra']: argv += pgrec['argextra']
         cmd += ' ' + argv + self.append_delayed_mode(chkcmd, argv)
         chkcmd += ' ' + argv
      self.pglog("Chk{}: issues '{}' onto {} for {}".format(cidx, chkcmd, host, pgrec['specialist']), self.LOGWRN)
      self.PGLOG['ERR2STD'] = ['chmod: changing']
      cstr = self.pgsystem(cmd, logact&(~self.EXITLG), 278)  # 2+4+16+256
      self.PGLOG['ERR2STD'] = []
      pid = 0
      if cstr:
         lines = cstr.split('\n')
         for line in lines:
            if not line: continue
            ms = re.match(r'^Job <(\d+)> is submitted', line)
            if ms:
               pid = int(ms.group(1))
               break
            ms = re.match(r'^(\d+)\.casper-pbs', line)
            if ms:
               pid = int(ms.group(1))
               break
            ms = re.match(r'^Submitted batch job (\d+)', line)
            if ms:
               pid = int(ms.group(1))
               break
      if not pid:
         if self.PGLOG['SYSERR']:
            if self.PGLOG['SYSERR'].find('Job not submitted') > -1:
               cstr = "submit job"
            elif self.PGLOG['SYSERR'].find('working directory') > -1:
               cstr = "change working directory"
            else:
               cstr = "execute"
            self.lock_dscheck(cidx, 0)
            return self.pglog("Chk{}: {} Failed {} on {}{}{}\n{}".format(cidx, self.get_command_info(pgrec),
                               cstr, self.PGLOG['HOSTNAME'], bstr, self.curtime(1), self.PGLOG['SYSERR']),
                               self.LOGWRN|self.FRCLOG)
      self.pglog("Chk{}: {} started on {}{}{}".format(cidx, self.get_command_info(pgrec), 
                  self.PGLOG['HOSTNAME'], bstr, self.curtime(1)), self.LOGWRN|self.FRCLOG)
      return self.fill_dscheck_info(pgrec, pid, host, logact)

   # get qsub shell command
   def get_specialist_shell(self, specialist):
      if specialist not in self.SHELLS:
         pgrec = self.pgget("dssgrp", "shell_flag", "logname = '{}'".format(specialist))
         if pgrec and pgrec['shell_flag'] == 'B':
            self.SHELLS[specialist] = 'bash'
         else:
            self.SHELLS[specialist] = 'tcsh'
      return self.SHELLS[specialist]

   # get and cache process limit for a given dsid
   def get_dataset_limit(self, dsid):
      if dsid in self.DSLMTS: return self.DSLMTS[dsid]
      pgrec = self.pgget('dslimit', 'processlimit', "dsid = '{}'".format(dsid))
      dslmt = 45
      if pgrec:
         dslmt = pgrec['processlimit']
      elif 'default' in self.DSLMTS:
         dslmt = self.DSLMTS['default']
      else:
         pgrec = self.pgget('dslimit', 'processlimit', "dsid = 'all'")
         if pgrec: self.DSLMTS['default'] = dslmt = pgrec['processlimit']
      self.DSLMTS[dsid] = dslmt
      return self.DSLMTS[dsid]

   # check if reaching running limit for a specified dataset
   def reach_dataset_limit(self, pgrec):
      if pgrec['command'] != 'dsrqst': return 0
      dsid = pgrec['dsid']
      if dsid and pgrec['action'] in ['BR', 'SP', 'PP']:
         dslmt = self.get_dataset_limit(dsid)
         lmt = self.pgget('dscheck', '', "dsid = '{}' AND status <> 'C' AND action IN ('BR', 'SP', 'PP')".format(dsid))
         if lmt > dslmt:
            self.lock_dscheck(pgrec['cindex'], 0)
            return 1
      return 0

   # get and cache request limit for a given given email
   def get_user_limit(self, email):
      if email in self.EMLMTS: return self.EMLMTS[email]
      emlmts = [20, 10, 36]
      flds = 'maxrqstcheck, maxpartcheck'
      pgrec = self.pgget('userlimit', flds, "email = '{}'".format(email))
      if pgrec:
         emlmts = [pgrec['maxrqstcheck'], pgrec['maxpartcheck']] 
      elif 'default' in self.EMLMTS:
         emlmts = self.EMLMTS['default']
      else:
         pgrec = self.pgget('userlimit', flds, "email = 'all'".format(email))
         if pgrec:
            self.EMLMTS['default'] = emlmts = [pgrec['maxrqstcheck'], pgrec['maxpartcheck']] 
      self.EMLMTS[email] = emlmts.copy()
      return self.EMLMTS[email]

   # check and return the time limit in seconds before a planned system down for given hostname
   def get_system_down_limit(self, hostname, logact = 0):
      dlimit = 0
      down = self.get_system_downs(hostname, logact)
      if down['start']:
         dlimit = down['start'] - down['curtime'] - 2*self.PGSIG['CTIME']
         if dlimit < self.PGOPT['minlimit']: dlimit = -1
      return dlimit

   # check and get the option string for submit a PBS job
   def get_pbs_options(self, pgrec, limit = 0, logact = 0):
      opttime = 0
      qoptions = self.build_dscheck_options(pgrec, 'qoptions', 'PBS')
      qname = self.get_pbsqueue_option(pgrec)
      maxtime = self.max_batch_time(qname)
      runtime = self.PBSTIMES['default']
      if qoptions:
         ms = re.match(r'^(-.+)/(-.+)$', qoptions)
         if ms: qoptions = ms.group(2 if pgrec['otype'] == 'P' else 1)
         ms = re.search(r'-l\s+\S*walltime=([\d:-]+)', qoptions)
         if ms:
            optval = ms.group(1)
            vcs = optval.split(':')
            vcl = len(vcs)
            vds = vcs[0].split('-')
            opttime = 3600*int(vds[0])
            if len(vds) > 1:
               opttime *= 24
               opttime += 3600*int(vds[1])
            if vcl > 1:
               opttime += 60*int(vcs[1])
               if vcl > 2: opttime += int(vcs[2])
         runtime = opttime
         qoptions += ' '
      if limit > 0 and runtime > limit: runtime = limit
      if runtime > maxtime: runtime = maxtime
      if runtime != opttime and runtime != self.PBSTIMES['default']:
         optval = "walltime={}:{:02}:{:02}".format(int(runtime/3600), int(runtime/60)%60, runtime%60)
         if opttime:
            if runtime < opttime: qoptions = re.sub(r'walltime=[\d:-]+', optval, qoptions)
         elif qoptions.find('-l ') > -1:
            qoptions = re.sub(r'-l\s+', "-l {},".format(optval), qoptions)
         else:
            qoptions += "-l " + optval
      if pgrec['modules']:
         options = self.build_dscheck_options(pgrec, 'modules', 'PBS')
         if options: qoptions += "-mod {} ".format(options)
      if pgrec['environments']:
         options = self.build_dscheck_options(pgrec, 'environments', 'PBS')
         if options: qoptions += "-env {} ".format(options)
      if qname: qoptions += "-q {} ".format(qname)
      return qoptions

   # check rda queue for pending jobs to switch PBS queue if needed
   def get_pbsqueue_option(self, pgrec):
      qname = pgrec['pbsqueue']
      if qname in self.PBSQUEUES: return self.PBSQUEUES[qname]
      return None

   #  build individual option string for given option name 
   def build_dscheck_options(self, pgcheck, optname, optstr = None):
      options = pgcheck[optname]
      if not options or options == 'default': return ''
      if not re.match(r'^!', options): return options
      cidx = pgcheck['cindex']
      # reget the option field to see if it is processed
      pgrec = self.pgget('dscheck', optname, 'cindex = {}'.format(cidx))
      if not pgrec or options != pgrec[optname]: return options
      record = {}
      errmsg = ''
      record[optname] = options = self.get_dynamic_options(options[1:], pgcheck['oindex'], pgcheck['otype'])
      if not options and self.PGLOG['SYSERR']:
         record['status'] = pgcheck['status'] = 'E'
         record['pid'] = 0
         record['tcount'] = pgcheck['tcount'] + 1
         if not optstr: optstr = optname.capitalize()
         errmsg = "Chk{}: Fail to build {} Options, {}".format(cidx, optstr, self.PGLOG['SYSERR'])
      self.pgupdt("dscheck", record, "cindex = {}".format(cidx))
      if errmsg:
         pgrqst = None
         if pgcheck['otype'] == 'R':
            ridx = pgcheck['oindex']
            pgrqst = self.pgget('dsrqst', '*', 'rindex = {}'.format(ridx))
            if pgrqst:
               record = {}
               record['status'] = self.send_request_email_notice(pgrqst, errmsg, 0, 'E')
               record['ecount'] = pgrqst['ecount'] + 1
               self.pgupdt("dsrqst", record, "rindex = {}".format(ridx), self.PGOPT['errlog'])
               errmsg = ''
         elif pgcheck['otype'] == 'P':
            pidx = pgcheck['oindex']
            pgpart = self.pgget('ptrqst', 'rindex', 'pindex = {}'.format(pidx))
            if pgpart:
               self.pgexec("UPDATE ptrqst SET status = 'E' WHERE pindex = {}".format(pidx))
               ridx = pgpart['rindex']
               pgrqst = self.pgget('dsrqst', '*', 'rindex = {}'.format(ridx))
               if pgrqst and pgrqst['status'] != 'E':
                  record = {}
                  record['status'] = self.send_request_email_notice(pgrqst, errmsg, 0, 'E')
                  record['ecount'] = pgrqst['ecount'] + 1
                  self.pgupdt("dsrqst", record, "rindex = {}".format(ridx), self.PGOPT['errlog'])
                  errmsg = ''
         if errmsg: self.pglog(errmsg, self.PGOPT['errlog'])
      return options

   # fill up dscheck record in case the command does not do it itself
   def fill_dscheck_info(self, ckrec, pid, host, logact = 0):
      chkcnd = "cindex = {}".format(ckrec['cindex'])
      self.pgexec("UPDATE dscheck SET tcount = tcount+1 WHERE " + chkcnd, logact)
      if pid and self.lock_host_dscheck(ckrec['cindex'], pid, host, logact) <= 0: return 1 # under processing
      record = {}
      stat = 'R'
      if pid:
         record['pid'] = pid
         if host == self.PGLOG['PBSNAME']:
            info = self.get_pbs_info(pid, 0, logact, 2)
            if info: stat = info['State']
         else:
            record['runhost'] = self.PGLOG['HOSTNAME']
            record['bid'] = 0
      else:
         stat = 'F'
      record['status'] = stat
      record['stttime'] = record['subtime'] = record['chktime'] = int(time.time())
      pgrec = self.pgget("dscheck", "status, stttime", chkcnd, logact)
      if not pgrec: return 0
      if pgrec['status'] != ckrec['status'] or pgrec['stttime'] > ckrec['stttime']: return 1
      if not pid and self.lock_dscheck(ckrec['cindex'], 0) <= 0: return 1
      return self.pgupdt("dscheck", record, chkcnd, logact)

   # return 1 to skip running if the dscheck record is not ready; 0 otherwise
   def skip_dscheck_record(self, pgrec, host, logact = 0):
      workdir = pgrec['workdir']
      if workdir and workdir.find('$') > -1: workdir = '' 
      if self.check_host_down(workdir, host, logact): return 1
      if pgrec['command'] == "dsrqst":
         if self.check_host_down(self.PGLOG['RQSTHOME'], host, logact): return 1
      elif pgrec['command'] == "dsupdt" or pgrec['command'] == "dsarch":
         if self.check_host_down(self.PGLOG['DSDHOME'], host, logact): return 1
      newrec = self.pgget("dscheck", "pid, status, stttime, tcount", "cindex = {}".format(pgrec['cindex']), logact)
      if(not newrec or newrec['pid'] > 0 or newrec['status'] != pgrec['status'] or
         newrec['stttime'] > pgrec['stttime'] or newrec['tcount'] > pgrec['tcount']): return 1
      if self.lock_dscheck(pgrec['cindex'], 1) <= 0: return 1
      if pgrec['subtime'] or pgrec['stttime']:
         newrec = {'stttime' : 0, 'subtime' : 0, 'runhost' : '', 'bid' : 0}
         (newrec['ttltime'], newrec['quetime']) = self.get_dscheck_runtime(pgrec)
         if not self.pgupdt("dscheck", newrec, "cindex = {}".format(pgrec['cindex']), logact): return 1
      return 0

   # start recording Queued reuqests to checks
   def start_dsrqsts(self, cnd, logact = 0):
      self.check_dsrqst_locks(cnd, logact)
      self.email_dsrqsts(cnd, logact)
      self.purge_dsrqsts(cnd, logact)
      rcnd = cnd
      rcnd += ("status = 'Q' AND rqsttype <> 'C' AND (pid = 0 OR pid < ptcount) AND " +
               "einfo IS NULL ORDER BY priority, rindex")
      pgrecs = self.pgmget("dsrqst", "*",  rcnd, logact)
      cnt = (len(pgrecs['rindex']) if pgrecs else 0)
      ccnt = self.pgget("dscheck", '', "status = 'C'", logact)
      pcnt = self.pgget("dscheck", '', "status = 'P'", logact)
      if (ccnt+pcnt) > self.PGOPT['waitlimit']:
         if cnt: self.pglog("{}/{} Checks are Waiting/Pending; Add new dscheck records {} later".format(ccnt, pcnt, self.PGLOG['HOSTNAME']),
                             self.LOGWRN|self.FRCLOG)
      rcnt = self.PGOPT['waitlimit']-ccnt-pcnt
      if cnt == 0:
         acnt = 0
         cnts = self.start_dsrqst_partitions(None, rcnt, logact)
         rcnt = cnts[0]
         pcnt = cnts[1]
      else:
         tcnt = cnt
         if cnt > rcnt: cnt = rcnt
         if cnt > 1: self.pglog("Try to add dschecks for {} DSRQST records on {}".format(cnt, self.PGLOG['HOSTNAME']), self.WARNLG)
         i = acnt = ccnt = pcnt = rcnt = 0
         while i < tcnt and ccnt < cnt:
            pgrec = self.onerecord(pgrecs, i)
            i += 1
            if pgrec['ptcount'] == 0 and self.validate_dsrqst_partitions(pgrec, logact):
               acnt += self.add_dsrqst_partitions(pgrec, logact)
            elif pgrec['ptcount'] < 2:
               rcnt += self.start_one_dsrqst(pgrec, logact)
            else:
               cnts = self.start_dsrqst_partitions(pgrec, (cnt-ccnt), logact)
               rcnt += cnts[0]
               pcnt += cnts[1]
            ccnt += (acnt+pcnt+rcnt)
      if rcnt > 1: self.pglog("build {} requests on {}".format(rcnt, self.PGLOG['HOSTNAME']), self.WARNLG)
      if pcnt > 1: self.pglog("build {} request partitions on {}".format(pcnt, self.PGLOG['HOSTNAME']), self.WARNLG)
      if acnt > 1: self.pglog("Add partitions to {} requests on {}".format(acnt, self.PGLOG['HOSTNAME']), self.WARNLG)
      return rcnt

   # validate a given request if ok to do partitions
   def validate_dsrqst_partitions(self, pgrec, logact = 0):
      pgctl = self.get_dsrqst_control(pgrec, logact)
      if pgctl and (pgctl['ptlimit'] or pgctl['ptsize']): return True
      record = {'ptcount' : 1}
      pgrec['ptcount'] = 1
      if pgrec['ptlimit']: pgrec['ptlimit'] = record['ptlimit'] = 0
      if pgrec['ptsize']: pgrec['ptsize'] = record['ptsize'] = 0
      self.pgupdt('dsrqst', record, "rindex = {}".format(pgrec['rindex']), logact)
      return False

   # call given command to evaluate dynamically the dscheck.qoptions
   def set_dscheck_options(self, chost, cnd, logact):
      if chost not in self.DOPTHOSTS: return
      qcnt = 0
      skipcmds = self.DOPTHOSTS[chost]
      pgrecs = self.pgmget("dscheck", "*", cnd + "pid = 0 AND status = 'C' AND LEFT(qoptions, 1) = '!'", logact)
      cnt = len(pgrecs['cindex']) if pgrecs else 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         if skipcmds and pgrec['qoptions'] in skipcmds: continue   # skip
         if self.lock_dscheck(pgrec['cindex'], 1) <= 0: continue
         qoptions = self.build_dscheck_options(pgrec, 'qoptions', 'PBS')
         if not qoptions and pgrec['status'] == 'E': continue  # failed evaluating qoptions
         record = {'pid' : 0, 'qoptions': qoptions}
         qcnt += self.pgupdt('dscheck', record, "cindex = {}".format(pgrec['cindex']), self.PGOPT['errlog'])
      if qcnt and cnt > 1: self.pglog("{} of {} DSCHECK PBS options Dynamically set on {}".format(qcnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   # add a new dscheck record if a given request record is due
   def start_one_dsrqst(self, pgrec, logact = 0):
      if self.pgget("dscheck", "", "oindex = {} AND command = 'dsrqst' AND action = 'BR'".format(pgrec['rindex']), logact): return 0
      pgctl = self.get_dsrqst_control(pgrec, logact)
      if pgctl:
         if 'qoptions' in pgctl and pgctl['qoptions']:
            ms = re.match(r'^(-.+)/(-.+)$', pgctl['qoptions'])
            if ms: pgctl['qoptions'] = ms.group(1)
      argv = "{} BR -RI {} -b -d".format(pgrec['dsid'], pgrec['rindex'])
      return self.add_one_dscheck(pgrec['rindex'], 'R', "dsrqst", pgrec['dsid'], "BR",
                                  '', pgrec['specialist'], argv, pgrec['email'], pgctl, logact)

   # add a dscheck record for a given request to setup partitions
   def add_dsrqst_partitions(self, pgrec, logact = 0):
      if self.pgget("dscheck", "", "oindex = {} AND command = 'dsrqst'".format(pgrec['rindex']), logact): return 0
      pgctl = self.get_dsrqst_control(pgrec, logact)
      if pgctl:
         if 'qoptions' in pgctl and pgctl['qoptions']:
            ms =re.match(r'^(-.+)/(-.+)$', pgctl['qoptions'])
            if ms: pgctl['qoptions'] = ms.group(1)
      argv = "{} SP -RI {} -NP -b -d".format(pgrec['dsid'], pgrec['rindex'])
      return self.add_one_dscheck(pgrec['rindex'], 'R', "dsrqst", pgrec['dsid'], 'SP',
                                  '', pgrec['specialist'], argv, pgrec['email'], pgctl, logact)
   
   # add multiple dscheck records of partitions for a given request
   def start_dsrqst_partitions(self, pgrqst, ccnt, logact = 0):
      cnts = [0, 0]
      if pgrqst:
         rindex = pgrqst['rindex']
         cnd = "rindex = {} AND status = ".format(rindex)
         if pgrqst['pid'] == 0:
            cnt = self.pgget("ptrqst", "", cnd + "'E'", logact)
            if cnt > 0 and (pgrqst['ecount'] + cnt) <= self.PGOPT['PEMAX']:
               # set Error partions back to Q
               self.pgexec("UPDATE ptrqst SET status = 'Q' WHERE {}'E'".format(cnd), self.PGOPT['extlog'])
      else:
         rindex = 0
         cnd = "status = "
      pgrecs = self.pgmget("ptrqst", "*", cnd + "'Q' AND pid = 0 ORDER by pindex", logact)
      cnt = len(pgrecs['pindex']) if pgrecs else 0
      if cnt > 0:
         if cnt > ccnt: cnt = ccnt
         pgctl = self.get_dsrqst_control(pgrqst, logact) if pgrqst else None
         for i in range(cnt):
            pgrec = self.onerecord(pgrecs, i)
            if pgrec['rindex'] != rindex:
               rindex = pgrec['rindex']
               pgrqst = self.pgget("dsrqst", "*", "rindex = {}".format(rindex), logact)
               if pgrqst: pgctl = self.get_dsrqst_control(pgrqst, logact)
            if not pgrqst:  # request missing
                 self.pgdel('ptrqst', "rindex = {}".format(rindex))
                 continue
            if pgrec['ptcmp'] == 'Y':
               pgptctl = None
            else:
               pgptctl = self.get_partition_control(pgrec, pgrqst, pgctl, logact)
               if pgptctl:
                  if 'qoptions' in pgptctl and pgptctl['qoptions']:
                     ms = re.match(r'^(-.+)/(-.+)$', pgptctl['qoptions'])
                     if ms: pgptctl['qoptions'] = ms.group(2)
            if self.pgget("dscheck", "", "oindex = {} AND command = 'dsrqst' AND action = 'PP'".format(pgrec['pindex']), logact): continue
            argv = "{} PP -PI {} -RI {} -b -d".format(pgrqst['dsid'], pgrec['pindex'], pgrqst['rindex'])
            cnts[1] += self.add_one_dscheck(pgrec['pindex'], 'P', "dsrqst", pgrqst['dsid'], "PP",
                                            '', pgrqst['specialist'], argv, pgrqst['email'], pgptctl, logact)
      elif pgrqst and pgrqst['pid'] == 0 and pgrqst['ptcount'] == self.pgget("ptrqst", "", cnd + " 'O'", logact):
         cnts[0] = self.start_one_dsrqst(pgrqst, logact)
      return cnts

   #  check long procssing reuqests and unlock the processes that are aborted
   def check_dsrqst_locks(self, cnd, logact = 0):
      ltime = int(time.time())
      lochost = self.PGLOG['HOSTNAME']
      cnd += "pid > 0 AND "
      dtime = ltime - self.PGSIG['DTIME']
      ctime = ltime - self.PGSIG['CTIME']
      rtime = ltime - self.PGSIG['RTIME']
      cnd += "locktime > 0 AND (locktime < {} OR locktime < {} AND lockhost {} OR locktime < {} AND lockhost = 'rda_config')".format(ctime, dtime, self.CHKHOST['hostcond'], rtime)
      self.check_partition_locks(cnd, ltime, logact)   # check partitions first
      pgrecs = self.pgmget("dsrqst", "rindex, lockhost, pid, locktime", cnd, logact)
      cnt = (len(pgrecs['rindex']) if pgrecs else 0)
      lcnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         lmsg = "{}({}) at {} on {}".format(pgrec['lockhost'], pgrec['pid'], self.current_datetime(), self.PGLOG['HOSTNAME'])
         ridx = pgrec['rindex']
         if self.CHKHOST['chkhost'] or pgrec['lockhost'] == lochost:
            if self.lock_request(ridx, 0) > 0:
               self.pglog("Rqst{}: unlocked {}".format(ridx, lmsg), self.LOGWRN)
               lcnt += 1
               continue
            if(self.pgexec("UPDATE dsrqst set locktime = {} WHERE rindex = {} AND pid = {}".format(ltime, ridx, pgrec['pid']), logact) and
               not self.pgget("dscheck", "", "oindex = {} AND command = 'dsrqst'".format(ridx))):
               self.pglog("Rqst{}: time updated for {}".format(ridx, lmsg), self.LOGWRN|self.FRCLOG)
         elif(not pgrec['lockhost'] or pgrec['lockhost'] == 'rda_config' or pgrec['lockhost'] == 'partition' and
              not self.pgget('ptrqst', '', "rindex = {} AND pid > 0".format(ridx), logact)):
            record = {'pid' : 0, 'lockhost' : ''}
            if self.pgupdt("dsrqst", record, "rindex = {} AND pid = {}".format(ridx, pgrec['pid']), logact):
               self.pglog("Rqst{}: unlocked {}".format(ridx, pgrec['lockhost'], pgrec['pid'], self.current_datetime(ltime)), self.LOGWRN)
               lcnt += 1
               continue
         elif (logact&self.EMEROL) == self.EMEROL:
            self.pglog("Rqst{}: time NOT updated for {} of {}".format(ridx, pgrec['lockhost'], pgrec['pid'], self.dscheck_runtime(pgrec['locktime'], ltime)), logact)
         self.RUNPIDS["{}{}".format(pgrec['lockhost'], pgrec['pid'])] = 1
      if cnt > 1: self.pglog("{} of {} DSRQST records unlocked on {}".format(lcnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   #  check long procssing reuqest partitions and unlock the processes that are aborted
   def check_partition_locks(self, cnd, ltime, logact = 0):
      pgrecs = self.pgmget("ptrqst", "pindex, rindex, lockhost, pid, locktime", cnd, (logact&~self.LGEREX))
      cnt = (len(pgrecs['pindex']) if pgrecs else 0)
      lcnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         lmsg = "{}({}) at {} on {}".format(pgrec['lockhost'], pgrec['pid'], self.current_datetime(), self.PGLOG['HOSTNAME'])
         pidx = pgrec['pindex']
         if self.CHKHOST['chkhost'] or pgrec['lockhost'] == self.PGLOG['HOSTNAME']:
            if self.lock_partition(pidx, 0) > 0:
               self.pglog("RPT{}: unlocked {}".format(pidx, lmsg), self.LOGWRN)
               lcnt += 1
               continue
            if(self.pgexec("UPDATE ptrqst set locktime = {} WHERE pindex = {} AND pid = {}".format(ltime, pidx, pgrec['pid']), logact) and
               self.pgexec("UPDATE dsrqst set locktime = {} WHERE rindex = {}".format(ltime, pgrec['rindex']), logact) and
               not self.pgget("dscheck", "", "oindex = {} AND command = 'dsrqst' AND otype = 'P'".format(pidx))):
               self.pglog("RPT{}: time updated for {}".format(pidx, lmsg), self.LOGWRN)
         elif not pgrec['lockhost'] or pgrec['lockhost'] == 'rda_config':
            record = {'pid' : 0, 'lockhost' : ''}
            if self.pgupdt("ptrqst", record, "pindex = {} AND pid = {}".format(pidx, pgrec['pid']), logact):
               self.pglog("RPT{}: unlocked {}".format(pidx, lmsg), self.LOGWRN)
               lcnt += 1
               continue
         elif (logact&self.EMEROL) == self.EMEROL:
            self.pglog("RPT{}: time NOT updated for {} of {}".format(pidx, self.dscheck_runtime(pgrec['locktime'], ltime), lmsg), logact)
         self.RUNPIDS["{}{}".format(pgrec['lockhost'], pgrec['pid'])] = 1
      if cnt > 1: self.pglog("{} of {} DSRQST partitions unlocked on {}".format(lcnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   #  check dsrqsts and purge them if done already
   def purge_dsrqsts(self, cnd, logact = 0):
      (sdate, stime) = self.get_date_time()
      cnd += "(status = 'P' AND (date_purge IS NULL OR date_purge < '{}' OR date_purge = '{}' AND time_purge < '{}')".format(sdate, sdate, stime)
      cnd += " OR status = 'O' AND (date_purge < '{}' OR date_purge = '{}' AND time_purge < '{}')) ORDER BY rindex".format(sdate, sdate, stime)                   
      pgrecs = self.pgmget("dsrqst", "rindex, dsid, email, specialist", cnd, logact)
      cnt = (len(pgrecs['rindex']) if pgrecs else 0)
      pgctl = {'qoptions' : "-l walltime=1:00:00"}
      pcnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         ridx = pgrec['rindex']
         if self.pgget("dscheck", "", "oindex = {} AND command = 'dsrqst'".format(ridx), logact): continue
         argv = "{} PR -RI {} -b -d".format(pgrec['dsid'], ridx)
         self.add_one_dscheck(ridx, 'R', 'dsrqst', pgrec['dsid'], 'PR', '',
                         pgrec['specialist'], argv, pgrec['email'], pgctl, logact)

   #  check dsrqsts and send saved email
   def email_dsrqsts(self, cnd, logact = 0):
      emlact = self.LOGWRN|self.FRCLOG
      if logact and (logact&self.EMEROL) == self.EMEROL: emlact |= self.EMEROL
      cnd += "pid = 0 AND einfo IS NOT NULL"
      pgrecs = self.pgmget("dsrqst", "rindex, ptcount, einfo", cnd, logact)
      cnt = (len(pgrecs['rindex']) if pgrecs else 0)
      ecnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         ridx = pgrec['rindex']
         if self.lock_request(ridx, 1) <= 0: continue
         einfo = self.verify_request_einfo(ridx, pgrec['ptcount'], pgrec['einfo'], logact)
         if einfo:
            sent = 1 if (self.send_customized_email("Rqst{}".format(ridx), einfo, emlact) and
                         self.pgexec("UPDATE dsrqst set einfo = NULL WHERE rindex = {}".format(ridx), logact)) else -1
         else:
            sent = 0
         self.lock_request(ridx, 0)
         if sent == -1: break
         ecnt += sent
      if cnt > 1: self.pglog("{} of {} DSRQST emails sent on {}".format(ecnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   # veriy email info for partition errors
   # retrun None if not all partitions finished
   def verify_request_einfo(self, ridx, ptcnt, einfo, logact = 0): 
      # no further checking if no partitionseinfo is empty   
      if ptcnt < 2 or not einfo: return einfo   
      # partition processes are not all done yet
      if self.pgget("ptrqst", "", "rindex = {} AND (pid > 0 OR status = 'R')".format(ridx), logact): return None
      pkey = ["<PARTERR>", "<PARTCNT>"]
      # einfo does not contain partition error key
      if einfo.find(pkey[0]) < 0: return einfo
      einfo = re.sub(pkey[0], '', einfo)
      ecnt = self.pgget("ptrqst", "", "rindex = {} AND status = 'E'".format(ridx), logact)   
      cbuf = "{} of {}".format(ecnt, ptcnt)   
      einfo = re.sub(pkey[1], cbuf, einfo)
      return einfo   

   # start recording due updates to checks
   def start_dsupdts(self, cnd, logact = 0):
      ctime = self.curtime(1)
      self.check_dsupdt_locks(cnd, logact)
      self.email_dsupdt_controls(cnd, logact)
      self.email_dsupdts(cnd, logact)
      cnd += "pid = 0 and cntltime <= '{}' and action > '' AND einfo IS NULL ORDER by cntltime".format(ctime)
      pgrecs = self.pgmget("dcupdt", "*", cnd, logact)
      cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      ucnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         if self.pgget("dscheck", "pid, lockhost", "oindex = {} AND command = 'dsupdt'".format(pgrec['cindex']), logact): continue
         if pgrec['pindex'] and not self.valid_data_time(pgrec): continue
         argv = "{} {} -CI {} -b -d".format(pgrec['dsid'], pgrec['action'], pgrec['cindex'])
         if not self.add_one_dscheck(pgrec['cindex'], 'C', "dsupdt", pgrec['dsid'], pgrec['action'],
                                     '', pgrec['specialist'], argv, None, pgrec, logact): break
         ucnt += 1
      if cnt > 1: self.pglog("update {} of {} DSUPDT controls on {}".format(ucnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)
      return ucnt

   # check if the parent update control is finished
   def parent_not_finished(self, pgrec):
      freq = [0, 0, 0]
      ms = re.match(r'^(\d+)([YMWDH])$', pgrec['frequency'], re.I)
      if ms:
         val = int(ms.group(1))
         unit = ms.group(2).upper()
         if not val: return 0
         if unit == 'Y':
            freq[0] = val
         elif unit == 'M':
            freq[1] = val
         elif unit == 'W':
            freq[2] = 7 * val
         elif unit == 'D':
            freq[2] = val
         elif unit == 'H':    # update frequency is hourly controlled
            freq.append(val)
      else:
         ms = re.match(r'^(\d+)M/(\d+)', pgrec['frequency'], re.I)
         if ms:
            val = int(ms.group(1))
            nf = int(ms.group(2))
            if nf < 2 or nf > 10 or (30%nf): return 0
            freq = [0, val, 0, 0, 0, 0, nf]    # number of fractions in a month
      dtime = self.adddatetime(pgrec['datatime'], freq[0], freq[1], freq[2], freq[3], freq[4], freq[5], freq[6])
      if self.pgget("dcupdt", "", "cindex = {} AND datatime < '{}'".format(pgrec['pindex'], dtime), self.PGOPT['extlog']):
         return 1
      else:
         return 0

   #  check long procssing updates and unlock the processes that are aborted
   def check_dsupdt_locks(self, ocnd, logact = 0):
      ltime = int(time.time())
      lochost = self.PGLOG['HOSTNAME']
      dtime = ltime - self.PGSIG['DTIME']
      cnd = ocnd + "pid > 0 AND "
      ctime = ltime - 4*self.PGSIG['CTIME']
      rtime = ltime - self.PGSIG['RTIME']
      cnd += "chktime > 0 AND (chktime < {} OR chktime < {} AND lockhost {} OR chktime < {} AND lockhost = 'rda_config')".format(ctime, dtime, self.CHKHOST['hostcond'], rtime)
      pgrecs = self.pgmget("dcupdt", "cindex, lockhost, pid, chktime", cnd, logact)
      cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      lcnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         lmsg = "{}({}) at {} on {}".format(pgrec['lockhost'], pgrec['pid'], self.current_datetime(), self.PGLOG['HOSTNAME'])
         idx = pgrec['cindex']
         if self.CHKHOST['chkhost'] or pgrec['lockhost'] == lochost:
            if self.lock_update_control(idx, 0) > 0:
               self.pglog("UC{}: unlocked {}".format(idx, lmsg), self.LOGWRN)
               lcnt += 1
               continue
            if(self.pgexec("UPDATE dcupdt SET chktime = {} WHERE cindex = {} AND pid = {}".format(ltime, idx, pgrec['pid']), logact) and
               not self.pgget("dscheck", "", "oindex = {} AND command = 'dsupdt'".format(idx))):
               self.pglog("UC{}: time updated for {}".format(idx, lmsg), self.LOGWRN)
         elif not pgrec['lockhost'] or pgrec['lockhost'] == 'rda_config':
            record = {'pid' : 0, 'lockhost' : ''}
            if self.pgupdt("dcupdt", record, "cindex = {} AND pid = {}".format(idx, pgrec['pid']), logact):
               self.pglog("UC{}: unlocked {}".format(idx, lmsg), self.LOGWRN)
               lcnt += 1
               continue
         elif (logact&self.EMEROL) == self.EMEROL:
            self.pglog("UC{}: time NOT updated for {} of {}".format(idx, self.dscheck_runtime(pgrec['chktime'], ltime), lmsg), logact)
         self.RUNPIDS["{}{}".format(pgrec['lockhost'], pgrec['pid'])] = 1
      if cnt > 1: self.pglog("{} of {} DSUPDT Controls unlocked on {}".format(lcnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)
      cnd = ocnd + "pid > 0 AND locktime > 0 AND "
      cnd += "(locktime < {} OR locktime < {} AND hostname {} OR locktime < {} AND hostname = 'rda_config')".format(ctime, dtime, self.CHKHOST['hostcond'], rtime)
      pgrecs = self.pgmget("dlupdt", "lindex, hostname, pid, locktime", cnd, logact)
      cnt = (len(pgrecs['lindex']) if pgrecs else 0)
      lcnt = 0
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         lmsg = "{}({}) at {} on {}".format(pgrec['hostname'], pgrec['pid'], self.current_datetime(), self.PGLOG['HOSTNAME'])
         idx = pgrec['lindex']
         if self.CHKHOST['chkhost'] or pgrec['hostname'] == lochost:
            if self.lock_update(idx, None, 0) > 0:
               self.pglog("Updt{}: unlocked {}".format(idx, lmsg), self.LOGWRN)
               lcnt += 1
               continue
            self.pgexec("UPDATE dlupdt SET locktime = {} WHERE lindex = {} AND pid = {}".format(ltime, idx, pgrec['pid']), logact)
         elif not pgrec['hostname'] or pgrec['hostname'] == 'rda_config':
            record = {'pid' : 0, 'hostname' : ''}
            if self.pgupdt("dlupdt", record, "lindex = {} AND pid = {}".format(idx, pgrec['pid']), logact):
               self.pglog("Updt{}: unlocked {}".format(idx, lmsg), self.LOGWRN)
               lcnt += 1
               continue
         elif (logact&self.EMEROL) == self.EMEROL:
            self.pglog("Updt{}: time NOT updated for {} of {}".format(idx, self.dscheck_runtime(pgrec['locktime'], ltime), lmsg), logact)
         self.RUNPIDS["{}{}".format(pgrec['hostname'], pgrec['pid'])] = 1
      if cnt > 1: self.pglog("{} of {} DSUPDT Local Files unlocked on {}".format(lcnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   #  check dsupdts and send saved email
   def email_dsupdt_controls(self, cnd, logact = 0):
      emlact = self.LOGWRN|self.FRCLOG
      if logact and (logact&self.EMEROL) == self.EMEROL: emlact |= self.EMEROL
      cnd += "pid = 0 AND einfo IS NOT NULL"
      pgrecs = self.pgmget("dcupdt", "cindex", cnd, logact)
      cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      ecnt = 0
      for i in range(cnt):
         cidx = pgrecs['cindex'][i]
         if self.lock_update_control(cidx, 1) <= 0: continue
         pgrec = self.pgget("dcupdt", "einfo", "cindex = {}".format(cidx), logact)
         if pgrec['einfo']:
            sent = 1 if (self.send_customized_email("UC{}".format(cidx), pgrec['einfo'], emlact) and
                         self.pgexec("UPDATE dcupdt set einfo = NULL WHERE cindex = {}".format(cidx), logact)) else -1
         else:
            sent = 0
         self.lock_update_control(cidx, 0)
         if sent == -1: break
         ecnt += sent
      if cnt > 1: self.pglog("{} of {} DSUPDT Control emails sent on {}".format(ecnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   #  check dsupdts and send saved email
   def email_dsupdts(self, cnd, logact = 0):
      emlact = self.LOGWRN|self.FRCLOG
      if logact and (logact&self.EMEROL) == self.EMEROL: emlact |= self.EMEROL
      cnd += "pid = 0 AND emnote IS NOT NULL"
      pgrecs = self.pgmget("dlupdt", "lindex, cindex", cnd, logact)
      cnt = (len(pgrecs['lindex']) if pgrecs else 0)
      ecnt = 0
      for i in range(cnt):
         idx = pgrecs['cindex'][i]
         if idx > 0 and self.pgget("dcupdt", "", "cindex = {} AND pid > 0".format(idx), logact): continue
         idx = pgrecs['lindex'][i]
         if self.lock_update(idx, None, 1) <= 0: continue
         pgrec = self.pgget("dlupdt", "emnote", "lindex = {}".format(idx), logact)
         if pgrec['emnote']:
            sent = 1 if(self.send_customized_email("Updtidx", pgrec['emnote'], emlact) and
                        self.pgexec("UPDATE dlupdt set emnote = NULL WHERE lindex = {}".format(idx), logact)) else -1
         else:
            sent = 0
         self.lock_update(idx, None, 0)
         if sent == -1: break
         ecnt += sent
      if cnt > 0: self.pglog("{} of {} DSUPDT emails sent on {}".format(ecnt, cnt, self.PGLOG['HOSTNAME']), self.WARNLG)

   # create an dscheck record for a given command
   def add_one_dscheck(self, oindex, otype, cmd, dsid, action, workdir, specialist, argv, remail, btctl, logact = 0):
      cidx = 0
      if len(argv) > 100:
         argextra = argv[100:]
         argv = argv[0:100]
      else:
         argextra = None
      record = {'command' : cmd, 'argv' : argv, 'specialist' : specialist, 'workdir' : workdir,
                'dsid' : dsid, 'action' : action, 'oindex' : oindex, 'otype' : otype}
      (record['date'], record['time']) = self.get_date_time()
      if argextra: record['argextra'] = argextra
      if 'PI' in self.params: record['pindex'] = self.params['PI'][0]
      if 'MC' in self.params and self.params['MC'][0] > 0: record['mcount'] = self.params['MC'][0]
      record.update(self.get_batch_options(btctl))
      if cmd == 'dsrqst' and remail:
         record['remail'] = remail
         if otype == 'P':
            pgcnt = self.pgget("dscheck", "", "remail = '{}' AND otype = 'P'" .format(remail), logact)
            if pgcnt >= self.get_user_limit(remail)[1]: return self.FAILURE
         elif action != 'PR':
            pgcnt = self.pgget("dscheck", "", "remail = '{}' AND otype = 'R'".format(remail), logact)
            if pgcnt >= self.get_user_limit(remail)[0]: return self.FAILURE
      if oindex and otype:
         pgrec = self.pgget('dscheck', '*', "oindex = {} AND otype = '{}'".format(oindex, otype), logact)
      else:
         pgrec = self.get_dscheck(cmd, argv, workdir, specialist, argextra, logact)
      if pgrec:
         return self.pglog("Chk{}: {} added already {} {}".format(pgrec['cindex'], self.get_command_info(pgrec), pgrec['date'], pgrec['time']), self.LOGWRN|self.FRCLOG)
      cidx = self.pgadd("dscheck", record, logact|self.AUTOID)
      if cidx:
         self.pglog("Chk{}: {} added {} {}".format(cidx, self.get_command_info(record), record['date'], record['time']), self.LOGWRN|self.FRCLOG)
      else:
         if oindex and otype:
            self.pglog("{}-{}-{}: Fail add check for {}".format(cmd, otype, oindex, specialist), self.LOGWRN|self.FRCLOG)
         else:
            self.pglog("{}: Fail add check for {}".format(cmd, specialist), self.LOGWRN|self.FRCLOG)
         time.sleep(self.PGSIG['ETIME'])
         return self.FAILURE
      return self.SUCCESS

   # get dscheck status
   @staticmethod
   def dscheck_status(stat):
      STATUS = {
         'C' : "Created",
         'D' : "Done",
         'E' : "Exit",
         'F' : "Finished",
         'H' : "Held",
         'I' : "Interrupted",
         'P' : "Pending",
         'Q' : "Queueing",
         'R' : "Run",
         'S' : "Suspended",
      }
      return (STATUS[stat] if stat in STATUS else "Unknown")

   # validate given daemon control indices
   def validate_daemons(self):
      if self.OPTS['DI'][2]&8: return     # already validated
      dcnt = len(self.params['DI']) if 'DI' in self.params else 0
      if not dcnt:
         if self.PGOPT['CACT'] == 'SD':
            if 'ND' not in self.params:
               self.action_error("Mode option -ND must be present to add new Daemon Control record")
            dcnt = self.get_max_count("HN", "CM")
            if dcnt > 0:
               self.params['DI'] = [0]*dcnt
         return
      i = 0
      while i < dcnt:
         val = self.params['DI'][i]
         if val:
            if not isinstance(val, int):
               if re.match(r'^(!|<|>|<>)$', val):
                  if self.OPTS[self.PGOPT['CACT']][2] > 0:
                     self.action_error("Invalid condition '{}' of Daemon Control index".format(val))
                  break
               self.params['DI'][i] = int(val)
         else:
            self.params['DI'][i] = 0
         i += 1
      if i >= dcnt: # normal daemon control index given
         for i in range(dcnt):
            val = self.params['DI'][i]
            if not val:
               if self.PGOPT['CACT'] != 'SD':
                  self.action_error("Daemon Control Index 0 is not allowed\nUse Action SD with Mode option -ND to add new record")
               elif not self.params['ND']:
                  self.action_error("Mode option -ND must be present to add new Daemon Control record")
               continue
            if i > 0 and val == self.params['DI'][i-1]: continue
            pgrec = self.pgget("dsdaemon", "specialist", "dindex = {}".format(val), self.PGOPT['extlog'])
            if not pgrec:
               self.action_error("Daemon Control Index '{}' is not in RDADB".format(val))
            elif(self.OPTS[self.PGOPT['CACT']][2] > 0 and self.params['LN'] != pgrec['specialist'] and
                 self.PGLOG['CURUID'] != self.PGLOG['GDEXUSER']):
               self.action_error("{}: must be {}, owner of Daemon Control Index {}".format(self.params['LN'], pgrec['specialist'], val))
      else: # found none-equal condition sign
         pgrec = self.pgmget("dsdaemon", "DISTINCT dindex",
                              self.get_field_condition("dindex", self.params['DI'], 0, 1), self.PGOPT['extlog'])
         if not pgrec: self.action_error("No Daemon Control matches given Index condition")
         self.params['DI'] = pgrec['dindex']
      self.OPTS['DI'][2] |= 8  # set validated flag

   # validate given check indices
   def validate_checks(self):
      if (self.OPTS['CI'][2]&8) == 8: return # already validated
      if 'CI' in self.params:
         cnt = len(self.params['CI'])
         i = 0
         while i < cnt:
            val = self.params['CI'][i]
            if val:
               if not isinstance(val, int):
                  if re.match(r'^(!|<|>|<>)$', val):
                     if self.OPTS[self.PGOPT['CACT']][2] > 0:
                        self.action_error("Invalid condition '{}' of Check index".format(val))
                     break
                  self.params['CI'][i] = int(val)
            else:
               self.params['CI'][i] = 0
            i += 1
         if i >= cnt: # normal check index given
            for i in range(cnt):
               val = self.params['CI'][i]
               if not val: self.action_error("Check Index 0 is not allowed")
               if i > 0 and val == self.params['CI'][i-1]: continue
               pgrec = self.pgget("dscheck", "specialist", "cindex = {}".format(val), self.PGOPT['extlog'])
               if not pgrec:
                  self.action_error("Check Index '{}' is not in RDADB".format(val))
               elif(self.OPTS[self.PGOPT['CACT']][2] > 0 and self.params['LN'] != pgrec['specialist'] and
                    self.PGLOG['CURUID'] != self.PGLOG['GDEXUSER']):
                  self.action_error("{}: must be {}, owner of Check Index {}".format(self.params['LN'], pgrec['specialist'], val))
         else: # found none-equal condition sign
            pgrec = self.pgmget("dscheck", "cindex", self.get_field_condition("cindex", self.params['CI'], 0, 1), self.PGOPT['extlog'])
            if not pgrec: self.action_error("No Check matches given Index condition")
            self.params['CI'] = pgrec['cindex']
      self.OPTS['CI'][2] |= 8  # set validated flag

   # validate given dataset IDs
   def validate_datasets(self):
      if self.OPTS['DS'][2]&8: return    # already validated
      dcnt = len(self.params['DS'])
      for i in range(dcnt):
         dsid = self.params['DS'][i]
         if not dsid: self.action_error("Empty Dataset ID is not allowed")
         if i and dsid == self.params['DS'][i-1]: continue
         if not self.pgget("dataset", "", "dsid = '{}'".format(dsid), self.PGOPT['extlog']):
            self.action_error("Dataset '{}' is not in RDADB".format(dsid))
      self.OPTS['DS'][2] |= 8    # set validated flag
