# test.py

import time
import random
import datetime as dt

from looperator import QueueOperator, OperationQueue

def main() -> None:
    """A function to run the main test."""

    queue = OperationQueue[int]()

    operator = QueueOperator[int](
        operation=lambda value: value,
        args_collector=lambda: (random.randint(0, 10),),
        delay=dt.timedelta(seconds=1),
        queue=queue
    )

    operator.run(timeout=dt.timedelta(seconds=10))

    while operator.operating and (len(queue) < 5):
        print(
            "less than 5 seconds", f"queue length: {len(queue)}",
            "last value:", queue.values[-1].outputs.returns
        )

        time.sleep(1)
    # end while

    operator.pause()

    print()
    print("passed 5 seconds")
    print("paused for 5 more seconds")

    time.sleep(5)

    print("5 seconds left")
    print()

    operator.unpause()

    while operator.operating:
        print(
            "more than 5 seconds", f"queue length: {len(queue)}",
            "last value:", queue.values[-1].outputs.returns
        )

        time.sleep(1)
    # end while
# end main

if __name__ == "__main__":
    main()
# end if