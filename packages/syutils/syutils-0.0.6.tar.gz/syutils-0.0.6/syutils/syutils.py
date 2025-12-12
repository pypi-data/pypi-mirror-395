import unittest
import re
import sys
import os
import datetime
import json
import subprocess
import time
import threading
import queue
import pickle
from functools import wraps
from trade_date import trade_date




def srun(cmd_queue, noprint, stop_on_error, lock, stop_flag):
    '''
    顺序执行命令
    '''
    while not cmd_queue.empty() and not stop_flag["stop"]:
        cmd = cmd_queue.get()
        try:
            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            if not noprint:
                with lock:
                    print(f"Runcmd {cmd}")

            # 实时读取 stdout/stderr
            for line in process.stdout:
                if not noprint:
                    with lock:
                        print(line.rstrip().decode("utf-8"))

            for line in process.stderr:
                with lock:
                    print(line.rstrip().decode("utf-8"), file=sys.stderr)

            process.wait()

            if process.returncode != 0:
                with lock:
                    print(f"ERROR return {process.returncode} {cmd}", file=sys.stderr)
                if stop_on_error:
                    stop_flag["stop"] = True
                    break

        except Exception as e:
            with lock:
                print(f"ERROR execute {cmd}\n{e}", file=sys.stderr)
            if stop_on_error:
                stop_flag["stop"] = True
                break
        finally:
            cmd_queue.task_done()



def mrun(commands, proc_count, noprint, stop_on_error):
    """并行执行命令"""
    cmd_queue = queue.Queue()
    for cmd in commands:
        cmd_queue.put(cmd)

    lock = threading.Lock()
    stop_flag = {"stop": False}
    threads = []

    for _ in range(proc_count):
        t = threading.Thread(target=srun, args=(cmd_queue, noprint, stop_on_error, lock, stop_flag))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

class TickerTimer:
    """打点计时器 - 用于记录和输出时间间隔"""
    def __init__(self,name=""):
        self.name = name
        """初始化计时器,记录创建时间"""
        self.start_time = time.time()
        self.last_tick_time = self.start_time
    
    def tick(self, message="",print_out=True,ndigits=4) -> str:
        """打点计时,记录当前时间并输出时间间隔"""
        current_time = time.time()
        total_elapsed = current_time - self.start_time
        interval = current_time - self.last_tick_time
        self.last_tick_time = current_time
        output=[self.name,message,round(interval,ndigits),round(total_elapsed,ndigits)]
        output =[x for x in output if x!=""]
        print_str = "\t".join(str(x) for x in output)
        if print_out:
            print(print_str)
        return [interval,total_elapsed]


def replace_macro(cmd, dt=0) -> str:
    """
    替换<DATE> <YEAR>等为指定日期的年月日
    """
    dt = str(dt or str(trade_date.today()))
    pred = str(trade_date.prebizd(dt))
    macro_dict = {
        "PRED": pred,
        "TODAY": dt,
        "DATE": dt,
        "YEAR": dt[0:4],
        "MONTH": dt[4:6],
        "DAY": dt[6:],
    }
    for k in macro_dict.keys():
        cmd = cmd.replace(f"<{k}>", macro_dict[k])
    return cmd
def run_func_limit_time(func,func_args,limit_time):
    '''
    运行一个任务并设定最长运行时间
    用进程的原因是线程停不了
    p=lambda x,y:print(x+y)
    print(run_func_limit_time(p,[10,24],2))
    '''
    from multiprocessing import Process
    p = Process(target=func, args=func_args)
    p.start()
    p.join(timeout=limit_time)
    if p.exitcode== 0:
        return 0
        #print(f"Done finishing child process with exit code {p.exitcode}")
    else:
        p.terminate()
        return -1
def get_last_line(filename):
    """
    读取最后一行
    get last line of a file
    :param filename: file name
    :return: last line or None for empty file
    """
    try:
        filesize = os.path.getsize(filename)
        if filesize == 0:
            return None
        else:
            count=0
            block_size = 4096                       #文件占用空间一般最小是4k
            res=filesize%block_size or block_size   
            offset=res + block_size                 #首次读两个整块 如果这都凑不够一行多 那就指数增加读取数量
            with open(filename, 'rb') as fp:        # to use seek from end, must uss mode 'rb'
                while offset < filesize:  # offset cannot exceed file size
                    fp.seek(-1*offset, 2)   # read # offset chars from eof(represent by number '2')
                    lines = fp.readlines()   # read from fp to eof
                    if len(lines) >= 2:  # if contains at least 2 lines
                        return lines[-1]   # then last line is totally included
                    count=count+1
                    offset=(2**count)*block_size # double the read size
                fp.seek(0)
                lines = fp.readlines()
                return lines[-1]
    except FileNotFoundError:
        print(f'''get last line {filename}  not found!''')


