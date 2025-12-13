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

'''
The `qpython.qtypes` module provides custom integer types that properly display
q's special values (null and infinity) as NaN/inf instead of raw sentinel values.

This module complements qtype.py by providing user-friendly wrappers for q integer types.
'''

import pandas as pd
import numpy
import datetime
from typing import Union

# Standard C integer limit constants (for LLM comprehension)
# These match C99 stdint.h constants and are widely recognized by LLMs
# Note: These are NOT the same as q constants - q uses different naming (0Ni, 0Wi, etc.)
# But using C standard names makes the code much more comprehensible to LLMs
INT8_MIN = -128
INT8_MAX = 127
INT16_MIN = -32768
INT16_MAX = 32767
INT32_MIN = -2147483648
INT32_MAX = 2147483647
INT64_MIN = -9223372036854775808
INT64_MAX = 9223372036854775807


class QInteger:
    """Base class for q integer types with special value display.
    
    q uses specific integer values as sentinels for special meanings:
    - Most negative value: null (0Ni, 0Nh, 0Nj, 0Nb)
    - Most positive value: positive infinity (0Wi, 0Wh, 0Wj, 0Wb)
    - Most positive - 1: negative infinity (-0Wi, -0Wh, -0Wj, -0Wb)
    
    This class displays these sentinel values as NaN/inf for better user experience.
    """
    
    # Define special value patterns for each bit size
    # Based on actual q behavior:
    # - int8 (byte): no special values
    # - int16 (short): only null 
    # - int32 (int): null, pos_inf, neg_inf
    # - int64 (long): null, pos_inf, neg_inf
    #
    # Mapping between C constants and q special values:
    # - C_MAX = q positive infinity (0Wi, 0Wj)
    # - C_MIN = q null (0Ni, 0Nj) 
    # - C_MIN + 1 = q negative infinity (-0Wi, -0Wj)
    _SPECIAL_VALUES = {
        8:  {},  # No special values for byte
        16: {'null': INT16_MIN},  # Only null for short
        32: {'null': INT32_MIN, 'pos_inf': INT32_MAX, 'neg_inf': INT32_MIN + 1},
        64: {'null': INT64_MIN, 'pos_inf': INT64_MAX, 'neg_inf': INT64_MIN + 1}
    }
    
    def __init__(self, value, bit_size=32):
        """Initialize a q integer with specified bit size.
        
        Args:
            value: Integer value (can be regular int or special sentinel)
            bit_size: Size in bits (8, 16, 32, or 64)
        """
        if bit_size not in self._SPECIAL_VALUES:
            raise ValueError(f"Unsupported bit size: {bit_size}. Must be one of {list(self._SPECIAL_VALUES.keys())}")
            
        self._value = int(value) if value is not None else None
        self._bit_size = bit_size
        self._specials = self._SPECIAL_VALUES[bit_size]
        
        # Set type name for display
        type_names = {8: 'QInt8', 16: 'QInt16', 32: 'QInt32', 64: 'QInt64'}
        self._type_name = type_names[bit_size]
    
    @property
    def value(self):
        """Get the underlying integer value."""
        return self._value
    
    @property 
    def bit_size(self):
        """Get the bit size of this integer type."""
        return self._bit_size
    
    def __str__(self):
        """Display special values using C constants for LLM comprehension."""
        if 'null' in self._specials and self._value == self._specials['null']:
            return "nan"
        elif 'pos_inf' in self._specials and self._value == self._specials['pos_inf']:
            # Show as INT32_MAX, INT64_MAX etc for LLM understanding
            return f"INT{self._bit_size}_MAX"
        elif 'neg_inf' in self._specials and self._value == self._specials['neg_inf']:
            return f"INT{self._bit_size}_MIN"
        else:
            return str(self._value)
    
    def __repr__(self):
        """Repr shows the type and C constant names for LLM comprehension."""
        if 'null' in self._specials and self._value == self._specials['null']:
            return f"{self._type_name}(nan)"
        elif 'pos_inf' in self._specials and self._value == self._specials['pos_inf']:
            return f"{self._type_name}(INT{self._bit_size}_MAX)"
        elif 'neg_inf' in self._specials and self._value == self._specials['neg_inf']:
            return f"{self._type_name}(INT{self._bit_size}_MIN)"
        else:
            return f"{self._type_name}({self._value})"
    
    def __eq__(self, other):
        """Compare with other QInteger or regular integer."""
        if isinstance(other, QInteger):
            return self._value == other._value
        return self._value == other
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self._value)
    
    def is_null(self):
        """Check if this value represents null (0N)."""
        return 'null' in self._specials and self._value == self._specials['null']
    
    def is_inf(self):
        """Check if this value represents infinity (0W or -0W)."""
        return (('pos_inf' in self._specials and self._value == self._specials['pos_inf']) or 
                ('neg_inf' in self._specials and self._value == self._specials['neg_inf']))
    
    def is_pos_inf(self):
        """Check if this value represents positive infinity (0W)."""
        return 'pos_inf' in self._specials and self._value == self._specials['pos_inf']
    
    def is_neg_inf(self):
        """Check if this value represents negative infinity (-0W)."""
        return 'neg_inf' in self._specials and self._value == self._specials['neg_inf']
    
    def is_finite(self):
        """Check if this value is finite (not null or infinity)."""
        return not (self.is_null() or self.is_inf())
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """Handle numpy universal functions like np.isnan, np.isinf for pandas compatibility."""
        if ufunc is numpy.isnan and method == '__call__':
            # For np.isnan(), return True if this is a null value
            return self.is_null()
        elif ufunc is numpy.isinf and method == '__call__':
            # For np.isinf(), return True if this is an infinity value
            return self.is_inf()
        elif ufunc is numpy.isfinite and method == '__call__':
            # For np.isfinite(), return True if this is finite
            return self.is_finite()
        else:
            # For other ufuncs, try to convert to regular int and apply the function
            try:
                return ufunc(int(self._value), **kwargs)
            except:
                # If that fails, return NotImplemented to let numpy handle it
                return NotImplemented


