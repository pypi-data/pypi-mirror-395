import configparser
import logging
import os
import sys

from sqlalchemy import URL,create_engine
from hu2.email2 import Email

logger = logging.getLogger(__name__)

class ConfigInfo:

    def __init__(self, cfgfilename):
        """
        使用指定的配置文件构建 ConfigInfo 对象。
        1，首先使用代码中指定的配置文件名
        2，再尝试从sys.argv运行参数中查找形如 --config=xxxx 内容，作为文件名
        :param cfgfilename:
        """
        self.filename = cfgfilename
        use_file_type = "参数配置文件"

        find_filename = ""
        for arg in sys.argv:
            if arg.startswith('--config'):
                find_filename = arg.split('=')[1]
        if not find_filename: # 遇到 空串 None 都会 为 True
            print(f"尝试 在 sys.argv 中搜索配置文件参数(--config=xxx) 未找到")
        else:
            self.filename = find_filename
            use_file_type = "运行参数配置文件"
        find_filename = os.getenv("HU2_CONFIG")
        if not find_filename:
            print(f"尝试 在环境变量中搜索配置文件参数(HU2_CONFIG=xxx) 未找到")
        else:
            self.filename = find_filename
            use_file_type = "环境变量配置文件"
        print(f'使用 {use_file_type} :::: {self.filename}')
        configfile = os.path.abspath(self.filename)
        config = configparser.ConfigParser()
        if os.path.exists(configfile):
            config.read(configfile, encoding='utf-8')
        else:
            print(f"配置文件 {configfile} 未找到")
            raise FileNotFoundError(configfile)

        print(type(config))
        self.config = config


    def create_db_engine(self):
        """利用配置文件类数据库片段参数创建 sqlalchemy 所需的Engine实例 """
        __db_user = self.config['db']['user']
        __db_pass = self.config['db']['pass']
        __db_host = self.config['db']['host']
        __db_port = self.config['db']['port']
        __db_database_name = self.config['db']['database_name']
        dburl = URL.create('mysql+pymysql', username=__db_user, password=__db_pass, host=__db_host,
                           database=__db_database_name, port=__db_port, query={"charset": 'utf8'})
        logger.warning('%s %s', type(dburl), dburl)
        xmdb_engine = create_engine(dburl)
        return xmdb_engine

    def create_email(self):
        """利用配置文件类 邮件片段参数 创建 Email工具类"""
        __db_user = self.config['mail']['user']
        __db_pass = self.config['mail']['pass']
        __db_host = self.config['mail']['host']
        __db_port = self.config['mail']['port']
        port = 25
        if __db_port:
           port = int(__db_port)
        eme = Email(__db_user, __db_pass, __db_host, port)
        return eme