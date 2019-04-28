import json
import lxml
import requests
from lxml import etree
#使用ie的User-Agent
headers={"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"}
res = requests.get("https://www.qiushibaike.com/text/page/2/",headers=headers)
#将html转换成html.dom格式
html = etree.HTML(res.text)
#匹配所有需要提取的文本，含评论，发帖人、点赞等
content_list = html.xpath('//*[contains(@id,"qiushi_tag_")]')

for item in content_list:
    #使用try，防止出现匹配到空列表，indexerror报错
    try:
        #建议用chrome的xpath里匹配，如遇到不同的div，如div[1]或div[2]，可全部用div代替
        #发帖人
        name = item.xpath('./div[1]//h2/text()')[0].strip("\n")#每个列表只有一个或0个元素，去掉字符串带的换行符
        #发帖人年龄
        age = item.xpath('./div[1]/div/text()')[0].strip("\n")
        #帖子内容
        text = item.xpath('./a/div/span/text()')[0].strip("\n")
    except IndexError:
        pass
    #将每个帖子对应的发帖人，年龄，内容组合成一个字典
    items ={"name":name,
           "age":age,
           "text":text}
    #使用ab，二进制追加的方式，写入每个帖子
    with open("qiushi.json","ab") as f:
        #用json.dumps将python字典格式转换为json字符串，加上换行符后，可以将每个帖子的信息分行展示，使用ensure_ascii=False,并采用encode（"utf-8"）转换成中文
        f.write((json.dumps(items,ensure_ascii=False)+"\n").encode('utf-8'))
    
