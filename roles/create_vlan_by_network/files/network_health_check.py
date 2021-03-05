#!/usr/bin/python


import os,sys,time, subprocess

#get the time need to running
start_time, failed_times, ampcon_ip = sys.argv[1:4]

time.sleep(int(start_time))
failed = 0

def network_ping_ampcon(sHost):
   try:
      output = subprocess.check_output("ping -{} 1 {}".format('c', sHost), shell=True)
   except Exception, e:
      return False
   return True

def rollback_config():
   try:
      output = subprocess.check_output('/pica/bin/pica_sh -c "configure;rollback 1;commit"', shell=True)
   except Exception, e:
      return False
   return True

while True:
   #check the network health
   if not network_ping_ampcon(ampcon_ip):
      failed = failed + 1
      print("Check network health failed")
      if failed > int(failed_times):
          #rollback  config
          if rollback_config():
             print("Success to rollback config")
          else:
             print("Failed to rollback config")
          exit()
      time.sleep(10)
   else:
       exit()