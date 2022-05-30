import os
import threading


def threads_manager(thread_function, threads_args=[]):
    cpu_qty = os.cpu_count()
    if cpu_qty is None:
        cpu_qty = 1
    threads = list()
    for index in range(cpu_qty):
        args = [index,cpu_qty]
        for a in threads_args:
            args.append(a)
        x = threading.Thread(target=thread_function, args=(args))
        threads.append(x)
        x.start()
    for index, thread in enumerate(threads):
        thread.join()
