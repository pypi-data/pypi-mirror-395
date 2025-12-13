import os.path
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from loguru import logger
from tqdm import tqdm

log_dir = "logs"
time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
logger.add(os.path.join(log_dir, f"dl_{time_str}.log"), mode="w", encoding="utf-8")


class Spider:
    def __init__(self, task_list, thread_num=1):
        """
        多线程下载
        :param task_list: [(url,file_name),(url,file_name),...]
        :param thread_num: 线程数
        """
        self.task_list = task_list
        self.thread_num = thread_num
        self.save_path = os.path.join(
            os.path.expanduser("~"), "Desktop", "SpiderDownload"
        )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        self.proxies = None

    def _download(self, url, file_path):
        if os.path.exists(file_path):
            logger.info(f"{url} 已下载，跳过\n")
            return
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        resp = requests.get(
            url, headers=self.headers, stream=True, timeout=10, proxies=self.proxies
        )
        resp.raise_for_status()
        # 获取文件总大小
        total_size = int(resp.headers.get("content-length", 0))
        if total_size < 5 * 1024 * 1024:  # 小于5MB的文件，不显示进度条
            with open(file_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            with open(file_path, "wb") as f, tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    desc=file_path,
                    initial=0,
                    ascii=True,
            ) as pbar:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        time.sleep(random.uniform(1, 2))
        res, size = self._check_result(file_path)
        if res:
            logger.success(f"{file_path}下载成功,{size=}kb")
        else:
            raise Exception(f"{file_path}下载失败,{size=}kb")

    @staticmethod
    def _check_result(file_path):
        file = Path(file_path)
        size_kb = file.stat().st_size // 1024
        if size_kb < 1:
            logger.info(f"{file}下载失败，删除文件,size={size_kb}kb")
            file.unlink()
            return False, size_kb
        return True, size_kb

    @staticmethod
    def _write_failed_txt(task):
        with open(
                os.path.join(log_dir, "failed.txt"),
                "a",
                encoding="utf-8",
        ) as f:
            f.write(str(task))
            f.write(",")
            f.write("\n")

    @staticmethod
    def _clean_filename(filename):
        return re.sub(r'[\\/:*?"<>|]', '_', filename)

    def _do_task(self, task, retry):
        logger.info(f"下载链接: {task[0]}")
        for i in range(retry + 1):
            try:
                self._download(task[0], os.path.join(self.save_path, self._clean_filename(task[1])))
                break
            except Exception as e:
                logger.error(e)
                time.sleep(2)
        else:
            if retry > 0:
                logger.warning(f"{task[0]}重试{retry}次,下载失败")
            else:
                logger.warning(f"{task[0]}下载失败")
            # 下载失败，将失败任务写入文件
            self._write_failed_txt(task)
            Path(os.path.join(self.save_path, task[1])).unlink(missing_ok=True)

    # 启动多线程爬虫
    def run(self, retry=0):
        logger.info(f"文件下载目录：{self.save_path}")
        with ThreadPoolExecutor(max_workers=self.thread_num) as executor:
            for task in self.task_list:
                executor.submit(self._do_task, task, retry)


if __name__ == "__main__":
    spider = Spider(
        task_list=[
            (
                "https://live.staticflickr.com/65535/48192531236_8c6faf300_4k.jpg",
                "48192531236_8c6faf309_4k.jpg",
            ),
        ],
        thread_num=4,
    )
    spider.run(retry=0)
