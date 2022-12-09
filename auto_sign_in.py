# coding=UTF-8

import json
import logging
import argparse
import requests


class CheckIn(object):
    client = requests.Session()
    login_url = "https://w1.v2free.net/auth/login"
    sign_url = "https://w1.v2free.net/user/checkin"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.masked_username = self.email_masking(username)

    # 1234567@qq.com -> 1******@q*.com
    def email_masking(self, email):
        length = len(email)
        at_index = email.rfind('@')
        dot_index = email.rfind('.')
        masked_email = email[0].ljust(at_index, '*') + email[at_index:at_index + 2] + \
            email[dot_index:length].rjust(length - at_index - 2, '*')
        return masked_email

    # 谷歌浏览器输入 about:version 获取本机 User-Agent
    def check_in(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Referer": "https://w1.v2free.net/auth/login",
        }
        data = {
            "email": self.username,
            "passwd": self.password,
            "code": "",
        }
        self.client.post(self.login_url, data=data, headers=headers)

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Referer": "https://w1.v2free.net/user",
        }
        response = self.client.post(self.sign_url, headers=headers)

        logging.info(self.masked_username + "\t" + response.json()["msg"])


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s\t%(levelname)s\t%(message)s"
    logging.basicConfig(filename='flow.log',
                        level=logging.INFO, format=LOG_FORMAT)

    parser = argparse.ArgumentParser(description='V2ray签到脚本')
    parser.add_argument('--username', type=str, help='账号')
    parser.add_argument('--password', type=str, help='密码')
    args = parser.parse_args()
    helper = CheckIn(args.username, args.password)
    helper.check_in()