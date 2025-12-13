from ast import Import
import sys
from easy_utils_dev.debugger import DEBUGGER
import requests , json , subprocess
from requests.auth import HTTPBasicAuth as BAuth    
from .utils import get_free_space, pingAddress , fixTupleForSql , start_thread , mkdirs  , getTimestamp
from time import sleep
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from threading import Thread
from easy_utils_dev.Events import EventEmitter
from .EasySsh import CREATESSH
import xmltodict
from .FastQueue import FastQueue
import tempfile , os 
from kafka import KafkaConsumer
from easy_utils_dev.utils import kill_thread
import atexit
try :
    from snakebite.client import Client as HdfsClient
    SNAKEBITEIMPORTED = True
except Exception as e:
    print(f'Warning: snakebite is not installed. PM Hadoop client will not be available. {e}')
    HdfsClient = None
    SNAKEBITEIMPORTED = False
    
from datetime import datetime


class KafkaConfig :
    def __init__(self , subscriptionId = None , response = None , topicId = None ) :
        self.subscriptionId = subscriptionId 
        self.response = response
        self.topicId= topicId
        self.kafka_address = None
        self.kafka_port = None ,
        self.refresh_inprogress = False
        self.nsp_key = None
        self.nsp_cert = None
        self.ca_cert = None
        self.kafka_api_port =8443
        self.kafka_refresh_period = 1500
        self.kafka_nsp_os_name = None
        self.kafka_subscription_deleted = False 
        self.base_url = None
        self.kafka_thread=None
        self.enable_auto_refresh = False


