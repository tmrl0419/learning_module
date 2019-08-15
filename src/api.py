import requests
import json
import datetime

url_base = "http://localhost/"

token = ""
server_uuid = []
server_names = []


def get_projectID():
    global token
    url = url_base + "identity/v3/auth/projects"
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    res = requests.get(url, headers=headers)
    body = res.json()
    projects = [ x['id'] for x in body['projects'] if not x['name'] == "invisible_to_admin"]
    return projects

# for ask what kinds of instances admin control on dashboard
def get_server_list():
    global server_uuid
    global server_names
    global token
    url = url_base + "compute/v2.1/servers"
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    res = requests.get(url, headers=headers)
    body = res.json()

    server_uuid = [ x['id'] for x in body['servers']]
    server_names = [ x['name'] for x in body['servers']]

    return body

def get_token(id,passwd):
    global token
    data = \
        {"auth":
            {
                "identity":
                    {"password":
                         {"user":
                              {"domain":
                                   {"name": "Default"},
                               "password": passwd,
                               "name": id
                               }
                          },
                     "methods": ["password"]
                     }
            }
        }

    # pixed header
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    # TODO get project id

    res = requests.post(url_base + 'identity/v3/auth/tokens', headers=headers, data=json.dumps(data), verify=True)
    token = res.headers['X-Subject-Token']
    projectID = get_projectID()[0]
    data['auth']['scope'] = {
        "project":
            {"id": projectID }
    }
    res = requests.post(url_base + 'identity/v3/auth/tokens', headers=headers, data=json.dumps(data), verify=True)
    token = res.headers['X-Subject-Token']
    return

def get_resource_list(instance_uuid):
    global token

    url = url_base + "metric/v1/resource/generic/%s"%(instance_uuid)
    headers = {'Content-Type': 'application/json, */*', 'X-Auth-Token':token}
    res = requests.get( url, headers = headers )
    #print(res)
    #print(res.json())
    body = res.json()
    return body

def get_mesuare_list(body):
    global token

    now = datetime.datetime.now()
    five_mins = datetime.timedelta(minutes=5)
    five_mins_ago = now - five_mins
    headers = {'Content-Type': 'application/json, */*', 'X-Auth-Token': token}
    PARAMS = {'start': None, 'granularity': None, 'resample': None, 'stop': None, 'aggregation': None, 'refresh': False}
    cpu = 'cpu_util'
    memory = 'memory.usage'
    disk = 'disk.usage'
    url = url_base + 'metric/v1/metric/%s/measures'%(body['metrics'][cpu])
    res = requests.get(url = url, headers = headers, params= PARAMS )
    print(str(res.json()[-1][2]) + " %")

    url = url_base + 'metric/v1/metric/%s/measures' % (body['metrics'][memory])
    res = requests.get(url=url, headers=headers, params=PARAMS)
    print(str(res.json()[-1][2]/(1024) )+ " GB")

    url = url_base + 'metric/v1/metric/%s/measures' % (body['metrics'][disk])
    res = requests.get(url=url, headers=headers, params=PARAMS)
    print(str(res.json()[-1][2]/(8*1024*1024*1024)) + " GB")
#'''openstack metric show'''

if __name__ == '__main__':
    get_token('demo','devstack')
    get_projectID()
    print(token)
    get_server_list()