class QInt8(QInteger):
    """q byte type (8-bit integer) with special value display."""
    
    def __init__(self, value):
        super().__init__(value, 8)


class QInt16(QInteger):
    """q short type (16-bit integer) with special value display."""
    
    def __init__(self, value):
        super().__init__(value, 16)


class QInt32(QInteger):
    """q int type (32-bit integer) with special value display."""
    
    def __init__(self, value):
        super().__init__(value, 32)


class QInt64(QInteger):
    """q long type (64-bit integer) with special value display."""
    
    def __init__(self, value):
        super().__init__(value, 64)


# Custom dtypes for pandas display
class QIntegerDtype:
    """Base class for custom integer dtypes that display nicely in pandas"""
    
    def __init__(self, name, base_dtype):
        self.name = name
        self._base = numpy.dtype(base_dtype)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    # Delegate all other attributes to base dtype
    def __getattr__(self, name):
        return getattr(self._base, name)


class QInt8Dtype(QIntegerDtype):
    def __init__(self):
        super().__init__('int8', numpy.int8)


class QInt16Dtype(QIntegerDtype):
    def __init__(self):
        super().__init__('int16', numpy.int16)


class QInt32Dtype(QIntegerDtype):
    def __init__(self):
        super().__init__('int32', numpy.int32)


class QInt64Dtype(QIntegerDtype):
    def __init__(self):
        super().__init__('int64', numpy.int64)


# Conversion utilities for pandas integration

def qinteger_array_to_pandas(qint_array):
    """Convert array of QInteger objects to pandas nullable integer Series.
    
    Args:
        qint_array: List/array of QInteger objects
        
    Returns:
        pandas Series with nullable integer dtype, using pd.NA for nulls
    """
    if not qint_array:
        return pd.Series([], dtype="Int32")
    
    # Determine pandas dtype from first non-null element
    bit_size = qint_array[0].bit_size
    dtype_map = {8: "Int8", 16: "Int16", 32: "Int32", 64: "Int64"}
    pandas_dtype = dtype_map[bit_size]
    
    values = []
    for item in qint_array:
        if not isinstance(item, QInteger):
            raise TypeError(f"Expected QInteger, got {type(item)}")
        if item.bit_size != bit_size:
            raise ValueError("All QInteger objects must have same bit size")
            
        if item.is_null():
            values.append(pd.NA)
        else:
            values.append(item.value)
    
    return pd.Series(values, dtype=pandas_dtype)


