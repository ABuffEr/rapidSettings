# -*- coding: UTF-8 -*-
# A simple module to bypass the addon translation system,
# so it can take advantage from the NVDA translations directly.

def message(message, amp=False):
	"""Return translated message according to NVDA local translations, put amp to True to not remove & symbol"""
	if message == "":
		# blank string translated reports NVDA information, so...
		return message
	message = _(message)
	# & is useful for menu, but generally we don't want it
	if not amp:
		message = message.replace('&', '')
	return message
