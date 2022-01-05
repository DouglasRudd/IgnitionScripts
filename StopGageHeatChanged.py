def logDebugMsg(msgID, message, msgSource):
		
	params = {'msgID':msgID,
			  'message':message,
			  'msgSource':msgSource}
	import system
	system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)

try:

	if (initialChange == 1):  # 1 means this script may have been 'saved' and that saving it generated the change event 
		quit()

	path = str(event.getTagPath())
	path = path.replace('[default]', '')
	pathAry = path.split('/')
	GageID = pathAry[0]
	
	path = '[default]' + GageID + '/' + GageID + '/MES/MES Control Hold' 
	logDebugMsg('StopGageHeatChanged, bravo corrected', path, event.getValue().value)
	system.tag.writeBlocking([path], [True])
	
except Exception as e:

	eParams = {'msgID':'StopGageHeatChanged error',
               'message':getattr(e, 'message', repr(e)),
               'msgSource':'GatewayScript StopGageHeatChanged 1X5ETJY'}
           
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)