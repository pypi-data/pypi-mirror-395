import json
from datetime import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, obj)

def todumps(obj) -> str :
    """
    将参数对象转换为json字符串
    datetime类型转为：年-月-日 时:分:秒
    中文内容原样输入，不进行\\uxxxx的Unicode编码转换
    :param obj:
    :return:
    """
    return json.dumps(obj, cls=DateEncoder, ensure_ascii=False)