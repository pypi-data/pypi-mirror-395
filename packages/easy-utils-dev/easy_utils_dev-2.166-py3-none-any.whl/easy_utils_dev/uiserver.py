import gc
import json
import time
from flask.ctx import F
from werkzeug.serving import ThreadedWSGIServer
from easy_utils_dev.utils import convertTimestampToDate, getRandomKey , generateToken , getTimestamp
from flask_socketio import SocketIO
from engineio.async_drivers import gevent
from engineio.async_drivers import threading as threading_engineio
from flask_cors import CORS
import logging  , os
from flask import jsonify, request , current_app , copy_current_request_context
from flask import Flask
from threading import Thread
import threading
from easy_utils_dev.custom_env import cenv
from easy_utils_dev.utils import kill_thread
from multiprocessing import Process
import traceback
from werkzeug.serving import make_ssl_devcert
from time import sleep
from easy_utils_dev.utils import start_thread , getRandomKeysAndStr , mkdirs , lget
from easy_utils_dev.temp_memory import TemporaryMemory
from easy_utils_dev.debugger import DEBUGGER
import signal
import sys 
from tempfile import gettempdir
from urllib.parse import parse_qs

TMP_PATH = gettempdir()

def getClassById( id ) :
    return cenv[id]

def create_ssl(host,output) :
    '''
    host : is the IP/Adress of the server which servers the web-server
    output: the output locaiton to generate the ssl certificate. it should end with filename without extension
    '''
    return make_ssl_devcert( output , host=host)

def clone_request(request):
    """Return a plain dict clone of Flask request data."""
    return {
        "method": request.method,
        "path": request.path,
        "url": request.url,
        "headers": dict(request.headers),
        "args": request.args.to_dict(flat=False),
        "form": request.form.to_dict(flat=False),
        "json": request.get_json(silent=True),
        "data": request.get_data(),   # raw body bytes
        "files": {k: v.filename for k, v in request.files.items()},
        "remote_addr": request.remote_addr,
        "cookies": request.cookies,
    }

class Stream :
    def __init__(self) :
        self.rows = []

    def register_row(self , row , options={}) :
        _row_stream_id = getRandomKeysAndStr(n=20)
        row['_row_stream_id'] = _row_stream_id
        for key , value in options.items() :
            if not key.startswith('_') :
                raise ValueError(f"Option key '{key}' must start with '_'")
            row[key] = value
        return row

    def send_cell_update(self , row , cell , value , sid=None ) :
        _row_stream_id = row['_row_stream_id']
        self.socketio.emit(f'/stream/{_row_stream_id}/{cell}' , value , to=sid)

    def send_new_row(self , tid , row , sid=None , insert_ontop=False ) :
        if not row.get('_row_stream_id') :
            row = self.register_table_row_stream(row)
        self.socketio.emit(f'/stream/table/{tid}/row' , {
            'row' : row,
            'options' : {
                'insert_ontop' : insert_ontop
            }
        } , to=sid )

