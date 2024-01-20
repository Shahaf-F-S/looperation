# looperator

> A python module to easily run loop based or condition-based operations, control the starting, pausing, unpausing, timeout, delay, and stopping of the loop, and handle exceptions in real time.


Installation
-----------
````
pip install looperator
````

example
-----------
* all attributes of the operator are being evaluated at runtime, thus any change for any attribute during runtime is valid.
* when pausing the operator or superator, the timeout and stopping processes are paused as well.

create an operator object
````python
import time
import random
import datetime as dt

from looperator import Operator

operator = Operator(
    operation=lambda value: print(value),
    args_collector=lambda: (random.randint(0, 10),),
    delay=dt.timedelta(seconds=1)
)
````

run the operation with timeout pause adter some time
````python
print("starting process, 10 seconds timeout")

operator.run(timeout=dt.timedelta(seconds=10))

time.sleep(5)

operator.pause()

print("passed after 5 seconds")
print("paused for 5 more seconds")
````

output
````
starting process, 10 seconds timeout
10
6
2
7
0
passed after 5 seconds
paused for 5 more seconds
````

wait some time while paused and continue
````python
time.sleep(5)

print("5 seconds left")

operator.unpause()

time.sleep(5)

print("process ending")
````

output
````
5 seconds left
5
1
4
4
9
process ending
````

for exception handling pass to the operator object a handler object
````python
from looperator import Handler, Operator

handler = Handler(
    exceptions=[ZeroDivisionError],
    exception_handler=print,
    exception_callback=lambda h: print("error")
)

operator = Operator(
    operation=lambda value: print(1 / value),
    args_collector=lambda: (0,),
    delay=dt.timedelta(seconds=1),
    handler=handler
)

operator.run()
````

output
````
error
division by zero
````

run an operation as long as a condition is met
````python
import time
import random
import datetime as dt

from looperator import Operator

conditions = [False, False, False]

operator = Operator(
    operation=lambda value: print(value),
    args_collector=lambda: (random.randint(0, 11),),
    stopping_collector=lambda: any(conditions),
    delay=dt.timedelta(seconds=1),
    loop_stopping=True
)

# loop_stopping=True for evaluating the stopping_collector callable during the operation loop, 
# loop_stopping=False to evaluate in a different thread.

print("starting process")
      
operator.run()

time.sleep(5)

conditions.append(True)

print("process ending")
````

output
````
starting process
2
7
4
6
8
process ending
````

run a loop operation as long as a condition is met
````python
import time
import random
import datetime as dt

from looperator import Operator

def loop_operation(operation: Operator):
    while operation.operating:
        print(random.randint(0, 11))

        operation.start_waiting(operation.delay)
        
conditions = [False, False, False]

operator = Operator(
    stopping_collector=lambda: any(conditions),
    delay=dt.timedelta(seconds=1),
    loop=False  # for calling the operation callable only once.
)

operator.operation = lambda: loop_operation(operator)

print("starting process")
      
operator.run()

time.sleep(5)

conditions.append(True)

print("process ending")
````

output
````
starting process
2
9
7
9
8
process ending
````

run the operation in the main thread
````python
import random
import datetime as dt

from looperator import Operator

operator = Operator(
    operation=lambda value: print(value),
    args_collector=lambda: (random.randint(0, 11),),
    delay=dt.timedelta(seconds=1),
    timeout=dt.timedelta(seconds=5)
)

print("starting process")
      
operator.run(block=True)

print("process ending")
````

output
````
starting process
8
9
5
2
3
process ending
````

Operator constructor signature
````python
TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

def __init__(
        self,
        name: str = None, *,
        operation: Callable[..., _O] = None,
        args_collector: Callable[[], Iterable[Any]] = None,
        kwargs_collector: Callable[[], dict[str, Any]] = None,
        stopping_collector: Callable[[], bool] = None,
        termination: Callable[[], Any] = None,
        handler: Handler = None,
        loop: bool = True,
        warn: bool = False,
        loop_stopping: bool = None,
        delay: TimeDuration = None,
        block: bool = False,
        coroutine: bool = False,
        wait: float | TimeDestination = None,
        timeout: float | TimeDestination = None
)
````

.run method signature
````python
TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

def run(
        self,
        loop: bool = None,
        loop_stopping: bool = None,
        block: bool = None,
        wait: TimeDestination = None,
        timeout: TimeDestination = None
)
````

all main methods of the Operator class
```python
operator.run()
operator.start_timeout(duration=dt.timedelta(seconds=5))
operator.stop_timeout()
operator.pause()
operator.unpause()
operator.start_stopping()
operator.stop_stopping()
operator.start_waiting(duration=dt.timedelta(seconds=5))
operator.stop()
```

Using a Superator object - an Operator of Operators
````python
import time
import datetime as dt
import random

from looperator import Operator, Superator

operator1 = Operator(
    operation=lambda value: print(value, "operator 1"),
    args_collector=lambda: (random.randint(0, 5),),
    delay=dt.timedelta(seconds=1)
)
operator2 = Operator(
    operation=lambda value: print(value, "operator 2"),
    args_collector=lambda: (random.randint(5, 10),),
    delay=dt.timedelta(seconds=1)
)

superator = Superator(
    operators=[operator1, operator2]
)

print("starting process, 10 seconds timeout")

superator.run(timeout=dt.timedelta(seconds=4))

time.sleep(2)

superator.pause()

print("passed after 5 seconds")
print("paused for 5 more seconds")

time.sleep(2)

print("5 seconds left")

superator.unpause()

time.sleep(2)

print("process ending")
````

output
````
starting process, 10 seconds timeout
0 operator 1
9 operator 2
2 operator 1
7 operator 2
passed after 5 seconds
paused for 5 more seconds
5 seconds left
2 operator 1
6 operator 2
2 operator 1
7 operator 2
process ending
````

Superator constructor signature
````python
TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

def __init__(
        operators: Iterable[Operator],
        handler: Handler = None,
        stopping_collector: Callable[[], bool] = None,
        termination: Callable[[], Any] = None,
        delay: TimeDuration = None,
        block: bool = False,
        wait: TimeDestination = None,
        timeout: TimeDestination = None
)
````

.run method signature
````python
TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime

def run(
        self,
        loop: bool = None,
        loop_stopping: bool = None,
        block: bool = None,
        wait: TimeDestination = None,
        timeout: TimeDestination = None
)
````

all main methods of the Operator class
```python

CONTROL_ALL_OPERATORS = True  # when False, doesn't affect the operators.

superator.run()
superator.start_timeout(duration=dt.timedelta(seconds=5))
superator.stop_timeout()
superator.pause(operators=CONTROL_ALL_OPERATORS)
superator.unpause(operators=CONTROL_ALL_OPERATORS)
superator.start_stopping()
superator.stop_stopping()
superator.start_waiting(duration=dt.timedelta(seconds=5))
superator.stop(operators=CONTROL_ALL_OPERATORS)
```