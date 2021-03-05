#!/usr/bin/python

import os,re,sys,subprocess

mlag_facts=''
mac_facts=''


def get_mlag_status():
   mlag_output = subprocess.check_output('/pica/bin/sif/tools/print_mlag -m LINKSUMMARY', shell=True)

   if 'MLAG Link ID is not found' not in mlag_output:
      total_mlag = int(re.findall("Total Links: ([0-9]+)",mlag_output)[0])
      heath_mlag = len(re.findall("(FULL         UP            UP           Yes)",mlag_output))
      ng_mlag = total_mlag - heath_mlag
   else:
      total_mlag = 0
      heath_mlag = 0
      ng_mlag = 0

   mlag_facts={"total_mlag": total_mlag,"working_well": heath_mlag,"not_working": ng_mlag}
   print mlag_facts

def get_mac_status():
   mac_output = subprocess.check_output('/pica/bin/sif/tools/print_fdb -b -f 2', shell=True)

   total_mac = int(re.findall("Total entries in switching table:   ([0-9]+)",mac_output)[0])
   static_mac = int(re.findall("Static entries in switching table:  ([0-9]+)",mac_output)[0])
   dynamic_mac = int(re.findall("Dynamic entries in switching table: ([0-9]+)",mac_output)[0])

   mac_facts={"total_mac": total_mac, "static_mac": static_mac,"dynamic_mac": dynamic_mac}
   print mac_facts

get_mlag_status()
get_mac_status()