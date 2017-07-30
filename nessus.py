#!/usr/bin/env python
import requests, json, sys, os, getpass, time
import nessrest

url = 'https://vm.totvscloud.net:8834'
#url = 'https://10.172.72.31:8834'
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


#### logout ###
def logout():
        connect('DELETE', '/session')


print("Login...")
username = 'admin'  #raw_input('Enter Nessus Username: ')
password = 'VulnerabilityManagement'	 #getpass.getpass(
token = login(username, password)
rep_list = list_scan()
print_scans(rep_list)
print("List of reports...")

print("Exporting reports...")

logout()

raw_input('Logout... press [Enter] to exit')
