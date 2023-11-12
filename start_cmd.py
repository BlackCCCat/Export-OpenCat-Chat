import click
import os

from load_table import LoadTable
from write_file import Content2File
from export_log import Logger

loadtable = LoadTable()
content2file = Content2File()


def export_all_dialogues(title, out):
    logger = Logger(title)
    # 指定时间为0，导出所有回话记录
    kwargs = {title: 0}
    sql = loadtable.sqlQuery(**kwargs)
    content = loadtable.getContent(sql)
    if content[title]:
        file_type = content2file.write(content, out)
        logger.writeLog(out, kwargs[title], file_type)
        print('导出成功')
    else:
        print('没有可以导出的对话信息')


def export_new_dialogues(title, out):
    logger = Logger(title)
    read_log_info = logger.readLog()
    read_log = read_log_info if read_log_info else dict()
    
    last_timestamp = read_log.get('timestamp', 0)

    # 指定时间为最新时间，导出最新回话记录
    kwargs = {title: last_timestamp}
    sql = loadtable.sqlQuery(**kwargs)
    content = loadtable.getContent(sql)
    if content[title]:
        file_type = content2file.write(content, out)
        logger.writeLog(out, kwargs[title], file_type)
        print('导出成功')
    else:
        print('没有可以导出的对话信息')


@click.command()
@click.option('--title', '-t', required=True, help='Title of the dialogue to be exported.') # 标题为必要参数
@click.option('--out', '-o', required=True, type=click.Path(), help='Output path where the files will be saved.') # 输出路径为必要参数
@click.option('--all', 'export_type', flag_value='all', help='Export all dialogues.') # 标记是否导出全部
@click.option('--new', 'export_type', flag_value='new', help='Export new dialogues.') # 标记是否导出最新
def export(title, out, export_type):
    """Export dialogue with a given title to the specified path."""
    if not export_type:
        raise click.UsageError('You must provide an export type (--all or --new).')

    click.echo(f"Exporting dialogue '{title}' to '{out}'.")

    # 根据export_type的值实现不同的导出逻辑
    if export_type == 'all':
        click.echo("Exporting all dialogues.")
        export_all_dialogues(title, out)
    elif export_type == 'new':
        click.echo("Exporting the newest part of the dialogue.")
        export_new_dialogues(title, out)


if __name__ == '__main__':
    export()