import os
from settings import *


# SSH测试连接设备
def connect_test(host):
    
    try:
        flag, conn = connect_handler(host)
        if flag:
            # 获取到设备名称则表示ssh连接测试成功
            hostname = conn.find_prompt()
            result = '{} SSH测试连接成功,获取到设备提示符： {}'.format(host['ip'], hostname)
            print(result)
            conn.disconnect()
            sucessful_list.append(result)
        else:
            # SSH连接测试失败，同记录
            result = '{} SSH测试连接失败,未获取到设备提示符'.format(host['ip'])
            failed_list.append(result)

    except Exception as e:
        print("connect_test Failed: {}".format(e))
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
            pool.apply_async(connect_test, args=(host,))
        pool.close()
        pool.join()

        return task_name, sucessful_list, failed_list

    except Exception:
        print('Something Wrong!')


if __name__ == "__main__":
    main()
