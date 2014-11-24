class RolodexRouter(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'rolodex':
			return 'rolodex'
		else:
			return 'default'
	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'rolodex':
			return 'rolodex'
		else:
			return 'default'
	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'rolodex' or obj2._meta.app_label == 'rolodex':
			return True
		return None

	def allow_migrate(self, db, model):
		if db == 'rolodex':
			return model._meta.app_label == 'rolodex'
		elif model._meta.app_label == 'rolodex':
			return False
		return None