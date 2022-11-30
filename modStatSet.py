#
# Author: R. Niewolik Expertise Connect Team EMEM
# 2022-11-09 : Version 1
# 
# This is a sample jythin script to set 
#  - staticSet to custom/basic
#  - set pmi counter per pmi module and per server as defined in APMILIST
#
# importing some packages which may be used
import re
import os
import socket
import sys
import java
import java.util as util
import java.io as javaio
#
# Functions
#
def usage():
  print ""
  print "Usage :   ./wsadmin.sh -lang jython -f modStatSet.py {custom, basic, help}"
  print "   custom  = statistkitSet will be modfied to 'custom'. The pmi counter will be set as defined in this jython script (see MAIN section for more details"
  print "   basic   = tatistkitSet will be modfied to 'basic'"
  print "   help    = Script usage information"
  print ""
# endDef

def f_getnode():
   dmgrname = AdminControl.queryNames('WebSphere:name=DeploymentManager,*')
   #  WebSphere:name=DeploymentManager,process=dmgr,platform=common,node=e200n-z1tl0001,diagnosticProvider=true,version=
   if dmgrname == "":
     print "INFO: - getnode - No DeploymentManager exists"
     objn = AdminControl.completeObjectName('WebSphere:type=Server,*')
     node_name = AdminControl.getAttribute(objn, 'nodeName')
   else:
     match=re.search("node=([^\,]*)",dmgrname)
     if match:
       dmgrnode = match.group(1)
       print "INFO: - getnode - DeploymentManager = " + dmgrnode
     #endif
     system_name = f_GetShorthostname(socket.gethostname())
     nodes = AdminConfig.list('Node').splitlines()
     for node_id in nodes:
       #node_id=AdminConfig.getid("/Node:"+node_name+"/")
       node_name = AdminConfig.showAttribute(node_id,'name')
       nodehost = AdminConfig.showAttribute(node_id,'hostName')
       dcbindip = nodehost
       nodehost = f_GetShorthostname(nodehost)
       dmgrmatch = re.search(dmgrnode, node_name)
       if nodehost == system_name:
         if not dmgrmatch:
           nodefound = 1
           print "INFO: - getnode - Running on: " + dcbindip
           break
         #endif
       #endif
     #endif
   #endfor
   print "INFO: - getnode - Nodename = " + node_name
   return node_name
# endDef

def f_GetShorthostname(provided_name):
  match = re.search("^(\w+)(\.\w+)(\.\w+)*$", provided_name)
  if match:
    shortname = match.group(1)
  else:
    shortname = provided_name
  #endif
  return shortname
# endDef

def f_disSelectedSrv (selsvr, server_list):
  print "INFO: - disSelectedSrv - Selected servers on node '" + node_name + "' are:"
  #print "DBG - disSelectedSrv - selsvr=" + str(selsvr)
  result_list = []
  if str(selsvr) == "*":
    result_list = server_list
    i = 1
    for sn in result_list:
      server_name = AdminConfig.showAttribute(sn,'name')
      print '       ->    %2s. %-32s ' % ( str(i), server_name )
      i = i + 1
    #endfor
  else:
    serverOfInterrestsplt = map(int, selsvr.split(','))
    serverOfInterrestsplt.sort(reverse=False)
    for nr in serverOfInterrestsplt:
      if nr == " " or nr == "":
        continue
      #endif
      #nname=re.search("nodes\/(.*)\/servers", server_list[int(nr)-1])
      #print 'INFO: - disSelectedSrv -    %-32s (%-s)' % (  server_name , nname.group(1) )
      inr = int(nr)-1
      server_name = AdminConfig.showAttribute(server_list[inr],'name')
      print '       ->    %2s. %-32s ' % ( str(nr), server_name )
      result_list.extend([server_list[int(nr)-1]])
    #endfor
  #endif
  return result_list
# endDef 

