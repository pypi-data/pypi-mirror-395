#
#  Copyright (c) 2011-2014 Exxeleron GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import socket
import struct
import threading
import time

from .qmetaconversion import MetaData, CONVERSION_OPTIONS

# Debug logging control
DEBUG = False

from .qtype import QException
from .qreader import QReader, QReaderException
from .qwriter import QWriter, QWriterException



class QConnectionException(Exception):
    '''Raised when a connection to the q service cannot be established.'''
    pass



class QAuthenticationException(QConnectionException):
    '''Raised when a connection to the q service is denied.'''
    pass



class MessageType(object):
    '''Enumeration defining IPC protocol message types.'''
    ASYNC = 0
    SYNC = 1
    RESPONSE = 2

class ListenerThread(threading.Thread):
    def __init__(self, connection, callback_handler=None, data_only=False, raw=False):
        super(ListenerThread, self).__init__()
        self.connection = connection
        self.callback_handler = callback_handler
        self.messages = []
        self._stopper = threading.Event()
        self.data_only = data_only
        self.raw = raw

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def is_alive(self):
        """Check if the listener thread is still running"""
        return threading.Thread.is_alive(self)

    def wait_for_response(self, timeout_seconds):
        """
        Clear messages and wait for a response message (type 2).

        Args:
            timeout_seconds: Maximum time to wait for response

        Returns:
            bool - True if response arrived within timeout, False otherwise
        """
        self.messages.clear()  # Start fresh
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            # If thread is dead, return False immediately
            if not self.is_alive():
                return False

            if self.messages and self.messages[-1].type == MessageType.RESPONSE:
                return True
            time.sleep(0.01)  # 10ms polling

        return False

    def run(self):
        import logging
        import traceback
        import os

        # Set up logging only if DEBUG is enabled
        logger = None
        if DEBUG:
            log_file = '/tmp/qmcp_listener.log'
            logger = logging.getLogger('ListenerThread')

            # Remove any existing handlers to avoid duplicates
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            # Create file handler
            file_handler = logging.FileHandler(log_file, mode='a')
            file_handler.setLevel(logging.DEBUG)

            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Add handler to logger
            logger.addHandler(file_handler)
            logger.setLevel(logging.DEBUG)

            logger.info("ListenerThread started")

        while not self.stopped():
            try:
                message = self.connection.receive(data_only=self.data_only, raw=self.raw)
                if self.callback_handler:
                    self.callback_handler(message)
                else:
                    self.messages.append(message)
            except QException as e:
                if DEBUG and logger:
                    logger.error(f"Q exception in listener: {e}")
                    logger.debug(f"Q exception traceback: {traceback.format_exc()}")
            except Exception as e:
                if DEBUG and logger:
                    logger.error(f"Socket/connection error in listener: {e}")
                    logger.debug(f"Full traceback: {traceback.format_exc()}")
                    logger.info("Stopping listener thread due to connection error")
                # Connection is likely dead, stop the thread
                break


