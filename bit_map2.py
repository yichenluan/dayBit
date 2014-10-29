#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


class Bit_Map:
    def __init__(self):
        # 良乡地图
        self.points = [u'北校门',u'中食堂',u'良乡大学城北地铁站',u'南校门',u'理教',u'良乡大学城地铁站',
                      u'物理实验室',u'化学实验室',u'操场',u'疏桐园',u'南食堂',
                      u'博雅园',u'生物楼']
        
        # 中关村地图
        self.points2 = [u'6号教学楼',u'软件楼',u'1食堂',u'教工餐厅',u'远志楼',u'校医院',u'实验区',
                        u'10号办公楼',u'求是楼',u'3号教学楼',u'2号办公楼',u'1号教学楼',
                        u'体育馆',u'中心教学楼',u'中心花园',u'主楼',u'东门',u'地铁站',
                        u'7号教学楼',u'号教学楼',u'图书馆',u'5号教学楼',
                        u'1号学生公寓',u'8号教学楼']
        
        #良乡路线
        self.lines = [[u'北校门',u'中食堂'],[u'中食堂',u'良乡大学城北地铁站'],[u'中食堂',u'南校门'],[u'南校门',u'理教'],
                      [u'良乡大学城北地铁站',u'良乡大学城地铁站'],[u'理教',u'物理实验室'],[u'物理实验室',u'化学实验室'],
                      [u'南校门',u'疏桐园'],[u'疏桐园',u'操场'],[u'操场',u'化学实验室'],[u'疏桐园',u'南食堂'],[u'操场',u'博雅园'],
                      [u'南食堂',u'博雅园'],[u'博雅园',u'生物楼'],[u'南校门',u'操场']]
        
        #中关村路线
        
        self.lines2 = [[u'软件楼',u'6号教学楼'],[u'软件楼',u'1食堂'],[u'1食堂',u'京工餐厅'],
                       [u'京工餐厅',u'远志楼'],[u'远志楼',u'校医院'],[u'校医院',u'试验区'],
                       [u'京工餐厅',u'10号楼'],[u'远志楼',u'求是楼'],[u'校医院',u'3号教学楼'],
                       [u'实验区',u'2号办公楼'],[u'10号办公楼',u'求是楼'],[u'求是楼',u'3号教学楼'],
                       [u'3号教学楼',u'2号办公楼'],[u'2号办公楼',u'1号教学楼'],[u'10号办公楼',u'体育馆'],
                       [u'求是楼',u'中心教学楼'],[u'3号教学楼',u'中心教学楼'],[u'1号教学楼',u'主楼'],
                       [u'体育馆',u'中心教学楼'],[u'中心教学楼',u'中心花园'],[u'中心花园',u'主楼'],
                       [u'主楼',u'东门'],[u'东门',u'地铁站'],[u'中心教学楼',u'4号教学楼'],
                       [u'主楼',u'5号教学楼'],[u'7号教学楼',u'4号教学楼'],[u'4号教学楼',u'图书馆'],
                       [u'图书馆',u'5号教学楼'],[u'7号教学楼',u'1号学生公寓'],[u'7号教学楼',u'8号教学楼'],
                       [u'1号学生公寓',u'8号教学楼'],[u'1号学生公寓',u'南门'],[u'南门烤翅',u'南门']
                       
                       ]
        
        #self.birth_points = [u'疏桐园',u'博雅园']
        self.birth_points = [u'疏桐园']
        self.blood_points = [u'中食堂',u'南食堂']
        
        self.birth_points2 = [u'1号学生公寓']
        self.blood_points2 = [u'京工餐厅',u'校医院',u'1食堂',u'南门烤翅']
    
    #返回地图所有位置
    def get_points(self,t = -1):
        if t == -1:
            return self.points
        else:
            return self.points2
    
    #返回出生点
    def get_birth_point(self, t = -1):
        if t == -1:
            return self.birth_points
        else:
            return self.birth_points2
    
    #判断name是否是出生点
    def is_birth_point(self,name,t = -1):
        if t == -1:
            if name in self.birth_points:
                return True
            else:
                return False
        else:
            if name in self.birth_points2:
                return True
            else:
                return False
        
    #返回回血点
    def get_blood_point(self,t = -1):
        if t == -1:
            return self.blood_points
        else:
            return self.blood_points2
    #判断name是否是回血点
    def is_blood_point(self,name,t = -1):
        if t == -1:
            
            if name in self.blood_points:
                return True
            else:
                return False
            
        else:
            
            if name in self.blood_points:
                return True
            else:
                return False
    #返回name的邻居节点名
    def get_point_neigh(self,name, t = -1):
        if t == -1:
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
        else:
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
    def porint_map(self,t = -1):
        if t == -1:
            point = map.get_points(t)
            for ele1 in point:
                print ele1,'******'
                p = map.get_point_neigh(ele1)
                for ele2 in p:
                    print ele2
        else:
            point = map.get_points(t)
            for ele1 in point:
                print ele1,'******'
                p = map.get_point_neigh(ele1)
                for ele2 in p:
                    print ele2

    def print_story(self,name):
        if name == u'软件楼':
            strr = u'北理最有名的鬼楼就是红楼了。红楼在5系系楼的后面，一片草丛之中十几棵百年老松拱卫着的两层红砖楼就是'
            strr+= u'红楼了。 \n在北理5系上了三年学都不知道这么一个教学楼的存在，因为一方面它太隐秘，另一方面它是成教的'
            strr+= u'课堂。 \n终于在大四知道它的存在是因为实习的缘故。实习的时候终于可以有了老师办公室的钥匙，也终于可'
            strr+= u'以在老师加班都走了以后，仍然可以留在办公室里。不是加班，是玩警察抓小偷，一个老掉牙的经典电脑游戏，'
            strr+= u'一个和俄罗斯方块同时代的游戏。 \n我玩游戏是很专注的，能把我从游戏中惊起的声音自然是很大的。那天深'
            strr+= u'夜风很大，想必是哪个教室的窗户被风吹得咣当而破。我从桌上抬起头，突然看见窗外两个眼睛正定定地看着我。'
            strr+= u' \n外面一片漆黑，风仍然在呜呜地咆哮，什么都没有，没有四肢，没有身体，也没有脸，只有两只眼！！！我全'
            strr+= u'身的血往头上涌，虽然身子仍钉在椅子上，心脏却使劲往后躲，似乎想跑出我的身体，找个旮旯躲起来。 \n看到我'
            strr+= u'抬头看它，那眼睛开始漂移，忽然就不见了。我缓过劲来，眨了眨眼，看见对面那个楼的二楼还亮着两盏灯。我不'
            strr+= u'禁有些疑惑，刚才是不是看花眼了? \n第二天白天，为了验证是不是花了眼，我叫了两个同学来到红楼。上了二楼，'
            strr+= u'正对楼梯的教室里玻璃撒了一地，应该是昨晚的那声音。从窗户望外望去，刚好可以看到我昨晚呆的办公室。那么那'
            strr+= u'两盏灯应该也是这个教室的了。知道没有鬼，我心里放松了许多。 \n中午吃饭时，同做一张桌的'
        if name == u'1号学生公寓':
            strr = u'我在三号楼住的四年里见证了多场北理北外男生之间的口水战，但是最经典那场还是04年'
            strr+= u'那次。那次的导火索是由于北外男生的挑衅，大声叫喊北理女生丑。我X，北理女生在北理'
            strr+= u'男生心目中可是神圣不可侵犯的，他们敢骂我们的女生那可恨之极简直比骂我们男生自己还'
            strr+= u'不可饶恕。广大北理男生在这个原则上保持了高度的统一后开始反击，于是双方骂娘的，问'
            strr+= u'候爹妈以及十八代祖宗的都出现了，两边吵吵嚷嚷已经乱成了一锅粥，酒瓶早已经准备好'
            strr+= u'了，但是一扔酒瓶警车就来，所以就等合适的时机吹冲锋号冲锋了。'
        if name == u'南操场':
            strr = u'北院为禁地，闲杂人等不得入内'
            strr+= u'此处成为禁地的原因得从作者大二的那个春天说起'
            strr+= u'北湖曾经一个美好的地方，有天鹅有小桥，景色别致'
            strr+= u'但是就在那个春天，发生了可怕的事情'
            strr+= u'此处马赛克……详情请自行百度'
            strr+= u'禁言禁语'
        if name == u'食堂':
            strr = u'北理的食堂是卫生评级为A的食堂\n'
            strr+= u'也是冒险爱好者复活的圣地\n'
            strr+= u'进入食堂后请谨慎选择食物，同时冒险者也有可能得到传中的黑暗料理\n'
            strr+= u'或者绝对新鲜的的节肢动物料理\n'
            strr+= u'此处设定为回血地点，但是请冒险者在现实中不要轻易尝试，正常情况下会得到满血复活的良好效果，或者遭受巫师或术士的攻击得到继续的中毒效果，持续时间最长为1星期，攻击名为食物中毒'
         if name ==u'南门':
             strr = u'走出小南门就可以见到传说中的南门烤翅了\n'
             strr += u'南门烤翅为北理长久以来永垂不朽的一完美回血点之一，这就是打广告！！！！（此处广告位招商）\n'
             strr += u'请特定时间小心经过，此处为校园外围环境，危险系数高，会遇到各种快递员，小摊贩，醉酒男醉酒女或醉酒大叔大妈级人物，请冒险者小心'
             strr += u'请尽量避开与北外口水战时间，小心误伤=。=……如果遇到意外或尴尬问题请大喊我是北航的自可化解一切危机。'

        
if __name__ == '__main__':
    map = Bit_Map()
    
