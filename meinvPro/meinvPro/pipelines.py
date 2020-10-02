# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymysql import Connect
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class MeinvproPipeline:
    fp = None

    # 重写父类方法，该方法只在开始爬虫的时候别调用一次
    def open_spider(self, spider):
        print('开始爬虫并打开文件')
        self.fp = open('./meinv.txt', 'w', encoding='utf-8')

    # 专门用来处理item类型对象
    # 该方法可以接收爬虫文件提交过来的item对象
    # 该方法接收一个item就调用一次
    def process_item(self, item, spider):
        img_name = item['img_name']
        img_size = item['img_size']
        img_src = item['img_src']
        img_path = img_src.split('/')[-1]
        data = img_name + '\t' + img_size + '\t' + img_path + '\n'
        self.fp.write(data)
        return item

    # 结束爬虫时调用
    def close_spider(self, spider):
        print('结束爬虫并关闭文件')
        self.fp.close()

# 管道文件中一个管道对应将一组数据存储到一个平台中或载体中
class mysqlPipeLine(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        print('开始爬虫并连接数据库')
        self.conn = Connect(host='127.0.0.1', port=3306, user='root', password='root', db='my_django_project_2', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        img_src = item['img_src']
        img_path = img_src.split('/')[-1]
        sql = 'insert into pic_4k(img_name,img_size,img_path,img_cls) values("%s","%s","%s","%s")'%(item['img_name'], item['img_size'], img_path, '4k动物')
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('向数据库中插入数据异常:',e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        print('结束爬虫并关闭数据库连接')
        self.cursor.close()
        self.conn.close()

class imgsPipleLine(ImagesPipeline):

    # 就是可以根据图片地址进行图片数据的请求
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['img_src'])

    # 指定图片存储路径
    def file_path(self, request, response=None, info=None):
        img_path = request.url.split('/')[-1]
        return img_path

    def item_completed(self, results, item, info):
        return item