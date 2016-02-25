#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5
import re
import os
import datetime, time
import cgi
import random

import bit_map
import battle

from settings import saedb

import tornado.web
import tornado.database
from tornado.httpclient import AsyncHTTPClient


class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		dayBitdb = tornado.database.Connection(
			host = saedb['host'] + ":" + saedb['port'],
			database = saedb['db'],
			user = saedb['user'],
			password = saedb['password']
			)
		return dayBitdb

	def get_current_user(self):
		usrid = self.get_secure_cookie('usrid')
		if not usrid:
			return None
		me = self.db.get('select * from usertable where usrid = %s', usrid)
		return me



	def getRoleValue(self):
		usrid = self.current_user.usrid
		typeToName = {1:u'学神', 2:u'大牛', 3:u'弱菜'}
		roletableValue = self.db.query("select * from roletable where usrid = %s", usrid)
		roleValue = dict()

		roleValue['roleTypeID'] = roletableValue[0]['roletype']
		roleValue['roleType'] = typeToName[roleValue['roleTypeID']]
		roleValue['roleNick'] = roletableValue[0]['rolenick']
		roleValue['roleID'] = roletableValue[0]['roleid']
		roleValue['rolePostion'] = self.getPostionNow(roleValue['roleID'])

		attrValue = self.getAttrValue(roleValue['roleID'])

		roleValue['roleRank'] = attrValue['rank']
		roleValue['roleBaseHpVal'] = attrValue['hpval']
		roleValue['roleBaseMpVal'] = attrValue['mpval']
		roleValue['roleExpVal'] = attrValue['expval']
		roleValue['roleBaseAttVal'] = attrValue['attval']

		equValue = self.getEquValue(roleValue['roleID'])

		roleValue['coatName'] = equValue['coatName']
		roleValue['coatAttr'] = equValue['coatAttr']

		roleValue['laptopName'] = equValue['laptopName']
		roleValue['laptopAttr'] = equValue['laptopAttr']

		roleValue['bookName'] = equValue['bookName']
		roleValue['bookAttr'] = equValue['bookAttr']

		roleValue['bagName'] = equValue['bagName']
		roleValue['bagAttr'] = equValue['bagAttr']

		equList = ['coatAttr', 'laptopAttr', 'bookAttr', 'bagAttr']

		roleValue['roleHpVal'] = roleValue['roleBaseHpVal']
		roleValue['roleMpVal'] = roleValue['roleBaseMpVal']
		roleValue['roleAttVal'] = roleValue['roleBaseAttVal']

		for equ in equList:
			roleValue['roleHpVal'] += roleValue[equ]['dthp']
			roleValue['roleMpVal'] += roleValue[equ]['dtmp']
			roleValue['roleAttVal'] += roleValue[equ]['dtatt']

		fixedValue = self.getFixedValue(str(roleValue['roleTypeID']), roleValue['roleRank'])
		roleValue['roleExpNeed'] = fixedValue['exptonext']

		roleValue['roleBagID'] = self.getBagID(roleValue['roleID'])


		return roleValue

	def getBagID(self, roleID):
		bagID = self.db.query("select * from bagbelong where roleid = %s", roleID)
		bagID = bagID[0]['bagid']
		return bagID

	def getPostionNow(self, roleID):
		postionNowID = self.db.query("select locid from roleloc where roleid = %s", roleID)
		postionNowID = postionNowID[0]['locid']
		postionNow = self.db.query("select locname from loccata where locid = %s", postionNowID)
		postionNow = postionNow[0]['locname']
		return postionNow

	def getAttrValue(self, roleID):
		attrtableValue = self.db.query("select * from roleattr where roleid = %s", roleID)
		attrValue = attrtableValue[0]
		return attrValue

	def getEquValue(self, roleID):
		equIDValue = self.db.query("select * from roleequ where roleid = %s", roleID)
		coatid = equIDValue[0]['coatid']
		laptopid = equIDValue[0]['laptopid']
		bookid = equIDValue[0]['bookid']
		bagid = equIDValue[0]['bagid']

		equValue = dict()

		coatName = self.db.query("select * from itemcata where itemid = %s", coatid)
		equValue['coatName'] = coatName[0]['itemname']
		laptopName = self.db.query("select * from itemcata where itemid = %s", laptopid)
		equValue['laptopName'] = laptopName[0]['itemname']
		bookName = self.db.query("select * from itemcata where itemid = %s", bookid)
		equValue['bookName'] = bookName[0]['itemname']
		bagName = self.db.query("select * from itemcata where itemid = %s", bagid)
		equValue['bagName'] = bagName[0]['itemname']

		coatAttr = self.db.query("select * from equdelt where itemid = %s", coatid)
		equValue['coatAttr'] = coatAttr[0]
		laptopAttr = self.db.query("select * from equdelt where itemid = %s", laptopid)
		equValue['laptopAttr'] = laptopAttr[0]
		bookAttr = self.db.query("select * from equdelt where itemid = %s", bookid)
		equValue['bookAttr'] = bookAttr[0]
		bagAttr = self.db.query("select * from equdelt where itemid = %s", bagid)
		equValue['bagAttr'] = bagAttr[0]

		return equValue


	def getFixedValue(self, roleType, roleRank):
		#formFromRoleType = {'1':u'xueshenrank','2':u'daniurank','3':u'ruocairank'}
		if roleType == '1':
			answer = self.db.query("select * from xueshenrank where rank = %s",roleRank)
			#answer = (formFromRoleType[str(roleType)], str(roleRank))
		elif roleType == '2':
			answer = self.db.query("select * from daniurank where rank = %s",roleRank)
		elif roleType == '3':
			answer = self.db.query("select * from ruocairank where rank = %s",roleRank)
		fixedValue = answer[0]
		return fixedValue


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html", signUpInfo = [])

