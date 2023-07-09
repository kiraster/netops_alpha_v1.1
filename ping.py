import os
import ping3
import time
from settings import *


# 批量ping测试
def ping_test(host):
    
    ping3.EXCEPTIONS = True
    time.sleep(2)
    try:
        ping3.ping(host['ip'])
        res = "{:<18}ping测试成功.".format(host['ip'])
        print(res)
        sucessful_list.append(host['ip'])
    except ping3.errors.HostUnknown:
        res = "{:<18}ping测试失败. Host unknown error raised.".format(host['ip'])
        print(res)
        failed_list.append(host['ip'])
    except ping3.errors.PingError:
        res = "{:<18}ping测试失败. A ping error raised.".format(host['ip'])
        print(res)
        failed_list.append(host['ip'])


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
            pool.apply_async(ping_test, args=(host,))
        pool.close()
        pool.join()

        return task_name, sucessful_list, failed_list

    except Exception:
        print('Something Wrong!')


if __name__ == "__main__":
    main()
