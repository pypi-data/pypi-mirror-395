#!/usr/bin/env python3
#
##################################################################################
#
#     Title: dscheck
#    Author: Zaihua Ji, zji@ucar.edu
#      Date: 09/28/2020
#            2025-02-05 transferred to package rda_python_dscheck from
#            https://github.com/NCAR/rda-utility-programs.git
#             2025-12-05 convert to class DsCheck
#   Purpose: python utility program to check and start command saved in dscheck
#
#    Github: https://github.com/NCAR/rda-python-dscheck.git
#
##################################################################################
#
import os
import re
import sys
import time
from os import path as op
from .pg_check import PgCheck

class DsCheck(PgCheck):

   def __init__(self):
      super().__init__()  # initialize parent class
      self.ALLCNT = 0  # global counting variables

   # read in command line parameters
   def read_parameters(self):   
      self.set_help_path(__file__)
      aname = 'dscheck'
      self.parsing_input(aname)
      self.check_dscheck_options(self.PGOPT['CACT'], aname)

   # start action of dscheck
   def start_actions(self):
      if self.PGOPT['CACT'] == 'AC':
         self.add_check_info()
      elif self.PGOPT['CACT'] == 'CH':
         self.check_host_connection()
      elif self.PGOPT['CACT'] == 'DL':
         if 'CI' in self.params:
            self.ALLCNT = len(self.params['CI'])
            self.delete_check_info()
         if 'DI' in self.params:
            self.ALLCNT = len(self.params['DI'])
            self.delete_daemon_info()
      elif self.PGOPT['CACT'] == 'EC':
         self.email_check_info()
      elif self.PGOPT['CACT'] == 'GC':
         self.get_check_info()
      elif self.PGOPT['CACT'] == 'GD':
         self.get_daemon_info()
      elif self.PGOPT['CACT'] == "IC":
         self.ALLCNT = len(self.params['CI'])
         self.interrupt_dschecks()
      elif self.PGOPT['CACT'] == 'PC':
         self.set_batch_options(self.params, 2, 1)
         if 'DM' in self.params:
            self.ALLCNT = 0
            self.handle_dschecks()
         else:
            self.process_dschecks()
      elif self.PGOPT['CACT'] == 'SD':
         self.ALLCNT = len(self.params['DI'])
         self.set_daemon_info()
      elif self.PGOPT['CACT'] == 'SO':
         self.set_batch_options(self.params, 2, 1)
         self.process_dscheck_options()
      elif self.PGOPT['CACT'] == "UL":
         self.ALLCNT = len(self.params['CI']) if 'CI' in self.params else 0
         self.unlock_checks()
      if self.OPTS[self.PGOPT['CACT']][2]: self.cmdlog()  # log end time if not getting action

   # add a check for customized command
   def add_check_info(self):
      cmd = self.params['CM'].pop(0)
      argstr = self.argv_to_string(self.params['CM'], 0)
      if 'AV' in self.params:
         if argstr: argstr += " "
         argstr += self.argv_to_string(self.params['AV'], 0)
      dsid = self.params['DS'][0] if 'DS' in self.params else None
      action = self.params['AN'][0] if 'AN' in self.params else None
      self.set_batch_options(self.params, 2, 1)
      specialist = self.params['SN'][0] if 'SN' in self.params else self.params['LN']
      workdir = self.params['WD'][0] if 'WD' in self.params else self.PGLOG['CURDIR']
      self.add_one_dscheck(0, '', cmd, dsid, action, workdir, specialist,
                           argstr, None, None, self.PGOPT['extlog'])

   # delete dscheck daemon controls for given daemon control indices
   def delete_daemon_info(self):
      s = 's' if self.ALLCNT > 1 else ''
      self.pglog("Delete {} dscheck daemon control{} ...".format(self.ALLCNT, s), self.WARNLG)
      delcnt = 0
      for i in range(self.ALLCNT):
         delcnt += self.pgdel("dsdaemon", "dindex = {}".format(self.params['DI'][i]), self.PGOPT['extlog'])
      self.pglog("{} of {} dscheck daemon control{} deleted".format(delcnt, self.ALLCNT, s), self.PGOPT['wrnlog'])

   # delete checks for given check indices
   def delete_check_info(self):
      s = 's' if self.ALLCNT > 1 else ''
      self.pglog("Delete {} dscheck record{} ...".format(self.ALLCNT, s), self.WARNLG)
      delcnt = 0
      for i in range(self.ALLCNT):
         cidx = self.lock_dscheck(self.params['CI'][i], 2, self.PGOPT['extlog'])
         if cidx <= 0: continue
         delcnt += self.delete_dscheck(None, "cindex = {}".format(cidx), self.PGOPT['extlog'])
      self.pglog("{} of {} check record{} deleted".format(delcnt, self.ALLCNT, s), self.PGOPT['wrnlog'])

   # email notice of check status for specialist
   def email_check_info(self):
      cnd = self.get_hash_condition("dscheck", None, None, 1)
      pgrecs = self.pgmget("dscheck", "*", cnd + " ORDER BY cindex", self.PGOPT['extlog'])
      allcnt = (len(pgrecs['cindex']) if pgrecs else 0)
      if not allcnt: return self.pglog("{}: No Check Information Found to send email for {}".format(self.PGLOG['CURUID'], cnd), self.LOGWRN)
      if allcnt > 1:
         s = 's'
         ss = "are"
      else:
         s = ''
         ss = "is"
      subject = "{} active Check Record{}".format(allcnt, s)
      mbuf = "{} {} listed:\n".format(subject, ss)
      pgrecs = {'status' : self.get_check_status(pgrecs, allcnt)}
      for i in range(allcnt):
         if i > 0: mbuf += self.PGLOG['SEPLINE']
         mbuf += self.build_check_message(self.onerecord(pgrecs, i))
      if 'CC' in self.params: self.add_carbon_copy(self.params['CC'])
      subject += " found"
      self.send_email(subject, self.params['LN'], mbuf)
      self.pglog("Email sent to {} With Subject '{}'".format(self.params['LN'], subject), self.LOGWRN)

   # build email message for a given check record
   def build_check_message(self, pgrec):
      msg = "Check Index: {}\nCommand: {} {}".format(pgrec['cindex'], pgrec['command'], pgrec['argv'])
      if pgrec['argextra']: msg += self.break_long_string(pgrec['argextra'], 100, "...", 1)
      msg += ("\nWork Directory: {}\n".format(pgrec['workdir']) +
              "Initial Execution: {} {} byb {}\n".format(pgrec['date'], pgrec['time'], pgrec['specialist']) +
              "Current Status: {}\n".format(pgrec['status']))
      if pgrec['errmsg']:
        msg += "Error Message: {}\n".format(pgrec['errmsg'])
      elif not pgrec['pid']:
        msg += "Error Message: Aborted abnormally\n";     
      return msg

   # get dscheck daemon control information
   def get_daemon_info(self):
      tname = "dsdaemon"
      hash = self.TBLHASH[tname]   
      self.pglog("Get dscheck daemon control information from RDADB ...", self.WARNLG)
      oflds = lens = fnames = None
      if 'FN' in self.params: fnames = self.params['FN']
      fnames = self.fieldname_string(fnames, self.PGOPT[tname], self.PGOPT[tname])
      onames = self.params['ON'] if 'ON' in self.params else "I"
      qnames = fnames + self.append_order_fields(onames, fnames, tname)
      condition = self.get_hash_condition(tname, None, None, 1); 
      if 'ON' in self.params and 'OB' in self.params:
         oflds = self.append_order_fields(onames, None, tname)
      else:
         condition += self.get_order_string(onames, tname)
      pgrecs = self.pgmget(tname, self.get_string_fields(qnames, tname), condition, self.PGOPT['extlog'])
      if pgrecs:
         if 'OF' in self.params: lens = self.all_column_widths(pgrecs, fnames, hash)
         if oflds: pgrecs = self.sorthash(pgrecs, fnames, hash, self.params['OB'])
      self.OUTPUT.write(self.get_string_titles(fnames, hash, lens) + "\n")
      if pgrecs:
         cnt = self.print_column_format(pgrecs, fnames, hash, lens)
         s = 's' if cnt > 1 else ''
         self.pglog("{} daemon control{} retrieved".format(cnt, s), self.PGOPT['wrnlog'])
      else:
         self.pglog("No daemon control information retrieved", self.PGOPT['wrnlog'])

   # get check information
   def get_check_info(self):
      tname = 'dscheck'
      hash = self.TBLHASH[tname]     
      self.pglog("Get check information from RDADB ...", self.WARNLG)
      lens = oflds = fnames = None
      if 'FN' in self.params: fnames = self.params['FN'] 
      fnames = self.fieldname_string(fnames, self.PGOPT[tname], self.PGOPT['chkall'])
      onames = self.params['ON'] if 'ON' in self.params else "I"
      condition = self.get_hash_condition(tname, None, None, 1); 
      if 'ON' in self.params and 'OB' in self.params:
         oflds = self.append_order_fields(onames, None, tname)
      else:
         condition += self.get_order_string(onames, tname)
      pgrecs = self.pgmget(tname, "*", condition, self.PGOPT['extlog'])
      if pgrecs:
         if 'CS' in self.params:
            pgrecs['status'] = self.get_check_status(pgrecs)
            if fnames.find('U') < 0: fnames == 'U'
         if 'FO' in self.params: lens = self.all_column_widths(pgrecs, fnames, hash)
         if oflds: pgrecs = self.sorthash(pgrecs, oflds, hash, self.params['OB'])
      self.OUTPUT.write(self.get_string_titles(fnames, hash, lens) + "\n")
      if pgrecs:
         cnt = self.print_column_format(pgrecs, fnames, hash, lens)
         s = 's' if cnt > 1 else ''
         self.pglog("{} check record{} retrieved".format(cnt, s), self.PGOPT['wrnlog'])
      else:
         self.pglog("No check information retrieved", self.PGOPT['wrnlog'])

   # add or modify dscheck daemon control information
   def set_daemon_info(self):
      tname = "dsdaemon"
      hash = self.TBLHASH[tname]
      s = 's' if self.ALLCNT > 1 else ''
      self.pglog("Set information of {} dscheck daemon control{} ...".format(self.ALLCNT, s), self.WARNLG)
      addcnt = modcnt = 0
      flds = self.get_field_keys(tname, None, 'I')
      self.validate_multiple_values(tname, self.ALLCNT, flds)
      for i in range(self.ALLCNT):  
         didx = self.params['DI'][i] if 'DI' in self.params else 0
         if didx > 0:
            cnd = "dindex = {}".format(didx)
            pgrec = self.pgget(tname, "*", cnd, self.PGOPT['extlog'])
            if not pgrec: self.action_error("Miss daemon record for " + cnd, 'SD')
         else:
            pgrec  = None
         record = self.build_record(flds, pgrec, tname, i)
         if record:
            if 'priority' in record and (record['priority'] < 0 or record['priority'] > 10):
               self.action_error("{}: Priority value must in range 0(highest) - 10(lowest)".format(record['priority']), 'SD')
            if pgrec:
               modcnt += self.pgupdt(tname, record, cnd, self.PGOPT['extlog'])
            else:
               if 'specialist' not in record and self.params['LN'] != self.PGLOG['GDEXUSER']: record['specialist'] = self.params['LN']
               didx = self.pgadd(tname, record, self.PGOPT['extlog']|self.AUTOID)
               if didx:
                  self.pglog("Daemon Control Index {} added".format(didx), self.PGOPT['wrnlog'])
                  addcnt += 1
      self.pglog("{}/{} of {} daemon control{} added/modified in RDADB!".format(addcnt, modcnt, self.ALLCNT, s), self.PGOPT['wrnlog'])

   # expand check status info
   def get_check_status(self, pgrecs, cnt = 0):
      if not cnt: cnt = (len(pgrecs['cindex']) if pgrecs else 0)
      stats = [None]*cnt
      for i in range(cnt):
         pgrec = self.onerecord(pgrecs, i)
         if pgrec['pid']:
            percent = self.complete_percentage(pgrec)
            runhost = ""
            if percent < 0:
               stats[i] = "Pending"
            else:
               stats[i] = self.get_execution_string(pgrec['status'], pgrec['tcount'])
               rtime = self.dscheck_runtime(pgrec['stttime'])
               if rtime: stats[i] += " {}".format(rtime)
               if percent > 0: stats[i] += ", {}% done".format(percent)
               if pgrec['runhost']: runhost = pgrec['runhost']
            stats[i] += self.lock_process_info(pgrec['pid'], pgrec['lockhost'], runhost)
         else:
            stats[i] = self.dscheck_status(pgrec['status'])
            if pgrec['status'] == 'D' or pgrec['status'] == 'P':
               runhost = (pgrec['runhost'] if pgrec['runhost'] else pgrec['lockhost'])
               if runhost: stats[i] += " on " + runhost
            elif pgrec['status'] == 'C' and pgrec['pindex']:
               stats[i] = "Wait on CHK {}".format(pgrec['pindex'])
      return stats

   # get the percentage of the check job done 
   def complete_percentage(self, check):
      percent = 0
      if check['bid'] and not check['stttime']:
         percent = -1
      elif check['fcount'] > 0 and check['dcount']:
         percent = int(100*check['dcount']/check['fcount'])
      elif check['command'] == "dsrqst" and check['oindex']:
         if check['otype'] == 'P':
            percent = self.get_partition_percentage(check['oindex'])
         else:
            percent = self.get_dsrqst_percentage(check['oindex'])
      return (percent if percent < 100 else 99)

   # get a request percentage finished
   def get_dsrqst_percentage(self, ridx):
      rcnd = "rindex = {}".format(ridx)
      pgrqst = self.pgget("dsrqst", "fcount, pcount", rcnd)
      if pgrqst:
         fcnt = pgrqst['fcount'] if pgrqst['fcount'] else 0
         if fcnt < 1: fcnt = self.pgget("wfrqst", "", rcnd)
         if fcnt > 0:
            dcnt = pgrqst['pcount'] if pgrqst['pcount'] else 0
            if dcnt < 1: dcnt = self.pgget("wfrqst", "", rcnd + " AND status = 'O'")
            if dcnt > 0:
               percent = int(100*dcnt/fcnt)
               if percent > 99: percent = 99
               return percent
      return 0

   # get a partition percentage finished
   def get_partition_percentage(self, pidx, cidx = 0):
      pcnd = "pindex = {}".format(pidx)
      pgrec = self.pgget('ptrqst', "fcount", pcnd)
      if pgrec:
         fcnt = pgrec['fcount'] if pgrec['fcount'] else 0
         if fcnt < 1: fcnt = self.pgget("wfrqst", "", pcnd)
         if fcnt > 0:
            dcnt = self.pgget("wfrqst", "", pcnd + " AND status = 'O'")
            if dcnt > 0:
               percent = int(100*dcnt/fcnt)
               if percent > 99: percent = 99
               return percent
      return 0

   #  get excecution string for give try count
   def get_execution_string(self, stat, trycnt = 0):
      str = self.dscheck_status(stat)
      if trycnt > 1: str += "({})".format(self.int2order(trycnt))
      return str

   # interrupt checks for given dscheck indices
   def interrupt_dschecks(self):
      s = 's' if self.ALLCNT > 1 else ''
      delcnt = 0
      for i in range(self.ALLCNT):
         cidx = self.params['CI'][i]
         cnd = "cindex = {}".format(cidx)
         cstr = "Check Index {}".format(cidx)
         pgrec = self.pgget("dscheck", "*", cnd, self.PGOPT['extlog'])
         if not pgrec: self.pglog(cstr +": NOT in RDADB", self.PGOPT['extlog'])
         pid = pgrec['pid']
         if pid == 0:
            self.pglog(cstr + ": Check is not under process; no interruption", self.PGOPT['wrnlog'])
            continue
         host = pgrec['lockhost']
         if not self.local_host_action(host, "interrupt check", cstr, self.PGOPT['errlog']): continue
         opts = "-h {} -p {}".format(host, pid)
         buf = self.pgsystem("rdaps " + opts, self.LOGWRN, 20)  # 21 = 4 + 16
         if buf:
            ms = re.match(r'^\s*(\w+)\s+', buf)
            if ms:
               uid = ms.group(1)
               if uid != self.params['LN']:
                  self.pglog("{}: login name '{}'; must be '{}' to interrupt".format(cstr, self.params['LN'], uid), self.PGOPT['wrnlog'])
                  continue
               if 'FI' not in self.params:
                  self.pglog("{}: locked by {}/{}; must add Mode option -FI (-ForceInterrupt) to interrupt".format(cstr, pid, host), self.PGOPT['wrnlog'])
                  continue
               if not self.pgsystem("rdakill " + opts, self.LOGWRN, 7):
                  self.pglog("{}: Failed to interrupt Check locked by {}/{}".format(cstr, pid, host), self.PGOPT['errlog'])
                  continue
            else:
               self.pglog("{}: check process stopped for {}/{}".format(cstr, pid, host), self.PGOPT['wrnlog'])
         pgrec = self.pgget("dscheck", "*", cnd, self.PGOPT['extlog'])
         if not pgrec['pid']:
            if self.lock_dscheck(cidx, 1, self.PGOPT['extlog']) <= 0: continue
         elif pid != pgrec['pid'] or host != pgrec['lockhost']:
            self.pglog("{}: Check is relocked by {}/{}".format(cstr, pgrec['pid'], pgrec['lockhost']), self.PGOPT['errlog'])
            continue
         pgrec['status'] = 'I'
         self.delete_dscheck(pgrec, None, self.PGOPT['extlog'])
         if pgrec['command'] == 'dsupdt':
            if pgrec['oindex']:
               cnd = "cindex = {} AND pid = {} AND ".format(pgrec['oindex'], pid)
               if self.pgexec("UPDATE dcupdt set pid = 0 WHERE {}lockhost = '{}'".format(cnd, host), self.PGOPT['extlog']):
                  self.pglog("Update Control Index {} unlocked".format(pgrec['oindex']), self.LOGWRN)
            else:
               cnd = "dsid = '{}' AND pid = {} AND ".format(pgrec['dsid'], pid)
            dlupdt = self.pgget("dlupdt", "lindex", "{}hostname = '{}'".format(cnd , host))
            if dlupdt and self.pgexec("UPDATE dlupdt set pid = 0 WHERE lindex = {}".format(dlupdt['lindex']), self.PGOPT['extlog']):
               self.pglog("Update Local File Index {} unlocked".format(dlupdt['lindex']), self.LOGWRN)
         elif pgrec['command'] == 'dsrqst':
            record = {'status' : 'I', 'pid' : 0}
            if pgrec['otype'] == 'P':
               table = "ptrqst"
               field = "pindex"
               msg = "Request Partition Index"
            else:
               table = "dsrqst"
               field = "rindex"
               msg = "Request Index"
            if pgrec['oindex']:
               cnd = "{} = {} AND pid = {} AND lockhost = '{}'".format(field, pgrec['oindex'], pid, host)
            else:
               cnd = "dsid = '{}' AND pid = {} AND lockhost = '{}'".format(pgrec['dsid'], pid, host)
            if self.pgupdt(table, record, cnd, self.PGOPT['extlog']):
               self.pglog("{} {} unlocked".format(msg, pgrec['oindex']), self.LOGWRN)
         delcnt += 1
      if self.ALLCNT > 1: self.pglog("{} of {} check{} interrupted".format(delcnt, self.ALLCNT, s), self.LOGWRN)

   # unlock checks for given check indices
   def unlock_checks(self):
      if self.ALLCNT > 0:
         s = 's' if self.ALLCNT > 1 else ''   
         self.pglog("Unlock {} check{} ...".format(self.ALLCNT, s), self.WARNLG)
         modcnt = 0
         for cidx in self.params['CI']:
            pgrec = self.pgget("dscheck", "pid, lockhost", "cindex = {}".format(cidx), self.PGOPT['extlog'])
            if not pgrec:
               self.pglog("Check {}: Not exists".format(cidx), self.PGOPT['errlog'])
            elif not pgrec['pid']:
               self.pglog("Check {}: Not locked".format(cidx), self.PGOPT['wrnlog'])
            elif self.lock_dscheck(cidx, -1, self.PGOPT['extlog']) > 0:
               modcnt += 1
               self.pglog("Check {}: Unlocked {}/{}".format(cidx, pgrec['pid'], pgrec['lockhost']), self.PGOPT['wrnlog'])
            elif(self.check_host_down(None, pgrec['lockhost']) and
                 self.lock_dscheck(cidx, -2, self.PGOPT['extlog']) > 0):
               modcnt += 1
               self.pglog("Check {}: Force unlocked {}/{}".format(cidx, pgrec['pid'], pgrec['lockhost']), self.PGOPT['wrnlog'])
            else:
               self.pglog("Check {}: Unable to unlock {}/{}".format(cidx, pgrec['pid'], pgrec['lockhost']), self.PGOPT['wrnlog'])
         if self.ALLCNT > 1: self.pglog("{} of {} check{} unlocked from RDADB".format(modcnt, self.ALLCNT, s), self.LOGWRN)
      else:
         cnd = "lockhost = '{}' AND ".format(self.get_host(1))
         self.check_dsrqst_locks(cnd, self.PGOPT['extlog'])
         self.check_dsupdt_locks(cnd, self.PGOPT['extlog'])
         self.check_dscheck_locks(cnd, self.PGOPT['extlog'])

   # process the checks
   def process_dschecks(self):
      logact = self.LOGERR
      if self.PGLOG['CURUID'] == self.PGLOG['GDEXUSER'] and (time.time()%(3*self.PGSIG['CTIME'])) < 60:
         logact |= self.EMEROL
      cnd = self.get_hash_condition("dscheck", "ST", None, 1)
      if cnd: cnd += " AND "
      if 'SN' not in self.params and self.params['LN'] != self.PGLOG['GDEXUSER']:
          cnd += "specialist = '{}' AND ".format(self.params['LN'])
      if 'WR' in self.params: self.start_dsrqsts(cnd, logact)
      if 'WU' in self.params: self.start_dsupdts(cnd, logact)
      acnd = self.get_hash_condition("dscheck", None, "ST", 1)
      if acnd: acnd += " AND "
      self.start_dschecks(cnd + acnd, logact)
      if self.PGLOG['ERRCNT']: self.send_error_email()

   # process the checks
   def process_dscheck_options(self):
      logact = self.LOGERR
      if self.PGLOG['CURUID'] == self.PGLOG['GDEXUSER'] and (time.time()%(3*self.PGSIG['CTIME'])) < 60:
         logact |= self.EMEROL
      cnd = self.get_hash_condition("dscheck", "ST", None, 1)
      if cnd: cnd += " AND "
      if 'SN' not in self.params and self.params['LN'] != self.PGLOG['GDEXUSER']:
          cnd += "specialist = '{}' AND ".format(self.params['LN'])
      acnd = self.get_hash_condition("dscheck", None, "ST", 1)
      if acnd: acnd += " AND "
      self.set_dscheck_options(self.get_host(1), cnd + acnd, logact)
      if self.PGLOG['ERRCNT']: self.send_error_email()

   # rdadata daemon handles the daemon controls
   def handle_dschecks(self):
      logact = ccnt = rcnt = ucnt = 0
      self.PGLOG['NOQUIT'] = 1
      ctime = 4*self.PGSIG['CTIME']
      etime = ctime
      while not self.PGSIG['QUIT']:
         if etime >= ctime:
            logact = self.LGEREX|self.EMEROL
            etime = 0
         else:
            logact = self.LGEREX
         ncnt = 0
         cnt = self.start_dsrqsts("", logact)
         ncnt += cnt
         rcnt += cnt
         cnt = self.start_dsupdts("", logact)
         ncnt += cnt
         ucnt += cnt
         cnt = self.start_dschecks("", logact)
         ncnt += cnt
         ccnt += cnt
         if self.PGLOG['ERRCNT']: self.send_error_email()
         if not ncnt: self.pgdisconnect(1)
         etime += self.sleep_daemon()
      self.PGLOG['NOQUIT'] = 0
      self.stop_daemon(self.prepare_quit(ccnt, rcnt, ucnt))

   # send an error email to the specialist
   def send_error_email(self):
      msg = "Error message for DSCHECK on " + self.PGLOG['HOSTNAME']
      self.send_email(msg)

   # prepare a summary string for quit
   @staticmethod
   def prepare_quit(ccnt, rcnt, ucnt):   
      msg = ""
      if rcnt > 0:
         s = 's' if rcnt > 1 else ''
         msg = "{} dsrqst{}".format(rcnt, s)
      if ccnt > 0:
         if msg: msg += ", "
         s = 's' if ccnt > 1 else ''
         msg += "{} dscheck{}".format(ccnt, s)
      if ucnt > 0:
         if msg: msg += ", "
         s = 's' if ucnt > 1 else ''
         msg += "{} dsupdt{}".format(ucnt, s)
      return msg

   # check a daemon host if connectable
   def check_host_connection(self):
      tname = "dsdaemon"
      hash = self.TBLHASH[tname]
      condition = self.get_hash_condition(tname, None, "H", 1)
      if 'HN' in self.params:
         pgrecs = {'specialist' : [], 'hostname' : []}
         spclsts = self.pgmget(tname, "DISTINCT specialist", condition, self.PGOPT['extlog'])
         if spclsts:
            for specialist in spclsts['specialist']:
               for hostname in self.params['HN']:
                  pgrecs['specialist'].append(specialist)
                  pgrecs['hostname'].append(hostname)
      else:
         pgrecs = self.pgmget(tname, "DISTINCT specialist, hostname", condition, self.PGOPT['extlog'])
      cnt = len(pgrecs['specialist']) if pgrecs else 0
      if not cnt:
         self.pglog("No daemon host found to check connectivity", self.LOGWRN)
         return
      if cnt > 1: self.pglog("Check {} daemon hosts for connectivity ...".format(cnt), self.WARNLG)
      for i in range(cnt):
         specialist = pgrecs['specialist'][i]
         hostname = pgrecs['hostname'][i]
         cmd = "ssh {} ps".format(hostname)
         if specialist != self.PGLOG['CURUID']:
            if self.PGLOG['CURUID'] != self.PGLOG['GDEXUSER']:
               self.pglog("{}: Cannot check connection to '{}' for {}".format(self.PGLOG['CURUID'], hostname, specialist), self.LOGERR)
               continue
            else:
               cmd = "pgstart_{} {}".format(specialist, cmd)
         self.pglog("Check conection to '{}' for {} ...".format(hostname, specialist), self.WARNLG)
         self.pgsystem(cmd, self.LOGERR, 4, None, 15)

# main function to excecute this script
def main():
   object = DsCheck()
   object.read_parameters()
   object.start_actions()
   object.pgexit(0)

# call main() to start program
if __name__ == "__main__": main()
