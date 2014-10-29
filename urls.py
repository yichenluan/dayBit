#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dayBit

urls = [
	(r"/", dayBit.IndexHandler),
	(r"/signIn", dayBit.SignInHandler),
	(r"/signUp", dayBit.SignUpHandler),
	(r"/chooseRole", dayBit.ChooseRoleHandler),
	(r"/addRole", dayBit.AddRoleHandler),
	(r"/main", dayBit.MainHandler),
	(r"/signOut", dayBit.SignOutHandler),
	(r"/deleteRole", dayBit.DeleteRoleHandler),
	(r"/showForms", dayBit.ShowFormsHandler),
]