def pandas_to_qinteger_array(series, qint_type=QInt32):
    """Convert pandas nullable integer Series to array of QInteger objects.
    
    Args:
        series: pandas Series with nullable integer data
        qint_type: QInteger class to use (QInt8, QInt16, QInt32, QInt64)
        
    Returns:
        List of QInteger objects with appropriate null sentinels
    """
    result = []
    for val in series:
        if pd.isna(val):
            # Create null value using appropriate sentinel
            null_sentinel = qint_type._SPECIAL_VALUES[qint_type(0).bit_size]['null'] 
            result.append(qint_type(null_sentinel))
        else:
            result.append(qint_type(val))
    
    return result


def create_qinteger(value, bit_size):
    """Factory function to create appropriate QInteger subclass.
    
    Args:
        value: Integer value
        bit_size: Bit size (8, 16, 32, or 64)
        
    Returns:
        Appropriate QInteger subclass instance
    """
    class_map = {8: QInt8, 16: QInt16, 32: QInt32, 64: QInt64}
    if bit_size not in class_map:
        raise ValueError(f"Unsupported bit size: {bit_size}")
    
    return class_map[bit_size](value)


# q-style arithmetic operations (optional - for future enhancement)

def q_add(a, b):
    """Addition following q's integer overflow semantics.
    
    In q, integer arithmetic with overflow wraps to special values:
    - Overflow beyond max positive → null  
    - Underflow below min negative → positive infinity
    - null + anything → null
    - infinity + anything → infinity (with appropriate sign rules)
    """
    if not isinstance(a, QInteger) or not isinstance(b, QInteger):
        raise TypeError("Both operands must be QInteger types")
    
    if a.bit_size != b.bit_size:
        raise TypeError("Operands must have same bit size")
    
    # Handle special values first
    if a.is_null() or b.is_null():
        return type(a)(a._specials['null'])  # null + anything = null
    
    # For now, just do regular arithmetic - could enhance with q overflow rules
    result_value = a.value + b.value
    return type(a)(result_value)


# ============================================================================
# Temporal wrapper classes for q temporal types
# ============================================================================


