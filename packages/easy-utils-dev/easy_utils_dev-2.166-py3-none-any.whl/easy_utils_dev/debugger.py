import logging
import os
import shutil
import  sys , re , random
from datetime import datetime
from logging.handlers import RotatingFileHandler
from .utils import getRandomKey , convert_mb_to_bytes , getTimestamp, mkdirs , start_thread
from .custom_env import custom_env , setupEnvironment
from .Events import EventEmitter
from threading import Thread
from time import sleep

gEvent = EventEmitter()
logging.addLevelName(25, "SCREEN")

def setGlobalHomePath( path ) :
    env = custom_env()
    env['debugger_homepath'] = path
    gEvent.dispatchEvent('update_home_path')

def setGlobalDisableOnScreen(on_screen=False) :
    env = custom_env()
    env['debugger_on_screen'] = on_screen
    if not on_screen :
        gEvent.dispatchEvent('disable_global_printing')
    else :
        gEvent.dispatchEvent('enable_global_printing')
        
    
def setGlobalDebugLevel(level='info') :
    env = custom_env()
    env['debugger_global_level'] = level
    gEvent.dispatchEvent('update_debug_level')


class CensorFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.censored_strings = []
        self.censor_ip = True
        # Regex for IPv4
        self.ip_regex = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")

    def add_censored_string(self, value):
        if value :
            if str(value) not in self.censored_strings : 
                self.censored_strings.append(str(value))

    def filter(self, record):
        msg = record.getMessage()

        # Replace registered sensitive strings
        for s in self.censored_strings:
            x = random.randint(5, 10)
            msg = msg.replace(s, '*'*x)
        # Replace IPs
        if self.censor_ip :
            msg = self.ip_regex.sub("***.***.***.***", msg)
        # Overwrite message
        record.msg = msg
        record.args = ()
        return True

