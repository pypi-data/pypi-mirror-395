import sys
import datetime
import logging


# 运行辅助工具

def confirm(desc,input_tip=None):
    """
    提示并等待输入。特殊情况：当命令行运行增加--noconfirm时，用其等号后面的内容作为值，例如 --noconfirm=abc  即返回 abc
    :param desc: 功能介绍说明，会在确认执行时展示
    :param input_tip: 等待输入的提示文本
    :return:
    """
    print('运行参数：', sys.argv)
    for arg in sys.argv:
        if arg.startswith('--noconfirm'):
            ipt = arg.split('=')[1]
            return ipt

    print(desc)
    print("请输入并回车以继续:" if input_tip is None else input_tip, end='')
    txt = input()
    return txt


def log(*,logname_prefix=None,stream_level=logging.INFO,rootlogger_level=logging.DEBUG,logger_level_dict=dict(),log_single=True):
    """
    启用日志功能，控制台为 INFO 等级，输出到 err 流中
    :param logname_prefix: 日志文件名前缀，不设置时不启用文件日志。可以是单独的文件或含路径的文件 的名称前缀。生成的日志文件会在后面追加 [年月日时分秒.log]
    :param stream_level: 控制台日志等级，默认为INFO
    :param rootlogger_level: 根日志记录器等级，默认DEBUG
    :param logger_level_dict: 日志记录器等级字典，key-日志名称，value-日志等级，如logging.INFO
    :param log_single: 日志文件不增加时间戳，默认True，
    :return:
    """
    handlers = []
    if logname_prefix is not None:
        logfilename = logname_prefix + ( '1' if log_single else datetime.datetime.now().strftime("%Y%m%d%H%M%S") ) + '.log'
        fileHandler = logging.FileHandler(filename=logfilename, mode='w', encoding='utf-8')
        handlers.append(fileHandler)

    streamHandler = logging.StreamHandler(sys.stderr)
    streamHandler.setLevel(stream_level)
    handlers.append(streamHandler)
    for k,v in logger_level_dict.items():
        logging.getLogger(k).setLevel(v)

    logging.basicConfig(level=rootlogger_level, format='%(asctime)s - %(levelname)-8s - %(name)s - %(message)s',
                        handlers=handlers)