class SignUpHandler(BaseHandler):
	def post(self):
		info = dict()
		info['name'] = self.get_argument('name', '')
		info['password'] = self.get_argument('password','')
		info['password'] = md5.new(info['password']).hexdigest()
		userNum = len(self.db.query('select * from usertable'))
		info['usrid'] = 100000 + userNum
		info['usrtype'] = 1

		if self.checkName(info):
			signUpInfo = [u'注册成功，请登录。']
			self.db.execute("insert into usertable (usrname, usrid, pwd, usrtype) values (%s, %s, %s, %s)",
				info['name'], info['usrid'], info['password'], info['usrtype'])
		else:
			signUpInfo = [u'用户名已存在，请直接登录。']			
		self.render('index.html', signUpInfo = signUpInfo)

	def checkName(self, info):
		nameExist = self.db.get("select * from usertable where usrname = %s", info['name'])
		if nameExist or (len(info['name']) >= 15):
			return False
		else :
			return True

class SignInHandler(BaseHandler):
	def post(self):
		info = dict()
		info['name'] = self.get_argument('name', '')
		info['password'] = self.get_argument('password','')
		userID = self.checkUser(info)
		if userID:
			self.set_secure_cookie('usrid', str(userID))
			self.redirect('/chooseRole')
		else:
			signUpInfo = [u'用户名或密码错误。']
			self.render('index.html', signUpInfo = signUpInfo)

	def checkUser(self, info):
		user = self.db.get("select * from usertable where usrname = %s", info['name'])
		if user:
			password = md5.new(info['password']).hexdigest()
			if password == user.pwd:
				return user.usrid
			else:
				return False
		else:
			return False

class ChooseRoleHandler(BaseHandler):
	def get(self):
		if self.current_user:
			roleList = self.db.query('select * from roletable where usrid = %s', str(self.current_user.usrid))
			self.render('choice.html', roleList = roleList)
		else:
			self.redirect('/')

class AddRoleHandler(BaseHandler):
	def post(self):
		info = dict()
		info['roletype'] = self.get_argument('roletype', '')
		info['rolenick'] = self.get_argument('rolenick', '')

		roleNum = len(self.db.query('select * from roletable'))
		info['roleid'] = 100000 + roleNum

		bagNum = len(self.db.query("select * from bagbelong"))
		info['bagid'] = 100000 + bagNum

		info['usrid'] = self.current_user.usrid
		if not self.db.query("select * from roletable where usrid = %s", info['usrid']):
			#message = [info]
			#self.render('test.html', message = message)
			roleValue = BaseHandler.getFixedValue(self, info['roletype'], '1')
			self.db.execute("insert into roletable (roleid, usrid, roletype, rolenick) values (%s, %s, %s, %s)",
				info['roleid'], info['usrid'], info['roletype'], info['rolenick'])
			self.db.execute("insert into roleloc (roleid, locid) values (%s, %s)", info['roleid'], 1)
			self.db.execute("insert into roleattr (roleid, hpval, mpval, expval, attval, rank) values (%s, %s, %s, %s, %s, %s)",
				info['roleid'], roleValue['hpval'], roleValue['mpval'], 0, roleValue['att'], roleValue['rank'])
			self.db.execute("insert into roleequ (roleid, coatid, laptopid, bookid, bagid) values (%s, %s, %s, %s, %s)",
				info['roleid'], 1, 39, 53, 82)
			self.db.execute("insert into bagbelong (roleid, bagid) values (%s, %s)",
				info['roleid'], info['bagid'])
			self.db.execute("insert into achiv (roleid, killenemy, killedbyenemy, getequip, totalexp) values (%s, %s, %s, %s, %s)",
				info['roleid'], 0, 0, 0, 0)
		self.redirect('/chooseRole')


