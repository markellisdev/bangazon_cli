class CustomerStatusManager():
	'''Method: changes user status from inactive to active
		Arguments: user, which indicates which user's status to change
		Author: L.Sales, Python Ponies
	'''

	def change_status(user):
		user.active = True;