class QTemporal:
    """Base class for q temporal types with null/infinity display.
    
    q temporal types use special values for null and infinity:
    - null: 0Nd, 0Nm, 0Nt, etc. (usually minimum integer value)
    - infinity: 0Wd, 0Wm, 0Wt, etc. (usually maximum integer value)
    
    This class displays these sentinel values as NaT (Not-a-Time) for better user experience.
    The suffix indicates what unit arithmetic operates on (day, month, minute, second, ms, ns).
    """
    
    def __init__(self, raw_value, qtype, display_name, storage_size=32):
        """Initialize a q temporal with raw value and type info.
        
        Args:
            raw_value: The underlying value (could be integer, datetime, timedelta, etc.)
            qtype: q type number (13, 14, 15, 16, 17, 18, 19)
            display_name: Human-readable type name (e.g., "date_day", "time_ms")
            storage_size: Storage size in bits (32 or 64) for null/infinity detection
        """
        self._raw_value = raw_value
        self._qtype = qtype
        self._display_name = display_name
        self._storage_size = storage_size
    
    @property
    def raw(self):
        """Get the underlying raw value."""
        return self._raw_value
    
    @property
    def qtype(self):
        """Get the q type number."""
        return self._qtype
    
    def is_null(self):
        """Check if this value represents null (0N)."""
        # For integer-based temporal types, check for specific sentinel values
        if hasattr(self, '_storage_size') and self._storage_size is not None:
            if self._storage_size == 32:
                return isinstance(self._raw_value, int) and self._raw_value == INT32_MIN
            elif self._storage_size == 64:
                return isinstance(self._raw_value, int) and self._raw_value == INT64_MIN
        
        # For float-based temporal types (datetime), use NaN checking
        import math
        if isinstance(self._raw_value, float):
            return math.isnan(self._raw_value)
        
        # Check if it's pandas NaT or numpy NaT
        if hasattr(self._raw_value, '__class__'):
            if 'NaT' in str(self._raw_value):
                return True
        return pd.isna(self._raw_value)
    
    def is_inf(self):
        """Check if this value represents infinity (0W)."""
        # For temporal types, infinity is stored as INT32_MAX or INT64_MAX
        # depending on the temporal type's storage size
        if hasattr(self, '_storage_size'):
            if self._storage_size == 32:
                return (isinstance(self._raw_value, int) and 
                       (self._raw_value == INT32_MAX or self._raw_value == INT32_MIN + 1))
            elif self._storage_size == 64:
                return (isinstance(self._raw_value, int) and 
                       (self._raw_value == INT64_MAX or self._raw_value == INT64_MIN + 1))
        
        # Fallback for non-integer raw values
        try:
            if hasattr(self._raw_value, 'year'):
                return abs(self._raw_value.year) > 100000
            elif hasattr(self._raw_value, 'total_seconds'):
                return abs(self._raw_value.total_seconds()) > 1e15
            elif isinstance(self._raw_value, (int, float)):
                return abs(self._raw_value) > 1e15
        except:
            pass
        return False
    
    def is_pos_inf(self):
        """Check if this value represents positive infinity (0W)."""
        if hasattr(self, '_storage_size'):
            if self._storage_size == 32:
                return isinstance(self._raw_value, int) and self._raw_value == INT32_MAX
            elif self._storage_size == 64:
                return isinstance(self._raw_value, int) and self._raw_value == INT64_MAX
        return False
    
    def is_neg_inf(self):
        """Check if this value represents negative infinity (-0W)."""
        if hasattr(self, '_storage_size'):
            if self._storage_size == 32:
                return isinstance(self._raw_value, int) and self._raw_value == INT32_MIN + 1
            elif self._storage_size == 64:
                return isinstance(self._raw_value, int) and self._raw_value == INT64_MIN + 1
        return False
    
    def is_finite(self):
        """Check if this value is finite (not null or infinity)."""
        return not (self.is_null() or self.is_inf())
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """Handle numpy universal functions like np.isnan, np.isinf for pandas compatibility."""
        if ufunc is numpy.isnan and method == '__call__':
            return self.is_null()
        elif ufunc is numpy.isinf and method == '__call__':
            return self.is_inf()
        elif ufunc is numpy.isfinite and method == '__call__':
            return self.is_finite()
        else:
            # For other ufuncs, return NotImplemented to let numpy handle it
            return NotImplemented
    
    def __str__(self):
        """Display temporal values, showing NaT for null and infinity appropriately."""
        # Get special value strings from class-specific config
        special_values = TEMPORAL_SPECIAL_VALUES.get(self.__class__, {
            'nan': 'NaT',
            'posinf': f"INT{self._storage_size}_MAX",
            'neginf': f"INT{self._storage_size}_MIN"
        })
        
        if self.is_null():
            return special_values['nan']
        elif self.is_pos_inf():
            return special_values['posinf']
        elif self.is_neg_inf():
            return special_values['neginf']
        return self._format_value()
    
    def _format_value(self):
        """Format the temporal value for display. Override in subclasses."""
        return str(self._raw_value)
    
    def __repr__(self):
        """Repr shows clean class name with semantic string value."""
        # Get class name from dictionary, fallback to removing Q prefix
        config = TEMPORAL_SPECIAL_VALUES.get(self.__class__, {})
        class_name = config.get('repr_class', self.__class__.__name__[1:])
        str_value = str(self)
        
        # Special handling for datetime types with separate date/time components
        if class_name in ['DatetimeFloat', 'DateTimeNS'] and 'T' in str_value and str_value != 'NaT':
            date_part, time_part = str_value.split('T')
            return f'{class_name}("{date_part}", "{time_part}")'
        
        return f'{class_name}("{str_value}")'
    
    def __eq__(self, other):
        """Compare with other QTemporal or raw value."""
        if isinstance(other, QTemporal):
            return self._raw_value == other._raw_value
        return self._raw_value == other
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        try:
            return hash(self._raw_value)
        except:
            return hash(str(self._raw_value))


