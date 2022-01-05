def logDebugMsg(msgID, message, msgSource):
		
	params = {'msgID':msgID,
			  'message':message,
			  'msgSource':msgSource}
	import system
	system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)


def GetGageFromPath(path):
		# passed value like  [default]G11/G11/Gage/Count/Batch Good Count
		# returns 'G11'
		try:
			pth = path.replace('[default]', '')
			pathAry = pth.split('/')
			return pathAry[0]
		
		except Exception as e:
			errParams = {'msgID':'Gateway Script error',
		                 'message':getattr(e, 'message', repr(e)),
	                     'msgSource':'StopGageRejectToteMaxed.GetGageFromPath GFY8OB'}
				   
			system.db.runNamedQuery("Gages", "Debug/LogMsg", errParams)



try:
	
	GageID = GetGageFromPath(str(event.tagPath))
	pathGageID = '[default]' + GageID + '/' + GageID
	pathToTag = pathGageID + '/Gage/Count/Batch Target'  # [default]G11/G11/Gage/Count/Batch Target
	
	currentVal = event.getValue().value
	maxVal = system.tag.readBlocking([pathToTag])[0].value # element [0] is the max value, full batch, full tote 
	
	if (currentVal is None): quit()
	if strFuncs.isInteger(currentVal) == False: quit()
	currentVal = int(currentVal)

	if (maxVal is None): quit()
	if strFuncs.isInteger(maxVal) == False: quit()
	maxVal = int(maxVal / 2)
	
	if currentVal >= maxVal: 
		path = '[default]' + GageID + '/' + GageID + '/MES/MES Control Hold'
		system.tag.writeBlocking([path], [True])
		
		#logDebugMsg('~~~~~', pathToTag, type(maxVal))
	
	
except Exception as e:

	eParams = {'msgID':'Gateway Script error',
               'message':getattr(e, 'message', repr(e)),
               'msgSource':'StopGageRejectToteMaxed CC4P71'}
           
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)
	
	
	
	