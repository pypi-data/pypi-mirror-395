import unittest

import hu2.stat2 as hstat2
from hu2.stat2 import CommentEnum

class TestEnum(CommentEnum):
    First = (1, "第一类")
    Second = (2, "第二类")
    Third = (3, "第三类")
    Four = (4, "第四类")

class TestStatistics(unittest.TestCase):
    def test_stat2(self):
        stat = hstat2.Statistics()
        stat.increase(TestEnum.First)
        stat.increase(TestEnum.First)
        stat.increase(TestEnum.Second)
        stat.increase(TestEnum.Third)
        print(stat.format())
        print(stat.get_count(TestEnum.First))
        print(stat.get_count(TestEnum.Four))