import time
import re

from load_table import LoadTable
from write_file import Content2File
from export_log import Logger

class User():
    def __init__(self):
        self.title_list = LoadTable().getTitle()
            
    @property
    def mainMenu(self):
        """
        主菜单，选择要导出的对话标题
        :return: None or title_pick:str
        """
        print("""
            ==========OpenCat对话记录导出==========

        所有对话标题如下:
            """)
        for index, value in enumerate(self.title_list):
            title_info = f'{index + 1}.{value}'
            print(f"{title_info}")
        print('0.退出')
        
        title_pick_num = input('请输入要导出的对话标题(输入序号):')
        if title_pick_num == '0':
            return None
        elif re.match(r'^\d+$', title_pick_num):
            title_pick = self.title_list[int(title_pick_num) - 1]
            return title_pick
        else:
            return None
        
    
    @property
    def pathMenu(self):
        """
        选择要导出的目的路径
        :return: export_path:str
        """
        dir_pick_num = input("""
1.导出到桌面    2.导出到当前文件夹    3.导出到自定义路径    0.返回主菜单
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
    

    def askMenu(self, title, timestamp, formattime):
        """
        显示已导出数据的情况，询问是重新导出全部还是接着导出未导出部分
        :param: title: 当前要导出的对话标题
        :param: timestamp: 当前要导出的对话已导出的数据的最新时间
        """
        print(f'当前选择的对话标题为:{title}，上次导出数据的最新时间为:{formattime}({timestamp})')
        print("""
1.确认导出最新对话记录
2.重新导出所有对话记录
0.返回主菜单
"""
        )
        continue_pick_num = input('请选择导出方式:')
        if re.match(r'^\d+$', continue_pick_num):
            return int(continue_pick_num)
        else:
            return 0


def interaction():
    # 实例化读取数据库
    loadtable = LoadTable()
    # 实例化用户交互
    user_interaction = User()
    # 实例化导出
    content2file = Content2File()

    menu = user_interaction.mainMenu
    logger = Logger(menu)
        
    read_log_info = logger.readLog()
    read_log = read_log_info if read_log_info else dict()
    
    last_timestamp, formattime = read_log.get('timestamp', 0), read_log.get('time', 0)
    if not menu:
        return 
    
    export_path = user_interaction.pathMenu
    if not export_path:
        return interaction()
    
    export_way = user_interaction.askMenu(title=menu, timestamp=last_timestamp, formattime=formattime)
    if export_way == 0:
        return interaction()
    
    if export_way not in [1, 2]:
        print('输入有误')
        return

    try:
        if export_way == 1:
            kwargs = {menu: last_timestamp}
        elif export_way == 2:
            kwargs = {menu: 0}

        sql = loadtable.sqlQuery(**kwargs)
        content = loadtable.getContent(sql)
        if content[menu]:
            file_type = content2file.write(content, export_path)
            logger.writeLog(export_path, kwargs[menu], file_type)
            print('导出成功')
        else:
            print('没有可以导出的对话信息')
    except Exception as e:
        print('导出过程中出现异常：%s', str(e))
    
    time.sleep(1)
    return interaction()

def main():
    return interaction()

if __name__ == "__main__":
    main()