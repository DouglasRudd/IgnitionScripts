def logDebugMsg(msgID, message, msgSource):
		
	params = {'msgID':msgID,
			  'message':message,
			  'msgSource':msgSource}
	import system
	system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)


try:

	if (initialChange == 1):  # 1 means this script may have been 'saved' and that saving it generated the change event 
		quit()


	pth = str(event.tagPath).replace('[default]', '')
	pathAry = pth.split('/')
	GageID = pathAry[0]
	pathGageID = '[default]' + GageID + '/' + GageID
	pathTotPart = pathGageID + '/Gage/Total Parts'  # [default]G11/G11/Gage/Count/Batch Target	
	
	CurrentTick = int(event.getValue().value)
	divRemain  = divmod(CurrentTick, 10) # each 10th part
	
	if (divRemain[1] != 0):  # each 10th part
		quit()

	resultSet = system.db.runNamedQuery("Gages", "GageMaintenance/Get_Last_Tuneup_Tick", {"Gage":GageID})
	
	# logDebugMsg('green_these_2', GageID, resultSet.getValueAt(0, 1))
	LastMaintenanceTick = int(resultSet.getValueAt(0, 0))		
	if (LastMaintenanceTick == 0): # if this is the first time the Gage is reading this data 
		# Seed the table with the current (total part count) / Initialize the table with CurrentTick (total part count)
		system.db.runNamedQuery("Gages", "GageMaintenance/Set_Last_Tuneup_Tick", {"Gage":GageID,
																				  "TotalParts":CurrentTick})
		quit() # this was the first time the Gage read this data

	partsThreshold = int(resultSet.getValueAt(0, 1))  #  the number of parts ran through the Gage since the maintenance work / mes-lock (originally this number was 4000)

	if (CurrentTick - LastMaintenanceTick >= partsThreshold):
		mesLockPath = '[default]' + GageID + '/' + GageID + '/MES/MES Control Hold' 
		# system.tag.writeBlocking([mesLockPath], [True])
		system.db.runNamedQuery("Gages", "GageMaintenance/Set_Last_Tuneup_Tick", {"Gage":GageID,
																				  "TotalParts":CurrentTick})		
	else:
		system.db.runNamedQuery("Gages", "GageMaintenance/Set_Current_Tick", {"Gage":GageID,
																			  "TotalPartCount":CurrentTick})	

		
		
except Exception as e:

	eParams = {'msgID':'Gateway Script error',
			   'message':getattr(e, 'message', repr(e)),
			   'msgSource':'StopGageTuneupNeeded 3R9LAO'}
		   
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)