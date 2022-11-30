# Modify-WebSpher-PMI-counter-ITCAM

This scripts sets the WebSphere StatistikSet to Custom and set specific counter or it sets the StatiskicSet back to Basic

Author: Richard Niewolik

Contact: niewolik@de.ibm.com

Revision: 1.0

#

[1 General](#1-general)
[2 Usage](#2-usage)


1 General
=========

Below the list of PMI modules and counter which can be set with that procedure, If you need other, you can add modules or modify the counter list.

ITCAM recommandation are: https://www.ibm.com/docs/en/iad/7.2.1?topic=applications-websphere-pmi-attribute-mapping

WebSPhere PMI referance: https://www.ibm.com/docs/en/was/9.0.5?topic=pmi-data-organization

 
Changes proposed by ITCAM documentation:
- Availability Manager (appears to be z/OS) only      
- alarmManagerModule:1,2,3,4,5,6                                    ->  All high
- connectionPoolModule:1,2,3,4,5,6,7,8,9,10,12,13,21,22             ->  5-7,9,10 high
- cacheModule:1,2,3,4,21,22,23,24,25,26,27,28,29,30,31,32,34,35,36  ->  All low
- DCSStats:1,2,3,6,7,8,9,10,11,12,14,16                             ->  3-12 high
- j2cModule:1,2,3,4,5,6,7,8,9,10,12,13,14,15                        ->  5-7,9,10 high
- schedulerModule,1,2,3,4,5,6,7,8,9,10,11                           ->  All high
- servletSessionsModule:1,2,3,4,6,7,8,9,10,11,12,13,14,15,17,18     ->  6,7 high ; 18 max
- threadPoolModule:1,2,3,4,5                                        -> 5 high
- transactionModule:1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19   ->  No high
- webAppModule:1,2,11,12,13,14                                      ->  No high
- webServicesModule:11,12,13,14,15,16,17,18,19,20"                  ->  No high
- Workload Management (appears to be z/OS) only                     
- wsgwModule:1,2,3,4                                                ->  No high  # WebServices Gateway
- All 'SIB Service' (StatGroup.SIBService..?)                       > cannot be set by this procedure use IBM Console

More about the ITCAM recommandation can be found in the attached Excel document.

You may modify the procedure to set the PMI as appropriate for you (just modify the APMLSIT array with your setttings). By default following is set:
```
APMILIST = [ \
             "connectionPoolModule:1,2,3,4,5,6,7,8,9,10,12,13,21,22", \
             "j2cModule:1,2,3,4,5,6,7,8,9,10,12,13,14,15", \
             "servletSessionsModule:1,2,3,4,6,7,8,9,10,11,12,13,14,15,17", \
             "threadPoolModule:1,2,3,4,5", \
             "webAppModule:1,2,11,12,13,14", \
             "webServicesModule:11,12,13,14,15,17,18", \
             "wsgwModule:1,2,3,4" \
           ]
```           

2 Usage
=======

Execution:

    ./wsadmin.sh -lang jython -f modStatSet.py {custom, basic, help}

  
  custom  = statistkitSet will be modfied to 'custom'. The pmi counter will be set as defined in this jython script (see MAIN section for more details
  
  basic   = tatistkitSet will be modfied to 'basic'
  
  help    = Script usage information