class QDateDay(QTemporal):
    """q date type (qtype 14): 2000.01.01 (days from epoch)
    
    Arithmetic operates on days: adding 1 adds 1 day.
    Storage: INT32 (null=INT32_MIN, inf=INT32_MAX/-INT32_MIN+1)
    """
    
    def __init__(self, raw_value):
        self._raw_int = raw_value  # Store for null/infinity checks
        # Convert raw integer to proper datetime64 using existing qtemporal conversion  
        converted_value = self._convert_raw_to_datetime(raw_value)
        super().__init__(converted_value, 14, "date_day", storage_size=32)
    
    def _convert_raw_to_datetime(self, raw_value):
        """Convert raw q date to numpy datetime64"""
        # Use the same logic as qtemporal._from_qdate
        if raw_value == INT32_MIN:  # null
            return numpy.datetime64('NaT', 'D')
        elif raw_value == INT32_MAX or raw_value == INT32_MIN + 1:  # infinity  
            return raw_value  # Keep as int for special handling
        else:
            # q date epoch is 2000-01-01
            epoch_date = numpy.datetime64('2000-01-01', 'D') 
            return epoch_date + numpy.timedelta64(int(raw_value), 'D')
    
    def is_null(self):
        """Override to check raw integer value"""
        return self._raw_int == INT32_MIN
    
    def is_pos_inf(self):
        """Override to check raw integer value"""
        return self._raw_int == INT32_MAX
    
    def is_neg_inf(self):
        """Override to check raw integer value"""
        return self._raw_int == INT32_MIN + 1
    
    def _format_value(self):
        """Format date as YYYY-MM-DD for clarity."""
        if hasattr(self._raw_value, 'strftime'):
            return self._raw_value.strftime('%Y-%m-%d')
        elif isinstance(self._raw_value, numpy.datetime64):
            # Convert numpy.datetime64 to pandas Timestamp for strftime
            import pandas as pd
            timestamp = pd.Timestamp(self._raw_value)
            return timestamp.strftime('%Y-%m-%d')
        return str(self._raw_value)


class QDateMonth(QTemporal):
    """q month type (qtype 13): 2000.01m (months from epoch)
    
    Arithmetic operates on months: adding 1 adds 1 month.
    """
    
    def __init__(self, raw_value):
        self._raw_int = raw_value  # Store for null/infinity checks
        converted_value = self._convert_raw_to_datetime(raw_value)
        super().__init__(converted_value, 13, "date_month", storage_size=32)
    
    def _convert_raw_to_datetime(self, raw_value):
        """Convert raw q month to numpy datetime64"""
        # Use the same logic as qtemporal._from_qmonth
        if raw_value == INT32_MIN:  # null
            return numpy.datetime64('NaT', 'M')
        elif raw_value == INT32_MAX or raw_value == INT32_MIN + 1:  # infinity  
            return raw_value  # Keep as int for special handling
        else:
            # q month epoch is 2000-01
            epoch_month = numpy.datetime64('2000-01', 'M')
            return epoch_month + numpy.timedelta64(int(raw_value), 'M')
    
    def is_null(self):
        """Override to check raw integer value"""
        return self._raw_int == INT32_MIN
    
    def is_pos_inf(self):
        """Override to check raw integer value"""
        return self._raw_int == INT32_MAX
    
    def is_neg_inf(self):
        """Override to check raw integer value"""
        return self._raw_int == INT32_MIN + 1
    
    def _format_value(self):
        """Format month as 'Jan 2000' for human-friendly display."""
        if hasattr(self._raw_value, 'strftime'):
            return self._raw_value.strftime('%b %Y')
        elif isinstance(self._raw_value, numpy.datetime64):
            # Convert numpy.datetime64 to pandas Timestamp for strftime
            import pandas as pd
            timestamp = pd.Timestamp(self._raw_value)
            return timestamp.strftime('%b %Y')
        return str(self._raw_value)


