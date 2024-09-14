import psutil
import time
import subprocess
import os

# 获取当前脚本的进程 ID
def get_current_pid():
    return os.getpid()

# 获取指定进程的 CPU 使用率
def get_cpu_usage(pid):
    try:
        process = psutil.Process(pid)
        return process.cpu_percent(interval=1)
    except psutil.NoSuchProcess:
        return None

# 获取指定进程的内存使用情况
def get_memory_usage(pid):
    try:
        process = psutil.Process(pid)
        return process.memory_info().rss
    except psutil.NoSuchProcess:
        return None

# 获取指定进程的磁盘 I/O 情况
def get_disk_io(pid):
    try:
        process = psutil.Process(pid)
        return process.io_counters()
    except psutil.NoSuchProcess:
        return None

# 获取指定进程的线程数
def get_thread_count(pid):
    try:
        process = psutil.Process(pid)
        return process.num_threads()
    except psutil.NoSuchProcess:
        return None

# 获取指定进程的上下文切换次数
def get_context_switches(pid):
    try:
        process = psutil.Process(pid)
        return process.num_ctx_switches()
    except psutil.NoSuchProcess:
        return None

# 获取指定进程的网络 I/O 情况
def get_network_io(pid):
    try:
        process = psutil.Process(pid)
        return process.io_counters()
    except psutil.NoSuchProcess:
        return None

# 获取系统级别的 CPU 负载
def get_system_cpu_load():
    return psutil.cpu_percent(interval=1)

# 生成 HTML 表格
def generate_html_table(data):
    html = """
    <html>
    <head>
        <style>
            table {
                width: 80%;
                border-collapse: collapse;
                margin: 20px auto;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h2 style="text-align: center;">性能监控结果</h2>
        <table>
            <tr>
                <th>部分</th>
                <th>CPU 使用率 (%)</th>
                <th>内存使用 (MB)</th>
                <th>磁盘读取 (KB)</th>
                <th>磁盘写入 (KB)</th>
                <th>线程数</th>
                <th>上下文切换次数</th>
                <th>网络接收 (KB)</th>
                <th>网络发送 (KB)</th>
                <th>系统 CPU 负载 (%)</th>
            </tr>
    """
    for row in data:
        html += f"""
            <tr>
                <td>{row['part']}</td>
                <td>{row['cpu_usage']}</td>
                <td>{row['memory_usage']}</td>
                <td>{row['disk_read']}</td>
                <td>{row['disk_write']}</td>
                <td>{row['thread_count']}</td>
                <td>{row['context_switches']}</td>
                <td>{row['network_recv']}</td>
                <td>{row['network_send']}</td>
                <td>{row['system_cpu_load']}</td>
            </tr>
        """
    html += """
        </table>
    </body>
    </html>
    """
    return html

# 主函数
def main():
    # 获取当前脚本的进程 ID
    current_pid = get_current_pid()
    print(f"当前脚本的进程 ID: {current_pid}")

    # 启动 main.py 和 test.py 脚本
    main_process = subprocess.Popen(['python', 'main.py', 'orig.txt', 'orig_0.8_add.txt', 'result.txt'])
    test_process = subprocess.Popen(['python', 'test.py'])

    main_pid = main_process.pid
    test_pid = test_process.pid

    print(f"main.py 脚本的进程 ID: {main_pid}")
    print(f"test.py 脚本的进程 ID: {test_pid}")

    # 监控结果数据
    data = []

    try:
        while main_process.poll() is None or test_process.poll() is None:
            if main_process.poll() is None:
                cpu_usage = get_cpu_usage(main_pid)
                memory_usage = get_memory_usage(main_pid)
                disk_io = get_disk_io(main_pid)
                thread_count = get_thread_count(main_pid)
                context_switches = get_context_switches(main_pid)
                network_io = get_network_io(main_pid)
                system_cpu_load = get_system_cpu_load()

                # 记录监控结果
                data.append({
                    'part': 'main.py',
                    'cpu_usage': cpu_usage,
                    'memory_usage': f"{memory_usage / 1024 / 1024:.2f}",
                    'disk_read': f"{disk_io.read_bytes / 1024:.2f}" if disk_io else "N/A",
                    'disk_write': f"{disk_io.write_bytes / 1024:.2f}" if disk_io else "N/A",
                    'thread_count': thread_count,
                    'context_switches': context_switches.voluntary + context_switches.involuntary,
                    'network_recv': f"{network_io.read_bytes / 1024:.2f}" if network_io else "N/A",
                    'network_send': f"{network_io.write_bytes / 1024:.2f}" if network_io else "N/A",
                    'system_cpu_load': system_cpu_load
                })

            if test_process.poll() is None:
                cpu_usage = get_cpu_usage(test_pid)
                memory_usage = get_memory_usage(test_pid)
                disk_io = get_disk_io(test_pid)
                thread_count = get_thread_count(test_pid)
                context_switches = get_context_switches(test_pid)
                network_io = get_network_io(test_pid)
                system_cpu_load = get_system_cpu_load()

                # 记录监控结果
                data.append({
                    'part': 'test.py',
                    'cpu_usage': cpu_usage,
                    'memory_usage': f"{memory_usage / 1024 / 1024:.2f}",
                    'disk_read': f"{disk_io.read_bytes / 1024:.2f}" if disk_io else "N/A",
                    'disk_write': f"{disk_io.write_bytes / 1024:.2f}" if disk_io else "N/A",
                    'thread_count': thread_count,
                    'context_switches': context_switches.voluntary + context_switches.involuntary,
                    'network_recv': f"{network_io.read_bytes / 1024:.2f}" if network_io else "N/A",
                    'network_send': f"{network_io.write_bytes / 1024:.2f}" if network_io else "N/A",
                    'system_cpu_load': system_cpu_load
                })

            time.sleep(1)
    except KeyboardInterrupt:
        print("监控中断")
    finally:
        main_process.terminate()
        test_process.terminate()
        main_process.wait()
        test_process.wait()
        print("main.py 和 test.py 脚本已终止")

    # 生成 HTML 表格并保存到文件
    html_content = generate_html_table(data)
    with open('monitor_results.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("监控结果已保存到 monitor_results.html 文件中。")

if __name__ == "__main__":
    main()
