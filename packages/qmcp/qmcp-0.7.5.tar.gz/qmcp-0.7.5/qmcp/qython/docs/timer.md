# Timer Functions

Qython provides built-in functions for managing asynchronous timer callbacks.

## Functions

### `set_timer_callback(func)`
Set the function to be called on each timer tick.

**Parameters:**
- `func`: A function taking either zero or one argument
  - **Zero arguments**: Called with no parameters
  - **One argument**: Called with current datetime as `DateTimeNS` (GMT timezone)

**Examples:**
```python
# Zero-argument callback
def on_tick():
    print(String("Timer tick!"))

set_timer_callback(on_tick)

# One-argument callback with timestamp
def on_tick_with_time(current_time):
    print(String("Timer tick at:"), current_time)

set_timer_callback(on_tick_with_time)
```

### `start_timer(interval_ms)`
Start the timer with the specified interval.

**Parameters:**
- `interval_ms`: Interval in milliseconds between timer ticks

**Example:**
```python
start_timer(1000)  # Tick every 1 second
```

### `stop_timer()`
Stop the currently running timer.

**Returns:** None

**Example:**
```python
stop_timer()
```

### `get_timer_interval()`
Get the current timer interval in milliseconds.

**Returns:** Integer representing the interval in milliseconds, or 0 if timer is not configured

**Example:**
```python
interval = get_timer_interval()
print(String("Timer interval:"), interval)
```

### `is_timer_running()`
Check if the timer is currently running.

**Returns:** Boolean - `True` if timer is running, `False` otherwise

**Example:**
```python
if is_timer_running():
    print(String("Timer is active"))
else:
    print(String("Timer is stopped"))
```

## Complete Example

```python
# Define callback function
def update_data():
    # Your periodic update logic here
    print(String("Updating data..."))

# Configure and start timer
set_timer_callback(update_data)
start_timer(5000)  # Run every 5 seconds

# Later: check status
if is_timer_running():
    current_interval = get_timer_interval()
    print(String("Timer running at"), current_interval, String("ms"))

# Stop when done
stop_timer()
```

## Notes

- The timer callback function can take zero or one argument
  - **Zero arguments**: Function is called without parameters
  - **One argument**: Function receives current datetime as `DateTimeNS` (GMT timezone)
- Use `partial` to wrap functions that need additional arguments:
  - `set_timer_callback(partial(my_func, arg1, arg2))`
- Only one timer can be active at a time
- Starting a new timer while one is running will replace the existing timer
- Timer continues running until explicitly stopped with `stop_timer()`