class WSNOCLIB : 
    def __init__( 
        self, 
        ip , 
        username , 
        password ,
        debug_level='info', 
        debug_name='wsnoclib' ,
        debug_homepath=os.getcwd(),
        request_max_count=30,
        tmp_dir = tempfile.gettempdir() ,
        kafka = KafkaConfig(),
        register_atexit=True,
        trust_env=True
    ): 
        self.logger = DEBUGGER(f'{debug_name}-{ip}',level=debug_level,homePath=debug_homepath)
        self.disabledWarnings = self.disableUrlWarnings()
        self.event = EventEmitter(id=ip)
        self.address = ip
        self.username = username
        self.password = password
        self.trust_env = trust_env
        self.external_nsp = False
        self.api_count = 0
        self.api_count_limit = 999999999999
        self.temp_dir = os.path.join(tmp_dir , 'wsnoclib' )
        self.baseUrl = self.createBaseUrl()
        self.numberOfRequests=0
        self.request_max_count = request_max_count
        self.onGoingRequests=0
        self.fastQueue = FastQueue(request_max_count)
        self.queue = []
        self.token = {}
        self.tokenRefreshPeriod = None
        self.final_results = []
        self.killed=False
        self.nes=[]
        self.loggedOut = False
        self.alarms_store=[]
        self.refresh_inprogress = False
        self.kafka = kafka
        self.refresh_thread = None
        self.token_refresh_count = 0
        self.session = WSNOCSession(self)
        self.max_concurrent_requests = 40
        self.current_requests = 0
        self.connected = False
        self.pm_hadoop = PmHadoopClient(self)
        self.verify_connection_by_ping = True
        if register_atexit :
            atexit.register(self.goodbye)

    def getLogger(self) : 
        return self.logger

    def supress_logs(self) :
        self.logger.disable_print()
    
    def change_token_refresh_period(self , period=2700) :
        '''
        period is in seconds.
        '''
        self.tokenRefreshPeriod = int(period)

    def createBaseUrl(self) :
        self.baseUrl = f'https://{self.address}'
        return self.baseUrl

    def change_debug_level(self , level) :
        self.logger.warning("This function -change_debug_level- is deprecated and will be removed. please use set_debug_level instead")
        if not level in ['info' , 'error' , 'debug' , 'warn'] :
            raise Exception(f"Not valid debugging level: {level}. Levels {['info' , 'error' , 'debug' , 'warn']}")
        self.logger.set_level(level)
    
    def set_debug_level(self , level) :
        if not level in ['info' , 'error' , 'debug' , 'warn'] :
            raise Exception(f"Not valid debugging level: {level}. Levels {['info' , 'error' , 'debug' , 'warn']}")
        self.logger.set_level(level)

    def disableUrlWarnings(self) :
        disable_warnings(InsecureRequestWarning)
        return True

    def getSession(self) :
        return self.session

    def connect(self,auto_refresh_token=True) -> dict :
        self.auto_refresh_token = auto_refresh_token 
        #refresh the session
        self.logger.debug(f"loggedOut flag is {self.loggedOut}")
        if self.loggedOut :
            return
        if self.verify_connection_by_ping :
            if not pingAddress(self.address)  :
                raise Exception(f'Address {self.address} is not pingable.')
        # self.logger.info(f'Connecting to {self.address} using username: {self.username}')
        self.logger.debug(f'Connecting to {self.address} using username: {self.username}')
        URL = f"https://{self.address}/rest-gateway/rest/api/v1/auth/token"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "grant_type": "client_credentials"
        }
        r = self.session.post(url = URL , headers=headers , auth=BAuth(self.username, self.password), json=data , retries=5)
        if not r.ok :
            self.logger.debug(f'fail message {r.text}')
            raise Exception(f'Failed to authenticate WSNOC. Return status code : {r.status_code}')
        self.access_token = r.json()["access_token"]
        self.refresh_token = r.json()["refresh_token"]
        if not self.tokenRefreshPeriod :
            self.tokenRefreshPeriod = int(r.json()["expires_in"]) - 100
        self.bearer_token = f'Bearer {self.access_token}'
        self.token = r.json()
        self.token.update({'bearer_token' :  self.bearer_token })
        if auto_refresh_token :
            self.autoRefreshThread = self.refresh_thread = start_thread(target=self.runAutoRefreshThread)
        self.logger.debug(f'token => {r.text}')
        self.connected = True
        return self.token


    def getLatestToken(self) :
        return self.token


    def logout(self,logout=True) :
        self.logger.info(f"Logging out from {self.address} ...")
        body = f"token={self.access_token}&token_type_hint=token"
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        URL = f"https://{self.address}/rest-gateway/rest/api/v1/auth/revocation"
        r = self.session.post(
            url = URL ,
            auth=BAuth(self.username, self.password),
            data=body,
            headers=header
        )
        try :
            kill_thread(self.refresh_thread)
        except :
            pass
        try :
            kill_thread(self.kafka.kafka_thread)
        except :
            pass
        if logout :
            self.loggedOut = True
        try :
            r.close()
        except :
            pass
        self.connected = False
        return True

    def goodbye(self):
        try :
            self.logout(True)
        except :
            pass

    def runAutoRefreshThread(self) : 
        self.logger.info(f'Waiting for auto refresh in {self.tokenRefreshPeriod}sec...')
        sleep(self.tokenRefreshPeriod)
        self.logger.info(f"Waiting period completed. Starting Revoking/Login process ...")
        self.refresh_inprogress = True
        self.renew_by_refresh_token()
        self.refresh_inprogress = False
        self.kafka.refresh_inprogress = True
        if self.kafka.enable_auto_refresh :
            self.renewSubscription()
        self.kafka.refresh_inprogress = False
        self.token_refresh_count += 1
        self.runAutoRefreshThread()

    def kafka_connect( self , 
            user , 
            password, 
            auto_refresh=True ,
            severities=[], 
            nodeNames=[] , 
            nodeIps=[] , 
            affectedObjects=[] , 
            alarms=[] , 
            kafka_api_port=8443, 
            ssh_port=22 , 
            custom_filter_expression=None ,
            external_nsp=False,
            nsp_address=None ,
            new_release=False,
        ) -> KafkaConfig : 
        '''
        @ parameters :
        @user: [SSH USER] must be the username of kafka host machine\n
        @password: [SSH PASSWORD] must be the password of kafka host machine\n
        @kafka_api_port : is the port for creating/renewing subscription. It the API port not the listening port. default is 8443.\n
        @possible serverities ['major','minor', 'critical' , 'warning' , 'cleared' , 'indeterminate']\n
        @possible affectedObjects ["TRAIL","ASONTRAIL","service.Service","PHYSICALCONNECTION","NetworkElement"]\n
        @custom_filter_expression example : AND neName in (nes) OR possibleCause = 'card-missing'\n
        {
            "alarms": [akjsd,asdmkasdm,asdjiasdi],  
            "severities": [],
            "affectedObjectTypes": [],
        }
        '''
        self.kafka.kafka_api_port = kafka_api_port
        self.external_nsp = external_nsp
        self.logger.debug(f"Extranal NSP: {self.external_nsp}")
        self.logger.debug(f"severities: {severities}")
        self.logger.debug(f"nodeNames: {nodeNames}")
        self.logger.debug(f"nodeIps: {nodeIps}")
        self.logger.debug(f"affectedObjects: {affectedObjects}")
        self.logger.debug(f"alarms: {alarms}")
        self.logger.debug(f"kafka_api_port: {kafka_api_port}")
        self.logger.debug(f"ssh_port: {ssh_port}")
        self.logger.debug(f"custom_filter_expression: {custom_filter_expression}")
        self.logger.debug(f"nsp_address: {nsp_address}")
        self.logger.debug(f"NewRelease: {new_release}")
        self.kafka.kafka_subscription_deleted= False
        if not self.external_nsp : 
            if new_release :
                self.kafka.kafka_nsp_os_name = 'nspos-kafka'
            else :
                self.kafka.kafka_nsp_os_name = 'nspos'
            self.kafka.kafka_port = 9193
            self.kafka.kafka_address = self.address
        else :
            self.kafka.kafka_address = nsp_address
            self.kafka.kafka_port = 9192
            self.kafka.kafka_nsp_os_name = 'nspos-tomcat'
        if self.loggedOut or self.killed:
            self.logger.error(f"WSNOC API Authentication process loggedout or killed. exit")
            raise Exception('WSNOC API Authentication process loggedout or killed. exit')
        self.ssh = CREATESSH(
            address=self.kafka.kafka_address,
            user=user,
            password=password,
            sshPort=ssh_port
        )
        self.sshclient = self.ssh.init_shell()
        self.channel = self.ssh.init_ch()
        sftp = self.ssh.init_sftp()
        mkdirs(self.temp_dir)
        self.nsp_key = f'{self.temp_dir}/nsp.key'
        self.nsp_cert = f'{self.temp_dir}/nsp.pem'
        if not self.external_nsp :
            ####################
            ####################
            #
            #   IN CASE OF INTERNAL NSP
            #   
            ####################
            ####################
            checkContainer = self.ssh.ssh_execute(f"docker ps | grep -i 'nspos-kafka' | wc -l")
            if checkContainer != '0' :
                self.kafka.kafka_nsp_os_name = 'nspos-kafka'
            self.kafka.kafka_port = None
            self.logger.debug(f"Working on internal NSP to copy the files ...")
            self.ssh.ssh_execute(f"docker cp {self.kafka.kafka_nsp_os_name}:/opt/nsp/os/ssl/certs/nsp/nsp.pem /tmp/nsp.pem")
            self.ssh.ssh_execute(f"docker cp {self.kafka.kafka_nsp_os_name}:/opt/nsp/os/ssl/nsp.key /tmp/nsp.key")
            sftp.get('/tmp/nsp.pem' , f'{self.temp_dir}/nsp.pem')
            sftp.get('/tmp/nsp.key' , f'{self.temp_dir}/nsp.key')
            self.kafka.ca_cert = f'{self.temp_dir}/nsp.pem'
            self.kafka.base_url = f'https://{self.address}'
        else :
            ####################
            ####################
            #
            #   IN CASE OF EXTERNAL NSP
            #   
            ####################
            ####################
            self.logger.debug(f"Working on external NSP to copy the files ...")
            CertLoc = f"""find /var/lib/kubelet/pods/ -type d -path "*/volumes/kubernetes.io~empty-dir/shared-tls-volume" | head -n1"""
            CertLoc = self.ssh.ssh_execute(CertLoc).replace('\n','')
            self.logger.debug(f"CertLoc Host: {CertLoc}")
            self.kafka.base_url = f'https://{nsp_address}'
            self.kafka.kafka_port = None
            if len(CertLoc) > 15 :
                self.logger.debug(f"Copying cert files from nsp host machine ....")
                copies = [
                    (f"{CertLoc}/ca_cert.pem" , f'{self.temp_dir}/cert.pem'),
                    (f"{CertLoc}/nsp.key" , f'{self.temp_dir}/nsp.key'),
                    (f"{CertLoc}/certs/nsp/nsp.pem" , f'{self.temp_dir}/nsp.pem'),
                ]
                for f in copies :
                    self.logger.debug(f"Copying {f[0]} to {f[1]}")
                    sftp.get( f[0] , f[1])
                self.kafka.ca_cert = f'{self.temp_dir}/cert.pem'
            else :
                self.logger.error(f'invalid shared volume location: {CertLoc}')
                raise Exception(f'invalid shared volume location')
        if sftp :
            sftp.close()
        if len(severities) == 0 :
            severities = ['major','minor', 'critical' , 'warning' , 'cleared' , 'indeterminate']
        filter = f"severity in {fixTupleForSql(severities)}"
        self.logger.debug(f'severity filter is  "{filter}"')
        if len(alarms) > 0 :
            filter += f" AND ( alarmName in {fixTupleForSql(alarms)} )"
            self.logger.debug(f'filter updated with "{filter}"')
        if len(nodeNames) > 0 :
            neArray = self.get_nes()
            for ne in neArray :
                if ne['tid'] in nodeNames :
                    nodeIps.append(ne['ipAddress'])
        if len(nodeIps) > 0 :
            filter += f" AND neId in {fixTupleForSql(nodeIps)}"
            self.logger.debug(f'nodeIpFilter : filter updated with "{filter}"')
        if len(affectedObjects) > 0 :
            filter += f" AND affectedObjectTypes in {fixTupleForSql(affectedObjects)}" 
            self.logger.debug(f'affectedObjectType Filter : filter updated with "{filter}"')
        if custom_filter_expression :
            filter += f" {custom_filter_expression}"
        kafkaForm = {
                "categories": [
                    {
                    "name": "NSP-FAULT",
                    "propertyFilter": filter
                    }
                ]
        }
        self.logger.debug(f"Kafka Filter Form : {kafkaForm}")
        if self.kafka.kafka_port is not None :
            URL = f"{self.kafka.base_url}:{self.kafka.kafka_port}/nbi-notification/api/v1/notifications/subscriptions"
        else :
            URL = f"{self.kafka.base_url}/nbi-notification/api/v1/notifications/subscriptions"
        response = self.session.post(URL , json=kafkaForm , retries=3)
        if response.ok :
            response = response.json()
            self.kafka.subscriptionId = response['response']['data']['subscriptionId']
            self.kafka.response = response
            self.kafka.topicId = response['response']['data']['topicId']
            if auto_refresh :
                self.kafka.enable_auto_refresh = True
            self.killed=False
        else :
            self.logger.error(f"Failed to create kafka subscription.")
            self.logger.debug(f"response: {response.text}")
            raise Exception(f"Failed to create kafka subscription.")
        return self.kafka

    def change_kafka_refresh_period(self , period : int =3000) :
        self.logger.warning('Deprecated, Kafka refresh period is now managed by WSNOC API SLEEP PERIOD. Nothing is applied from this function.')

    def renewSubscription(self) :
        self.logger.info('Renewing subscription ...')
        if self.kafka.kafka_port is not None :
            URL = f"{self.kafka.base_url}:{self.kafka.kafka_port}/nbi-notification/api/v1/notifications/subscriptions/{self.kafka.subscriptionId}/renewals"
        else :
            URL = f"{self.kafka.base_url}/nbi-notification/api/v1/notifications/subscriptions/{self.kafka.subscriptionId}/renewals"
        response = self.session.post(URL , retries=3)
        if not response.ok :
            self.logger.error(f'failed to renew subscription. {response.text}')


    def kafka_listen(self) : 
        def hold_if_kafka_refresh_inprogress() :
            while self.kafka.refresh_inprogress :
                sleep(.1)
        self.logger.info('Listening to Kafka Notifications ...')
        if not self.kafka.topicId :
            self.logger.error(f'kafka is not established. exit.')
            return False
        self.logger.debug(f'kafka_address : {self.kafka.kafka_address}')
        self.logger.debug(f'kafka_port : {self.kafka.kafka_port}')
        self.logger.debug(f'ca_cert : {self.kafka.ca_cert}')
        self.logger.debug(f'nsp_cert : {self.nsp_cert}')
        self.logger.debug(f'nsp_key : {self.nsp_key}')
        kafka_consumer = KafkaConsumer(
            self.kafka.topicId,
            bootstrap_servers=f"{self.kafka.kafka_address}:9193",
            security_protocol="SSL",
            ssl_cafile=self.kafka.ca_cert,
            ssl_certfile=self.nsp_cert,
            ssl_keyfile=self.nsp_key,
            enable_auto_commit=True,
            auto_offset_reset='latest',
            key_deserializer=lambda m: m.decode('utf-8') if m else None,
            value_deserializer=lambda m: json.loads(
            m.decode('utf-8')) if m else None
        )
        try:
            while True:
                hold_if_kafka_refresh_inprogress()
                if self.kafka.kafka_subscription_deleted :
                    self.logger.info(f"Kafka subscription is deleted. exit.")
                    break
                self.logger.debug(f"Polling kafka ...")
                for message in kafka_consumer.poll(timeout_ms=1000).values():
                    self.logger.debug(f"kafka message: {message}")
                    for record in message:
                        if 'eventTime' in str(record) :
                            self.logger.debug(
                                f"Message received, message value is {record.value}")
                            yield record.value
        except KeyboardInterrupt:
            self.logger.info("Script stopped by user")
        except Exception as e:
            self.logger.error(f"Unforeseen error {e} happened")


    def get(self, url , headers={} , port=8443 , return_json=True ) :
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{self.baseUrl}{url}"
        else :
            url = f"{self.baseUrl}:{port}{url}"
        self.logger.info(f'request [GET] : {url}')
        headers={ 'Authorization' : self.bearer_token }
        r = requests.get(url , headers=headers , verify=False )
        self.logger.info(f'request [GET] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [GET]: {url} status code: [{r.status_code}]')
        if return_json :
            return r.json()
        return r

    def post(self, url , port=8443 , body={} , headers={} , return_json=False , contentType=f'application/json' , baseUrl=None ) :
        self.logger.debug(f"URL: {url} , baseUrl: {baseUrl} , port: {port} , body: {body} , headers: {headers} , return_json: {return_json} , contentType: {contentType}")
        if not baseUrl :
            baseUrl = self.baseUrl
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{baseUrl}{url}"
        else :
            url = f"{baseUrl}:{port}{url}"
        self.logger.info(f'request [POST] : {url}')
        _headers={ 
            'Authorization' : self.bearer_token 
        }
        if body : 
            _headers['Content-Type'] = contentType
        headers.update(_headers)
        r = requests.post( url , headers=headers , data=body , verify=False )
        self.logger.info(f'request [POST] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [POST]: {url} status code: [{r.status_code}]')
            return False
        try :
            if 'sign in' in r.text.lower() :
                raise Exception("WSNOC Authentication Failed")
        except :
            pass
        if return_json :
            return r.json()
        return r
    
    def update(self, url , port=8443 , body={} , headers={} , return_json=False , contentType=f'application/json' ) :
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{self.baseUrl}{url}"
        else :
            url = f"{self.baseUrl}:{port}{url}"
        self.logger.info(f'request [UPDATE] : {url}')
        _headers={ 
            'Authorization' : self.bearer_token 
            }
        if body : 
            _headers['Content-Type'] = contentType
        headers.update(_headers)
        r = requests.update( url , headers=headers , data=body , verify=False )
        self.logger.info(f'request [UPDATE] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [UPDATE]: {url} status code: [{r.status_code}]')
            return False
        if return_json :
            return r.json()
        return r
    

    def delete(self, url , port=8443 , body={} , headers={} , return_json=False ) :
        if not str(url).startswith('/') :
            url = f"/{url}"
        if port is None :
            url = f"{self.baseUrl}{url}"
        else :
            url = f"{self.baseUrl}:{port}{url}"
        self.logger.info(f'request [DELETE] : {url}')
        _headers={ 
            'Authorization' : self.bearer_token 
            }
        if body : 
            _headers['Content-Type'] = 'application/json'
        headers.update(_headers)
        r = requests.delete( url , headers=headers , data=body , verify=False )
        self.logger.info(f'request [DELETE] : {url} [{r.status_code}]')
        self.logger.debug(f'response {url} : {r.text}')
        if r.status_code not in [200,201,206]:
            self.logger.error(f'request [DELETE]: {url} status code: [{r.status_code}]')
            return False
        if return_json :
            return r.json()
        return r

    def renew_by_refresh_token(self) :
        URL = f"https://{self.address}/rest-gateway/rest/api/v1/auth/token"
        headers = {
             "Content-Type": "application/json"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": f"{self.refresh_token}"
            
        }
        r = self.session.post(URL , headers=headers , json=data , auth=BAuth(self.username, self.password) , skip_hold_for_token_refresh=True)
        if r.ok :
            if not self.tokenRefreshPeriod :
                self.tokenRefreshPeriod = int(r.json()["expires_in"]) - 100
            self.access_token = r.json()["access_token"]
            self.refresh_token = r.json()["refresh_token"]
            self.bearer_token = f'Bearer {self.access_token}'
            self.token = r.json()
            self.token.update({'bearer_token' :  self.bearer_token })
        self.connected = True
        return r

    def session_info(self) :
        self.logger.debug('Getting Version ...')
        response = self.get( url='/oms1350/data/common/sessionInfo')
        return response

    def get_nodes(self) :
        self.logger.debug(f"Requesting Nodes ..")
        response = self.get( url="/oms1350/data/npr/nodes" )
        return response

    def get_nes(self) :
        self.logger.debug(f"Requesting Network Elements ..")
        response = self.get( url="/oms1350/data/npr/nes")
        return response

    def get_version(self) :
        self.logger.debug(f"Getting Version ...")
        response = self.get('/oms1350/data/otn/system/getVersion')
        return response

    def fullSync(self , nodeId, nodeName ) :
        self.logger.debug(f'Trigger Full Sync for node %s' % nodeId)
        url = f'/oms1350/data/npr/nodes/{nodeId}'
        headers={"Content-Type" : "application/json" , "Accept" : "application/json" }
        body= json.dumps({"Tag":"F_POP_neFullSyncro","userLabel": nodeName })
        response=self.post( url=url , body=body , headers=headers ,return_json=False )
        return response.json()

    def getUserRecords(self) :
        self.logger.debug("Trigger GET request for user records ...")
        url = f'/oms1350/data/npr/AdminCommandLogs'
        headers={"Content-Type" : "application/json" , "Accept" : "application/json" }
        response=self.get( url=url , headers=headers ,return_json=False )
        if response :
            return response.json()

    def cliCutThough(self , neName , command) : 
        if len(self.nes) == 0:
            self.nes = self.get_nes()
        emlDomId=None
        emlNeId=None
        for elem in self.nes :
            if elem['guiLabel'] == neName :
                emlDomId= elem['emlDomId']
                emlNeId= elem['emlNeId']
        if not emlDomId or not emlNeId :
            self.logger.error(f'Error: Cannot find network element {neName}')
            return False
        URL = f'/oms1350/eqm/cliRequest/processCLIRequest/{emlDomId}/{emlNeId}'
        payload = f"<CLIRequestCommand><neName>{neName}</neName><ncName>{emlDomId}_SNA</ncName><cliCommandText>{command}</cliCommandText></CLIRequestCommand>"
        response = self.post(URL ,body=payload ,contentType='application/xml')
        if response.status_code in [200,201] :
            parsed_xml = xmltodict.parse(response.text)
            return parsed_xml

    def getBackupJobs(self) :
        URL = '/oms1350/data/plat/jobs'
        return self.get(URL)
    
    def getAllConnections(self) :
        '''
        get trails and services in one array.
        '''
        URL = '/oms1350/data/otn/connections/trails'
        trails = self.get(URL).get('items' , [])
        URL = '/oms1350/data/otn/connections/paths'
        paths = self.get(URL).get('items' , [])
        return trails + paths
    
    def getSystemLicense(self) :
        self.logger.info(f'get license ...')
        return self.get('/systemmonitor/sysadmin/stats/licenseinfo/v2')

    def getUnscheduledNetworkElementsBackup(self) :
        URL = "/oms1350/data/swim/NeScheduledBckpData"
        return self.get(URL).get('items' , [])
    
    def getAlarms(self) :
        URL= "/FaultManagement/rest/api/v2/alarms/details"
        return self.get(URL,port=8544)
    
    def getSessionInfo(self) :
        URL = "/oms1350/data/common/sessionInfo"
        return self.get(URL)