class DEBUGGER:
    def __init__(self 
            , name
            , level='info', 
            fullSyntax=True, 
            onscreen=True,
            log_rotation=3,
            homePath=None,
            id=getRandomKey(9) , 
            global_debugger=None,
            disable_log_write=False,
            file_name=None,
            seperate_files=True,
            trust_env_log_path=True
        ):
        env = custom_env()
        setupEnvironment( 'debugger' )
        debugger_on_screen = env.get('debugger_on_screen' , True)
        env['debugger_on_screen'] = debugger_on_screen
        self.env = env
        self.events = gEvent
        self.debuggerLabel = f"{name}"
        self.logger = logging.getLogger(self.debuggerLabel)
        self.set_level(level)
        self.file_handler_class=None
        self.LOG_SIZE_THRESHOLD_IN_BYTES = 10 * 1024 * 1024
        self.BACKUP_COUNT = log_rotation
        self.name = name
        self.create_log_path(homePath, file_name)
        self.fullSyntax=fullSyntax
        self.onScreen= onscreen
        self.trust_env_log_path = trust_env_log_path
        self.id = id
        self.stream_service = None
        if not env['debugger'].get(name) :
            self.console = console_handler = logging.StreamHandler()
        else :
            self.console = console_handler = env['debugger'].get(name).console
        if not self.logger.hasHandlers() :
            self.logger.addHandler(self.console)
        self.rotate_disabled=False
        self.isInPyinstaller = False
        self.log_iterations=0
        self.log_iterations_threshold = 200
        self.global_debugger = global_debugger
        self.isLogWriteDisabled = disable_log_write
        self.type = "CUSTOM_DEBUGGER"
        self.censor = CensorFilter()
        console_handler.addFilter(self.censor)

        self.seperate_files=seperate_files
        if fullSyntax :
            f = f"[%(asctime)s]-[{self.name}]-[%(levelname)s]: %(message)s"
        else :
            f = f"[{self.name}]-[%(levelname)s]: %(message)s"
        self.syntax = f
        self.formatter = logging.Formatter(f , datefmt='%Y-%m-%d %H:%M:%S' )
        if not env['debugger'].get(name) :
            console_handler.setFormatter(self.formatter)
        if not disable_log_write :
            if not env['debugger'].get(name) :
                self.file_handler_class = self.createRotateFileHandler(self.log_path_with_filename)
        if onscreen : 
            self.enable_print()
        elif not onscreen : 
            self.disable_print()
        self.events.addEventListener('disable_global_printing' , self.disable_print )
        self.events.addEventListener('enable_global_printing' , self.enable_print )
        self.events.addEventListener('update_home_path' , self.updateGlobalHomePath )
        self.events.addEventListener('update_debug_level' , self.updateGlobalSetLevel )
        if env['debugger'].get(name) :
            self =  env['debugger'].get(name)
        else:
            env['debugger'][id] = self
            env['debugger'][name] = self
        if not env.get('debugger_on_screen' , True ) :
            self.disable_print()
        if env.get('debugger_on_screen' , True ) :
            self.enable_print()
        if os.environ.get("EASY_UTILS_DEBUG_LEVEL") :
            EASY_UTILS_DEBUG_LEVEL = os.environ.get("EASY_UTILS_DEBUG_LEVEL")
            if not EASY_UTILS_DEBUG_LEVEL.lower() in ['info' , 'debug' , 'warning' , 'error' , 'critical'] :
                self.logger.error(f'EASY_UTILS_DEBUG_LEVEL ENV must be one of [info,debug,warning,error,critical] | Current Env Variable Is "{EASY_UTILS_DEBUG_LEVEL}". Skipping ')
            else :
                self.set_level(EASY_UTILS_DEBUG_LEVEL)
        if os.environ.get("EASY_UTILS_ENABLE_PRINT" , '' ).lower() == 'true' :
            self.enable_print()
        start_thread(target=self.checks_in_bg)

    def create_log_path(self , base_path , logname ) :
        # print(f"Creating log path : {base_path} {logname}")
        if not base_path :
            base_path = os.getcwd()
        if not logname :
            logname = self.name
        if base_path :
            mkdirs(base_path)
            self.baseHomePath = base_path
            self.filename = logname
            self.lastAbsoluteHomePath = base_path
            self.log_path_with_filename = os.path.join(base_path, f'{logname}.log')

    def switch_full_syntax(self , toggle) :
        if toggle :
            f = f"[%(asctime)s]-[{self.name}]-[%(levelname)s]: %(message)s"
        else :
            f = f"[{self.name}]-[%(levelname)s]: %(message)s"
        self.syntax = f
        self.formatter = logging.Formatter(f , datefmt='%Y-%m-%d %H:%M:%S' )
        self.console.setFormatter(self.formatter)    

    def custom_log_syntax(self , syntax) :
        '''
        f"[%(asctime)s]-[{self.name}]-[%(levelname)s]: %(message)s"
        '''
        f = syntax
        self.syntax = f
        self.formatter = logging.Formatter(f , datefmt='%Y-%m-%d %H:%M:%S' )
        self.console.setFormatter(self.formatter)    

    def updateGlobalHomePath(self ) :
        if not self.trust_env_log_path :
            return
        if not self.isLogWriteDisabled :
            getFromEnv = self.env.get('debugger_homepath' , None )
            if getFromEnv : 
                self.create_log_path(getFromEnv, self.filename)
                self.file_handler_class = self.createRotateFileHandler(self.log_path_with_filename)

    def updateGlobalSetLevel( self ) :
        self.set_level(self.env['debugger_global_level'])

    def advertiseGlobalDebugLevel(self , level) :
        setGlobalDebugLevel(level)

    def disable_rotate(self) :
        self.rotate_disabled = True

    def enable_rotate(self) :
        self.rotate_disabled = False

    def createRotateFileHandler( self , path ) :
        old = self.file_handler_class
        if old :
            self.logger.removeHandler(old)
        file_handler = RotatingFileHandler(path ,  maxBytes=self.LOG_SIZE_THRESHOLD_IN_BYTES , backupCount=self.BACKUP_COUNT , delay=True )
        self.file_handler= file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
        return file_handler

    def update_log_iterantions_threshold(self,threshold : int ):
        '''
        set value when rotation should be checked. when every on_log function called.
        by default rotation will be checked every 200 on_log function call.
        '''
        self.log_iterations_threshold = threshold

    def updateGlobalDebugger(self , logger ) :
        '''
        this function pass the log message to other logger to write the same log message to it.
        logger must be debugger class.
        '''
        if logger.type != 'CUSTOM_DEBUGGER' :
            raise Exception(f'Invalid logger type. must pass debugger class.')
        self.global_debugger = logger

    def getStreamServiceUrlPath(self) :
        return self.streampath

    def getStreamService(self) :
        return self.stream_service

    def isStreamServiceAvailable(self) :
        if self.stream_service :
            return True
        return False

    def addStreamService( self , socketio , streampath='/debugger/stream/log' ) :
        """
        This function takes a live socketio server. it emit the log message using default path which is /debugger/stream/log
        """
        self.stream_service = socketio
        self.streampath = streampath
        
    def updateLogName( self , name ) :
        self.name = name

    def disable_log_write(self) :
        '''
        this function is used to disable the log write to file. if onScreen is enabled, logs will be displayed only on screen.
        '''
        self.isLogWriteDisabled = True
        if self.file_handler_class :
            self.logger.removeHandler(self.file_handler_class)
    
    def enable_log_write(self) :
        self.createRotateFileHandler(self.log_path_with_filename)

    def get_rotate_handler(self) :
        return self.file_handler_class
            
    def change_log_size(self, size) -> bool:
        '''
        change the size of each log file rotation.
        default is 10M
        size should be passed as MB
        '''
        size = convert_mb_to_bytes(size)
        self.LOG_SIZE_THRESHOLD_IN_BYTES = size
        handler = self.get_rotate_handler()
        handler.maxBytes = size
        return True
    
    def checks_in_bg(self) :
        while True :
            if self.env.get('GLOBAL_DEBUGGER_STREAM_SERVICE') :
                self.addStreamService(socketio=self.env.get('GLOBAL_DEBUGGER_STREAM_SERVICE'))
            if self.env.get('debugger_global_level' , None) : 
                self.set_level( level=self.env.get('debugger_global_level') )
            if not self.env.get('debugger_on_screen' , True ) :
                self.disable_print()
            if self.env.get('debugger_on_screen' , True ) :
                self.enable_print()
            if os.environ.get("EASY_UTILS_DEBUG_LEVEL") :
                EASY_UTILS_DEBUG_LEVEL = os.environ.get("EASY_UTILS_DEBUG_LEVEL")
                if not EASY_UTILS_DEBUG_LEVEL.lower() in ['info' , 'debug' , 'warning' , 'error' , 'critical'] :
                    self.logger.error(f'EASY_UTILS_DEBUG_LEVEL ENV must be one of [info,debug,warning,error,critical] | Current Env Variable Is "{EASY_UTILS_DEBUG_LEVEL}". Skipping ')
                else :
                    self.set_level(EASY_UTILS_DEBUG_LEVEL)
            if self.trust_env_log_path :
                self.updateGlobalHomePath()
            if os.environ.get("EASY_UTILS_ENABLE_PRINT" , '' ).lower() == 'true' :
                self.enable_print()
            sleep(10)

    def close(self) :
        try :
            logging.shutdown()
        except :
            pass


    def get_current_levels(self):
        """
        Returns a list of log levels that will be printed based on the current logging level.
        """
        levels_order = [
            ('debug', logging.DEBUG),
            ('info', logging.INFO),
            ('warning', logging.WARNING),
            ('error', logging.ERROR),
            ('critical', logging.CRITICAL),
        ]
        # Optional custom level
        if hasattr(logging, 'SCREEN'):
            levels_order.append(('screen', logging.SCREEN))
        current_level = self.logger.level
        # Return all levels with numeric value >= current_level
        return [name for name, value in levels_order if value >= current_level]

    def enable_print(self) :
        self.onScreen = True
        self.logger.addHandler(self.console)

    def disable_print(self) : 
        self.onScreen = False
        self.logger.removeHandler(self.console)

    def changeHomePath( self , path ) :
        def delet_later(lastAbsoluteHomePath) :
            if lastAbsoluteHomePath :
                sleep(1)
                try :
                    shutil.rmtree(lastAbsoluteHomePath)
                except :
                    pass
        start_thread(target=delet_later, args=[self.lastAbsoluteHomePath])
        sleep(.5)
        self.create_log_path( path , self.filename)
        self.file_handler_class = self.createRotateFileHandler(self.log_path_with_filename)

    def isGlobalDebuggerDefined(self) :
        if self.global_debugger :
            return True
        else :
            return False

    def set_level(self, level : str):
        if 'info' in level.lower() : lvl = logging.INFO
        elif 'warn' in level.lower() : lvl = logging.WARNING
        elif 'warning' in level.lower() : lvl = logging.WARNING
        elif 'critical' in level.lower() : lvl = logging.CRITICAL
        elif 'debug' in level.lower() : lvl = logging.DEBUG
        elif 'error' in level.lower() : lvl = logging.ERROR
        elif 'screen' in level.lower() : lvl = logging.SCREEN
        else : raise ValueError('Unknown level, not one of [info,warn,warning,critical,debug,error,screen]')
        self.currentDebugLevel = level
        self.logger.setLevel(lvl)

    def get_current_debug_level(self) :
        return self.currentDebugLevel

    def get_logger(self) : 
        return self.logger
    
    def before_log(self , message , level) :

        def __call_thread__() :
            if not level in self.get_current_levels() :
                return
            if self.isStreamServiceAvailable() :
                d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                streamUrl = self.getStreamServiceUrlPath()
                try :
                    self.stream_service.emit( streamUrl , {
                        'message' : message ,
                        'level' : level ,
                        'msg' : message,
                        'date' : d ,
                        'id' : self.id,
                        'formate' : 'json' ,
                        'source' : self.name ,
                        'getTimestamp' : getTimestamp()
                    })
                except :
                    pass
        try :
            t= Thread(target=__call_thread__)
            # t.daemon=True
            t.start()
        except :
            __call_thread__()
            
        params = {
                'screen' : True  ,
                'file': True
            }
        if self.onScreen and self.env['debugger_on_screen'] == True :
            params['screen'] = True
        else :
            params['screen'] = False
        return params
        

    def info(self, message , external_debugger=None,source=None):
        def __call__(message) :
            if source :
                message = f'[{source}]-{message}'
            self.before_log(message , 'info')
            self.logger.info(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.info(message)
            if external_debugger :
                external_debugger.info(message)
        try :
            r=Thread(target=__call__,args=[message])
            r.daemon=True
            r.start()
            r.join()
        except :
            __call__(message)

    def debug(self, message , external_debugger=None,source=None):
        def __call__(message) :
            if source :
                message = f'[{source}]-{message}'
            self.before_log(message , 'debug')
            self.logger.debug(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.debug(message)
            if external_debugger :
                external_debugger.debug(message)
        try :
            r=Thread(target=__call__,args=[message])
            r.daemon=True
            r.start()
            r.join()
        except :
            __call__(message)

    def warning(self, message , external_debugger=None,source=None):
        def __call__(message) :
            if source :
                message = f'[{source}]-{message}'
            self.before_log(message , 'warning')
            self.logger.warning(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.warning(message)
            if external_debugger :
                external_debugger.warning(message)
        try :
            r=Thread(target=__call__,args=[message])
            r.daemon=True
            r.start()
            r.join()
        except :
            __call__(message)

    def error(self, message,external_debugger=None,source=None):
        def __call__(message) :
            if source :
                message = f'[{source}]-{message}'
            self.before_log(message , 'error')
            self.logger.error(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.error(message)
            if external_debugger :
                external_debugger.error(message)
        try :
            r=Thread(target=__call__,args=[message])
            r.daemon=True
            r.start()
            r.join()
        except :
            __call__(message)

    def critical(self, message,external_debugger=None,source=None):
        def __call__() :
            if source :
                message = f'[{source}]-{message}'
            self.before_log(message , 'critical')
            self.logger.critical(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.critical(message)
            if external_debugger :
                external_debugger.critical(message)
        try :
            r=Thread(target=__call__,args=[message])
            r.daemon=True
            r.start()
            r.join()
        except :
            __call__(message)

    def screen(self, message,external_debugger=None,source=None):
        def __call__() :
            if source :
                message = f'[{source}]-{message}'
            self.before_log(message , 'critical')
            print(f"{self.syntax}")
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.critical(message)
            if external_debugger :
                external_debugger.critical(message)
        try :
            r=Thread(target=__call__,args=[message])
            r.daemon=True
            r.start()
            r.join()
        except :
            __call__(message)