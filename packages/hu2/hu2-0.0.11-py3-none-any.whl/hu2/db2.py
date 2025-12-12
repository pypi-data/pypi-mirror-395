from sqlalchemy import text


class DbWrapper:


    def __init__(self,db_engine):
        self.db_engine = db_engine
        pass


    def query_list(self, sqlstr:str, param_dict=None)->list:
        """ 执行 select sql,可能返回多行记录，无结果时返回空列表，注意返回的记录行对象无法直接被序列化为json """
        if param_dict is None:
            param_dict = dict()
        with self.db_engine.connect() as conn:
            rt = conn.execute(text(sqlstr),param_dict).mappings().fetchall()
            if rt is not None:
                return rt

        return []

    def update(self, sqlstr:str, param_dict=None)->int:
        """执行一条 insert/update/delete sql，返回执行影响条数 """
        if param_dict is None:
            param_dict = dict()
        with self.db_engine.connect() as conn:
            rt = conn.execute(text(sqlstr),param_dict)
            conn.commit()
            if rt is not None:
                return rt.rowcount
            else:
                return -1

    def insert(self, sqlstr:str, param_dict=None)->int:
        if param_dict is None:
            param_dict = dict()
        with self.db_engine.connect() as conn:
            rt = conn.execute(text(sqlstr),param_dict)
            conn.commit()
            if rt is not None:
                return rt.lastrowid
            else:
                return -1