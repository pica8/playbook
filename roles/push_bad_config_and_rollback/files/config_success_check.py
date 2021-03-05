#!/usr/bin/python


import os,sys,commands,re

def getCmds():
    cmd = "/pica/bin/pica_sh -c 'configure;show all| display set'"
    status,output = commands.getstatusoutput(cmd)
    if status==0:
        cmds_arry=re.findall("(set .*)",output)
        return cmds_arry
    else:
        result = dict(msg='can not get config',rc=status)

def readConfigFile(file):
    orig_cmds_list = []
    if os.path.exists(file):
        with open(file) as cf:
            orig_cmds_list = cf.readlines()
    else:
       result = dict(msg='can not get config file',rc=False)
    orig_cmds = ";".join(orig_cmds_list)
    return orig_cmds

def checkCmds(cmds):
    cmd_arry=cmds.split(";")
    full_config_list = getCmds()
    full_config_str = ''.join(full_config_list)
    new_cmd = []
    for cmd in cmd_arry:
        if full_config_str.find(cmd.replace('\n','').replace('\r','').replace('\\','')) == -1:
            new_cmd.append(cmd)
    return new_cmd

config_file, = sys.argv[1:2]
orig_cmds=readConfigFile(config_file)
miss_cmds = checkCmds(orig_cmds)
if len(miss_cmds)>0:
    sys.exit(miss_cmds)
else:
    sys.exit()