def get_exist_file(file_name):
    """
    判断文件是否存在包括对应的gz和7z
    :param file_name: 文件名
    :return: 文件名
    """
    if os.path.exists(file_name):
        return file_name
    elif os.path.exists(file_name+'.gz'):
        return file_name+'.gz'
    elif os.path.exists(file_name+'.7z'): 
        return file_name+'.7z'
    raise FileNotFoundError(f'File {file_name}(.7z/.gz) not found!')
def read_gz_flow(filename):
    import gzip
    with gzip.open(filename, 'rb') as f:
        for line in f:
            yield line.decode().strip()
    f.close()
def read_7z_flow(filename):
    from py7zr import SevenZipFile
    archive = SevenZipFile(filename)
    name=archive.getnames()[0]
    content = archive.read(name)[name]
    for line in content:
        yield line.decode().strip()
    archive.close()
def read_file_flow(filename):
    filename=get_exist_file(filename)
    if filename.endswith('.7z'):
        return read_7z_flow(filename)
    elif filename.endswith('.gz'):
        return read_gz_flow(filename)
    else:
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip()

def read_7z_pd(filename,**argv):
    import pandas as pd
    from py7zr import SevenZipFile
    archive = SevenZipFile(filename)
    name=archive.getnames()[0]
    content = archive.read([name])[name]
    return pd.read_csv(content,**argv)
def read_gz_pd(filename,**argv):
    import gzip
    import pandas as pd
    with gzip.open(filename, 'rb') as f:
        return pd.read_csv(f,**argv)        

def read_file_pd(filename,**argv):    
    filename=get_exist_file(filename)
    if filename.endswith('.7z'):
        return read_7z_pd(filename,**argv)
    elif filename.endswith('.gz'):
        return read_gz_pd(filename,**argv)
    else:
        import pandas as pd
        return pd.read_csv(filename,**argv)

def error_callback(error):
    print(f"Error info: {error}")

def getsize(file_path):
    if not os.path.exists(file_path):
        print(f"{file_path} not exists!")
    else:
        fsize = os.path.getsize(file_path)
        div_n = 0
        while fsize >= 1024:
            fsize /= 1024
            div_n += 1
        size_dict = dict(zip([0,1,2,3, 4], ['B', 'KB', 'MB', 'GB', 'TB']))
        return f"{round(fsize, 2)} {size_dict[div_n]}"
        

def handle_mid_call(func, args, pkl_filepath=None, reload=False, force_save=False, ifprint=True, dump_protocol=None, **kwargs):
    """
    保存路径pkl_filepath
    存在文件就读文件内容返回;
    不存在文件就运行函数并保存返回值;
    """
    if os.path.exists(pkl_filepath) and not reload:
        if ifprint:
            print(f'Read data from {pkl_filepath}, {getsize(pkl_filepath)}')
        with open(pkl_filepath, 'rb') as f:
            res = pickle.load(f)
    else:
        res = func(*args, **kwargs)
        with open(pkl_filepath, 'wb') as f:
            pickle.dump(res, f, protocol=dump_protocol)
        if force_save:
            if ifprint:
                print(f'Save data to {pkl_filepath}, {getsize(pkl_filepath)}')
        else:
            if getsize(pkl_filepath).split(' ')[1] == 'B':
                print(f'Data too small {pkl_filepath}, {getsize(pkl_filepath)}')
                os.system(f"rm -f {pkl_filepath}")
            else:
                if ifprint:
                    print(f'Save data to {pkl_filepath}, {getsize(pkl_filepath)}')
    return res

# 定义一个函数，等待文件，默认等待时间为1秒
def wait_file(file, sec=1):
    while True:
        if os.path.isfile(file):
            return
        time.sleep(sec)


# 定义一个函数，等待文件列表，默认等待时间为1秒
def wait_files(files, sec=1):
    while True:
        if all(os.path.isfile(file) for file in files):
            return
        time.sleep(sec)


def read_cmd(cmd):
    """
    流式读取命令行的标注输出
    """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b"" and process.poll() is not None:
            break
        if output:
            yield str(output.strip(), encoding="utf-8")


def run_cmd(cmd, dryrun=0):
    if dryrun:
        print("Dryrun ", cmd)
    else:
        print("Realrun", cmd)
        os.system(cmd)


def printt(*args, **kw):
    print(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), *args, **kw)


def except_msg(msg):
    input(f"\n\n{msg}\n按回车键退出\n\n")
    exit()


def dump_dict(d):
    return json.dumps(d, sort_keys=True, indent=2, ensure_ascii=False)


