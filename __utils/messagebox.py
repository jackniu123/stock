# 如何进行dataframe的索引： https://blog.csdn.net/fantine_deng/article/details/105130904
# pandas教程：https://www.runoob.com/pandas/pandas-dataframe.html
import inspect, threading
import logging
from tkinter.commondialog import Dialog
from typing import Any, ClassVar

__all__ = ["showinfo", "showwarning", "showerror", "log",
           "askquestion", "askokcancel", "askyesno",
           "askyesnocancel", "askretrycancel"]

#
# constants

# icons
ERROR = "error"
INFO = "info"
QUESTION = "question"
WARNING = "warning"

# types
ABORTRETRYIGNORE = "abortretryignore"
OK = "ok"
OKCANCEL = "okcancel"
RETRYCANCEL = "retrycancel"
YESNO = "yesno"
YESNOCANCEL = "yesnocancel"

# replies
ABORT = "abort"
RETRY = "retry"
IGNORE = "ignore"
OK = "ok"
CANCEL = "cancel"
YES = "yes"
NO = "no"


#
# message dialog class

class Message(Dialog):
    "A message box"

    command = "tk_messageBox"


options_list = []

lock = threading.RLock()


#
# convenience stuff

# Rename _icon and _type options to allow overriding them in options
def _show(title=None, message=None, _icon=None, _type=None, **options):
    lock.acquire()
    caller_frame = inspect.stack()[2]
    caller_file = caller_frame[1]
    caller_line = caller_frame[2]
    caller_function = caller_frame[3]

    message = message + f'\n !!! real position is[{caller_file}:{caller_line}:{caller_function}:]'

    if _icon and "icon" not in options:    options["icon"] = _icon
    if _type and "type" not in options:    options["type"] = _type
    if title:   options["title"] = title
    if message: options["message"] = message

    logger.warning(options)
    print(options)
    options_list.append(options)
    lock.release()
    return YES
    # res = Message(**options).show()
    # # In some Tcl installations, yes/no is converted into a boolean.
    # if isinstance(res, bool):
    #     if res:
    #         return YES
    #     return NO
    # # In others we get a Tcl_Obj.
    # lock.release()
    # return str(res)


def showinfo(title=None, message=None, **options):
    "Show an info message"
    return _show(title, message, INFO, OK, **options)


def showwarning(title=None, message=None, **options):
    "Show a warning message"
    return _show(title, message, WARNING, OK, **options)


def showerror(title=None, message=None, **options):
    "Show an error message"
    return _show(title, message, ERROR, OK, **options)


def askquestion(title=None, message=None, **options):
    "Ask a question"
    return _show(title, message, QUESTION, YESNO, **options)


def askokcancel(title=None, message=None, **options):
    "Ask if operation should proceed; return true if the answer is ok"
    s = _show(title, message, QUESTION, OKCANCEL, **options)
    return s == OK


def askyesno(title=None, message=None, **options):
    "Ask a question; return true if the answer is yes"
    s = _show(title, message, QUESTION, YESNO, **options)
    return s == YES


def askyesnocancel(title=None, message=None, **options):
    "Ask a question; return true if the answer is yes, None if cancelled."
    s = _show(title, message, QUESTION, YESNOCANCEL, **options)
    # s might be a Tcl index object, so convert it to a string
    s = str(s)
    if s == CANCEL:
        return None
    return s == YES


def askretrycancel(title=None, message=None, **options):
    "Ask if operation should be retried; return true if the answer is yes"
    s = _show(title, message, WARNING, RETRYCANCEL, **options)
    return s == RETRY


def dump():
    for item in options_list:
        Message(**item).show()
        print(item)
    return


# %(name)s：Logger的名字
# %(levelno)s：打印日志级别的数值
# %(levelname)s：打印日志级别的名称
# %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s：打印当前执行程序名
# %(funcName)s：打印日志的当前函数
# %(lineno)d：打印日志的当前行号
# %(asctime)s：打印日志的时间
# % (msecs)03d：打印毫秒数
# %(thread)d：打印线程ID
# %(threadName)s：打印线程名称
# %(process)d：打印进程ID
# %(message)s：打印日志信息
format_str = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
formatter = logging.Formatter(fmt=format_str)
# logging.basicConfig(format=format_str)

logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('D:\不要删除牛爸爸的程序\__utils\python_log.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

if __name__ == '__main__':
    # showerror('错误', "出错了")
    # showwarning('警告', "警告来临")
    dump()