def f_getserver(node_name):
  serverfinal_list = []
  plist = "[-serverType APPLICATION_SERVER -nodeName " + node_name + "]"
  server_list = AdminTask.listServers(plist)
  server_list = AdminUtilities.convertToList(server_list)
  server_list.sort()
  
  print "INFO: - getserver - Existing server on node '" + node_name + "' are: " 
  ans = 1
  while ans == 1:
    i = 0
    allserver = 0
    for server in server_list:
      i = i + 1
      server_name = AdminConfig.showAttribute(server,'name')
      #nname=re.search("nodes\/(.*)\/servers", server)
      #print "  " + str(i) + ". " + " (" + nname.group(1) + ") " + server_name
      print '       %2s. %-20s ' % (str(i),  server_name )
      continue
    #endfor
    serverOfInterrest = raw_input(">Type the numbers for the server you want to use seperated by comma, \"*\" for ALL or \"q\" to quit procedure. : \n-> ")
    serverOfInterrest = serverOfInterrest.replace('.', ",")
    serverOfInterrest = serverOfInterrest.replace(' ', ",")
    serverOfInterrest = serverOfInterrest.replace(',,', ",")
    if serverOfInterrest == "":
       print "ERROR - getserver - Selection is empty only numeric values allowed. Please select again..."
       continue
    elif serverOfInterrest[-1]==',':
      serverOfInterrest=serverOfInterrest[:-1]
    #endif
    if len(serverOfInterrest) == 1 and serverOfInterrest[0] == "q":
      return 3
    elif len(serverOfInterrest) == 1 and serverOfInterrest[0] == "*":
      allserver=1
    else:
      #check if integer seperated by comma
      se = re.search("^(\d+(,\d+)*)?$", serverOfInterrest)
      if not se:
        print "ERROR - getserver - Selection is \"" + serverOfInterrest + "\" but only numeric list values allowed (e.g. '1,2,3'). Please select again..."
        continue
      #endif
    #endif

    if allserver == 1:
      serverfinal_list = f_disSelectedSrv("*", server_list)   
    else:   
      atmp = serverOfInterrest.split(',')
      rc=0
      for nr in atmp:
        if nr == " " or nr == "":
          continue
        #endif
        inr = int(nr) - 1 
        if 0 <= inr < len(server_list):
           pass
        else:
          print "ERROR - getserver - Selection \"" + nr + "\" not in range. Please select again..."
          rc = 1
        #endif
      #endfor
      if rc == 1:
        continue
      else:
        serverfinal_list = f_disSelectedSrv(serverOfInterrest, server_list)
      #endif        
    #endif
    ans = f_confirm()
    if ans == 3 : 
      # procdure ended by user "q"  
      return 3
    #endif
  #endwhile
  return serverfinal_list
# endDef

def f_confirm():
    rc = 0
    ans = 1
    while ans == 1:
      confirm=raw_input(">Would you like to continue = \"y\" or to select again = \"s\" or to quit procedure = \"q\".  \n-> ")
      if confirm == "":  
        print "ERROR: - confirm - Value is empty. Please select again..."
      elif confirm == "q":
        return 3 
      elif confirm == "y":
        rc = 0
        ans = 0
      elif confirm == "s":
        ans = 0
        rc = 1
      elif len(confirm) > 1 :
        print "ERROR: - confirm - Value is '" + confirm + "' Only single char allowed ('y' or 's' or 'q'). Please select again..."
        ans = 1
      else:
        print "ERROR: - confirm - Value is '" + confirm + "' not correct ('y' or 's' or 'q'). Please select again..."
        ans = 1
      #endif
    #endwhile 
    return rc
# endDef

def f_setCustCounter(server, ModuleName, counter):
  #print "DBG: - setCustCounter - " + server + " " + ModuleName + " " + counter
  pmim = AdminConfig.list('PMIModule', server)
  pmiList = AdminConfig.showAttribute(pmim,'pmimodules')[1:-1].split(" ")
  for modules in pmiList:
    modName = AdminConfig.showAttribute(modules,'moduleName')
    #print "DBG: - setCustCounter - ModName=" + modName + ": :" + ModuleName + ":"
    if modName == str(ModuleName):
      modconf = modules
      print 'INFO: - setCustCounter - %-25s -counter-> %s' % (x[0],x[1])  
      # enable the counters
      #AdminConfig.modify(modconf, [ ['enable',counter] ])
    #endif
  #endfor  
# endDef

