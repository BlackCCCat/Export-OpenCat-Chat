import os
# import shutil
import sqlite3

class LoadTable():
    def __init__(self):
        """
        指定opencat数据库默认路径，如路径不一致，可以自行传入路径参数(str)更改
        """
        # 默认路径
        HOME = os.environ['HOME']
        DB_PATH = os.path.join(HOME, 'Library/Group Containers/group.tech.baye.openai/OpenCat.sqlite')
        # CP_DB_PATH = 'OpenCat_copy.sqlite'
        # shutil.copy2(DB_PATH, CP_DB_PATH)
        self.db_path = DB_PATH

    
    def getTitle(self) -> list:
        """
        从ZCONVERSATION表中获取对话标题信息
        :return title: list [title]
        """
        title = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                            select ztitle 
                            from ZCONVERSATION
                            group by ztitle
                            """)
            _title = cursor.fetchall()
            for i in _title:
                title.append(i[0])
            return title
        except sqlite3.Error as e:
            raise Exception(e)
        
    def titleCount(self, title=None, start_time=0) -> dict:
        """
        :param title 默认None，获取所有已有对话截止最新时间范围内的消息数量
        :return title_count: dict {title: count}
        """
        title_count = dict()
        if title:
            condition = f"where ztitle='{title}' and b.zcreatedat>'{start_time}'"
        else:
            condition = ''

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"""
                            select a.ztitle
                                ,count(1)
                            from ZCONVERSATION a
                            left join ZMESSAGE b
                            on a.zid=b.zchatid
                            {condition}
                            group by a.ZTITLE
                            """)
            _title_count = cursor.fetchall()
            for i in _title_count:
                title_count[i[0]] = i[1]
            return title_count
        except sqlite3.Error as e:
            raise Exception(e)
        

    def sqlQuery(self, **kwargs) -> dict:
        """
        生成SQL查询语句
        :param **kwargs: {title: timestamp}
        :return sql_dict: dict
        """
        sql_dict = dict()
        if kwargs:
            for _title, _timestamp in kwargs.items():
                sql_query = f"""
                            select case b.zrole 
									when 'user' then '> ' || '(' || b.create_time || ')' || b.zrole
									when 'assistant' then '(' || b.create_time || ')' || b.zrole
								else b.zrole end zrole
                                ,b.zcontent
								,b.create_time,b.zcreatedat_rank
                            from
                            (
                            select z_pk
                                ,zid
                                ,zmodel
                                ,ZSYSTEMPROMPT
                                ,ztitle
                                ,ZLASTMESSAGEID
                            from ZCONVERSATION
                            ) a
                            left join
                            (
                            select z_pk
                                ,zid
                                ,zchatid
                                ,zcontent || '\n' zcontent
                                ,zrole
                                ,zcreatedat
                                ,case when length(zcreatedat) < 13 then datetime(zcreatedat, 'unixepoch', 'localtime') 
                                    else datetime(zcreatedat / 1000, 'unixepoch', 'localtime') end create_time
                                ,row_number() over(partition by zchatid order by zcreatedat) zcreatedat_rank
                                ,count(zcontent) over(partition by zchatid) chat_count
                            from ZMESSAGE
                            ) b
                            on a.zid=b.zchatid
                            where b.zcontent is not null
                                and a.ztitle='{_title}'
                                and b.zcreatedat>'{_timestamp}'
                            order by a.zid, b.zcreatedat_rank
                            """
                sql_dict[_title] = {"timestamp": _timestamp, "sql": sql_query}
            return sql_dict
        else:
            print('缺少要导出的对话标题与时间')


    def getContent(self, sql:dict) -> dict:
        """
        从ZCONVERSATION和ZMESSAGE表中获取对话内容信息
        :param sql: return of self.sqlQuery(**kwargs)
        :return content: dict
        """
        content = dict()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            for k_title, v_value in sql.items():
                cursor.execute(v_value['sql'])
                _content = cursor.fetchall()
                content[k_title] = _content
            return content
        except sqlite3.Error as e:
            raise Exception(e)
        
    def getPrompt(self, title):
        """
        获取指定对话的prompt信息
        :param title str 对话标题
        :return prompt: str
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"""
                            select zsystemprompt
                            from ZCONVERSATION
                            where ztitle='{title}'
                            """)
            _prompt = cursor.fetchall()
            prompt = _prompt[0][0]
            return prompt
        except sqlite3.Error as e:
            raise Exception(e)
        

    def getLastTime(self, title):
        """
        获取最后一条对话的时间戳和时间
        :param title str 对话标题
        :return timestamp, time: str, str
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            SQL = f"""
                        select a.ZTITLE
                            ,max(b.zcreatedat) createdat
                            ,case when length(max(b.zcreatedat)) < 13 then datetime(max(b.zcreatedat), 'unixepoch', 'localtime') 
                                else datetime(max(b.zcreatedat) / 1000, 'unixepoch', 'localtime') end create_time
                        from ZCONVERSATION a
                        left join ZMESSAGE b
                        on a.zid=b.zchatid
                        where a.ztitle='{title}'
                        group by a.ZTITLE
                        """
            cursor.execute(SQL)
            _time = cursor.fetchone()
            if _time:
                _timestamp = _time[1]
                formatted_time = _time[2]
                return _timestamp, formatted_time
            else:
                print('请检查SQL是否正确：\n',SQL)
        except sqlite3.Error as e:
            raise Exception(e)


def main():
    lt = LoadTable()
    # res = lt.titleCount()
    kwargs = {"SQL":'0',}
    sql = lt.sqlQuery(**kwargs)
    # print(sql)
    res = lt.getContent(sql)
    print(res)
    # print(lt.getPrompt('SQL'))
    # print(lt.getLastTime('Python'))

if __name__ == "__main__":
    main()