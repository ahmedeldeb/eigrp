import csv
from jinja2 import Template
from netmiko import ConnectHandler

def network (l):
   interface_configs = ""
   source_file = "interface.csv"
   interface_template_file = "router-interface-template.j2"
   with open(interface_template_file) as f:
      interface_template = Template(f.read())
   with open(source_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
         if l in row.values():
            interface_config = interface_template.render(
               Interface=row[ "interface" ],
               Ipaddress=row[ "ip" ],
               subnetmask=row[ "submask" ],
            )
            interface_configs += interface_config
   with open("%s interface_configs.txt" % l.rstrip(), "w") as f:
      f.write(interface_configs)
   return  interface_configs


def EIGRP (l):
   interface_configs = ""
   source_file = "EIGRP.csv"
   interface_template_file = "eigrp.j2"
   with open(interface_template_file) as f:
      interface_template = Template(f.read())
   with open(source_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
         if l in row.values():
            interface_config = interface_template.render(
               network=row[ "network" ],
               widemask=row[ "widemask" ],
            )
            interface_configs += interface_config
   with open("%s interface_configs.txt" % l.rstrip(), "a") as f:
      f.write(interface_configs)
   return  interface_configs


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    output=''
    b=['192.168.100.55',
       '192.168.100.56',
       '192.168.100.57',
       '192.168.100.58',
       '192.168.100.59']
    for a in b:
        cisco = {
            'device_type': 'cisco_ios',
            'host': a,
            'username': 'admin',
            'password': 'cisco',
        }
        ch = ConnectHandler(**cisco)
        if ch:
            print('success' + a)
        s = ch.send_command("show running-config | include hostname ")
        s = s.split()
        s = s[ 1 ]
        m = [ network(s), EIGRP(s) ]
        for a in m:
            config_set = a.split("\n")
            output = ch.send_config_set(config_set)
            print(output)
        with open("%s eigrp_configs.txt"% s.rstrip(), "w") as f:
            f.write(output)






