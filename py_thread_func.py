# encoding: utf-8

import time
import threading
import inspect
import ctypes

# class myThread (threading.Thread):
#     def __init__(self, threadID, name, delay):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.delay = delay
#     def run(self):
#         print ("开始线程：" + self.name)
#         print_time(self.name, self.delay, 5)
#         print ("退出线程：" + self.name)
#
# def print_time(threadName, delay, counter):
#     while counter:
#         # if exitFlag:
#         #     threadName.exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1

# class myThreadFunc(object):
#     def __init__(self, name, delay, func, args):
#         self.myThread = threading.Thread(self, target=func, args=args, name=name)
#         self.myThread.target = func
#         self.name = name
#         self.delay = delay
#         self.exit_flag = 0
#
#     def start(self):
#         print('线程启动')
#         self.myThread.start(self)
#
#     def state(self):
#         status = self.myThread.is_alive()
#         print('线程状态: {0}'.format(status))
#         return status
#
#     def join(self):
#         self.myThread.join(5)
#
#     def run(self):
#         while self.exit_flag == 0:
#             self.myThread.target
#
#
#
#     def stop(self):
#         print('线程终止')
#         try:
#             for i in range(5):
#                 self._async_raise(self.myThread.ident, SystemExit)
#                 time.sleep(1)
#         except Exception as e:
#             print(e)
#
#     def _async_raise(self, tid, exctype):
#         """raises the exception, performs cleanup if needed"""
#         tid = ctypes.c_long(tid)
#         if not inspect.isclass(exctype):
#             exctype = type(exctype)
#         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
#         if res == 0:
#             raise ValueError("invalid thread id")
#         elif res != 1:
#             # """if it returns a number greater than one, you're in trouble,
#             # and you should call it again with exc=NULL to revert the effect"""
#             ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#             raise SystemError("PyThreadState_SetAsyncExc failed")