# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class WorldometersPipeline(object):
    def open_spider(self, spider):
        self.connection = sqlite3.connect("worldometers.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute("""
                CREATE TABLE world_stats (
                    country_name TEXT,
                    year TEXT,
                    population TEXT
                )
            """)
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute("""
            INSERT INTO world_stats (country_name, year, population) VALUES (?,?,?)       
        """, (item.get('country_name'), item.get('year'), item.get('population')))
        self.connection.commit()
        return item
