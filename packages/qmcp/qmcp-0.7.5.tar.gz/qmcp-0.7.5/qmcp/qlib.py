"""
Q/kdb+ connection utilities for qmcp
Clean, minimal interface for connecting to and querying q servers
"""

from .qpython.qconnection import QConnection
from .qpython.qmetaconversion import MetaData
from .qpython.qtype import Char, String
import os
import time
import socket
from sugar import dmap, spl
import pandas as pd
import numpy as np


def _get_hostname():
    """Get current hostname"""
    return socket.gethostname()


class _QDecodeWrapper:
    """Wrapper for QConnection that handles pandas DataFrame encoding/decoding"""
    
    def __init__(self, q):
        self.q = q
        
    def decode(self, result):
        """
        Decode q types in pandas DataFrame results and iterables with type preservation
        
        Args:
            result: Result from q query (DataFrame, dict, list, etc.)
            
        Returns:
            Result with q types properly wrapped (Char/String) or preserved (symbols)
        """
        return result
        # Handle pandas DataFrames with meta information
        if type(result) == pd.DataFrame:
            rd = result.meta.as_dict()
            
            # Handle regular columns
            for col in rd:
                qtype = rd[col]
                if qtype in (0, 10, 11) and col in result.columns:  # string, char, or symbol columns
                    try:
                        if qtype == 0:  # string
                            result[col] = result[col].map(dmap(lambda x: String(x), result[col].drop_duplicates()))
                        elif qtype == 10:  # char  
                            result[col] = result[col].map(dmap(lambda x: Char(x), result[col].drop_duplicates()))
                        elif qtype == 11:  # symbol: decode bytes to plain strings
                            result[col] = result[col].map(dmap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x, result[col].drop_duplicates()))
                    except:
                        pass
            
            # Handle simple index
            for col in rd:
                qtype = rd[col]
                if qtype in (0, 10, 11) and result.index.name == col and hasattr(result.index, '__iter__'):
                    try:
                        if qtype == 0:  # string
                            decoded_index = [String(x) for x in result.index]
                            result.index = pd.Index(decoded_index, name=result.index.name)
                        elif qtype == 10:  # char
                            decoded_index = [Char(x) for x in result.index]
                            result.index = pd.Index(decoded_index, name=result.index.name)
                        elif qtype == 11:  # symbol: decode bytes to plain strings
                            decoded_index = [x.decode('utf-8') if isinstance(x, bytes) else x for x in result.index]
                            result.index = pd.Index(decoded_index, name=result.index.name)
                    except:
                        pass
            
            # Handle MultiIndex
            if isinstance(result.index, pd.MultiIndex):
                try:
                    new_levels = []
                    for i, level in enumerate(result.index.levels):
                        level_name = result.index.names[i]
                        if level_name in rd:
                            qtype = rd[level_name]
                            if qtype == 0:  # string
                                try:
                                    decoded_level = [String(x) for x in level]
                                    new_levels.append(pd.Index(decoded_level))
                                except:
                                    new_levels.append(level)
                            elif qtype == 10:  # char
                                try:
                                    decoded_level = [Char(x) for x in level]
                                    new_levels.append(pd.Index(decoded_level))
                                except:
                                    new_levels.append(level)
                            elif qtype == 11:  # symbol: decode bytes to plain strings
                                try:
                                    decoded_level = [x.decode('utf-8') if isinstance(x, bytes) else x for x in level]
                                    new_levels.append(pd.Index(decoded_level))
                                except:
                                    new_levels.append(level)
                            else:  # other types: keep as-is
                                new_levels.append(level)
                        else:
                            new_levels.append(level)
                    
                    # Reconstruct MultiIndex with type-wrapped levels
                    result.index = pd.MultiIndex(
                        levels=new_levels,
                        codes=result.index.codes,
                        names=result.index.names
                    )
                except:
                    pass
        
        # Handle iterables (lists, tuples, etc.) - decode bytes to strings recursively
        elif hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
            try:
                if isinstance(result, dict):
                    # Recursively decode dictionary values
                    return {k: self.decode(v) for k, v in result.items()}
                else:
                    # Handle lists, tuples, etc.
                    decoded_items = []
                    for item in result:
                        if isinstance(item, bytes):
                            # Decode bytes to plain strings (no type wrapper for generic lists)
                            decoded_items.append(item.decode('utf-8'))
                        else:
                            # Recursively decode nested structures
                            decoded_items.append(self.decode(item))
                    
                    # Return same type as input (list, tuple, etc.)
                    return type(result)(decoded_items)
            except:
                pass
                    
        return result

    def __call__(self, *args, **kwargs):
        # Handle DataFrame arguments
        for arg in args:
            if isinstance(arg, pd.DataFrame):
                if not hasattr(arg, 'meta'):
                    arg.meta = MetaData(qtype=98)
                    
                # Set date column metadata
                for c in 'd, date'-spl:
                    if (c in arg.columns and 
                        isinstance(arg[c].dtype, np.dtype) and 
                        arg[c].dtype != np.dtype(np.object_) and
                        c not in arg.meta.__dict__):
                        arg.meta[c] = 14
                        
                # Handle string columns
                if 'strcols' in kwargs:
                    for sc in kwargs['strcols']-spl:
                        arg.meta[sc] = 0
                        
        # Execute query
        r = self.q(*args, **kwargs)
        
        # Decode using the factored out method
        return self.decode(r)


def connect_to_q(connection_string, connection_timeout=5):
    """
    Connect to q server using a connection string

    Args:
        connection_string: Connection string in format 'host:port' or 'host:port:user:password'
        connection_timeout: seconds to wait for connection (default 5)

    Returns:
        _QDecodeWrapper instance

    Note: Connection logic and config management is handled by qcomms.connect_to_q,
          which calls this function with a fully-formed connection string.
    """
    if not connection_string:
        raise ValueError("Connection string required")

    return _qConnect(str(connection_string), pandas=True, connection_timeout=connection_timeout)


def _qConnect(qCredentials, pandas, connection_timeout=5):
    """
    Connect to q server with socket timeout
    
    Args:
        qCredentials: 'host:port' or 'host:port:user:passwd'
        pandas: return pandas-enabled connection
        connection_timeout: socket timeout in seconds
        
    Returns:
        QConnection or _QDecodeWrapper
    """
    qCreds = tuple(qCredentials.split(':'))
    host, port, user, passwd = qCreds if len(qCreds) == 4 else (qCreds + (None, None))
    port = int(port)
    
    if host == _get_hostname():
        host = 'localhost'
        
    # Create connection with socket timeout
    q = QConnection(host, port, user, passwd, pandas=pandas)
    
    # Set socket timeout before opening connection
    import socket
    original_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(connection_timeout)
    
    try:
        q.open()
        return _QDecodeWrapper(q) if pandas else q
    finally:
        # Restore original socket timeout
        socket.setdefaulttimeout(original_timeout)