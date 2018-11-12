# -***coding=utf-8***-
#!/usr/bin/env python
import requests

# 文件路径
path = './save'
num = 1


def response(flow):
    global num
    # 经测试发现视频url前缀主要是3个
    target_urls = ['http://v1-dy.ixigua.com/', 'http://v9-dy.ixigua.com/',
                   'http://v3-dy.ixigua.com/']
    for url in target_urls:
        # 过滤掉不需要的url
        if flow.request.url.startswith(url):
            # 设置视频名
            filename = path + str(num) + '.mp4'
            # 使用request获取视频url的内容
            # stream=True作用是推迟下载响应体直到访问Response.content属性
            res = requests.get(flow.request.url, stream=True)
            # 将视频写入文件夹
            with open(filename, 'ab') as f:
                f.write(res.content)
                f.flush()
                print(filename + '下载完成')
            num += 1