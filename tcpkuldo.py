import socket
import json
import time
import netifaces

bport = 6546
bss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
gwadd = netifaces.gateways()[2][0][0]
b = socket.inet_aton(gwadd)
badd = f'{b[0]}.{b[1]}.{b[2]}.255'
print('Broadcast address:' + badd)
#bss.bind(('0.0.0.0', bport))
tmp = 0;

while True:
    tmp += 1
    sorok = ['elso', f'masodik {tmp}', 'harmadik']
    txt = json.dumps(sorok)
    bss.sendto(txt.encode(), (badd, bport))
    time.sleep(0.1)
    