class WSNOCSession(requests.Session):
    from easy_utils_dev.wsnoclib import WSNOCLIB
    def __init__(self, wsnoc : WSNOCLIB):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})  # base defaults
        self._wsnoc = wsnoc
        self.verify = False
        self.retries = 0
        if not wsnoc.trust_env :
            os.environ['https_proxy'] = ""
            os.environ['http_proxy'] = ""
        self.debug_this_request = False
        self.skip_hold_for_token_refresh = False
        
    def rebuild_auth(self, prepared_request, response):
        return

    def _refactor_url(self , url) :
        if str(url).startswith('/') :
            url = f"{self._wsnoc.baseUrl}/{url}"
        return url

    def hold_for_token_refresh(self, url=None) :
        while self._wsnoc.refresh_inprogress :
            self._wsnoc.logger.info(f'Waiting for token refresh. {url if url else "No URL"}')
            sleep(.5)

    def hold_for_max_concurrent_requests(self, url=None) :
        while self._wsnoc.current_requests >= self._wsnoc.max_concurrent_requests :
            self._wsnoc.logger.info(f'Max concurrent requests reached. Waiting for a request to complete. {url if url else "No URL"}')
            self._wsnoc.logger.debug(f'Max concurrent requests reached. Waiting for a request to complete. {url if url else "No URL"} [current_requests={self._wsnoc.current_requests}] [max_concurrent_requests={self._wsnoc.max_concurrent_requests}]')
            sleep(1)

    def request(self, method, url , retries=0 , skip_hold_for_token_refresh=False , debug_this_request=False , **kwargs):
        url = self._refactor_url(url)
        self._wsnoc.logger.debug(f'[{method}] : {url}')
        if not skip_hold_for_token_refresh :
            self.hold_for_token_refresh(url)
        self.hold_for_max_concurrent_requests(url)
        self._wsnoc.api_count += 1
        token = self._wsnoc.getLatestToken().get('bearer_token')
        request_headers = kwargs.get('headers' , {})
        if token :
            if not request_headers.get('Authorization') :
                request_headers['Authorization'] = token
        kwargs['headers'] = request_headers
        start_ts = getTimestamp()
        self._wsnoc.current_requests += 1
        request = super().request(method, url, **kwargs  )
        if debug_this_request :
            self._wsnoc.logger.info(f'''
                [DEBUG] [{method}] : {url}
                [DEBUG] Headers: {request_headers}
                [DEBUG] Body: {kwargs.get('data' , {})}
                [DEBUG] Response: {request.text}
                [DEBUG] OK: {request.ok}
                [DEBUG] Method: {request.request.method}
                [DEBUG] StartTs: {start_ts}
            ''')
        for i in range(retries) :
            if request.ok :
                break
            if not request.ok :
                sleep(1)
                self.hold_for_token_refresh(url)
                request = super().request(method, url, **kwargs )
                self._wsnoc.logger.debug(f'[Try-{i}] [{method}] : {url}- {request.status_code}')
        end_ts = getTimestamp()
        execution_secs = round(end_ts - start_ts, 2)
        self._wsnoc.logger.info(f'[{method}] : {url} - [{request.status_code}][{execution_secs}sec]')
        request.start_ts = start_ts
        request.end_ts = end_ts
        request.execution = execution_secs
        self._wsnoc.current_requests -= 1
        return request

