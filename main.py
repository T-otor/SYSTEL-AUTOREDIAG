import sys
import os
import time

# Add the path to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def request_info():
    #IP du Systel:
    ip = input('IP :')
    port = 8000
    #Quel Systel ? (1 ou 2)
    print ('Quel Systel ? (1 = Tempo100-IP ou 2 = Syste Raspi ?)')
    systel = input('Systel :')
    return ip, port, systel


if __name__ == '__main__':
    request_info()
    
