- Install
```javascript
pip install kbmc
- Install```
```javascript
pip3 install kbmc
```

- Help
```javascript
Usage: kBmc <command> [OPTION] [<args>]
Version: 2.2
Inteligent BMC Tool

Supported <command>s are:
  is_up                              Is node UP?
  summary                            Show summary
  bootorder                          Set HDD boot mode
  is_admin_user                      Check current user is ADMINISTRATOR user
  lanmode                            Get current lanmode
  info                               Show info
  mac                                Get BMC Mac Address
  eth_mac                            Get Ethernet Mac Address
  reset                              Reset BMC
  power                              Send power signal
  vpower                             Send power signal and verify status
  redfish                            Redfish Command

[OPTION]
   -h, --help                        Help
   -i, --ip=BMC_IP                   BMC IP Address(required)
   -u, --user=BMC_USER               BMC User(default:ADMIN)
   -p, --passwd=BMC_PW               BMC Password(default:ADMIN)
   -t                                misc tool path(default:/home/kage/.local/lib/python3.6/site-packages/kmisc)
  -si                                SMC IPMITOOL file

 * bootorder                       Set HDD boot mode
       --pxe                         
       --ipxe                        
       --bios                        
       --hdd                         

 * power                           Send power signal
   -r, --reset                       Send reset signal
   -f, --off                         Send reset signal
   -o, --on                          Send on signal
   -s, --shutdown                    Send shutdown signal
   -c, --cycle                       Send cycle signal
  -vr, --vreset                      Send reset signal
  -vf, --voff                        Send off signal
  -vo, --von                         Send on signal
 -vfo, --voff_on                     Send off and on signal
  -vs, --vshutdown                   Send shutdown signal
  -vc, --vcycle                      Send cycle signal

 * redfish                         Redfish Command
  -rp, --rpower=PW                   Send power signal(on/off)
  -ri, --rinfo                       Get System Information
 -rrb, --reset_bmc                   Reset BMC
 -rni, --net_info                    Show Network Interface
```
