
def logDebugMsg(msgID, message, msgSource):
		
	params = {'msgID':msgID, 'message':message, 'msgSource':msgSource}
	import system  # (import system) has to be here (so (system.db...) will interpret correctly for some bug-like reason
	system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)
	
def CleanEmployeeID(empID):
	retVal = empID.replace('\r', '')  # remove any (carriage return) characters 
	retVal = empID.replace('\n', '')  # remove any (new line) characters
	retVal = empID.replace('<u>', '') # remove (identifying characters)
	retVal = retVal.strip()           # remove any spaces form left and right ends
	return retVal

def GetGageName(tagPath):
	tagPath = tagPath.replace("[default]", "")
	tagPath = tagPath.split("/")
	return tagPath[0].strip()

def CheckForMasterLock(gage, roles):



	import system  # (import system) has to be here (so (system.db...) will interpret correctly for some bug-like reason 
	dataSet = system.db.runNamedQuery("Gages", "GageLockingTable/CheckGageLockedMaintenance", {"Gage":gage})
	
	
#	return False
	

	if dataSet.getRowCount() > 0:


		locked = (dataSet.getValueAt(0, "Locked").upper() == 'Y')
		rabbited = (dataSet.getValueAt(0, "Red_Rabbit_Activated").upper() == 'Y')

#		params = {'msgID':'Steamboat', 'message':'A' , 'msgSource':'A'}
#		import system  # (import system) has to be here (so (system.db...) will interpret correctly for some bug-like reason
#		system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)


		test = '1'

		
		if locked == False:  # Under this condition, there is no 'master' lock, so just return False and let the rest of the script run.
			return False
		if locked == True and rabbited == False:  # Under these conditions, neither lock can be removed so just quit
			quit()   ##  brown cow

		if locked == True and rabbited == True:  # Under these conditions, there is a Table-Lock and the master is completed
			roles.append("Operator")  # add the 'Operator' role, allow (anyone) to remove the mes and table locks
			return True

	else:
#		params = {'msgID':'Eastwood3', 'message':gage + ', rabbited = ' , 'msgSource':'rabbited'}
#		import system  # (import system) has to be here (so (system.db...) will interpret correctly for some bug-like reason
#		system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)

		return False
	
def EvalUserRoles(ID, sprRoles):
	import system  # (import system) has to be here (so (system.db...) will interpret correctly for some bug-like reason
	users = system.user.getUsers("default")
	
	userRoles = []   # this is here for error ('userRoles' referenced before assignment)
	
	for user in users:
		if (str(user.get("username")) == ID):
			userRoles = user.getRoles()

			for i in range(len(userRoles)):          # loop each item in Role list
				userRoles[i] = userRoles[i].upper()  # convert each role to upper case

    		for role in sprRoles:                    # loop each of the (supervisor roles)/(approved roles)
    			if (role.upper() in userRoles):      # if an (approved role) is in (scanned Emp ID's roles)
    				return True

	return False     # if flow arrives here the (scanned empID's roles) do not have any (approved roles)

try:

	
	if (initialChange == 1): quit()  # 1 means this script may have been 'saved' and that saving it generated the change event 
	
	
	empID = str(event.getValue().value)
	
	
	superRoles = ["Supervisor", "Leader", "Administrator"]
	# Scans of  Emp IDs and WIP IDs can arrive here.  We're only targeting the Emp ID scans in this script
	
	
	if empID.find('<u>') > -1:   # '<u>' If the scan is an employee ID . . .
	
		
		empID = CleanEmployeeID(empID)
		gageID = GetGageName(str(event.getTagPath()))
		
#		logDebugMsg('Steamboat', 'A', empID)
		
		removeMasteredLock = CheckForMasterLock(gageID, superRoles) # this quite()s if conditions are . . 
		
		empID_IsSupervisor = EvalUserRoles(empID, superRoles)
		
#		logDebugMsg('Steamboat', 'BB', 'BB')

		if (empID_IsSupervisor == False):
#			logDebugMsg('Steamboat',  gageID + ', rquit()ing', empID_IsSupervisor)
			quit()  # scanned ID cannot remove any type of mes lock		


		tagPath =  '[default]' + gageID + '/' + gageID + '/MES/MES Control Hold'
		system.tag.writeBlocking([tagPath], [False])

		if (removeMasteredLock == True):	 # if a maintenance lock is in place and it's OK to unlock it

			logDebugMsg('Steamboat', empID + ', ' +  gageID, 'removeMasteredLock')
				
			system.db.runNamedQuery("Gages", "GageLockingTable/Unlock_Gage", {"Gage":gageID, "EmpID":empID})
		
except Exception as e:

	eParams = {'msgID':'UnlockGageScannedEmpID error',
               'message':getattr(e, 'message', repr(e)),
               'msgSource':'GatewayScript UnlockGageScannedEmpID 3K7K85'}
           
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)
		