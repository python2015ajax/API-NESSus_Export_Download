
#### The merits communit  tenable (spkody) #####
### modified by T3sla####

#!/usr/bin/ python

import requests, json, sys, os, getpass, time
from unicodedata import normalize

#url = 'https://Externo:8834'
url = 'https://IP_Interno:8834'
verify = False
token = ''
username = '' 
password = ''

def build_url(resource):
        return '{0}{1}'.format(url, resource)

##  persistencia de erros ao se conectar ######

def connect(method, resource, data=None):
        headers = {'X-Cookie': 'token={0}'.format(token), 'content-type': 'application/json'}
        data = json.dumps(data)
        if method == 'POST':
                r = requests.post(build_url(resource), data=data, headers=headers, verify=verify)
        elif method == 'PUT':
                r = requests.put(build_url(resource), data=data, headers=headers, verify=verify)
        elif method == 'DELETE':
                r = requests.delete(build_url(resource), data=data, headers=headers, verify=verify)
                return
        else:
                r = requests.get(build_url(resource), params=data, headers=headers, verify=verify)

        if r.status_code != 200:
                e = r.json()
                print e['error']
                sys.exit()

        if 'download' in resource:
                return r.content
        else:
                return r.json() 




## login #############


def login(usr, pwd):
        login = {'username': usr, 'password': pwd}
        data = connect('POST', '/session', data=login)
        return data['token']

def list_scan():
        data = connect('GET', '/scans')
        return data

def print_scans(data):
        for folder in data['folders']:
                print("\33[31m\33[1m * {0} - ({1})".format(folder['name'], folder['id']))



def login(usr, pwd):
        login = {'username': usr, 'password': pwd}
        data = connect('POST', '/session', data=login)
        return data['token']


def logout():
        connect('DELETE', '/session')

def list_scan():
        data = connect('GET', '/scans')
        return data

def count_scan(scans, folder_id):
        count = 0
        for scan in scans:
                if scan['folder_id']==folder_id: count=count+1
        return count


def print_scans(data):
        for folder in data['folders']:
                print("\33[31m\33[1m * {0} - ({1})".format(folder['name'], count_scan(data['scans'], folder['id'])))

def export_status(scan_id, file_id):
        data=connect('GET', '/scans/{0}/export/{1}/status'.format(scan_id, file_id))
        return data['status'] == 'ready'

def get_folder_id(serch_folder_name, data):
        folder_id = 0;
        for folder in data['folders']:
                if folder['name']==serch_folder_name:
                        folder_id = folder['id']
                        break
        return folder_id

def export_folder(folder_name, data):
        if folder_name == 'All' or folder_name == 'all':
                for scan in data['scans']:
                        file_id = export(scan['id'])
                        download(scan['name'], scan['id'], file_id,os.path.join(os.getcwd(),folder_name))
        else:
                folder_id = get_folder_id(folder_name,data)
                if count_scan(data['scans'], folder_id)==0:
                        print "\33[32m Nao contem na pasta"
                        return
                if folder_id!=0:
                        for scan in data['scans']:
                                if scan['folder_id'] == folder_id:
                                        file_id = export(scan['id'])
                                        download(scan['name'], scan['id'], file_id, os.path.join(os.getcwd(),folder_name))
                else:
                        print "\33[32m No such folder..."
                        
                        
        
def export(scan_id):
        data = {'format': 'nessus'}
        data = connect('POST', '/scans/{0}/export'.format(scan_id), data=data)
        file_id = data['file']
        while export_status(scan_id, file_id) is False:
                time.sleep(3)
        return file_id
#### Problems whiles downloading file with "/" = "UTF-8" - insette "UTF_8_sig = result pass"

try:
 def download(report_name, scan_id, file_id, save_path):
        if not(os.path.exists(save_path)): os.mkdir(save_path)
        data = connect('GET', '/scans/{0}/export/{1}/download'.format(scan_id, file_id))
        file_name = 'nessus_{0}_{1}.nessus'.format(report_name.encode('utf-8'), file_id)

        print('\33[32m Salvando as pastas {0}'.format(file_name))
        with open(os.path.join(save_path,file_name), 'w') as f:
          f.write(data)
except Exception:
 def download(report_name, scan_id, file_id, save_path):
        if not(os.path.exists(save_path)): os.mkdir(save_path)
        data = connect('GET', '/scans/{0}/export/{1}/download'.format(scan_id, file_id))
        file_name = 'nessus_{0}_{1}.nessus'.format(report_name.encode('utf_8_sig'), file_id)

        print('\33[32m Salvando as pastas {0}'.format(file_name))
        with open(os.path.join(save_path,file_name), 'w') as f:
          f.write(data)
 time.sleep(2)

 pass

## input login and password ###


print("\33[32m Nessus...")
username =  'input = login' #Blocked = raw_input('Enter Nessus Username: ')
password =  'input = password ' #blocked = getpass.getpass()

token = login(username, password)
print("Scans...")
rep_list = list_scan()
print_scans(rep_list)

exp_folder_name = raw_input('\33[34m\33[1m * Digite o nome dos arquivos a serem exportado (Todos = all ): ')
export_folder(exp_folder_name, rep_list)



while True:
 print("Scans...")
 rep_list = list_scan()
 print_scans(rep_list)

 exp_folder_name = raw_input('\33[34m\33[1m *Digite o nome dos arquivos a serem exportado (Todos = all ): ')
 export_folder(exp_folder_name, rep_list)  
else:
 print 'Pasta Nao Localizada'
 sleep.time(2)
 logout()
 raw_input('Logout... press [Enter] to exit')
