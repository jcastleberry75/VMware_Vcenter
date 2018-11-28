import logging
import threading
import time
from time import sleep
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from http.client import HTTPConnection
start = time.time()

try: 
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection

FORMAT = '%(asctime)-15s [%(levelname)s] (%(threadName)-10s)  %(message)s'
logging.basicConfig(filename='program.log',level=logging.DEBUG, format=FORMAT)
global session
session = requests.Session()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

master_vcenters = ('vcenter1', 'vcenter2', 'vcenter3', 'vcenter4')


def cookie_handler():
    vcenters_to_poll = ['vcenter1', 'vcenter2', 'vcenter3', 'vcenter4']


    def cookie_thief():
        poplist = vcenters_to_poll
        if poplist == []:
            pass
        else:
            x = poplist.pop()
            session_re_url = ('https://' + x +
                            '/rest/com/vmware/cis/session')
            username = 'CHANGEME'
            password = 'CHANGEME'
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            cookie_req = session.post(session_re_url,
                                        auth=HTTPBasicAuth(username,
                                                            password),
                                        verify=False, stream=True)
            cookie = (cookie_req.json())

    threads = []
    for i in range(4):
        t = threading.Thread(target=cookie_thief)
        threads.append(t)
        t.start()
        t.join()
cookie_handler()


sleep(2)

def get_clusters():
    vcenters_to_poll = ['vcenter1', 'vcenter2', 'vcenter3', 'vcenter4' ]
    def cluster_scraper():
        poplist = vcenters_to_poll
        if poplist == []:
            pass
        else:
            x = poplist.pop()
            session_re_url = ('https://' + x +
                            '/rest/vcenter/cluster')
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            cluster_req = session.get(session_re_url,verify=False,)
            cluster_data = cluster_req.json()
            print()
            print(cluster_data)
    threads = []
    for i in range(4):
        t = threading.Thread(target=cluster_scraper)
        threads.append(t)
        t.start()



def get_hosts():
    vcenters_to_poll = ['vcenter1', 'vcenter2', 'vcenter3', 'vcenter4' ]


    def host_scraper():
        poplist = vcenters_to_poll
        if poplist == []:
            pass
        else:
            x = poplist.pop()
            session_re_url = ('https://' + x +
                            '/rest/vcenter/host')
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            host_req = session.get(session_re_url,verify=False,)
            host_data = host_req.json()
            print()
            print(host_data)
    threads = []
    for i in range(4):
        t = threading.Thread(target=host_scraper)
        threads.append(t)
        t.start()


def get_folders():
    vcenters_to_poll = ['vcenter1', 'vcenter2', 'vcenter3', 'vcenter4' ]

    def folder_scraper():
        poplist = vcenters_to_poll
        if poplist == []:
            pass
        else:
            x = poplist.pop()
            session_re_url = ('https://' + x +
                            '/rest/vcenter/host')
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            folder_req = session.get(session_re_url,verify=False,)
            folder_data = folder_req.json()
            print()
            print(folder_data)
    threads = []
    for i in range(4):
        t = threading.Thread(target=folder_scraper)
        threads.append(t)
        t.start()



def do_it():
    get_clusters()
    get_folders()
    get_hosts()

do_it()

end = time.time()
print('Entire job took:', end - start)