def f_modStatSet(server, statTotSet):
  #print "INFO: - modStatSet - Setting StatisticSet"  
  pmi = AdminConfig.list('PMIService', server)
  temp = AdminConfig.show(pmi,'statisticSet')
  current = re.search("statisticSet (.*)]", temp)
  currentsetting = current.group(1)
  if statTotSet == "basic":
    if currentsetting == "basic":
      print "INFO: - modStatSet - StatisticSet is ALREADY \"" + statTotSet + "\". No change"
    else:
      AdminConfig.modify(pmi, [['enable', 'true'], ['statisticSet','basic']])
      print "INFO: - modStatSet - Current StatisticSet is '"+ currentsetting + "'. Changing to 'basic'"
    #endif
  elif statTotSet == "custom":
    if currentsetting == "custom":
      print "INFO: - modStatSet - StatisticSet is ALREADY \"" + statTotSet + "\". No change"
    else: 
      AdminConfig.modify(pmi, [['enable', 'true'], ['statisticSet','custom']])
      print "INFO: - modStatSet - Current StatisticSet is '"+ currentsetting + "'. Changing to 'custom'"
    #endif  
  else:
    print "ERROR: - modStatSet - Something went wrong."
    os_exit(1)
  #endif 
# endDef

def f_disSelectedPMI (selpmi, pmi_list):
  print "INFO: - disSelectedPMI - Selected pmi (" + str(selpmi) + ") are:"
  result_list = []
  if str(selpmi) == "*":
    result_list = pmi_list
    i = 1
    for pmin in result_list:
      print '       ->    %2s. %-32s )' % ( str(i), pmin )
      i =  i + 1
    #endfor
  else:
    selpmi = map(int, selpmi.split(','))
    selpmi.sort()
    for nr in selpmi:
      if nr == " " or nr == "":
        continue
      #endif
      inr = int(nr)-1
      print '       ->    %2s. %-32s ' % ( str(nr), pmi_list[inr]  )
      result_list.extend([pmi_list[int(nr)-1]])
    #endfor
  #endif
  return result_list
# endDef

def f_getListOfPMI( apmilist ):
  print "INFO: - getListOfPMI - List of possible PMI modules selection"
  pmifinal_list = []
  ans = 1
  while ans == 1: 
    i = 1
    for nv in apmilist:
      x = nv.split(":")
      print '       %2s. %-25s -counter-> %s' % (str(i),  x[0], x[1])
      #print str(i) + ". Module = " + x[0] + " Counter = " + x[1]
      i = i+1
    #endfor
    pmitoset = raw_input(">Type the numbers for the PMI setttings you want to modify for the selected servers seperated by comma, \"*\" for all or \"q\" to quit procedure. : \n -> ")
    pmitoset = pmitoset.replace('.', ",")
    pmitoset = pmitoset.replace('.', ",")
    pmitoset = pmitoset.replace(' ', ",")
    pmitoset = pmitoset.replace(',,', ",")
    if pmitoset == "":
       print "ERROR - getListOfPMI - Selection is empty, only numeric values allowed (e.g. '1,2,3'). Please select again..."
       continue
    elif pmitoset[-1]==',':
      pmitoset=pmitoset[:-1]
    #endif
    allpmi = 0
    if len(pmitoset) == 1 and pmitoset[0] == "q":
      return 3
    elif len(pmitoset) == 1 and pmitoset[0] == "*":
      allpmi = 1
    else: 
      se = re.search("^(\d+(,\d+)*)?$", pmitoset)
      if not se:
        print "ERROR - getListOfPMI - Selection list is \"" + pmitoset + "\" but only numeric values allowed. Please select again..."
        continue
      #endif
    #endif
    if allpmi == 1:
      pmifinal_list = f_disSelectedPMI("*", apmilist)
    else: 
      atmp=pmitoset.split(',')
      rc = 0
      for nr in atmp:
        if nr == " " or nr == "":
          continue
        #endif
        inr = int(nr) - 1 
        if 0 <= inr < i:
          pass
        else:
          print "ERROR - getListOfPMI - Selection \"" + nr + "\" not in range. Please select again..."
          rc = 1
        #endif
      #endfor
      if rc == 1:
        continue
      else:
        pmifinal_list = f_disSelectedPMI(pmitoset, apmilist)
      #endif      
    #endif
    ans = f_confirm() 
    if ans == 3 :
      # procdure ended by user "q"    
      return 3
    #endif
  #endwhile
  return pmifinal_list
# endDef

# ------------
# --- MAIN ---
# ------------
print "INFO: - main - Started"
if not (len(sys.argv) == 1 ):
  usage()
  os._exit(1)
#endif

jvm_act=sys.argv[0]
if jvm_act == "help":
  usage()
  sys.exit(0)
