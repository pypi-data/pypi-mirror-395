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

import os

import pandas
import struct
import sys
if sys.version > '3':
    basestring = (str, bytes)

from collections import OrderedDict

from .qmetaconversion import MetaData
from .qreader import QReader, QReaderException
from .qcollection import QDictionary, qlist
from .qwriter import QWriter, QWriterException
from .qtype import *



class PandasQReader(QReader):

    _reader_map = dict.copy(QReader._reader_map)
    parse = Mapper(_reader_map)

    @parse(QDICTIONARY)
    def _read_dictionary(self, qtype = QDICTIONARY):
        if self._options.pandas:
            keys = self._read_object()
            values = self._read_object()

            # Keyed table: BOTH keys and values must be DataFrames
            if isinstance(keys, pandas.DataFrame) and isinstance(values, pandas.DataFrame):
                indices = keys.columns
                table = keys
                table.meta = keys.meta
                table.meta.qtype = QKEYED_TABLE

                for column in values.columns:
                    table[column] = values[column]
                    table.meta[column] = values.meta[column]

                # Store key column names instead of creating MultiIndex to avoid sorting issues
                table.keys = list(indices)
                # table.set_index([column for column in indices], inplace = True)

                return table
            else:
                # Dictionary: any other combination (list→table, table→list, list→list, etc.)
                keys = keys if not isinstance(keys, pandas.Series) else keys.values
                values = values if not isinstance(values, pandas.Series) else values.values

                # Convert QList to plain list for easier handling
                from .qcollection import QList
                if isinstance(keys, QList):
                    keys = list(keys)
                if isinstance(values, QList):
                    values = list(values)

                # Check if keys or values are lists containing a single table
                keys_is_list = isinstance(keys, (list, tuple))
                values_is_list = isinstance(values, (list, tuple))
                keys_is_table = isinstance(keys, pandas.DataFrame)
                values_is_table = isinstance(values, pandas.DataFrame)

                # Unwrap single-element lists containing tables
                if keys_is_list and len(keys) == 1 and isinstance(keys[0], pandas.DataFrame):
                    keys = keys[0]
                    keys_is_table = True
                    keys_is_list = False

                if values_is_list and len(values) == 1 and isinstance(values[0], pandas.DataFrame):
                    values = values[0]
                    values_is_table = True
                    values_is_list = False

                # Special case: keys=list, values=table → make DataFrame with '' index
                if keys_is_list and values_is_table:
                    # Add keys as a column named '' and set it as index
                    result = values.copy()
                    result[''] = keys
                    result = result.set_index('')
                    return result

                # Special case: keys=table, values=list → make DataFrame with '' column
                elif keys_is_table and values_is_list:
                    # Add values as a column named ''
                    result = keys.copy()
                    result[''] = values
                    return result

                # General case: both are lists or other combinations → use dict
                else:
                    # When values is a single DataFrame (not a list of DataFrames),
                    # wrap it in a list so zip treats it as a single value
                    if isinstance(values, pandas.DataFrame):
                        values = [values]

                    def convert_string_to_char_list(data):
                        if isinstance(data, String):
                            return [Char(c) for c in data]
                        else:
                            return data

                    # Convert String keys/values to Char lists before creating dictionary
                    keys = convert_string_to_char_list(keys)
                    values = convert_string_to_char_list(values)

                    # Use regular dict (keys should be hashable in normal q dictionaries)
                    return dict(zip(keys, values))
        else:
            return QReader._read_dictionary(self, qtype = qtype)


    @parse(QTABLE)
    def _read_table(self, qtype = QTABLE):
        if self._options.pandas:
            self._buffer.skip()  # ignore attributes
            self._buffer.skip()  # ignore dict type stamp

            columns = self._read_object()
            self._buffer.skip() # ignore generic list type indicator
            data = QReader._read_general_list(self, qtype)

            odict = OrderedDict()
            meta = MetaData(qtype = QTABLE)
            for i in range(len(columns)):
                column_name = columns[i] if isinstance(columns[i], str) else columns[i].decode("utf-8")
                if isinstance(data[i], str):
                    if len(data[i]) == 1:
                        # Single character - treat as QCHAR, don't convert to list
                        meta[column_name] = QCHAR
                        odict[column_name] = pandas.Series([data[i]], dtype = str)
                    else:
                        # convert character list (represented as string) to numpy representation
                        meta[column_name] = QSTRING
                        char_list = [Char(c) for c in data[i]]
                        odict[column_name] = pandas.Series(char_list).replace(' ', numpy.nan)
                elif isinstance(data[i], bytes):
                    # convert character list (represented as string) to numpy representation
                    meta[column_name] = QSTRING
                    odict[column_name] = pandas.Series(list(data[i].decode()), dtype = str).replace(' ', numpy.nan)
                elif hasattr(data[i], 'meta') and data[i].meta.qtype == QSYMBOL_LIST:
                    # Handle symbol lists - decode bytes to plain strings
                    meta[column_name] = QSYMBOL
                    decoded_symbols = []
                    for symbol in data[i]:
                        if hasattr(symbol, 'decode'):
                            decoded_symbols.append(symbol.decode('utf-8'))
                        else:
                            decoded_symbols.append(str(symbol))
                    odict[column_name] = pandas.Series(decoded_symbols)
                elif isinstance(data[i], (list, tuple)):
                    meta[column_name] = QGENERAL_LIST
                    tarray = numpy.ndarray(shape = len(data[i]), dtype = numpy.dtype('O'))
                    for j in range(len(data[i])):
                        tarray[j] = data[i][j]
                    odict[column_name] = tarray
                else:
                    meta[column_name] = data[i].meta.qtype
                    odict[column_name] = data[i]

            df = pandas.DataFrame(odict)
            df._metadata = ["meta"]
            df.meta = meta
            return df
        else:
            return QReader._read_table(self, qtype = qtype)


    def _read_list(self, qtype):
        if self._options.pandas:
            self._options.numpy_temporals = True

        qlist_data = QReader._read_list(self, qtype = qtype)

        if self._options.pandas:
            # For integer types, return original qlist_data to preserve QInteger objects
            if qtype in [QBYTE_LIST, QSHORT_LIST, QINT_LIST, QLONG_LIST]:
                return qlist_data
            # For boolean types, return original qlist_data to preserve QList with bool dtype
            elif qtype == QBOOL_LIST:
                return qlist_data
            # For temporal types, return original qlist_data to preserve QTemporal objects
            elif qtype in [QMONTH_LIST, QDATE_LIST, QDATETIME_LIST, QTIMESPAN_LIST,
                          QMINUTE_LIST, QSECOND_LIST, QTIME_LIST, QTIMESTAMP_LIST]:
                return qlist_data
            # For float types, return original qlist_data to preserve float64 dtype
            elif qtype in [QFLOAT_LIST, QDOUBLE_LIST]:
                return qlist_data
            # For symbol types, DON'T return early - we need to decode bytes to strings below

            # Handle string types like in dataframe path
            processed_data = qlist_data
            if qtype == QSTRING:
                # String list - convert to Char objects for each character
                if isinstance(qlist_data, str):
                    processed_data = [Char(c) for c in qlist_data]
                elif isinstance(qlist_data, bytes):
                    processed_data = [Char(c) for c in qlist_data.decode()]
                else:
                    # Handle array-like qlist_data
                    if hasattr(qlist_data, '__iter__'):
                        processed_data = []
                        for item in qlist_data:
                            if isinstance(item, str):
                                processed_data.extend([Char(c) for c in item])
                            elif isinstance(item, bytes):
                                processed_data.extend([Char(c) for c in item.decode()])
                            else:
                                processed_data.append(item)
            elif qtype == QSYMBOL_LIST and hasattr(qlist_data, '__iter__'):
                # Handle symbol lists - decode bytes to plain strings but preserve QList metadata
                processed_data = []
                for symbol in qlist_data:
                    if hasattr(symbol, 'decode'):
                        processed_data.append(symbol.decode('utf-8'))
                    else:
                        processed_data.append(str(symbol))

                # Create a QList with decoded strings and preserve metadata
                decoded_qlist = qlist(numpy.array(processed_data, dtype=object), qtype=QSYMBOL_LIST, adjust_dtype=False)
                return decoded_qlist

            # For other types, use original behavior (convert to list)
            if -abs(qtype) not in [QBOOL, QMONTH, QDATE, QDATETIME, QMINUTE, QSECOND, QTIME, QTIMESTAMP, QTIMESPAN, QSYMBOL]:
                null = QNULLMAP[-abs(qtype)][1]
                ps = list(pandas.Series(data = processed_data).replace(null, numpy.nan))
            else:
                ps = list(pandas.Series(data = processed_data))
            return ps
        else:
            return qlist_data


    @parse(QGENERAL_LIST)
    def _read_general_list(self, qtype = QGENERAL_LIST):
        qlist = QReader._read_general_list(self, qtype)
        if self._options.pandas:
            return [numpy.nan if isinstance(element, basestring) and element == b' ' else element for element in qlist]
        else:
            return qlist


