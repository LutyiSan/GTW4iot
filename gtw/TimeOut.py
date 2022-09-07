import time
import multiprocessing


def timeout(func, control=30):
    p = multiprocessing.Process(target=func)
    p.start()
    p.join(timeout=control)
    if p.is_alive():
        p.kill()
        print("Process is stopped")
    time.sleep(2)



