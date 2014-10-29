#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


class Bit_Map:
    def __init__(self):
        self.points = [u'北校门',u'中食堂',u'良乡大学城北地铁站',u'南校门',u'理教',u'良乡大学城地铁站',
                      u'物理实验室',u'化学实验室',u'操场',u'疏桐园',u'南食堂',
                      u'博雅园',u'生物楼']
        self.lines = [[u'北校门',u'中食堂'],[u'中食堂',u'良乡大学城北地铁站'],[u'中食堂',u'南校门'],[u'南校门',u'理教'],
                      [u'良乡大学城北地铁站',u'良乡大学城地铁站'],[u'理教',u'物理实验室'],[u'物理实验室',u'化学实验室'],
                      [u'南校门',u'疏桐园'],[u'疏桐园',u'操场'],[u'操场',u'化学实验室'],[u'疏桐园',u'南食堂'],[u'操场',u'博雅园'],
                      [u'南食堂',u'博雅园'],[u'博雅园',u'生物楼'],[u'南校门',u'操场']]
        self.birth_points = [u'疏桐园',u'博雅园']
        self.blood_points = [u'中食堂',u'南食堂']
    
    #返回地图所有位置
    def get_points(self):
        return self.points
    
    #返回出生点
    def get_birth_point(self, t = -1):
        if t == -1:
            return [u'疏桐园',u'博雅园']
        if t == 0:
            if random.randint(0,10) >= 5:
                return [u'疏桐园']
            else:
                return [u'博雅园']
    #判断name是否是出生点
    def is_birth_point(self,name):
        if name in self.birth_points:
            return True
        else:
            return False
        
    #返回回血点
    def get_blood_point(self):
        return self.blood_points
    #判断name是否是回血点
    def is_blood_point(self,name):
        if name in self.blood_points:
            return True
        else:
            return False
    #返回name的邻居节点名
    def get_point_neigh(self,name):
        
        if not name in self.points:
            return None
        
        point = []
        for ele in self.lines:
            if name in ele:
                if ele[0] == name:
                    point.append(ele[1])
                elif ele[1] == name:
                    point.append(ele[0])
        return point
    
    
    #打印地图 测试
    def porint_map(self):
        point = map.get_points()
        for ele1 in point:
            print ele1,'******'
            p = map.get_point_neigh(ele1)
            for ele2 in p:
                print ele2 
if __name__ == '__main__':
    map = Bit_Map()
    