class QConnection(object):
    '''Connector class for interfacing with the q service.
    
    Provides methods for synchronous and asynchronous interaction.
    
    The :class:`.QConnection` class provides a context manager API and can be 
    used with a ``with`` statement::
    
        with qconnection.QConnection(host = 'localhost', port = 5000) as q:
            print(q)
            print(q('{`int$ til x}', 10))
    
    :Parameters:
     - `host` (`string`) - q service hostname
     - `port` (`integer`) - q service port
     - `username` (`string` or `None`) - username for q authentication/authorization
     - `password` (`string` or `None`) - password for q authentication/authorization
     - `timeout` (`nonnegative float` or `None`) - set a timeout on blocking socket operations
     - `encoding` (`string`) - string encoding for data deserialization
     - `reader_class` (subclass of `QReader`) - data deserializer
     - `writer_class` (subclass of `QWriter`) - data serializer
    :Options: 
     - `raw` (`boolean`) - if ``True`` returns raw data chunk instead of parsed 
       data, **Default**: ``False``
     - `numpy_temporals` (`boolean`) - if ``False`` temporal vectors are
       backed by raw q representation (:class:`.QTemporalList`, 
       :class:`.QTemporal`) instances, otherwise are represented as 
       `numpy datetime64`/`timedelta64` arrays and atoms,
       **Default**: ``False``
     - `single_char_strings` (`boolean`) - if ``True`` single char Python 
       strings are encoded as q strings instead of chars, **Default**: ``False``
    '''

    MAX_PROTOCOL_VERSION = 6

    def __init__(self, host, port, username = None, password = None, timeout = None, encoding = 'latin-1', reader_class = None, writer_class = None, **options):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self._connection = None
        self._connection_file = None
        self._protocol_version = None

        self.timeout = timeout

        self._encoding = encoding

        self._options = MetaData(**CONVERSION_OPTIONS.union_dict(**options))

        # Always use base QReader (pandas support is now conditional)
        self._reader_class = QReader
        
        try:
            from ._pandas import PandasQWriter
            self._writer_class = PandasQWriter
        except (ImportError, AssertionError):
            self._writer_class = QWriter

        if reader_class:
            self._reader_class = reader_class

        if writer_class:
            self._writer_class = writer_class


    def __enter__(self):
        self.open()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    @property
    def protocol_version(self):
        '''Retrieves established version of the IPC protocol.
        
        :returns: `integer` -- version of the IPC protocol
        '''
        return self._protocol_version


    def open(self):
        '''Initialises connection to q service.
        
        If the connection hasn't been initialised yet, invoking the 
        :func:`.open` creates a new socket and performs a handshake with a q 
        service.
        
        :raises: :class:`.QConnectionException`, :class:`.QAuthenticationException` 
        '''
        if not self._connection:
            if not self.host:
                raise QConnectionException('Host cannot be None')

            self._init_socket()
            self._initialize()

            self._writer = self._writer_class(self._connection, protocol_version = self._protocol_version, encoding = self._encoding)
            self._reader = self._reader_class(self._connection_file, encoding = self._encoding)


    def _init_socket(self):
        '''Initialises the socket used for communicating with a q service,'''
        try:
            self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._connection.connect((self.host, self.port))
            self._connection.settimeout(self.timeout)
            self._connection_file = self._connection.makefile('b')
        except:
            self._connection = None
            self._connection_file = None
            raise


    def close(self):
        '''Closes connection with the q service.'''
        if self._connection:
            self._connection_file.close()
            self._connection_file = None
            self._connection.close()
            self._connection = None


    def is_connected(self):
        '''Checks whether connection with a q service has been established. 
        
        Connection is considered inactive when: 
         - it has not been initialised, 
         - it has been closed.
         
        :returns: `boolean` -- ``True`` if connection has been established, 
                  ``False`` otherwise
        '''
        return True if self._connection else False


    def _initialize(self):
        '''Performs a IPC protocol handshake.'''
        credentials = (self.username if self.username else '') + ':' + (self.password if self.password else '')
        credentials = credentials.encode(self._encoding)
        self._connection.send(credentials + bytes([self.MAX_PROTOCOL_VERSION, 0]))
        response = self._connection.recv(1)

        if len(response) != 1:
            self.close()
            self._init_socket()

            self._connection.send(credentials + b'\0')
            response = self._connection.recv(1)
            if len(response) != 1:
                self.close()
                raise QAuthenticationException('Connection denied.')

        self._protocol_version = min(struct.unpack('B', response)[0], self.MAX_PROTOCOL_VERSION)


    def __str__(self):
        return '%s@:%s:%s' % (self.username, self.host, self.port) if self.username else ':%s:%s' % (self.host, self.port)


    def query(self, msg_type, query, *parameters, **options):
        '''Performs a query against a q service.
        
        In typical use case, `query` is the name of the function to call and 
        `parameters` are its parameters. When `parameters` list is empty, the 
        query can be an arbitrary q expression (e.g. ``0 +/ til 100``).
        
        Calls a anonymous function with a single parameter:
        
            >>> q.query(qconnection.MessageType.SYNC,'{til x}', 10)
        
        Executes a q expression:
        
            >>> q.query(qconnection.MessageType.SYNC,'til 10')
        
        :Parameters:
         - `msg_type` (one of the constants defined in :class:`.MessageType`) - 
           type of the query to be executed
         - `query` (`string`) - query to be executed
         - `parameters` (`list` or `None`) - parameters for the query
        :Options:
         - `single_char_strings` (`boolean`) - if ``True`` single char Python 
           strings are encoded as q strings instead of chars, 
           **Default**: ``False``
        
        :raises: :class:`.QConnectionException`, :class:`.QWriterException`
        '''
        if not self._connection:
            raise QConnectionException('Connection is not established.')

        if parameters and len(parameters) > 8:
            raise QWriterException('Too many parameters.')

        if not parameters or len(parameters) == 0:
            self._writer.write(query, msg_type, **self._options.union_dict(**options))
        else:
            self._writer.write([query] + list(parameters), msg_type, **self._options.union_dict(**options))


    def sendSync(self, query, *parameters, **options):
        '''Performs a synchronous query against a q service and returns parsed
        data.

        In typical use case, `query` is the name of the function to call and
        `parameters` are its parameters. When `parameters` list is empty, the
        query can be an arbitrary q expression (e.g. ``0 +/ til 100``).

        Executes a q expression:

            >>> print(q.sendSync('til 10'))
            [0 1 2 3 4 5 6 7 8 9]

        Executes an anonymous q function with a single parameter:

            >>> print(q.sendSync('{til x}', 10))
            [0 1 2 3 4 5 6 7 8 9]

        Executes an anonymous q function with two parameters:

            >>> print(q.sendSync('{y + til x}', 10, 1))
            [ 1  2  3  4  5  6  7  8  9 10]

            >>> print(q.sendSync('{y + til x}', *[10, 1]))
            [ 1  2  3  4  5  6  7  8  9 10]

        The :func:`.sendSync` is called from the overloaded :func:`.__call__`
        function. This allows :class:`.QConnection` instance to be called as
        a function:

            >>> print(q('{y + til x}', 10, 1))
            [ 1  2  3  4  5  6  7  8  9 10]


        :Parameters:
         - `query` (`string`) - query to be executed
         - `parameters` (`list` or `None`) - parameters for the query
        :Options:
         - `raw` (`boolean` or `None`) - if ``True`` returns raw data chunk instead of
           parsed data, if ``False`` returns parsed data, if ``None`` uses connection default.
           When set to a boolean, updates the connection's raw setting for this and future queries.
           **Default**: ``None``
         - `numpy_temporals` (`boolean`) - if ``False`` temporal vectors are
           backed by raw q representation (:class:`.QTemporalList`,
           :class:`.QTemporal`) instances, otherwise are represented as
           `numpy datetime64`/`timedelta64` arrays and atoms,
           **Default**: ``False``
         - `single_char_strings` (`boolean`) - if ``True`` single char Python
           strings are encoded as q strings instead of chars,
           **Default**: ``False``

        :returns: query result parsed to Python data structures

        :raises: :class:`.QConnectionException`, :class:`.QWriterException`,
                 :class:`.QReaderException`
        '''
        # Handle raw parameter specially - update connection options if specified
        if 'raw' in options and options['raw'] is not None:
            raw_value = options['raw']
            if isinstance(raw_value, bool):
                # Update connection options for this and future queries
                self._options.raw = raw_value
                if hasattr(self, '_reader') and self._reader and hasattr(self._reader, '_options'):
                    self._reader._options.raw = raw_value

        self.query(MessageType.SYNC, query, *parameters, **options)
        response = self.receive(data_only = False, **options)

        if response.type == MessageType.RESPONSE:
            return response.data
        else:
            self._writer.write(QException('nyi: qPython expected response message'), MessageType.ASYNC if response.type == MessageType.ASYNC else MessageType.RESPONSE)
            raise QReaderException('Received message of type: %s where response was expected')

    def sendSyncDetached(self, query, *parameters, **options):
        '''Sends a synchronous query without waiting for the response.

        Unlike sendAsync(), this generates a response from q which can be
        caught by a listener thread, along with any (neg .z.w) callbacks.

        :Parameters:
         - `query` (`string`) - query to be executed
         - `parameters` (`list` or `None`) - parameters for the query
        :Options:
         - `raw` (`boolean` or `None`) - if specified, updates the connection's raw setting
           for this and future queries. **Default**: ``None``
        '''
        # Handle raw parameter specially - update connection options if specified
        if 'raw' in options and options['raw'] is not None:
            raw_value = options['raw']
            if isinstance(raw_value, bool):
                # Update connection options for this and future queries
                self._options.raw = raw_value
                if hasattr(self, '_reader') and self._reader and hasattr(self._reader, '_options'):
                    self._reader._options.raw = raw_value

        self.query(MessageType.SYNC, query, *parameters, **options)
        
    def sendAsync(self, query, *parameters, **options):
        '''Performs an asynchronous query and returns **without** retrieving of
        the response.

        In typical use case, `query` is the name of the function to call and
        `parameters` are its parameters. When `parameters` list is empty, the
        query can be an arbitrary q expression (e.g. ``0 +/ til 100``).

        Calls a anonymous function with a single parameter:

            >>> q.sendAsync('{til x}', 10)

        Executes a q expression:

            >>> q.sendAsync('til 10')

        :Parameters:
         - `query` (`string`) - query to be executed
         - `parameters` (`list` or `None`) - parameters for the query
        :Options:
         - `raw` (`boolean` or `None`) - if specified, updates the connection's raw setting
           for this and future queries. **Default**: ``None``
         - `single_char_strings` (`boolean`) - if ``True`` single char Python
           strings are encoded as q strings instead of chars,
           **Default**: ``False``

        :raises: :class:`.QConnectionException`, :class:`.QWriterException`
        '''
        # Handle raw parameter specially - update connection options if specified
        if 'raw' in options and options['raw'] is not None:
            raw_value = options['raw']
            if isinstance(raw_value, bool):
                # Update connection options for this and future queries
                self._options.raw = raw_value
                if hasattr(self, '_reader') and self._reader and hasattr(self._reader, '_options'):
                    self._reader._options.raw = raw_value

        self.query(MessageType.ASYNC, query, *parameters, **options)


    def receive(self, data_only = True, **options):
        '''Reads and (optionally) parses the response from a q service.
        
        Retrieves query result along with meta-information:
        
            >>> q.query(qconnection.MessageType.SYNC,'{x}', 10)
            >>> print(q.receive(data_only = False, raw = False))
            QMessage: message type: 2, data size: 13, is_compressed: False, data: 10

        Retrieves parsed query result:

            >>> q.query(qconnection.MessageType.SYNC,'{x}', 10)
            >>> print(q.receive(data_only = True, raw = False))
            10

        Retrieves not-parsed (raw) query result:
        
            >>> from binascii import hexlify
            >>> q.query(qconnection.MessageType.SYNC,'{x}', 10)
            >>> print(hexlify(q.receive(data_only = True, raw = True)))
            fa0a000000
                
        :Parameters:
         - `data_only` (`boolean`) - if ``True`` returns only data part of the 
           message, otherwise returns data and message meta-information 
           encapsulated in :class:`.QMessage` instance 
        :Options:
         - `raw` (`boolean`) - if ``True`` returns raw data chunk instead of 
           parsed data, **Default**: ``False``
         - `numpy_temporals` (`boolean`) - if ``False`` temporal vectors are
           backed by raw q representation (:class:`.QTemporalList`, 
           :class:`.QTemporal`) instances, otherwise are represented as 
           `numpy datetime64`/`timedelta64` arrays and atoms,
           **Default**: ``False``
        
        :returns: depending on parameter flags: :class:`.QMessage` instance, 
                  parsed message, raw data 
        :raises: :class:`.QReaderException`
        '''
        result = self._reader.read(**self._options.union_dict(**options))
        return result.data if data_only else result


    def __call__(self, *parameters, **options):
        return self.sendSync(parameters[0], *parameters[1:], **options)

    def _safe_decode(self, data):
        """
        Safely decode bytes to string with UTF-8/Latin-1 fallback
        
        :returns: decoded string
        """
        if isinstance(data, bytes):
            try:
                return data.decode('utf-8')
            except UnicodeDecodeError:
                return data.decode('latin-1')  # Never fails
        else:
            return str(data)

    def query_with_console(self, *parameters, **options):
        """
        Execute query and return both console output and raw data.
        
        Prefixes the first parameter with {(.Q.s x; x)} to get both
        formatted console output and the actual data structure.
        
        :returns: tuple of (console_output_string, raw_data)
        """
        if not parameters:
            raise ValueError("query_with_console requires at least one parameter")
        
        try:
            # Clear any existing logs before running the query
            try:
                self.sendSync(".qython.delete_logs[]")
            except:
                # Silently ignore if .qython.delete_logs[] doesn't exist
                pass
            
            # Prefix the first parameter with the console output wrapper
            q_prefix = '''{v:$[`trp in key .Q; .Q.trp[{( (1b;`) ;value x)};x;{((0b;`);x;$[4<count y; .Q.sbt -4 _ y; \"\"])}]; ((1b;`);value x)]; a:99999>@[-22!;v;{0}]; (a;$[a;v;0b];.Q.s v 1)}'''
            #prefixed_query = f"{q_prefix} {parameters[0]}"
            #result = self.sendSync(prefixed_query, *parameters[1:], **options)
            result = self.sendSync(q_prefix, parameters[0])
            result = [str.__str__(result[2]), result[1][1]]
            # Handle None result or non-iterable result (like QLambda) - occurs with empty queries
            if result is None or not hasattr(result, '__iter__') or isinstance(result, str):
                return ("", result)
            # Handle None result[0] safely
            # Safely decode the console output
            return result
            
        except QException as e:
            # Q error occurred - extract and decode the actual error content
            if e.args and len(e.args) > 0:
                error_content = e.args[0]  # Extract the actual error bytes/content
                error_str = self._safe_decode(error_content)
            else:
                error_str = self._safe_decode(str(e))
            raise QException(f"Q Error: {error_str}")
        except Exception as e:
            # Print full traceback for debugging
            import traceback
            print(f"Exception in query_with_console: {e}")
            traceback.print_exc()
            raise


def parse_raw_bytes(raw_bytes):
    """
    Parse raw q bytes to Python structures with pandas support.

    Args:
        raw_bytes: Raw bytes from q server

    Returns:
        Parsed Python data structure
    """
    from .qreader import QReader
    from .qmetaconversion import MetaData, CONVERSION_OPTIONS
    from ._pandas import read_object_pandas

    # Create a temporary reader for parsing
    parser = QReader(None, encoding='latin-1')
    parser._options = MetaData(**CONVERSION_OPTIONS.union_dict(pandas=True))
    parser._is_native = True

    # Parse the raw bytes
    return read_object_pandas(parser, raw_bytes)