def err(*args, **kw):
    print(*args, **kw, file=sys.stderr)


def mkpath(path):
    if os.path.exists(path):
        return
    try:
        os.makedirs(path,exist_ok = True)
    except Exception as e:
        print("Error:", e)


def get_dir(file):
    return os.path.dirname(os.path.realpath(file))


def get_ip():
    """
    ip route get 1 | awk '{print $NF;exit}'
    """
    ip = "127.0.0.1"
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_internet_ip():
    import requests
    import re
    req = requests.get("http://txt.go.sohu.com/ip/soip")
    return re.findall(r"\d+.\d+.\d+.\d+", req)


def make_dir(dir_name):
    mkpath(dir_name)

def uniq_symbol(old_symbol, market=0):
    new_symbol = ""
    old_symbol = str(old_symbol)
    old_symbol = old_symbol.upper()
    old_symbol = (6 - len(old_symbol)) * "0" + old_symbol
    market = int(market)
    if market > 0 and re.match(r"^\d{6}$", old_symbol):
        if market == 1:
            new_symbol = f"{old_symbol[0:6]}.SH"
        elif market == 2:
            new_symbol = f"{old_symbol[0:6]}.SZ"
        else:
            raise Exception(
                f"ERROR: not vaild symbol format {old_symbol} {market} uniq_symbol"
            )
    elif re.match(r"^S[H|Z]\d{6}$", old_symbol):
        new_symbol = f"{old_symbol[2:]}.{old_symbol[0:2]}"
    elif re.match(r"^\d{6}\.S[H|Z]$", old_symbol):
        new_symbol = old_symbol
    elif re.match(r"^\d{6}_\d$", old_symbol):
        if old_symbol[-1] == "1":
            new_symbol = f"{old_symbol[:6]}.SH"
        elif old_symbol[-1] == "2":
            new_symbol = f"{old_symbol[:6]}.SZ"
    elif re.match(r"^\d{6}$", old_symbol):
        if old_symbol[0] in ["6", "5"]:
            new_symbol = f"{old_symbol[:6]}.SH"
        else:
            new_symbol = f"{old_symbol[:6]}.SZ"
    else:
        raise Exception(
            f"ERROR: symbol format not support {old_symbol} uniq_symbol"
        )
    return new_symbol


def cmd_parse(cmd):
    """
    cmd=cmd_parse(sys.argv)
    """
    argDict = {}
    last_key = False
    for i, j in enumerate(cmd):
        if i == 0:
            continue
        if j[0] == "-":
            while j[0] == "-":
                j = j[1:]
            argDict[j] = True
            last_key = j
        else:
            if last_key != False:
                argDict[last_key] = j
            else:
                argDict[j] = True
            last_key = False
    return argDict


def timer(func):
    """Function Level Timer via Decorator"""
    @wraps(func)
    def timed(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        elapse = (end - start).total_seconds()
        print(f"||{func.__name__}|| Using time: {elapse} s")
        return result
    return timed


def time_used(*dargs):
    def time_(f):
        @wraps(f)
        def count_time(*args, **kw):
            start = datetime.datetime.now()
            f_res = f(*args, **kw)
            end = datetime.datetime.now()
            interval = (end - start).seconds
            times = datetime.timedelta(seconds=interval)
            print("[{}]开始时间为：{}, 结束时间：{}，耗时{}".format(dargs, start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'), times))
            return f_res
        return count_time
    return time_

class TestDict(unittest.TestCase):
    def test_cmd_parse(self):
        d = cmd_parse("NAN -a 1 --b 2 e f -c 3 w".split(" "))
        self.assertEqual(d["a"], "1")
        self.assertEqual(d["b"], "2")
        self.assertEqual(d["e"], True)
        with self.assertRaises(KeyError):
            d["empty"]

    def test_uniq_symbol(self):
        self.assertEqual(uniq_symbol("SH600000"), "600000.SH")
        self.assertEqual(uniq_symbol("600000.SH"), "600000.SH")
        self.assertEqual(uniq_symbol("600000_1"), "600000.SH")
        self.assertEqual(uniq_symbol("600000", 1), "600000.SH")
        self.assertEqual(uniq_symbol("sz000001"), "000001.SZ")
        self.assertEqual(uniq_symbol("000001.sz"), "000001.SZ")
        self.assertEqual(uniq_symbol("000001_2"), "000001.SZ")
        self.assertEqual(uniq_symbol("000001", 2), "000001.SZ")
        with self.assertRaises(Exception):
            uniq_symbol("SH6000000")
        with self.assertRaises(Exception):
            uniq_symbol("600000", 3)


if __name__ == "__main__":
    unittest.main()
