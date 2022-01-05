def valueChanged(tag, tagPath, previousValue, currentValue, initialChange, missedEvents):
	"""
	Fired whenever the current value changes in value or quality.

	Arguments:
		tag: The source tag object. A read-only wrapper for obtaining tag
		     properties.
		tagPath: The full path to the tag (String)
		previousValue: The previous value. This is a "qualified value", so it
		               has value, quality, and timestamp properties.
		currentValue: The current value. This is a "qualified value", so it has
		              value, quality, and timestamp properties.
		initialChange: A boolean flag indicating whether this event is due to
		               the first execution or initial subscription.
		missedEvents: A flag indicating that some events have been skipped due
		              to event overflow.
	"""
	
	try:

		if currentValue.value is None:  # Sometimes currentValue is None, like when the Gage is turned off or perhaps in some other offline-like state
			quit()

# =========== WILL'S VANILLA CODE start ==============================================
		if currentValue.value[0:3] == "<u>":
			system.tag.write("[.]User",currentValue.value[3:7])
	
		elif len(currentValue.value) == 12:  # if a WIP Tag was scanned
		
			gageLock = system.tag.readBlocking(['[.]../MES/MES Control Hold'])
			gageLock = str(gageLock[0].value)

			if gageLock.upper() == 'True'.upper():
				quit() # Block or quit() the scanning of a WIP Tag when the Gage is locked		
		
			system.tag.write("[.]Active Wip",currentValue.value)
# =========== WILL'S VANILLA CODE end ==============================================			

	except Exception as e:
		eParams = {'msgID':'valueChanged err', # + system.tag.readBlocking(['[.]../Gage/Gage Name'])[0].value,
				   'message':getattr(e, 'message', repr(e)),
				   'msgSource':'UDT_Tag/Gage/Scanner/Scan String.valueChanged. . . XTA9ZQ'}
		system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)