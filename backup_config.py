import os
from settings import *


# 执行display/show命令
def run_cmd(task_name, host, cmds, enable=False):

    enable = True if host['secret'] else False
    flag, conn = connect_handler(host)
    try:
        if flag:
            # 从返回提示符获取设备名称
            hostname = conn.find_prompt().replace('<', '').replace('>', '').replace('#', '').strip()
            print("正在获取设备[{}]的配置……".format(hostname))
            # 文件保存路径和文件名 '当前目录\\EXPORT\\当天日期\\config_backup\\hostname+ip+当前时间.txt'
            logtime = datetime.now().strftime("%H%M%S")
            output_filename = hostname + '_' + host['ip'] + '_' + logtime + '.txt'

            if cmds:
                # 判断单元表里命令是否为空值
                output = ''
                for cmd in cmds:
                    if enable:
                        # 判断是否需要进入enable特权模式
                        conn.enable()
                        output +=  '\n' + '=' * 100 + '\n' + cmd.center(100, '=') + '\n'
                        output += conn.send_command(command_string=cmd)

                    else:
                        output +=  '\n' + '=' * 100 + '\n' + cmd.center(100, '=') + '\n'
                        output += conn.send_command(command_string=cmd)
            else:
                # 使用ftp/tftp/sftp/scp
                pass
            conn.disconnect()
            
            # write_data
            write_to_file(task_name, output_filename, output)
            sucessful_list.append(host['ip'] + ' ' + hostname)
        else:
            failed_list.append(conn)
            pass

    except Exception as e:
        print(f"run_cmd Failed: {e}")

@timer
@result_write
@result_count
# 代码运行主体框架设计
def main():
    try:
        # 获取当前运行的Python文件的路径
        current_file_path = os.path.abspath(__file__)
        # 提取文件名
        task_name = os.path.basename(current_file_path)
        print(f'\n当前执行的脚本是[{task_name}]，程序正在执行中>>>\n')

        hosts = get_device_info(task_name)
        pool = t_pool
        # hosts是一个返回的生成器，需要进行循环遍历
        for host in hosts:
            # 单线程同步输出方式执行
            # run_cmd(host, host['cmd_list'])
            # 多线程异步处理
            pool.apply_async(run_cmd, args=(task_name, host, host['cmd_list']))
        pool.close()
        pool.join()

        return task_name, sucessful_list, failed_list

    except Exception:
        print('Something Wrong!')


if __name__ == "__main__":
    main()
