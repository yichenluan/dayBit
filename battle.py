# -*- coding: utf-8 -*-
import random
# 角色 玩家和NPC 名称 血量 攻击力 经验
class Roles:
    def __init__ (self, a, b, c, d):
        self.name = a
        self.health = b
        self.vitality = c
        self.experience = c
        self.attack = d
# 对战过程
class Battle:
    def __init__(self, inputRole = Roles(u'Null', 0, 0, 0)):
        self.result = False
        self.outputProcess = ''
        self.expGet = 0
        self.role = inputRole
# 剧本 {0}代表的玩家会获胜
        self.listProcess = [
        u'{0}与{1}的对战{0}使出全真气功<br/>\
踢了{1}44加七七四十九下{1}被激怒了<br/>\
一气之下把{0}冲到马桶里，观赏{0}和大便的对决<br/>\
可怜的{0}拨电话65719372给伽利略求救<br/>\
巴哈姆特以正在打英雄为由，拒绝救援<br/>\
战火中，{1}仍不断逼近{0}<br/>\
{0}为了扭转情势，伺机施展平日所学在{1}脸上重重挥了一拳，<br/>\
{1}因不堪疼痛而败下阵来，'
        ,
        u'{1}向{0}发起攻击，{0}受到135点伤害<br/>\
{1}发动连击<br/>\
{1}向{0}发起攻击，但是被{0}闪开了<br/>\
{0}向{1}发起攻击，{1}受到136点伤害<br/>\
{1}向{0}发起攻击，{0}受到171点伤害<br/>\
{0}作出垂死抗争，所有数值上升<br/>\
{0}向{1}发起攻击，{1}受到317点伤害<br/>\
{1}被击败了'
        ,
        u'{1}向{0}发起攻击，{0}受到135点伤害<br/>\
{1}发动连击<br/>\
{1}向{0}发起攻击，但是被{0}闪开了<br/>\
{0}向{1}发起攻击，{1}受到136点伤害<br/>\
{1}向{0}发起攻击，{0}受到171点伤害<br/>\
{0}作出垂死抗争，所有数值上升<br/>\
{0}向{1}发起攻击，{1}受到317点伤害<br/>\
{1}被击败了'
    ,
    u'只见{0}阴测测的笑了几声，亮出了自己的九阴排骨手，<br/>\
带着风声直直地向{1}头顶插去<br/>\
在{0}那阴测测的笑声中，{1}一声惨叫，只见面门上出现了五个碗口大的窟窿<br/>\
只见{1}突然从背后取出一物放到{0}面前，竟然是个MP4，里面正在播放着还珠格格.<br/>\
MP4正砸中{0}的面门，{0}怒道：看你也是一代宗师，怎的也用板砖<br/>\
只见{0}对着{1}眉来眼去，笑颜如花，竟是江湖失传已久的郎情妾意剑<br/>\
{1}不禁狂吐不止，一个不留神将肝吐了一地，不禁赞道:好毒辣的郎情妾意剑.'
        ,
        u'下着小雨的白日，{0}在森林舞着刀走着，猛地，听到一声狂笑。<br/>\
{0}仔细一看，原来是一个大汉，端着钯冲向他。<br/>\
很明显，{1}的目的，就是袭击他的头部。{0}赶紧往后一退，骂道你找死吗？<br/>\
{1}说我们的帐应该了断了！然后又挥着兵器往前逼近。<br/>\
{0}赶忙还击，轻轻一拨，但{1}身子十分灵活，看来这个对手挺厉害。<br/>\
{0}抖擞精神，使出吃奶的力气用自己的家伙一点。<br/>\
{1}不愠不火，用兵器使劲一击，二人混战在了一起。<br/>\
连续大战了十个回合。{0}觉得体力不支，于是卖了个破绽。<br/>\
{1}大叫着扑了过来，{0}猛地反回一击，只听当的一声，兵器飞了。<br/>\
{1}死了，再看地上的死人，面目模糊.'
        ,
        u'{0}拿出了神秘的灵符，往{1}丢过去,<br/>\
{1}被灵符贴到额头以后动弹不得，只能任{0}对自己上下其手<br/>\
{1}把手伸到背后，拿出预先准备好的酒瓶，把{0}扁的是唏哩哗啦<br/>\
{0}对{1}施展了人体练成，把{1}变成了天真可爱小乌龟<br/>\
{1}用家传的小朋友捶胸拳娇柔的打向{0}，<br/>\
{0}喊着:唉哟哟你打的人家好疼阿，娇喘几声以后倒地不起<br/>\
{0}用皮鞭抽打{1}，凄惨的哀嚎声让隔壁老王都想来参一脚<br/>\
经过一番激烈的战斗之后,{1}败下阵来，哭着去找妈妈'
        ,
        u'{0}对{1}告白，{1}受到了十分严重的精神伤害<br/>\
{1}使出了龟派气功，把{0}跟那美克星一起打爆，变成宇宙灰尘<br/>\
{0}用皮鞭抽打{1}，{1}被鞭子打的遍体鳞伤，可是又有点舒服<br/>\
{1}对{0}告白，{0}受到了十分严重的精神伤害<br/>\
{0}一记漂亮的上勾拳，把{1}的假发打飞到擂台的边缘<br/>\
{1}开着砂石车往{0}辗过去，{0}被砂石车辗成豆腐乳<br/>\
{0}拿出了神秘的灵符，往{1}丟过去，{1}被灵符贴到额头以后动弹不得，只能任{0}对自己上下其手<br/>\
经过一番激烈的战斗之后，{1}败下阵来，哭着去找自己的妈咪'
        ,
        u'{0}把手伸到背后，拿出预先准备好的酒瓶，把{1}扁的是唏哩哗啦<br/>\
{1}伸出左手的食指，用力的戳进{0}的鼻孔<br/>\
{0}一记漂亮的上勾拳，把{1}的花花可爱星星小短裤打飞到擂台的边缘<br/>\
{1}召唤巨大召唤兽巴哈姆特，巴哈姆特对{0}吐了一坨口水，{0}差点被淹死<br/>\
{0}拿出一颗手榴弹，塞进{1}的衣服里，把{1}的小可爱炸了个歪七扭八<br/>\
{1}肚子饿了，跟{0}手牵手一起去吃大餐，画面温馨感人<br/>\
{0}跟{1}合体，变成了宇宙最强的赛亚战士<br/>\
经过一番激烈的战斗之后，{1}败下阵来，哭着去找自己的妈咪'
        ,
        u'{1}开着砂石车往{0}辗过去，{0}被砂石车辗成猪食。<br/>\
{0}使出了龟派气功，把{1}跟那美克星一起打爆，变成宇宙灰尘。<br/>\
{1}放出了魔法火球，烧掉了{0}的小裤裤，这让{0}十分害羞又开心。<br/>\
{0}拿出了男人必备的钻头，突破了{1}的天际。<br/>\
{1}跟{0}合体，变成了爱与正义的水手服战士。<br/>\
{0}听耶诞老人的话，一边施展金勾臂一边唱著「金勾臂～金勾臂～金勾殴了胃～」，<br/>\
{1}被金勾臂连击胃部，把昨天的早餐也吐了出来。<br/>\
{0}被击败了'
        ,
        u'{0}使用“无敌风火轮”攻击{1}，{1}损失21点血<br/>\
{1}身子一颤，发出“暴雨梨花”射向{0}{0}损失22点血<br/>\
{1}掏出平底锅大力扔向{0}{0}损失21点血<br/>\
{1}一纵身，离地三尺，一招“万恶淫为手”攻击{0}{0}损失24点血<br/>\
{0}开始抽风突然发出一招“老太太无敌大臭脚”攻击{1},{1}损失23点血<br/>\
{0}使用“无敌风火轮”攻击{1},{1}损失26点血<br/>\
{1}身子一颤，发出“暴雨梨花”射向{0}{0}损失17点血<br/>\
{0}使用“无敌风火轮”攻击{1},损失25点血<br/>\
{0}突然一个后撤，发出乌龟冲击波攻击{1},{1}损失26点血<br/>\
{1}掏出平底锅大力扔向{0},{0}损失24点血<br/>\
{0}采用吐痰攻击，一口浓痰喷向{1}损失28点血<br/>\
{1}掏出平底锅大力扔向{0}{0}损失15点血<br/>\
{0}胜利​​，{1}被彻底击败了'
        ]
        self.centence =[
           u'{0}使出了龟派气功，把{1}跟那美克星一起打爆，变成宇宙灰尘<br/>',
u'{0}一记漂亮的上勾拳，把{1}的假发打飞到擂台的边缘。<br/>',
u'{0}听圣诞老人的話，一边施展金勾臂一边唱着「金勾臂～金勾臂～金勾毆了胃～」，悽凌的歌声让{1}开始后悔自己活在这个世界上。<br/>',
u'{0}叫來了太平洋上的台风，把{1}吹的是东倒西歪、尸橫遍野、血流成河，十分的涼爽。<br/>',
u'{0}把手伸到背后，拿出预先准备好的酒瓶，把{1}扁的是唏里哗啦。<br/>',
u'{0}拿出一颗手榴弹，塞进{1}的嘴里，把{1}炸了个歪七扭八。<br/>',
u'{0}跟{1}合体，变成了爱与正义的水手服战士。<br/>',
u'{0}说：「你要咖啡，茶，还是要我呢。」，{1}回答：「我想去死」<br/>',
u'{0}拿起霹雳神剑大喊「霹雳，霹雳，霹雳貓～」，然後把旁边的西瓜砸到{1}脸上。<br/>',
u'{0}对{1}告白，{1}受到了十分严重的精神伤害。<br/>'
        ]
        # 名称 血量  经验 攻击力
        self.NPC = []


    def fight(self):
        # 随机一个NPC
        randomNPC = self.NPC[random.randint(0, len(self.NPC) - 1)]
        judge = random.randint(0, 15)
        self.outputProcess = ''
