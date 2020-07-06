# Version: Python 3.7.x
# install additional module using command pip install missing_module_name
import requests
import json
import string
import random
import threading
from queue import Queue
import socket
from sys import argv

threads_count = 40
socket.setdefaulttimeout(5)

class myThread(threading.Thread):
    def __init__(self, queue, *args):
        self.queue = queue
        self._args = args
        threading.Thread.__init__(self)

    def rand_pass(self):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(8))

    def is_insta_acc(self, cred):
        url = "https://www.instagram.com/accounts/login/ajax/"
        params = {
            "username": cred,
            "enc_password": "#PWD_INSTAGRAM_BROWSER:9:1594038549:AVdQAFYARyjVDVdsDuvQBvOZTfOuTaXSqWDboo3rlMZxTSEaPP/LzdcKsQn3x3Fii+WVRciyUpMlkjJi81KH2FE/fYV5emI9h7u8cINWVoWNKGF5ajvCLWqinVIfLgjsWO0xMXPLZxbYtoGDiC4SOMqxGPc=",
            "queryParams": "{\"source\":\"auth_switcher\"}",
            "optIntoOneTap": "false"
            }
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,bn;q=0.8",
            "content-length": "126",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "csrftoken=YG424J8dUtwG0wkhpFviRT7XJloAEB2g; mid=W5uoAwAEAAHQMrm9fx_BelLIVThw; mcd=3; rur=FRC",
            "dnt": "1",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/accounts/login/?source=auth_switcher",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "x-csrftoken": "YG424J8dUtwG0wkhpFviRT7XJloAEB2g",
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "0",
            "x-instagram-ajax": "d3ae0124792a-hot",
            "x-requested-with": "XMLHttpRequest"
            }
        try:
            return requests.post(url, headers=headers, data=params).text
        except:
            print("Site cannot be accessed! Increase timeout ...")
            return json.dumps({"user":"False"})

    def run(self):
        while True:
            acc = None
            try:
                acc = self.queue.get(timeout=1)
            except:
                return
            low_lim = int(acc.split(":")[0])
            high_lim = int(acc.split(":")[1])
            for x in range(low_lim, high_lim+1):
                print(str(x)+argv[1])
                try:
                    out = json.loads(self.is_insta_acc("+"+str(x)+argv[1]))
                    ans = out['user']
                except:
                    ans = "False"
                if str(ans) == "True":
                    print("good")
                    with open("success.txt", "a+") as suc_file:
                        suc_file.write("+" + str(x) + argv[1] + "\n")
            self.queue.task_done()

if __name__ == "__main__":
    queue= Queue()
    threads = []
    for i in range(threads_count):
        worker = myThread(queue, i)
        worker.setDaemon(True)
        worker.start()
        threads.append(worker)
    with open("list.txt", "r") as main_file:
        for line in main_file:
            line = line.replace("\n", "").strip()
            if line == "":
                continue
            queue.put(line)
        for item in threads:
            item.join()