class Response : 
    def __init__(self, socket : SocketIO , request : request ) :
        self.success = self.ok
        self.failure = self.error
        self.socket = socket
        self.request = request

    def _emit(self , data, role , options={} ) :
        self.socket.emit('/stream/notify' , { **data , '_role' : role , '_options' : options } , to=self.request.sid)

    def ok(self , result=[] , message=None , alert=False, toast=False , options={} , **kwargs) :
        role = None
        if alert :
            role = 'alert'
        elif toast :
            role = 'toast'
        timestamp = getTimestamp()
        r = {'status' : 200 , 'message' : message , 'result' : result , **kwargs, 'timestamp' : timestamp}
        if role :
            self._emit( r , role, options)
        return r

    def error(self , message=None , alert=False, toast=False , options={}  , **kwargs) :
        role = None
        if alert :
            role = 'alert'
        elif toast :
            role = 'toast'
        timestamp = getTimestamp()
        r = {'status' : 400 , 'message' : message , **kwargs , 'timestamp' : timestamp}
        if role :
            self._emit( r , role , options)
        return r
    
    def internal_error(self , message=None , alert=False, toast=False , options={}  , **kwargs ) :
        role = None
        if alert :
            role = 'alert'
        elif toast :
            role = 'toast'
        timestamp = getTimestamp()
        r = {'status' : 500 , 'message' : message , **kwargs , 'timestamp' : timestamp}
        if role :
            self._emit( r , role , options)
        return r

    def not_found(self , message=None , alert=False, toast=False , options={}  , **kwargs) :
        role = None
        if alert :
            role = 'alert'
        elif toast :
            role = 'toast'
        timestamp = getTimestamp()
        r = {'status' : 404 , 'message' : message , **kwargs , 'timestamp' : timestamp}
        if role :
            self._emit( r , role , options )
        return r
    
    def unauthorized(self , message=None , alert=False, toast=False , options={}  , **kwargs) :
        role = None
        if alert :
            role = 'alert'
        elif toast :
            role = 'toast'
        timestamp = getTimestamp()
        r = {'status' : 401 , 'message' : message , **kwargs , 'timestamp' : timestamp}
        if role :
            self._emit( r , role , options)
        return r

class AbortRequest :
    def __init__(self, request ) :
        self.request = clone_request(request)
        self.abort_id = None
        self.abortable = False
        self.thread = None
        self.cache = None
        self.start_ts = getTimestamp()
        self.result = None
        self.async_request = False
        self.internalid = None
        self.in_progress = False
        self.start_ts = None
        self.end_ts = None
        self.execution = None
        self.success = None
        self.traceback = None
        self.delete_async_request_ts = None
        self.killed = False

    def abort(self) : 
        kill_thread(self.thread)
        self.killed = True
        self.in_progress = False
        self.success = False
        self.traceback = None
        self.result = None
        self.delete_async_request_ts = getTimestamp(after_seconds=3600)
        self.end_ts = getTimestamp()
        self.execution = round(self.end_ts - self.start_ts, 2)
        if not self.async_request :
            self.cache.delete(self.abort_id)
        try :
            gc.collect()
        except :
            pass

class SocketClientObject :
    def __init__(self ) :
        self.client : SocketIO
        self.internalid : str = None
        self.request = {}
        self.sid = None
        self.rooms = None
        self.csid = None