def read_object_pandas(reader, raw_data):
    """
    Parse q raw data using pandas-enabled reader
    
    Args:
        reader: QReader instance with pandas options
        raw_data: Raw bytes from q server
        
    Returns:
        Parsed Python data structures with pandas support
    """
    # Create a temporary PandasQReader with the same stream as original
    pandas_reader = PandasQReader(reader._stream, encoding=reader._encoding)
    pandas_reader._options = reader._options
    pandas_reader._buffer.wrap(raw_data)  # Create fresh buffer with raw data
    
    # Copy _is_native attribute from the original reader (which already read the header)
    pandas_reader._is_native = reader._is_native
    
    return pandas_reader._read_object()


class PandasQWriter(QWriter):

    _writer_map = dict.copy(QWriter._writer_map)
    serialize = Mapper(_writer_map)


    @serialize(pandas.Series)
    def _write_pandas_series(self, data, qtype = None):
        if qtype is not None:
            qtype = -abs(qtype)

        if qtype is None and hasattr(data, 'meta'):
            qtype = -abs(data.meta.qtype)

        if data.dtype == '|S1':
            qtype = QCHAR

        if qtype is None:
            qtype = Q_TYPE.get(data.dtype.type, None)

        if qtype is None and data.dtype.type in (numpy.datetime64, numpy.timedelta64):
            qtype = TEMPORAL_PY_TYPE.get(str(data.dtype), None)

        if qtype is None:
            # determinate type based on first element of the numpy array
            qtype = Q_TYPE.get(type(data.iloc[0]), QGENERAL_LIST)

            if qtype == QSTRING:
                # assume we have a generic list of strings -> force representation as symbol list
                qtype = QSYMBOL

        if qtype is None:
            raise QWriterException('Unable to serialize pandas series %s' % data)

        if qtype == QGENERAL_LIST:
            self._write_generic_list(data.values)
        elif qtype == QCHAR:
            self._write_string(data.replace(numpy.nan, ' ').values.astype(numpy.bytes_).tobytes())
        elif data.dtype.type not in (numpy.datetime64, numpy.timedelta64):
            data = data.fillna(QNULLMAP[-abs(qtype)][1])
            data = data.values

            if PY_TYPE[qtype] != data.dtype:
                data = data.astype(PY_TYPE[qtype])

            self._write_list(data, qtype = qtype)
        else:
            data = data.values
            data = data.astype(TEMPORAL_Q_TYPE[qtype])
            self._write_list(data, qtype = qtype)


    @serialize(pandas.DataFrame)
    def _write_pandas_data_frame(self, data, qtype = None):
        data_columns = data.columns.values

        if hasattr(data, 'meta') and data.meta.qtype == QKEYED_TABLE:
            # data frame represents keyed table
            self._buffer.write(struct.pack('=b', QDICTIONARY))
            self._buffer.write(struct.pack('=bxb', QTABLE, QDICTIONARY))
            index_columns = data.index.names
            self._write(qlist(numpy.array(index_columns), qtype = QSYMBOL_LIST))
            data.reset_index(inplace = True)
            self._buffer.write(struct.pack('=bxi', QGENERAL_LIST, len(index_columns)))
            for column in index_columns:
                self._write_pandas_series(data[column], qtype = data.meta[column] if hasattr(data, 'meta') else None)

            data.set_index(index_columns, inplace = True)

        self._buffer.write(struct.pack('=bxb', QTABLE, QDICTIONARY))
        self._write(qlist(numpy.array(data_columns), qtype = QSYMBOL_LIST))
        self._buffer.write(struct.pack('=bxi', QGENERAL_LIST, len(data_columns)))
        for column in data_columns:
            self._write_pandas_series(data[column], qtype = data.meta[column] if hasattr(data, 'meta') else None)


    @serialize(tuple, list)
    def _write_generic_list(self, data):
        if self._options.pandas:
            self._buffer.write(struct.pack('=bxi', QGENERAL_LIST, len(data)))
            for element in data:
                # assume nan represents a string null
                self._write(' ' if type(element) in [float, numpy.float32, numpy.float64] and numpy.isnan(element) else element)
        else:
            QWriter._write_generic_list(self, data)
