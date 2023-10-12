# test.py

import time
import random
import datetime as dt

from looperator import QueueOperator, OperationQueue, Superator

def main() -> None:
    """A function to run the main test."""

    queue = OperationQueue[int]()

    operator1 = QueueOperator[int](
        operation=lambda value: value,
        args_collector=lambda: (random.randint(0, 10),),
        delay=dt.timedelta(seconds=1),
        queue=queue
    )

    operator2 = QueueOperator[int](
        operation=lambda value: value,
        args_collector=lambda: (random.randint(0, 10),),
        delay=dt.timedelta(seconds=1),
        queue=queue
    )

    superator = Superator(
        operators=[operator1, operator2],
        delay=dt.timedelta(seconds=1)
    )

    superator.run(timeout=dt.timedelta(seconds=10))

    while superator.operating and (len(queue) < 10):
        print("less than 5 seconds", f"queue length: {len(queue)}")

        time.sleep(1)
    # end while

    superator.pause()

    print()
    print("passed 5 seconds")
    print("paused for 5 more seconds")

    time.sleep(5)

    print("5 seconds left")
    print()

    superator.unpause()

    while superator.operating:
        print("more than 5 seconds", f"queue length: {len(queue)}")

        time.sleep(1)
    # end while
# end main

if __name__ == "__main__":
    main()
# end if