class UISERVER :
    def __init__(self ,
            logger : DEBUGGER = None,
            id=getRandomKey(n=15),
            secretkey=generateToken(),
            serve_with_secret_key=False,
            address='localhost',
            port=5312 , 
            https=False , 
            ssl_crt=None,
            ssl_key=None,
            template_folder='templates/' ,
            static_folder = 'templates/assets'
            ,**kwargs
        ) -> None:
        self.id = id
        self.static_folder = static_folder
        self.app = app = Flask(self.id , template_folder=template_folder  ,  static_folder=self.static_folder )
        app.config['SECRET_KEY'] = secretkey
        CORS(app,resources={r"/*":{"origins":"*"}})
        self.address= address 
        self.port = port
        self.thread = None
        self.ssl_crt=ssl_crt
        self.ssl_key=ssl_key
        self.serve_with_secret_key=serve_with_secret_key
        self.secretkey=secretkey
        self.enable_test_url=True
        self.abort_requests = {}
        self.bg_requests = {}
        self.socketio_clients = []
        self.abort_base_url = '/request/abort'
        self.return_exception_as_code_400 = True
        self.request_reply_base_url= '/request/result'
        self.sessions = {}
        if https :
            self.httpProtocol = 'https'
        else :
            self.httpProtocol = 'http'
        self.socketio = SocketIO(app , cors_allowed_origins="*"  ,async_mode='threading' , engineio_logger=False , always_connect=True ,**kwargs )
        cenv[id] = self
        self.fullAddress = f"{self.httpProtocol}://{self.address}:{self.port}"
        self.cache = TemporaryMemory()
        start_thread(target=self.delete_very_old_requests)
        self.secret_key_execlude_urls = []
        self.socketio_rooms = {}
        self.log_url_requests = True
        self.logger = logger
        self.stream = Stream()
        self.simulate_network_delay = False
        self.Response = Response(self.socketio , request )
        if not self.logger :
            self.logger = DEBUGGER(
                name='easy_utils_dev_uiserver',
                homePath=TMP_PATH
            )
    def update_cert(self , crt, ssl ) :
        self.ssl_crt=crt
        self.ssl_key=ssl

    def register_abortable_request(self , request , abort_id = None ) :
        path = request.path
        Abort = AbortRequest(request)
        if not path.startswith(self.abort_base_url) :
            if not abort_id :
                if not request.headers.get('abortid') :
                    abort_id = getRandomKeysAndStr(n=20)
                else :
                    abort_id = request.headers.get('abortid')
            
            Abort.abort_id = abort_id
            current_thread = threading.current_thread()
            Abort.thread = current_thread
            Abort.cache = self.cache
            Abort.start_ts = getTimestamp()
            self.cache.set( Abort , custom_key=abort_id , auto_destroy_period=120 , store_deleted_key=False )
        return Abort

    def delete_very_old_requests(self) :
        while True :
            sleep(320)
            now = getTimestamp()
            for key, value in list(self.bg_requests.items()) :
                value : AbortRequest = value
                if value.delete_async_request_ts :
                    if value.delete_async_request_ts > now :
                        del self.bg_requests[key]
            gc.collect()

    def create_room(self , room_id : str , members : list[str] ) :
        self.socketio_rooms[room_id] = members
    
    def add_member_to_room(self , room_id : str , member : str ) :
        self.socketio_rooms[room_id].append(member)
    
    def remove_member_from_room(self , room_id : str , member : str ) :
        self.socketio_rooms[room_id].remove(member)
    
    def get_room_members(self , room_id : str ) :
        return self.socketio_rooms[room_id]

    def start_before_request(self) : 

        @self.app.route(f'{self.abort_base_url}/<id>' , methods=['DELETE'])
        def abort_request(id : str ) :
            abort : AbortRequest = self.cache.get(id)
            timestamp = getTimestamp()
            if abort :
                abort.abort()
                for i in range(30) :
                    th = abort.thread
                    alive = th.is_alive()
                    if not alive :
                        break
                    time.sleep(.25)
                return self.Response.ok(message='Request aborted' , abort_timestamp=timestamp , abort_id=id , alive=alive , url=abort.request.get('path'))
            
            else :
                return self.Response.not_found(message='Request not found or request is not abortable. Check request headers for abortable flag.')
        
        @self.app.route(f"/request/traceback/<key>" , methods=['GET'])
        def get_traceback(key : str ) :
            traceback = self.cache.get(key)
            if traceback :
                return self.Response.ok(message='Traceback found' , traceback=traceback.get('traceback'))
            else :
                return self.Response.not_found(message='Traceback not found or expired')

        @self.app.route(f'{self.request_reply_base_url}/<id>' , methods=['GET'])
        def get_result_of_async_request(id : str ) :
            request : AbortRequest = self.bg_requests.get(id)
            if request :
                return self.Response.ok(
                    message='Result of async request found' , 
                    result=request.result ,
                    in_progress=request.in_progress ,
                    async_request=request.async_request ,
                    internalid=request.internalid , 
                    start_ts=request.start_ts , 
                    end_ts=request.end_ts , 
                    execution=request.execution ,
                    success=request.success ,
                    killed=request.killed
                )


        @self.app.before_request
        def before_request() :
            if self.log_url_requests and self.logger :
                self.logger.info(f'[{request.method}]: {request.url}'  , source='WebServer')

                
            if (self.serve_with_secret_key) and (request.path not in self.secret_key_execlude_urls) and (request.headers.get('secretkey') != self.secretkey):
                return self.Response.unauthorized(message='Secret key is invalid')
                        
            @copy_current_request_context
            def run_async_job_results( target_func , abort : AbortRequest ) :
                abort.in_progress = True
                abort.async_request = True
                abort.internalid = request.internalid
                abort.start_ts = getTimestamp()
                try :
                    result = target_func(*request.args, **request.form)
                    abort.success = True
                except Exception as e :
                    abort.success = False
                    abort.result = str(e)
                    abort.traceback = traceback.format_exc()
                    raise
                abort.result = result
                abort.end_ts = getTimestamp()
                abort.execution = round(abort.end_ts - abort.start_ts, 2)
                abort.in_progress = False
                abort.delete_async_request_ts = getTimestamp(after_seconds=3600)


            request.sid = ''
            abortable = request.headers.get('abortable')
            requestId = getRandomKeysAndStr(n=10)
            request.start_ts = getTimestamp()
            client : SocketClientObject = self.sessions.get(request.headers.get('csid'))
            request.sid = client.sid
            request.client = client
            request.csid = request.headers.get('csid')
            request.internalid = requestId
            if abortable :
                abort = self.register_abortable_request(request)
                request.abortable = True
                request.abort_id = abort.abort_id
                # check here if async in the headers
                # if yes . i will trigger the function in thread 
                # start_tread(#how to get the target function here ? )
                # now i want to return response to UI { status : 200 , message : 'request now in running bg' , abort_id : abort.abort_id }
                # the flask function should not be called again
                if request.headers.get('async') == 'false' : 
                    target_func = current_app.view_functions.get(request.endpoint)
                    if not target_func:
                        return self.Response.not_found(message='Route not found')
                    th = start_thread(target=run_async_job_results, args=[target_func , abort ])
                    abort.thread = th
                    self.bg_requests[requestId] = abort
                    return self.Response.ok(message='Request now in running bg' , abort_id=abort.abort_id)
    
        if self.return_exception_as_code_400 :
            @self.app.errorhandler(Exception)
            def handle_exception(e):

                exc_type, exc_value, exc_traceback = sys.exc_info()
                key = getRandomKeysAndStr(n=10)
                tb_last = traceback.extract_tb(exc_traceback)[-1]  # Get last traceback frame
                # Example: file, line, function, text
                error_file = tb_last.filename
                error_line = tb_last.lineno
                error_func = tb_last.name
                error_code = tb_last.line

                # Log the full traceback (optional)
                traceback.print_exc()
                # Customize the error response
                t = getTimestamp()
                response = {
                    "status" : 400 ,
                    "key" : key,
                    "error": str(e),
                    "message": str(e),
                    "type": type(e).__name__ ,
                    "request_full_url" : request.url ,
                    "request_method" : request.method ,
                    "endpoint" : request.endpoint ,
                    "request_path" : request.path ,
                    "error_file" : os.path.basename(error_file).replace('.py' , ''),
                    "error_line" : error_line,
                    "error_func" : error_func,
                    "error_code" : error_code,
                    'timestamp' : t ,
                    "date" : convertTimestampToDate(t) ,
                    'traceback_url' : f"/request/traceback/{key}"
                }
                self.logger.error(f'error: {json.dumps(response , indent=4)}')
                self.cache.set( custom_key=key , item={**response , 'traceback' : str(traceback.format_exc())} , auto_destroy_period=1800 , store_deleted_key=False )
                return self.Response.error( **response )

        @self.app.after_request
        def after_request(response) :

            if self.simulate_network_delay :
                time.sleep(self.simulate_network_delay)
            now = getTimestamp()
            x = round(now - request.start_ts, 2)
            try :
                response.headers['internalid'] = request.internalid
                response.headers['start_ts'] = request.start_ts
                response.headers['end_ts'] = now
                response.headers['execution'] = x
                if request.abortable :
                    response.headers['abortid'] = request.abort_id 
                    response.headers['abortable'] = True
            except :
                response.headers['abortable'] = False
            if self.log_url_requests and self.logger :
                self.logger.info(f'[{request.method}]: {request.url} - [{response.status_code}] [secs:{x}]'  , source='WebServer')
            return response


        # socketio client connected.
        @self.socketio.on('connect')
        def handle_client_connect():
            sid = request.sid
            client = SocketClientObject()
            client.internalid = getRandomKeysAndStr(n=20)
            client.sid = sid
            client.request = request
            query = parse_qs(request.query_string.decode('utf-8'))
            csid = lget(query.get('csid') , 0 , None )
            client.csid = csid
            client.rooms = self.socketio_rooms
            self.socketio_clients.append(client)
            self.socketio.emit('/internal/connect', { 
                'status': 200, 
                'message': 'client connected' , 
                'internalid' : client.internalid,
                'sid' : sid,
            }, 
                to=sid
            )
            if csid :
                self.sessions[csid] = client
            print(f'client connected : csid={csid} | SID={sid} | Clients : {len(self.socketio_clients)}')
        
        # socketio client connected.
        @self.socketio.on('disconnect')
        def handle_client_disconnect():
            for i , c in enumerate(list(self.socketio_clients)) :
                print(f'c.sid : {c.sid} | request.sid : {request.sid}')
                if c.sid == request.sid :
                    try :
                        del self.socketio_clients[i]
                    except :
                        pass
                    print(f'client disconnected : csid={c.csid} | SID={request.sid} | Clients : {len(self.socketio_clients)}')
                    break

    def getSocketio( self ):
        return self.socketio
    
    def getFlask( self ):
        return self.app
    
    def shutdownUi(self) :
        if hasattr(self, 'wsgi_server') and self.wsgi_server:
            try:
                self.wsgi_server.shutdown()
                self.wsgi_server.server_close()
            except:
                pass
        kill_thread(self.thread)

    def _wait_th(self , t ) :
        # t.join()
        while True :
            time.sleep(36000)
    

    def thrStartUi(self , suppress_prints=True) :
        if self.enable_test_url :
            if not suppress_prints :
                print(f'TEST URL GET-METHOD /connection/test/internal')
            @self.app.route('/connection/test/internal' , methods=['GET'])
            def test_connection():
                return f"Status=200<br> ID={self.id}<br> one-time-token={getRandomKey(20)}"

                
        if self.httpProtocol == 'http' :
            con = None
        elif self.httpProtocol == 'https' :
            con=(self.ssl_crt , self.ssl_key)
        self.wsgi_server = wsgi_server = ThreadedWSGIServer(
            host = self.address ,
            ssl_context=con,
            # ssl_context=('ssl.crt', 'ssl.key'),
            port = self.port,
            app = self.app )
        if not suppress_prints :
            print(f"web-socket: {self.fullAddress}")
            print(f"UI URL : {self.fullAddress}")
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        wsgi_server.serve_forever()
    
    def on_ctrl_c(self , sig=None, frame=None):
        self.stopUi()
        pid = os.getpid()
        os.kill(pid, signal.SIGTERM)
        sys.exit(0)


    def startUi(self , daemon=False , suppress_prints=True , block=False) :
        self.start_before_request()
        self.thread = self.flaskprocess = Thread(target=self.thrStartUi , args=[suppress_prints])
        self.flaskprocess.daemon = daemon
        self.flaskprocess.start()
        start_thread(target=self._wait_th , args=[self.thread] , daemon=daemon)
        signal.signal(signal.SIGINT, self.on_ctrl_c )
        if block:
            self.wait()
        return self.thread
    
    def wait(self):
        """
        Block the main thread to keep it alive for signal handling (Ctrl+C).
        This allows Ctrl+C to be properly detected. Call this after startUi() 
        if you want signal handling to work.
        """
        try:
            while self.flaskprocess.is_alive():
                self.flaskprocess.join(timeout=0.1)
        except KeyboardInterrupt:
            if not hasattr(self, '_shutting_down'):
                self._shutting_down = True
                self.on_ctrl_c()
        except SystemExit:
            # Re-raise SystemExit to allow proper program termination
            raise
    
    def stopUi(self) :
        if hasattr(self, 'wsgi_server') and self.wsgi_server:
            try:
                self.wsgi_server.shutdown()
            except:
                pass
        kill_thread(self.thread)
        return True