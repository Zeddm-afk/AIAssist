from openai import OpenAI
from colorama import Fore, Style, init
import time
import threading


def procedure_start():
    print(r'''

                     _ooOoo_
                    o8888888o
                    88" * "88
                    (| -_- |)
                    O\  =  /O
                 ____/`---'\____
               .'  \\|     |//  `.
              /  \\|||  :  |||//  \
             /  _||||| -:- |||||-  \
             |   | \\\  -  /// |   |
             | \_|  ''\---/''  |   |
             \  .-\__  `-`  ___/-. /
           ___`. .'  /--.--\  `. . __
        ."" '<  `.___\_<|>_/___.'  >'"".
       | | :  `- \`.;`\ _ /`;.`/ - ` : | |
       \  \ `-.   \_ __\ /__ _/   .-` /  /
  ======`-.____`-.___\_____/___.-`____.-'======
                     `=---='
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              佛祖保佑       永无Bug
  Author:zeddm
  Start_time:2025|2|16  
  v:1.2
  ''')


def get_multiline_input():
    print(Fore.GREEN + "\'_\':请输入内容，末行输入 'ok' 结束：")
    lines = []
    while True:
        line = input()
        if line == "ok":  # 输入 'END' 来结束输入
            break
        lines.append(line)  # 将每一行添加到列表中
    return "\n".join(lines)


def simple_stopwatch(stop_event):
    elapsed_time = 0  # 初始化已过时间
    while not stop_event.is_set():
        print(f"正在思考中: {elapsed_time} 秒", end="\r")  # 在同一行更新显示
        time.sleep(1)  # 暂停1秒
        elapsed_time += 1


class AI(object):

    def __init__(self):

        self.client = OpenAI(
            # 如果程序报错，切换apikey
            api_key='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'
            # api_key="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"
        )
        self.context_inf = [
            {"role": "system",
             "content": "你的回答不要使用任何富文本符号,检查你的回答并删除所有格式化标记[ **,- `',```python]。你是一为专精于网络安全的专家，负责使用中文解答我提出的问题。"},
            {"role": "user", "content": "接下来的回答中麻烦使用普通文本"}
        ]
        self.message = None

    def __str__(self):
        Updata = '1.1:添加上下文生成，优化多行内容输入'+'1.1:优化响应'+'1.2:去除单一生成，添加计时器，去除富文本标记'
        return Updata


    # 上下文生成
    def context(self,stop_event):
        # 发送请求
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=self.context_inf
        )

        message = completion.choices[0].message
        self.message = message.content
        stop_event.set()
        # return message.content

    def context_main(self, u_decision):
        # 多行适配
        if u_decision == 'y':
            u_input = get_multiline_input()
        else:
            u_input = input(Fore.GREEN + Style.BRIGHT + '\'_\'\n:')

        end_data = dict(role="user", content=f'{u_input}' + ',回答中不要使用任何富文本符号包括代码块符号')

        self.context_inf.append(end_data)
        # 多线程计数器
        stop_event = threading.Event()
        b_t = threading.Thread(target=simple_stopwatch, args=(stop_event,))
        b_t.start()

        a_t = threading.Thread(target=self.context,args=(stop_event,))
        a_t.start()
        a_t.join() #阻塞进程

        end_data = dict(role='assistant', content=f'{self.message}')
        self.context_inf.append(end_data)


        print(Fore.YELLOW + '\nopenAI:\n' + Style.BRIGHT + self.message)


if __name__ == '__main__':
    procedure_start()
    init()
    a = AI()
    while True:
        sin_con = None
        if not sin_con: sin_con = '0'

        if sin_con == '0':
            u_decision = input('是否开启多行数据适配y/n:')
            if not u_decision: u_decision = "y"
            if u_decision == 'y': print('===多行适配===')
            while True:
                try:
                    a.context_main(u_decision=u_decision)
                except:
                    print('1.token达到速率限制，尝试更换token或等待半小时','2.检查网络是否正常')


