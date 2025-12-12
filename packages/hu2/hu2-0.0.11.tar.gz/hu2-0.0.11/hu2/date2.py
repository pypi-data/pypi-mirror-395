import os


def strftime_nopad(date,fmtstr):
    """
    统一使用 %-d 格式来去掉前导0的处理。在windows平台中需要替换成 %#d
    :param date: datetime对象
    :param fmtstr: 日期格式字符串 例如 %Y-%m-%d %H:%M:%S
    :return: 日期字符串
    """
    if os.name == 'nt':
        fmtstr = fmtstr.replace('%-','%#')
    return date.strftime(fmtstr)