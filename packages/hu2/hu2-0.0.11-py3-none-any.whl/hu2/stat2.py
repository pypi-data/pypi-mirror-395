import enum
# 统计模块，方便根据结果状态分类统计结果
class CommentEnum(enum.Enum):
    # def __new__(cls, value, description):
    #     print('CommentEnum __new__')
    #     obj = object.__new__(cls)
    #     obj._value_ = value
    #     obj._description = description
    #     return obj

    def __init__(self, value, description):
        self._value_ = value
        self._description = description

    @property
    def value(self):
        return self._value_

    @property
    def description(self):
        return self._description


class Statistics:
    def __init__(self):
        self.result_dict: dict[CommentEnum,int] = {}

    def increase(self,key:CommentEnum):
        """ 增加指定enum key的计数值 +1 """
        if key not in self.result_dict:
            self.result_dict[key] = 0
        self.result_dict[key] += 1
    def format(self, sep=' '):
        """格式化输出 各个 enum key 的 计数结果，使用 description 属性展示"""
        strseg = []
        for k,v in self.result_dict.items():
            strseg.append('{} -> {}个'.format(k.description,v))
        return sep.join(strseg)
    def get_count(self,key:CommentEnum):
        """ 获取指定enum key的计数 """
        count = 0
        if key in self.result_dict:
            count = self.result_dict[key]
        return count