class PmHadoopClient :


    def __init__(self , _wsnoc : WSNOCLIB):
        self.ip = _wsnoc.address
        self.wsnoc = _wsnoc
        self.client : HdfsClient = None
        self.hdfs_port = 8020
        self.hdfs_user = 'otn'
        self.hdfs_root = '/'
        self.hdfs_use_trash = False
        self.PM24H = 1
        self.PM15M = 2
        self.KPIAGGR = 3
        self.CURRENT = 1
        self.ARCHIVE = 2
        self.logger : DEBUGGER = self.wsnoc.logger
        self.FREE_STORAGE_STRICT = True
        self.FREE_STORAGE_THRESHOLD_MB = 30000
        self.jhost = False
        self.jhost_obj = None

    
    def connect(self) :
        if not SNAKEBITEIMPORTED : 
            self.logger.error(f"HDFS Client importing had error. Maybe not supporting on this OS {sys.platform}. Exit")
            raise ImportError(f"HDFS Client importing had error. Maybe not supporting on this OS {sys.platform}. Exit")
        if not self.wsnoc.connected :
            raise Exception('WSNOC is not connected')
        try :
            self.logger.info(f"Connecting to PM Hadoop at {self.ip}:{self.hdfs_port}" , source='PmHadoopClient')
            self.client = HdfsClient(self.ip, self.hdfs_port, use_trash=self.hdfs_use_trash)
        except Exception as e:
            self.logger.warning('PM Hadoop client is using WSNOC port 8020/custom port. Please check if it is not blocked by firewall.' , source='PmHadoopClient')
            self.logger.error(f'Failed to connect to PM Hadoop: {e}' , source='PmHadoopClient')
            raise

    def change_date_to_timestamp(self , date_str) :
        '''
        this is a helper function to convert date string to timestamp
        date_str : must be in the format of %Y%m%d example: 20250101
        return : timestamp
        '''
        dt = datetime.strptime(date_str, "%Y%m%d")
        return int(dt.timestamp())

    def pm_list(self , mode , target_pm , date_range=[] , date_range_in_days=None) :
        '''
        mode : must be one of the following:
            - self.PM24H
            - self.PM15M
            - self.KPIAGGR
        target_pm : must be on the following :
            - self.CURRENT
            - self.ARCHIVE
        date_range : must be a list of two integers in the format of [start_timestamp, end_timestamp]
            -  for example: [1718217600, 1718221200]
        date_range_in_days : if provided, date_range will be set to last X days
            -  for example: 30 days ago to now
            - if date_range_in_days is not provided, date_range will be used as is
        - if date_range is not provided, all available PM dates will be returned
        '''
        self.logger.info(f"Getting available PM dates Original Args: {mode}/{target_pm}" , source='PmHadoopClient')
        if mode == self.PM24H :
            _mode = 'ONE_DAY'
        elif mode == self.PM15M :
            _mode = 'FIFTEEN_MINS'
        elif mode == self.KPIAGGR :
            _mode = 'KPIAGGR'
        else :
            raise Exception(f'Invalid mode: {mode}')
        if target_pm == self.CURRENT :
            _target = 'PMDATA'
        elif target_pm == self.ARCHIVE : 
            _target = "ARC_PMDATA"
        else :
            self.logger.error(f"target_pm arg must be self.CURRENT or self.ARCHIVE.")
            raise Exception("Invalid TARGET_PM")
        self.logger.info(f"Getting available PM dates for {_target}/{_mode}" , source='PmHadoopClient')
        dirs = list(self.client.ls([f'/{_target}/{_mode}']))
        if date_range_in_days :
            ts_now = getTimestamp() # this is in seconds
            self.logger.info(f"Setting date range to last {date_range_in_days} days" , source='PmHadoopClient')
            date_range = [ts_now - date_range_in_days * 24 * 60 * 60, ts_now]
        self.logger.info(f"Date range: {tuple(date_range)}" , source='PmHadoopClient')
        for index , dir in enumerate(dirs) :
            self.logger.info(f"Processing {dir.get('path')}" , source='PmHadoopClient')
            if 'ds' in dir.get('path' , '') :
                date_str = dir.get('path').split('=')[-1]
                dir['pm_date'] = int(date_str)
                dir['mode'] = _mode
                dt = datetime.strptime(date_str, "%Y%m%d")
                dir['pm_date_timestamp'] = int(dt.timestamp())
                if len(date_range) > 0 :
                    if dir['pm_date_timestamp'] < date_range[0] :
                        del dirs[index]
                    if dir['pm_date_timestamp'] > date_range[1] :
                        del dirs[index]
        return dirs
    
    def use_jump_host(self , jhost , use=True) :
        '''
        not yet implemented
        '''
        self.jhost = use
        if use :
            self.jhost_obj = None
        else :
            self.jhost_obj = None
        

    def _download_dir(self , hdfs_path, local_path):
        for entry in self.client.ls([hdfs_path]):
            entry_path = entry['path']
            entry_type = entry['file_type']
            if entry_type == 'd':
                subdir = os.path.join(local_path, os.path.basename(entry_path))
                mkdirs(subdir)
                self._download_dir(entry_path, subdir)
            else:  # FILE
                self.logger.info(f"Downloading {entry_path} → {local_path}" , source='PmHadoopClient')
                self.client.copyToLocal([entry_path], local_path)
        
    def download(self , obj , destination_path) :
        self.wsnoc.logger.info(f'Downloading {obj.get("pm_date")} to {destination_path}')
        destination_path = f"{destination_path}/{obj.get('mode')}/{obj.get('pm_date')}"
        self.logger.debug(f"FREE_STORAGE_THRESHOLD_MB={self.FREE_STORAGE_THRESHOLD_MB}  FREE_STORAGE_STRICT={self.FREE_STORAGE_STRICT}")
        mkdirs(destination_path)
        free_space = get_free_space(destination_path)
        if self.FREE_STORAGE_STRICT :
            if free_space < self.FREE_STORAGE_THRESHOLD_MB :
                self.logger.error(f'Free storage is less than {self.FREE_STORAGE_THRESHOLD_MB} MB. Skipping download. [free_space={free_space} MB]')
                raise Exception(f'No enough space to download PM data.')
        self._download_dir(obj.get('path'), destination_path)


if __name__ == '__main__' :
    # noc = WSNOCLIB('10.20.30.55' , 'admin' , 'Nokia@2024') 
    # noc.connect(auto_refresh_token=True)
# #     records= noc.getUserRecords()
# #     open( './w.json' , 'w').write(json.dumps(records))
# #     noc.logout()
    # kafka = nms.kafka_connect(
    #     external_nsp=True,
    #     nsp_address='10.250.4.176',
    #     user='root',
    #     password='Q1w2e3' ,
    #     # nodeIps=['10.198.34.3'] ,
    #     # severities=['minor' , 'critical' , 'major' , 'warning'] ,
    #     # alarms=['Card missing' , 'Loss of Signal'] ,
    #     # nodeNames=["RVMP_AUH2920-1"]
    # )
    # print(kafka.topicId)
    # messages = nms.kafka_listen()
    # for message in messages :
    #     print(message)
    #     pass
    pass