class DeleteRoleHandler(BaseHandler):
	def get(self):
		usrid = self.current_user.usrid
		#self.db.execute("delete from roletable set usrid = 0 where usrid = %s", usrid)
		self.db.execute("update roletable set usrid = 8088 where usrid = %s", usrid)
		self.redirect('/chooseRole')

class MainHandler(BaseHandler):
	def get(self):
		if self.current_user:
			roleList = self.db.query('select * from roletable where usrid = %s', str(self.current_user.usrid))
			self.render('main.html', roleList = roleList)
		else:
			self.redirect('/')

	def post(self):
		usrid = self.current_user.usrid
		roletableValue = self.db.query("select * from roletable where usrid = %s", usrid)
		orderContent = self.get_argument('orderContent','').strip()
		bitmap = bit_map.Bit_Map()
		roleValue = BaseHandler.getRoleValue(self)
		#self.render('test.html', message = orderContent)
		#self.write(orderContent)
		if orderContent == u'帮助':
			answerStrList = [
			'1. 输入「开始」开始游戏<br/>',
			'2. 输入「现在」查看角色目前位置<br/>',
			'3. 输入「周围」查看角色周围地点<br/>',
			'4. 输入「去##」让角色移动到 ## <br/>',
			'5. 输入「所有」查看地图的所有位置<br/>',
			'6. 输入「装备」查看角色身上装备<br/>',
			'7. 输入「属性」查看角色各项属性值<br/>',
			'8. 输入「背包」查看角色背包<br/>',
			'9. 输入「穿##」让角色穿上某件装备<br/>'
			]
			for answerStr in answerStrList:
				self.write(answerStr)

		elif orderContent == u'开始':
			#answerStr = str(roleValue)
			answerStr = roleValue['roleType'] + ' ' + roleValue['roleNick'] + u' 您好，您现在在' +roleValue['rolePostion'] + u'。<br/>'
			answerStr +=  u'角色等级为 ' + str(roleValue['roleRank']) + u' 级。<br/>'
			answerStr += u'角色属性为：  血量：' + str(roleValue['roleHpVal']) + u'，蓝量：' + str(roleValue['roleHpVal']) + u'，攻击力：' + str(roleValue['roleAttVal']) + u'，经验值：' + str(roleValue['roleExpVal']) + u'。<br/>'
			answerStr += u'装备为：  外套：' + roleValue['coatName'] + u'，电脑：' + roleValue['laptopName'] + u'， 书本：' + roleValue['bookName'] + u'，背包：' + roleValue['bagName'] 
			self.write(answerStr)

		elif orderContent == u'装备':
			answerStr = u'外套：' + roleValue['coatName'] + u'，电脑：' + roleValue['laptopName'] + u'， 书本：' + roleValue['bookName'] + u'，背包：' + roleValue['bagName']
			self.write(answerStr)

		elif orderContent == u'属性':
			answerStr = u'等级：'+ str(roleValue['roleRank']) + u'，血量：' + str(roleValue['roleHpVal']) + u'，蓝量：' + str(roleValue['roleHpVal']) + u'，攻击力：' + str(roleValue['roleAttVal']) + u'，经验值：' + str(roleValue['roleExpVal']) 
			self.write(answerStr)

		elif orderContent == u'现在':
			postionNow = roleValue['rolePostion']
			answerStr = u'现在您在' + postionNow
			self.write(answerStr)

		elif orderContent == u'周围':
			postionNow = roleValue['rolePostion']
			neighPostions = bitmap.get_point_neigh(postionNow)
			answerStr = u'您现在可以去：'
			for neighPostion in neighPostions:
				answerStr = answerStr +  neighPostion +' '
			self.write(answerStr)

		elif orderContent == u'背包':
			bagID = roleValue['roleBagID']
			bagItem = self.db.query("select * from bagitem where bagid = %s", bagID)
			itemValue = dict()
			if bagItem:
				for item in bagItem:
					itemID = item['itemid']
					itemName = self.db.query("select * from itemcata where itemid = %s", itemID)
					itemValue[itemID] = itemName[0]['itemname']

				answerStr = u''

				for (itemID, itemName) in itemValue.items():
					#answerStr += str(itemID) + u' : ' + str(itemName) + u'   '
					answerStr += str(itemID) + u'：' + itemName + '     '
			else:
				answerStr = u'</br>您的背包空无一物，快去刷刷刷！'
			self.write(answerStr)

		elif orderContent[:1] == u'穿':
			equToWearID = orderContent[1:]
			if self.db.query("select * from bagitem where bagid = %s and itemid = %s", roleValue['roleBagID'], equToWearID):
				#self.write('dfads')
				
				equToWearType = self.db.query("select * from itemcata where itemid = %s", equToWearID)
				equToWearType = equToWearType[0]['itemtype']
				typeToName = {'1':'coatid', '2':'laptopid', '3':'bookid', '4':'bagid'}
				equNow = self.db.query("select * from roleequ where roleid = %s", roleValue['roleID'])
				equNowID = equNow[0][typeToName[str(equToWearType)]]	
				self.db.execute("update roleequ set {0} = %s where roleid = %s".format(typeToName[str(equToWearType)]),
					equToWearID, roleValue['roleID'])		
				self.db.execute("delete from bagitem where bagid = %s and itemid = %s",
					roleValue['roleBagID'], equToWearID)

				if not self.db.query("select * from bagitem where bagid = %s and itemid = %s", roleValue['roleBagID'], equNowID):
					self.db.execute("insert into bagitem (bagid, itemid) values (%s, %s)", roleValue['roleBagID'], equNowID)

				self.write(u'装备已换上')
				
			else:
				self.write(u'你还没有该装备')

		elif orderContent[:1] == u'去':
			postionNow = roleValue['rolePostion']
			neighPostions = bitmap.get_point_neigh(postionNow)
			postionToGo = orderContent[1:]
			if postionToGo in neighPostions:
				if random.choice([1,1,0]):
					monsValue = self.getMonsValue()

					fight = battle.Battle()
					fight.setRole(roleValue['roleNick'], int(roleValue['roleHpVal']), int(roleValue['roleMpVal']), int(roleValue['roleAttVal']))
					fight.addNPC(monsValue['monsName'], monsValue['monsHp'], monsValue['monsExp'], monsValue['monsAtt'])
					fight.fight()
					fightStr = fight.getProcess()
					#expGet = fight.getExperience()
					resultStr = fight.getResult()
					
					answerStr = u'哈哈！您遇到了一只野生的 ' + monsValue['monsName'] + ' !<br/><br/>'
					self.write(answerStr)
					self.write(fightStr)
					if fight.getResult():

						killenemy = self.db.query("select killenemy from achiv where roleid = %s", roleValue['roleID'])
						killenemyNum = killenemy[0]['killenemy'] + 1
						self.db.execute("update achiv set killenemy = %s where roleid = %s", killenemyNum, roleValue['roleID'])

						#获取掉落
						if random.choice([1,1,1,0]):
							equDropID = random.randint(1, 98)
							equDropName = self.db.query("select * from itemcata where itemid = %s", equDropID)
							equDropName = equDropName[0]['itemname']
							if self.db.query("select * from bagitem where bagid = %s and itemid = %s",roleValue['roleBagID'], equDropID):
								pass
							else:
								getequip = self.db.query("select getequip from achiv where roleid = %s", roleValue['roleID'])
								getequipNum = getequip[0]['getequip'] + 1
								self.db.execute("update achiv set getequip = %s where roleid = %s", getequipNum, roleValue['roleID'])

								self.db.execute("insert into bagitem (bagid, itemid) values (%s, %s)",
									roleValue['roleBagID'], equDropID)
							answerStr = u'<br/><br/>怪物掉落了 ' + equDropName
							self.write(answerStr)

						else:
							self.write(u'怪物什么也没掉落')

						#获取经验
						expGet = fight.getExperience()

						totalexp = self.db.query("select totalexp from achiv where roleid = %s", roleValue['roleID'])
						totalexpNum = totalexp[0]['totalexp'] + expGet
						self.db.execute("update achiv set totalexp = %s where roleid = %s", totalexpNum, roleValue['roleID'])


						roleExpNow = roleValue['roleExpVal'] + expGet
						if roleExpNow >= roleValue['roleExpNeed']:
							roleRankNow = roleValue['roleRank'] + 1
							roleExpNow -= roleValue['roleExpNeed']
							roleFixedValue = BaseHandler.getFixedValue(self, str(roleValue['roleTypeID']), roleRankNow)
							self.db.execute("update roleattr set hpval = %s, mpval = %s, expval = %s, attval = %s, rank = %s where roleid = %s",
								roleFixedValue['hpval'], roleFixedValue['mpval'], roleExpNow, roleFixedValue['att'], roleRankNow, roleValue['roleID'])
						else:
							self.db.execute("update roleattr set expval = %s where roleid = %s",
								roleExpNow, roleValue['roleID'])
						self.write(u'<br/>你赢了！<br/>')

						postionToGo = orderContent[1:]
						postionToGoID = self.db.query("select locid from loccata where locname = %s", postionToGo)
						postionToGoID = str(postionToGoID[0]['locid'])
						self.db.execute("update roleloc set locid = %s where roleid = %s", postionToGoID ,roleValue['roleID'])
						answerStr = u'现在您在' + postionToGo
						self.write(answerStr)
					else :
						killedbyenemy = self.db.query("select killedbyenemy from achiv where roleid = %s", roleValue['roleID'])
						killedbyenemyNum = killedbyenemy[0]['killdebyenemy'] + 1
						self.db.execute("update achiv set killedbyenemy = %s where roleid = %s", killedbyenemyNum, roleValue['roleID'])


						self.db.execute("update roleloc set locid = 1 where roleid = %s", roleValue['roleID'])
						self.write(u'<br/>你被打败了，已经回到出生点！<br/>')
				else:
					self.write(u'没遇见怪物<br/>')
					postionToGo = orderContent[1:]
					postionToGoID = self.db.query("select locid from loccata where locname = %s", postionToGo)
					postionToGoID = str(postionToGoID[0]['locid'])
					self.db.execute("update roleloc set locid = %s where roleid = %s", postionToGoID ,roleValue['roleID'])
					answerStr = u'现在您在' + postionToGo
					self.write(answerStr)
			else:
				self.write(u'你现在不能去那')

		elif orderContent == u'所有':
			allPostion = bitmap.get_points()
			answerStr = u'所有地点如下：'
			for postion in allPostion:
				answerStr = answerStr + postion +  ' '
			self.write(answerStr)

		elif orderContent == u'测试':
			#answerStr = self.db.query("select itemcata.itemtype, equdelt.itemrank from itemcata, equdelt where itemid = 1")
			answerStr = 'adsfds'
			self.write(str(answerStr))

		else :
			answerStr = u'别乱输命令！'
			self.write(answerStr)

	def getMonsValue(self):
		monsValue = dict()
		monsValue['monsID'] = random.randint(1,14)
		monsName = self.db.query("select * from monscata where monsid = %s", monsValue['monsID'])
		monsValue['monsName'] = monsName[0]['monsname']
		monsAttr = self.db.query("select * from monsattr where monsid = %s", monsValue['monsID'])
		monsValue['monsHp'] = monsAttr[0]['monshp']
		monsValue['monsAtt'] = monsAttr[0]['monsatt']
		monsValue['monsExp'] = monsAttr[0]['monsexp']
		return monsValue





		



class SignOutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("usrid")
        self.redirect("/")	


class ShowFormsHandler(BaseHandler):
	def get(self):
		info = dict()
		roleValue = BaseHandler.getRoleValue(self)
		roleid = roleValue['roleID']
		info['roleName'] = roleValue['roleNick']
		achiv = self.db.query("select * from achiv where roleid = %s", roleid)
		achivInfo = achiv[0]
		info['roleKillEnemy'] = achivInfo['killenemy']
		info['roleKilledByEnemy'] = achivInfo['killedbyenemy']
		info['roleGetEquip'] = achivInfo['getequip']
		info['roleTotalExp'] = achivInfo['totalexp']
		self.render("report.html", info = info)
