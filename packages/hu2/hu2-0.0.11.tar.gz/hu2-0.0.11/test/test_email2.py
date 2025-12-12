import unittest

import hu2.cfg2
from hu2.email2 import Email,get_email_head

cfg_info = hu2.cfg2.ConfigInfo("test_email2_config.ini")

class TestEmail(unittest.TestCase):
    def test_email_head(self):
        h = [get_email_head('46133_7831中@qq.com'),
             get_email_head(None),
             get_email_head('None'),
             get_email_head('None@2@4'),
             ]
        print(h)

        pass
    def test_email2(self):
        eml = Email('13733160671@139.com','e991cc37c634941d1c00','smtp.139.com')

        eml.send(to_emails=['13733160671@139.com','461337831@qq.com'],
                 subject='检测任务说明3',
                 content='第三个检测到目前输入的原文和译文目标语种均为英文，已自动为您转换为英文翻译成中文的服务根据输入的原文 "increase"'
             )

    def test_cfg_email2(self):
        eml = cfg_info.create_email()
        eml.send(to_emails=['461337831@qq.com'],
                 subject='检测任务说明4',
                 content='第四个检测到目前输入的原文和译文目标语种均为英文，已自动为您转换为英文翻译成中文的服务根据输入的原文 "increase"'
                )

if __name__ == '__main__':
    unittest.main()