#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import copy
import json
import click
import threading

try:
    from modules import *
    from __init__ import __version__
except:
    try:
        from .modules import *
        from .__init__ import __version__
    except:
        from bot_plugin_musicdown_addons_musicdl.modules import *
        from bot_plugin_musicdown_addons_musicdl.__init__ import __version__
try:
    import getit
except:
    from bot_plugin_musicdown_addons_musicdl import getit
'''音乐下载器'''
class musicdl():
    def __init__(self, configpath=None, config=None, **kwargs):
        assert configpath or config, 'configpath or config should be given'
        self.config = loadConfig(configpath) if config is None else config
        self.logger_handle = Logger(self.config['logfilepath'])
        self.initializeAllSources()
    def run(self, target_srcs=None):
            # 音乐搜索
            user_input = getit.get_value("song")
            target_srcs = [
                'kugou',
                'netease', 'migu'
            ] if target_srcs is None else target_srcs
            search_results = self.search(user_input, target_srcs)
            # 打印搜索结果
            title = ['序号', '歌手', '歌名', '大小', '时长', '专辑', '来源']
            items, records, idx = [], {}, 0
            for key, values in search_results.items():
                for value in values:
                    items.append([
                        colorize(str(idx), 'number'), 
                        colorize(value['singers'], 'singer'), 
                        value['songname'], 
                        value['filesize'] if value['ext'] != 'flac' else colorize(value['filesize'], 'flac'), 
                        value['duration'], 
                        value['album'], 
                        colorize(value['source'].upper(), 'highlight'),
                    ])
                    records.update({str(idx): value})
                    idx += 1
            # 音乐下载
            user_input = '1,2,3,4,5,6'
            need_download_numbers = user_input.replace(' ', '').split(',')
            songinfos = []
            for item in need_download_numbers:
                songinfo = records.get(item, '')
                if songinfo: songinfos.append(songinfo)
            returnurl=""
            for i in songinfos:returnurl=returnurl+(i['singers']+i['songname']+"下载地址："+i['download_url']+"\n")
            getit.set_value("url",returnurl)
            #self.download(songinfos)

    def search(self, keyword, target_srcs):
        self.logger_handle.info(f'正在搜索 {colorize(keyword, "highlight")} 来自 {colorize("|".join([c.upper() for c in target_srcs]), "highlight")}')
        def threadSearch(search_api, keyword, target_src, search_results):
            try:
                search_results.update({target_src: search_api(keyword)})
            except Exception as err:
                self.logger_handle.error(str(err), True)
                self.logger_handle.warning('无法在%s中搜索 >>>> %s' % (target_src, keyword))
        task_pool, search_results = [], {}
        for target_src in target_srcs:
            task = threading.Thread(
                target=threadSearch,
                args=(getattr(self, target_src).search, keyword, target_src, search_results)
            )
            task_pool.append(task)
            task.start()
        for task in task_pool:
            task.join()
        return search_results
    '''音乐下载'''
    '''初始化所有支持的搜索/下载源'''
    def initializeAllSources(self):
        supported_sources = {
            'kuwo': Kuwo, 'joox': Joox, 'migu': Migu, 'kugou': Kugou,
            'lizhi': Lizhi, 'yiting': YiTing, 'netease': Netease, 'qqmusic': QQMusic,
            'qianqian': Qianqian, 'fivesing': FiveSing,
        }
        for key, value in supported_sources.items():
            setattr(self, key, value(copy.deepcopy(self.config), self.logger_handle))
        return supported_sources
    '''处理用户输入'''
    def dealInput(self, tip=''):
        user_input = input(tip)
        if user_input.lower() == 'q':
            self.logger_handle.info('ByeBye')
            sys.exit()
        elif user_input.lower() == 'r':
            self.initializeAllSources()
            self.run()
        else:
            return user_input
    '''str'''
    def __str__(self):
        return 'Welcome to use musicdl!\nYou can visit https://github.com/CharlesPikachu/musicdl for more details.'




'''run'''
if __name__ == '__main__':
    dl_client = musicdl('config.json')
    dl_client.run()