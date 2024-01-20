# test.py

import time
import random
import datetime as dt

from looperation import Operator

def main() -> None:
    """A function to run the main test."""

    operator = Operator(
        operation=lambda value: print(value),
        args_collector=lambda: (random.randint(0, 10),),
        delay=dt.timedelta(seconds=1)
    )

    print("starting process, 10 seconds timeout")

    operator.run(timeout=dt.timedelta(seconds=10))
    
    time.sleep(5)
    
    operator.pause()
    
    print("passed after 5 seconds")
    print("paused for 5 more seconds")

    time.sleep(5)

    print("5 seconds passed")
    
    operator.unpause()
    
    time.sleep(5)
    
    print("process ending")

if __name__ == "__main__":
    main()
