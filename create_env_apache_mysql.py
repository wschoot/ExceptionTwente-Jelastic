#!/usr/bin/python
import random, string, requests, json, sys, ConfigParser

config = ConfigParser.RawConfigParser()
config.read('jelastic.ini')

jelastic_url = 'https://app.groundctrl.nl/1.0/'
login_uri    = 'users/authentication/rest/signin'
login_url    = jelastic_url + login_uri
appid        = '1dd8d191d38fff45e62564fcf67fdcd6'
user         = config.get('auth', 'username')
password     = config.get('auth', 'password')

data = {
    'appid':    appid,
    'login':    user,
    'password': password}

r              = requests.get(login_url, params=data)
session        = json.loads(r.text)[u'session']

create_env_url = 'environment/environment/rest/createenvironment'
shortdomain    = 'exceptiontwente-' + ''.join(random.choice(string.ascii_lowercase) for x in range(6))

nodes = [{
    'nodeType':          'apache2',
    'extip':             False,
    'count':             2,
    'fixedCloudlets':    2,
    'flexibleCloudlets': 8},
{
    'nodeType':          'mysql5',
    'extip':             False,
    'count':             1,
    'fixedCloudlets':    2,
    'flexibleCloudlets': 8}
]

env = {
    'shortdomain': shortdomain,
    'ishaenabled': False,
    'engine':      'php5.6'}

params = {
    'appid':     appid,
    'session':   session,
    'actionkey': 'createenv',
    'env':       json.dumps(env),
    'nodes':     json.dumps(nodes)}


print requests.get(jelastic_url + create_env_url, params=params).text

requests.get(
    jelastic_url + 'users/authentication/rest/signout',
    params={ 'appid': appid, 'session':  session})
