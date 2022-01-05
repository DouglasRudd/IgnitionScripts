def logDebugMsg(msgID, message, msgSource):
		
	params = {'msgID':msgID,
			  'message':message,
			  'msgSource':msgSource}
	import system
	system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)

def isSupervisor(roles):

	try:

		for x in roles:
		
			if 'Supervisor'.upper() == x.upper():
				return True

			if 'Leader'.upper() == x.upper():
				return True

			if 'Administrator'.upper() == x.upper():
				return True

		return False

	except Exception as e:
		
			eParams = {'msgID':'UnlockGageScannedEmpID.isSupervisor err',
					   'message':getattr(e, 'message', repr(e)),
					   'msgSource':'Gateway UnlockGageScannedEmpID.isSupervisor RND72WU'}
			import system # Ignition needs this (import) in order to know what (system) is, it seems buggy
			system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)

	

try:

	if (initialChange == 1):  # 1 means this script may have been 'saved' and that saving it generated the change event 
		quit()

	empID = str(event.getValue().value)
		
	if empID.find('<u>') > -1:   # '<u>' denotes an (employee ID) was scanned
			
		empID = empID.replace('\r', '')  # remove any (carriage return) characters 
		empID = empID.replace('\n', '')  # remove any (new line) characters
		empID = empID.replace('<u>', '') # remove (identifying characters) 
		
		users = system.user.getUsers('default')
		for user in users:
			if user.get('username') == empID:  #  username is numeric like '1234'
			
				if isSupervisor(user.getRoles()) == False:
#					logDebugMsg('foxtrot ', 'supervisor = False', user.get('lastname'))
					quit()

				path = str(event.getTagPath())
				path = path.replace('[default]', '')
				pathAry = path.split('/')
				GageID = pathAry[0]
				path = '[default]' + GageID + '/' + GageID + '/MES/MES Control Hold'

			 	system.tag.writeBlocking([path], [False])

#				logDebugMsg('foxtrot ', GageID + ', supervisor = True', user.get('lastname'))
		
except Exception as e:

	eParams = {'msgID':'UnlockGageScannedEmpID error',
               'message':getattr(e, 'message', repr(e)),
               'msgSource':'GatewayScript UnlockGageScannedEmpID QFXESPB'}
           
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)