class QTimeMinute(QTemporal):
    """q minute type (qtype 17): 09:30 (minutes from midnight)
    
    Arithmetic operates on minutes: adding 1 adds 1 minute.
    """
    
    def __init__(self, raw_value):
        super().__init__(raw_value, 17, "time_minute", storage_size=32)
    
    def __str__(self):
        if self.is_null() or self.is_inf():
            return super().__str__()
        # Format as HH:MM
        if hasattr(self._raw_value, 'total_seconds'):
            # Convert timedelta to minutes and format
            total_minutes = int(self._raw_value.total_seconds() / 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return f"{hours:02d}:{minutes:02d}"
        elif isinstance(self._raw_value, int):
            # If it's raw minutes from midnight
            hours = self._raw_value // 60
            minutes = self._raw_value % 60
            return f"{hours:02d}:{minutes:02d}"
        return str(self._raw_value)


class QTimeSecond(QTemporal):
    """q second type (qtype 18): 09:30:15 (seconds from midnight)
    
    Arithmetic operates on seconds: adding 1 adds 1 second.
    """
    
    def __init__(self, raw_value):
        super().__init__(raw_value, 18, "time_second", storage_size=32)
    
    def __str__(self):
        if self.is_null() or self.is_inf():
            return super().__str__()
        # Format as HH:MM:SS
        if hasattr(self._raw_value, 'total_seconds'):
            total_seconds = int(self._raw_value.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        elif isinstance(self._raw_value, int):
            # If it's raw seconds from midnight
            hours = self._raw_value // 3600
            minutes = (self._raw_value % 3600) // 60
            seconds = self._raw_value % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return str(self._raw_value)


class QTimeMs(QTemporal):
    """q time type (qtype 19): 09:30:15.789 (milliseconds from midnight)
    
    Arithmetic operates on milliseconds: adding 1 adds 1 millisecond.
    """
    
    def __init__(self, raw_value):
        super().__init__(raw_value, 19, "time_ms", storage_size=32)
    
    def __str__(self):
        # Use centralized special value configuration
        special_values = TEMPORAL_SPECIAL_VALUES.get(self.__class__, {})
        if self.is_null():
            return special_values.get('nan', 'NaT')
        elif self.is_pos_inf():
            return special_values.get('posinf', 'inf')
        elif self.is_neg_inf():
            return special_values.get('neginf', '-inf')
        
        # Format as HH:MM:SS.mmm
        if hasattr(self._raw_value, 'total_seconds'):
            total_ms = int(self._raw_value.total_seconds() * 1000)
            hours = total_ms // 3600000
            minutes = (total_ms % 3600000) // 60000
            seconds = (total_ms % 60000) // 1000
            milliseconds = total_ms % 1000
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        elif isinstance(self._raw_value, int):
            # If it's raw milliseconds from midnight
            hours = self._raw_value // 3600000
            minutes = (self._raw_value % 3600000) // 60000
            seconds = (self._raw_value % 60000) // 1000
            milliseconds = self._raw_value % 1000
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        return str(self._raw_value)


class QTimeNs(QTemporal):
    """q timespan type (qtype 16): 1D02:30:15.123456789 (nanoseconds duration)
    
    Arithmetic operates on nanoseconds: adding 1 adds 1 nanosecond.
    This is a duration that can span multiple days.
    """
    
    def __init__(self, raw_value):
        super().__init__(raw_value, 16, "time_ns", storage_size=64)
    
    def __str__(self):
        if self.is_null() or self.is_inf():
            return super().__str__()
        # Format as DDDDhh:mm:ss.nnnnnnnnn or similar
        if hasattr(self._raw_value, 'total_seconds'):
            total_ns = int(self._raw_value.total_seconds() * 1_000_000_000)
            return self._format_nanoseconds(total_ns)
        elif isinstance(self._raw_value, int):
            return self._format_nanoseconds(self._raw_value)
        return str(self._raw_value)
    
    def _format_nanoseconds(self, total_ns):
        """Format nanoseconds as readable duration."""
        if total_ns == 0:
            return "00:00:00.000000000"
        
        sign = "-" if total_ns < 0 else ""
        total_ns = abs(total_ns)
        
        # Break down into components
        days = total_ns // (24 * 60 * 60 * 1_000_000_000)
        remaining_ns = total_ns % (24 * 60 * 60 * 1_000_000_000)
        
        hours = remaining_ns // (60 * 60 * 1_000_000_000)
        remaining_ns %= (60 * 60 * 1_000_000_000)
        
        minutes = remaining_ns // (60 * 1_000_000_000)
        remaining_ns %= (60 * 1_000_000_000)
        
        seconds = remaining_ns // 1_000_000_000
        nanoseconds = remaining_ns % 1_000_000_000
        
        if days > 0:
            return f"{sign}{days}D{hours:02d}:{minutes:02d}:{seconds:02d}.{nanoseconds:09d}"
        else:
            return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}.{nanoseconds:09d}"


class QDatetimeMs(QTemporal):
    """q datetime type (qtype 15): 2000.01.01T09:30:15.789 (DEPRECATED, millisecond precision)
    
    Arithmetic operates on milliseconds: adding 1 adds 1 millisecond.
    Note: This type is deprecated in q, use timestamp (datetime_ns) instead.
    """
    
    def __init__(self, raw_value):
        self._raw_float = raw_value  # Store for null/infinity checks
        converted_value = self._convert_raw_to_datetime(raw_value)
        super().__init__(converted_value, 15, "datetime_ms", storage_size=None)
    
    def _convert_raw_to_datetime(self, raw_value):
        """Convert raw q datetime float to numpy datetime64"""
        import math
        if math.isnan(raw_value):  # null (NaN)
            return numpy.datetime64('NaT', 'ms')
        elif math.isinf(raw_value):  # infinity
            return raw_value  # Keep as float for special handling
        else:
            # q datetime epoch is 2000-01-01, raw_value is fractional days from epoch
            epoch_datetime = numpy.datetime64('2000-01-01T00:00:00.000', 'ms')
            # Convert fractional days to milliseconds with proper rounding
            milliseconds_from_epoch = round(raw_value * 24 * 60 * 60 * 1000)
            return epoch_datetime + numpy.timedelta64(milliseconds_from_epoch, 'ms')
    
    def is_null(self):
        """Override to check raw float value"""
        import math
        return math.isnan(self._raw_float)
    
    def is_pos_inf(self):
        """Override to check raw float value"""
        import math
        return math.isinf(self._raw_float) and self._raw_float > 0
    
    def is_neg_inf(self):
        """Override to check raw float value"""
        import math
        return math.isinf(self._raw_float) and self._raw_float < 0
    
    def _format_value(self):
        """Format datetime as YYYY-MM-DDTHH:MM:SS.mmm for clarity."""
        if hasattr(self._raw_value, 'strftime'):
            return self._raw_value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # Trim to ms
        elif isinstance(self._raw_value, numpy.datetime64):
            # Convert numpy.datetime64 to pandas Timestamp for strftime
            import pandas as pd
            timestamp = pd.Timestamp(self._raw_value)
            return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]  # Trim to ms
        return str(self._raw_value)
    


