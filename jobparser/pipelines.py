# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re
import sys
from scrapy.pipelines.images import ImagesPipeline

class HhruPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy080421

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        item['site'] = spider.name
        item['salary'] = "".join(item['salary'])
        try:
            salary = item['salary']
            salary = re.sub('(?<=\d)\xa0(?=\d)', '', salary)
            salary_split_list = salary.split(" ")

            i = 0
            while i < len(salary_split_list):
                if salary_split_list[i] == 'от':
                    i += 1
                    item['min_salary'] = int(salary_split_list[i])
                elif salary_split_list[i] == 'до':
                    i += 1
                    item['max_salary'] = int(salary_split_list[i])
                else:
                    break
                i += 1
        except:
            print("Unexpected error:", sys.exc_info()[0])

        collection.insert_one(item)
        print()
        return item


class SuperjobPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy080421

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        item['site'] = spider.name
        salary = item['salary']

        if item['salary'][0] != 'По договорённости':
            try:
                if salary[0] == 'до':
                    item['max_salary'] = salary[2]
                    item['max_salary'] = str.replace(item['max_salary'], '\xa0', '')
                    item['max_salary'] = str.replace(item['max_salary'], 'руб.', '')
                    item['max_salary'] = int(item['max_salary'])
                elif salary[0] == 'от':
                    item['min_salary'] = salary[2]
                    item['min_salary'] = str.replace(item['min_salary'], '\xa0', '')
                    item['min_salary'] = str.replace(item['min_salary'], 'руб.', '')
                    item['min_salary'] = int(item['min_salary'])
                elif salary[1] == '\xa0':
                    item['min_salary'] = salary[0]
                    item['min_salary'] = str.replace(item['min_salary'], '\xa0', '')
                    item['min_salary'] = str.replace(item['min_salary'], 'руб.', '')
                    item['min_salary'] = int(item['min_salary'])
                else:
                    item['min_salary'] = salary[0]
                    item['min_salary'] = str.replace(item['min_salary'], '\xa0', '')
                    item['min_salary'] = int(item['min_salary'])

                    item['max_salary'] = salary[1]
                    item['max_salary'] = str.replace(item['max_salary'], '\xa0', '')
                    item['max_salary'] = int(item['max_salary'])

            except:
                print("Unexpected error:", sys.exc_info()[0])

        collection.insert_one(item)
        print()
        return item



class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        print()
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    #def file_path(self, request, response=None, info=None, *, item=None):
        #return path_to_saved_file


class InstaparserPipeline:
    def process_item(self, item, spider):
        print()
        return item