# 随机剧本模式
        if judge > 13:
            if self.judgeWin(self.role, randomNPC):
                self.outputProcess = self.listProcess[random.randint(0, len(self.listProcess)-1)].format( self.role.name, randomNPC.name)
                self.expGet = randomNPC.experience
            else:
                self.outputProcess = self.listProcess[random.randint(0, len(self.listProcess)-1)].format(randomNPC.name, self.role.name)
                self.expGet = 0
# 随机句子模式
        else:
            for num in range(0, 7):
                self.outputProcess = self.outputProcess + self.centence[random.randint(0, len(self.centence)-1)].format(randomNPC.name, self.role.name)
            if self.judgeWin(self.role, randomNPC):
                self.outputProcess = self.outputProcess + u'经过一番激烈的战斗之后,{0} 败下阵来'.format(randomNPC.name)
                self.expGet = randomNPC.experience
            else:
                self.outputProcess = self.outputProcess + u'经过一番激烈的战斗之后,{0} 败下阵来'.format(self.role.name)
                self.expGet = 0

    def getExperience(self):
        return self.expGet

    def getProcess(self):
        return self.outputProcess


    # 输赢判定
    def judgeWin(self, role1, role2):
        role1.health = role1.health - role2.attack
        role2.health = role2.health - role1.attack
        self.result = (role1.health > role2.health) and True or False
        return self.result

    def addNPC(self, name, health, vitality, attack):
        newNPC = Roles(name, health, vitality, attack)
        self.NPC.append(newNPC)

    def setRole(self, name, health, vitality, attack):
        self.role = Roles(name, health, vitality, attack)

    def getResult(self):
        return self.result

if __name__ == '__main__':
    battle = Battle()
    # 血量 经验/蓝 攻击力
    battle.setRole(u'金科', 10, 50, 10)
    # 血量 经验/蓝 攻击力
    battle.addNPC(u'Boss', 10, 1000, 100)
    battle.fight()
    print battle.getProcess()
    print battle.getExperience()
    print (battle.getResult() == True ) and u'获胜' or u'失败'
