import time
import re

from load_table import LoadTable
from write_file import Content2File
from export_log import Logger

class UserPicker():
    @property
    def pathMenu(self):
        """
        选择要导出的目的路径
        :return: export_path:str
        """
        print("""
            ==========OpenCat所有对话记录导出==========
            """)
        dir_pick_num = input("""
1.导出到桌面    2.导出到当前文件夹    3.导出到自定义路径    0.退出
请输入要导出的文件路径(输入序号):""")
        if dir_pick_num == '1':
            dir_num = 1
        elif dir_pick_num == '2':
            dir_num = 2
        elif dir_pick_num == '3':
            dir_num = 3
        elif dir_pick_num == '0':
            return None
        else:
            return None
        export_path = Content2File(dir_num).get_path()
        return export_path

    def askMenu(self):
        """
        显示已导出数据的情况，询问是重新导出全部还是接着导出未导出部分
        :param: title: 当前要导出的对话标题
        :param: timestamp: 当前要导出的对话已导出的数据的最新时间
        """
        print("""
1.确认导出所有最新对话记录
2.重新导出所有对话记录
0.返回主菜单
"""
        )
        continue_pick_num = input('请选择导出方式:')
        if re.match('^\d+$', continue_pick_num):
            return int(continue_pick_num)
        else:
            return 0

def interaction():
    loadtable = LoadTable()
    userpick = UserPicker()
    content2file = Content2File()
    

    title_list = loadtable.getTitle()
    export_path = userpick.pathMenu
    if not export_path:
        return
    
    continue_pick = userpick.askMenu()
    if not continue_pick:
        return interaction()
    
    if continue_pick not in [1, 2]:
        print('输入有误')
        return
        
    if title_list:
        for title in title_list:
            try:
                logger = Logger(title)
                read_log_info = logger.readLog()
                read_log = read_log_info if read_log_info else dict()
                last_timestamp = read_log.get('timestamp', 0)
                # print(title, last_timestamp)
                if continue_pick == 1:
                    kwargs = {title: last_timestamp}
                elif continue_pick == 2:
                    kwargs = {title: 0}
                
                sql = loadtable.sqlQuery(**kwargs)
                content = loadtable.getContent(sql)
                if content[title]:
                    file_type = content2file.write(content, export_path)
                    logger.writeLog(export_path, kwargs[title], file_type)
                    print(f'{title}-导出成功')
                else:
                    print(f'{title}-没有可以导出的对话信息')
            except Exception as e:
                print('导出过程中出现异常：%s', str(e))

    time.sleep(1)
    return interaction()

def main():
    return interaction()


if __name__ == "__main__":
    main()