class QDatetimeNs(QTemporal):
    """q timestamp type: YYYY-MM-DDTHH:MM:SS.nnnnnnnnn (nanosecond precision)
    
    Arithmetic operates on nanoseconds: adding 1 adds 1 nanosecond.
    This is the recommended temporal type for combined date+time in q.
    Note: This is a placeholder for when q adds nanosecond timestamp support.
    """
    
    def __init__(self, raw_value):
        super().__init__(raw_value, -12, "datetime_ns", storage_size=64)  # qtype 12
    
    def __str__(self):
        if self.is_null() or self.is_inf():
            return super().__str__()
        
        # Format as YYYY-MM-DDTHH:MM:SS.nnnnnnnnn
        if isinstance(self._raw_value, int):
            # Convert nanoseconds since q epoch (2000-01-01) to datetime
            import numpy as np
            epoch_ns = np.datetime64('2000-01-01T00:00:00', 'ns')
            dt = epoch_ns + np.timedelta64(self._raw_value, 'ns')
            
            # Convert to string and format with nanoseconds
            dt_str = str(dt)
            if '.' in dt_str:
                # Already has nanoseconds
                return dt_str
            else:
                # Add nanosecond precision
                return dt_str + ".000000000"
        elif hasattr(self._raw_value, 'strftime'):
            base = self._raw_value.strftime('%Y-%m-%dT%H:%M:%S')
            # Add nanoseconds if available
            if hasattr(self._raw_value, 'nanosecond'):
                return f"{base}.{self._raw_value.nanosecond:09d}"
            elif hasattr(self._raw_value, 'microsecond'):
                return f"{base}.{self._raw_value.microsecond * 1000:09d}"
            return base + ".000000000"
        return str(self._raw_value)


