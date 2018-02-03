# coding: UTF-8
import os
import time
import json
import logging
import datetime
import urllib.parse
import urllib.request

from selenium import webdriver

# 事前準備
# pythonにパスは通しておくこと

# 事前に必要なライブラリ
# python -m pip install selenium

# windowが閉じない場合はchromedriver.exeを最新に更新してみる

now = datetime.datetime.now()

LOG_LEVEL = 'INFO'

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s [%(levelname)s] %(module)s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
)
logfile=logging.FileHandler("logs/" + "application_log_{0:%Y%m%d}.txt".format(now), "a");
logfile.setLevel(logging.INFO)
logging.getLogger('').addHandler(logfile)

logger = logging.getLogger(__name__)


def main():
    # --------------------------
    # jsonファイルの存在チェック
    # --------------------------
    path = "./setting.json"

    if os.path.isfile(path) == 0:
        logger.error(path + "が見つかりません。")
        exit()

    # --------------------------
    # jsonファイルの読み込み
    # --------------------------

    json_file = open(path, 'r')
    dictionary = json.load(json_file)
    logger.info(dictionary)

    exists_param_json(dictionary, ['browser', 'urls', 'request_sleep_second', 'loop_count', 'loop_sleep_second'])

    urls = dictionary['urls']
    browser = dictionary['browser']
    loop_count = dictionary['loop_count']
    loop_sleep_second = dictionary['loop_sleep_second']
    request_sleep_second = dictionary['request_sleep_second']

    # --------------------------
    # 出力ファイルを開く
    # --------------------------

    export_file_name = "result_reqeat_access_{0:%Y%m%d-%H%M%S}.txt".format(now)

    logger.info("RepeatAccessApp --- start ---")

    # ブラウザを開く
    driver = webdriver.Chrome()

    for i in range(1, loop_count + 1):

        urls_length = len(urls)

        for j, url in enumerate(urls):

            # 指定秒間待機
            time.sleep(request_sleep_second)

            num = (i - 1) * urls_length + j  # 行番号

            # 出力フォーマット
            format = "[{num}] {url} [{message}] : {reason}"
            num_format = "%04d"

            o = urllib.parse.urlparse(url)
            if len(o.scheme) > 0:

                req = urllib.request.Request(url)

                try:
                    result = urllib.request.urlopen(req)
                    message = format.format(num=num_format % num, url=url, message="HTTP Response", reason=result.code)

                    logger.info(message)
                    f = open('./logs/' + export_file_name, 'a')
                    f.write(message + '\n')
                    f.close()

                except urllib.error.HTTPError as e:

                    message = format.format(num=num_format % num, url=url, message="HTTP Response Error",
                                            reason=e.code)

                    logger.info(message)
                    f = open('./logs/' + export_file_name, 'a')
                    f.write(message + '\n')
                    f.close()
                    continue

                except urllib.error.URLError as e:

                    message = format.format(num=num_format % num, url=url, message="URL Error", reason=e.reason)

                    logger.info(message)
                    f = open('./logs/' + export_file_name, 'a')
                    f.write(message + '\n')
                    f.close()
                    continue

                # urlを開く。
                driver.get(url)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            else:
                logger.info(url + "はURLではありません。")

        time.sleep(loop_sleep_second)

    # ブラウザを終了する。
    driver.close()

    logger.info("RepeatAccessApp --- end ---")


def exists_param_json(dictionary, names):
    for name in names:
        if name not in dictionary:
            logger.error("jsonファイルに" + name + "が見つかりません。")
            exit()


if __name__ == '__main__':
    main()
