# spider-download
usage
```python
from spider_download import Spider

task_list = []
url = "https://assets.mixkit.co/active_storage/sfx/833/833-preview.mp3"
filename = url.split('/')[-1]
task_list.append((url, filename))

spider = Spider(task_list)
spider.save_path = r'D:\Download'
spider.proxies = {'https': 'http://127.0.0.1:7890'}
spider.run()
```