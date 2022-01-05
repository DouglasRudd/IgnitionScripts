def logDebugMsg(msgID, message, msgSource):
		
	params = {'msgID':msgID,
			  'message':message,
			  'msgSource':msgSource}
	import system
	system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)


	# during debugging, this event can be triggered by. . . 
	# In the Tag Browser, navigate to . . .
	# [default]G99/G99/Gage/Running Part Number 
	# and change the existing value, it should look like ==> 'G99-###'

	# if (new value) = (old value) this event does not fire
	# This change event only fires when (new value) is not equal to (old value).  
		# For example, if your were to change the value to the same value that it already is, this Change event will not fire
		
	# logDebugMsg('bravo 11', event.getPreviousValue().getValue(), event.getValue().value) # returns (previous val) and (new val)
	# logDebugMsg('bravo', event.getTagPath(), event.getValue().value)                     # returns (path to tag) and (new val)
	
try:

	if (initialChange == 1):  # 1 means this script may have been 'saved' and that saving it generated the change event 
		quit()

	path = str(event.getTagPath())
	path = path.replace('[default]', '')
	pathAry = path.split('/')
	GageID = pathAry[0]

	path = '[default]' + GageID + '/' + GageID + '/MES/MES Control Hold' 
		
	# system.tag.writeBlocking('[default]G16/NEW_TEST_STOP', False)
	#### system.tag.writeBlocking(path, True)
	system.tag.writeBlocking([path], [True])
	
except Exception as e:

	eParams = {'msgID':'StopGagePartChanged error',
               'message':getattr(e, 'message', repr(e)),
               'msgSource':'GatewayScript StopGagePartChanged S0FVEG4'}
           
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)