# Custom dtypes for pandas display
class QTemporalDtype:
    """Base class for custom temporal dtypes that display nicely in pandas"""
    
    def __init__(self, name, base_dtype='object'):
        self.name = name
        self._base = numpy.dtype(base_dtype)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    # Delegate all other attributes to base dtype for pandas compatibility
    def __getattr__(self, name):
        return getattr(self._base, name)


class QDateDayDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('date_day')


class QDateMonthDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('date_month')


class QTimeMinuteDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('time_minute')


class QTimeSecondDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('time_second')


class QTimeMsDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('time_ms')


class QTimeNsDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('time_ns')


class QDatetimeMsDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('datetime_ms')


class QDatetimeNsDtype(QTemporalDtype):
    def __init__(self):
        super().__init__('datetime_ns')


# Factory function for creating temporal objects
def create_qtemporal(raw_value, qtype):
    """Factory function to create appropriate QTemporal subclass.
    
    Args:
        raw_value: The underlying temporal value
        qtype: q type number (13, 14, 15, 16, 17, 18, 19)
        
    Returns:
        Appropriate QTemporal subclass instance
    """
    class_map = {
        -12: QDatetimeNs,  # timestamp (single value)
        -13: QDateMonth,   # month (single value)
        -14: QDateDay,     # date (single value)  
        -15: QDatetimeMs,  # datetime (single value, deprecated)
        -16: QTimeNs,      # timespan (single value)
        -17: QTimeMinute,  # minute (single value)
        -18: QTimeSecond,  # second (single value)
        -19: QTimeMs,      # time (single value)
        12: QDatetimeNs,   # timestamp list
        13: QDateMonth,    # month list
        14: QDateDay,      # date list
        15: QDatetimeMs,   # datetime list (deprecated)
        16: QTimeNs,       # timespan list
        17: QTimeMinute,   # minute list
        18: QTimeSecond,   # second list
        19: QTimeMs,       # time list
    }
    
    if qtype not in class_map:
        raise ValueError(f"Unsupported temporal qtype: {qtype}")
    
    return class_map[qtype](raw_value)


# Configuration for special value display in temporal types
TEMPORAL_SPECIAL_VALUES = {
    QDateDay: {
        'nan': 'NaT',
        'posinf': 'INT32_MAX',
        'neginf': 'INT32_MIN',
        'repr_class': 'Date'
    },
    QDateMonth: {
        'nan': 'NaT', 
        'posinf': 'INT32_MAX',
        'neginf': 'INT32_MIN',
        'repr_class': 'DateMonth'
    },
    QTimeMinute: {
        'nan': 'NaT',
        'posinf': 'INT32_MAX', 
        'neginf': 'INT32_MIN',
        'repr_class': 'TimeMinute'
    },
    QTimeSecond: {
        'nan': 'NaT',
        'posinf': 'INT32_MAX',
        'neginf': 'INT32_MIN',
        'repr_class': 'TimeSecond'
    },
    QTimeMs: {
        'nan': 'NaT',
        'posinf': 'INT32_MAX',
        'neginf': 'INT32_MIN',
        'repr_class': 'TimeMS'
    },
    QTimeNs: {
        'nan': 'NaT',
        'posinf': 'INT64_MAX',
        'neginf': 'INT64_MIN',
        'repr_class': 'TimeNS'
    },
    QDatetimeMs: {
        'nan': 'NaT',
        'posinf': 'inf', 
        'neginf': '-inf',
        'repr_class': 'DatetimeFloat'
    },
    QDatetimeNs: {
        'nan': 'NaT',
        'posinf': 'INT64_MAX',
        'neginf': 'INT64_MIN',
        'repr_class': 'DateTimeNS'
    }
}