import sys
import os
import time
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def request_info():
    ip = input('IP :')
    print('Quel Systel ? (1 = Systel SysBOX ou 2 = Systel Tempo100-IP ?)')
    systel = input('Systel :')
    nbrloop = input('Nombre de boucle :')
    nbrloop = int(nbrloop)
    return (ip, systel, nbrloop)

def systel_raspi(ip, nbrloop):
    for i in range(nbrloop):
        url = 'http://' + ip + ':8000/api/testPOCSAG'
        payload = {'id': 0}
        response = requests.put(url, json=payload)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            print('Test réussi')
        else:
            print('Test échoué')
            sys.exit(1)
        time.sleep(27)

def main():
    ip, systel, nbrloop = request_info()
    print('IP :', ip)
    print('Systel :', systel)
    if systel == '1':
        systel_raspi(ip, nbrloop)
if __name__ == '__main__':
    main()