#endif

if jvm_act == "basic" or jvm_act == "custom":
  pass
else:
  usage()
  sys.exit(1) 
#endif

# Get cellname
cellname = AdminControl.getCell()
print "INFO: - main - Cellname: " + cellname

# Get node name
node_name = f_getnode()

# Get a list of servers for modfications
list_server=f_getserver(node_name)
if list_server == 3 : 
  print "INFO: - main - Procedure ended by user "
  os._exit(3) 
#endif

# list of PMI modules and counter which can be set with that procedure
# If you need other, you can add modules or modify the counter list
# ITCAM recommandation: https://www.ibm.com/docs/en/iad/7.2.1?topic=applications-websphere-pmi-attribute-mapping
# WebSPhere PMI referance: https://www.ibm.com/docs/en/was/9.0.5?topic=pmi-data-organization
# 
# Changes proposed by ITCAM documentation:
# Availability Manager (appears to be z/OS) only                   - not set
# alarmManagerModule:1,2,3,4,5,6                                   - not set ->  All high
# connectionPoolModule:1,2,3,4,5,6,7,8,9,10,12,13,21,22            -     set ->  5-7,9,10 high
# cacheModule:1,2,3,4,21,22,23,24,25,26,27,28,29,30,31,32,34,35,36 - not set ->  All low
# DCSStats:1,2,3,6,7,8,9,10,11,12,14,16                            - not set ->  3-12 high
# j2cModule:1,2,3,4,5,6,7,8,9,10,12,13,14,15                       -     set ->  5-7,9,10 high
# schedulerModule,1,2,3,4,5,6,7,8,9,10,11                          - not set ->  All high
# servletSessionsModule:1,2,3,4,6,7,8,9,10,11,12,13,14,15,17,18    -     set ->  6,7 high ; 18 max
# threadPoolModule:1,2,3,4,5                                       -     set ->  5 high
# transactionModule:1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19  -     set ->  No high
# webAppModule:1,2,11,12,13,14                                     -     set ->  No high
# webServicesModule:11,12,13,14,15,16,17,18,19,20"                 -     set ->  No high
# Workload Management (appears to be z/OS) only                    - not set
# wsgwModule:1,2,3,4                                               -     set ->  No high  # WebServices Gateway
# All 'SIB Service' (StatGroup.SIBService.. how to set??)          - not set     
#                                     
APMILIST = [ \
             "connectionPoolModule:1,2,3,4,5,6,7,8,9,10,12,13,21,22", \
             "j2cModule:1,2,3,4,5,6,7,8,9,10,12,13,14,15", \
             "servletSessionsModule:1,2,3,4,6,7,8,9,10,11,12,13,14,15,17", \
             "threadPoolModule:1,2,3,4,5", \
             "webAppModule:1,2,11,12,13,14", \
             "webServicesModule:11,12,13,14,15,17,18", \
             "wsgwModule:1,2,3,4" \
           ]
APMILIST.sort()

if jvm_act == "custom": 
  list_pmi = f_getListOfPMI(APMILIST)
  if list_pmi == 3 : 
    print "INFO: - main - Procedure ended by user "
    os._exit(3) 
  #endif
#endif

for server in list_server:
  server_name = AdminConfig.showAttribute(server,'name')
  print  "INFO: - main - Working on server --- " + server_name + " ---"
  plist = 'cell=' + cellname + ',node=' + node_name + ',name=' + server_name + ',type=Server,*'
  server_status = AdminControl.completeObjectName(plist)
  #print  "DBG: - main -  Server: " + server_name 
  if server_status == '':
    print  "WARN: - main - " + server_name + " is NOT not running. Continuing with the next server .."
  else:
    print  "INFO: - main - " + server_name + " is running."
    if jvm_act == "custom": 
      f_modStatSet(server, jvm_act)
      for nv in list_pmi:
        x = nv.split(":")
        #print ' %2s. %-25s -counter-> %s' % (str(i),x[0],x[1])
        f_setCustCounter( server, x[0], x[1] )
      #endfor 
    else:
      f_modStatSet(server, jvm_act)
    #endif
  #endif
#endfor
print "INFO: - main - End server list ---"

print "INFO: - main - AdmiConfig save"
AdminConfig.save()

print "INFO: - main - Ended"
os._exit(0) 
