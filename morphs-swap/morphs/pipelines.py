# -*- coding: utf-8 -*-
import os
import signal
import logging
from fuse_transmute.boutiques import removeNone
from fuse_transmute.init_horadric_db import address_table, boutiques_table
import pymysql
from sqlalchemy import insert, select, update
from twisted.enterprise import adbapi


class MorphsPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings['MYSQL_CONFIG']
        settings.update({
            'use_unicode': True,
            'cursorclass': pymysql.cursors.DictCursor
        })
        db_pool = adbapi.ConnectionPool('pymysql', **settings)
        return cls(db_pool)

    def process_item(self, item, spider):
        spider.log(f'hello item {item}', level=logging.INFO)
        self._select_boutique_item(item, spider)
        # ↓
        # ↓
        # ↓

    def _select_boutique_item(self, item, spider):
        boutique = item['boutique']
        assert boutique.slug_id is not None

        statement = select([boutiques_table]).\
            where(boutiques_table.c.slug_id == boutique.slug_id).\
            compile(compile_kwargs={"literal_binds": True})

        d = self.db_pool.runQuery(str(statement))

        d.addErrback(self._handle_error, item, spider)
        d.addCallback(self._insert_postal_item, item, spider)

        spider.log(statement, level=logging.DEBUG)
        # ↓
        # ↓
        # ↓

    def _insert_postal_item(self, resultset, item, spider):
        spider.log(f'obtained select result: {resultset}', level=logging.DEBUG)
        spider.log('inserting address item', level=logging.DEBUG)
        postal_code = item['postal']
        item_values = removeNone(postal_code.__dict__)

        statement = insert(address_table).values(item_values).\
            compile(compile_kwargs={"literal_binds": True})

        d = self.db_pool.runOperation(str(statement))

        update_flag = bool(resultset)
        spider.log(f'update flag: {update_flag}', level=logging.DEBUG)
        d.addErrback(self._handle_error, item, spider, True)  # supress error on duplicate insert
        d.addCallback(self._process_boutique_item, update_flag, item, spider)

        spider.log(statement, level=logging.DEBUG)
        # ↓                 # ↓
        # ↓ _insert...  or  # ↓ _update...
        # ↓                 # ↓

    def _process_boutique_item(self, _, update_flag, item, spider):

        boutique = item['boutique']
        item_values = removeNone(boutique.__dict__)

        if update_flag:
            spider.log('updating boutique item', level=logging.DEBUG)
            statement = update(boutiques_table).\
                where(boutiques_table.c.slug_id == item_values['slug_id']).\
                values(item_values).\
                compile(compile_kwargs={"literal_binds": True})
            st_type = 'update'
        else:
            spider.log('inserting boutique item', level=logging.DEBUG)
            statement = insert(boutiques_table).values(item_values).\
                compile(compile_kwargs={"literal_binds": True})
            st_type = 'insert'

        d = self.db_pool.runOperation(str(statement))
        d.addErrback(self._handle_error, item, spider)
        d.addCallback(self._log_result, st_type, spider)

        spider.log(statement, level=logging.DEBUG)

    def _log_result(self, result, st_type, spider):
        spider.log(f'result of statement {st_type}: {result}')

    def _handle_error(self, failure, item, spider, suppress=False):
        spider.log(f'failure on item : {item}', level=logging.ERROR)
        #          f'ffffff...ailure

        if suppress:
            spider.log(f'suppressing failure on item : {item}', level=logging.ERROR)
            return 'supress'
        else:
            spider.log(f'panicking due to failure : {failure}', level=logging.ERROR)
            # crawler.stop() works somewhat unreliably
            os.kill(os.getpid(), signal.SIGKILL)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass
