from random import randint
import threading
import time


def f(arr):
    for i in arr:
        print(i)
        time.sleep(randint(1,3))


if __name__ == '__main__':
    arr1 = [1, 3, 5]
    arr2 = [2, 4, 6]

    x1 = threading.Thread(target=f, args=(arr1,))
    x2 = threading.Thread(target=f, args=(arr2,))
    
    x1.start()
    x2.start()