from functools import wraps

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'

#Features
PEOPLE = 'people;

security_recs = None

temp_recs = {
	PEOPLE: {
		CREATE: {
			USER_LIST: [kuss@nyu.edu],
			CHECKS: {
				LOGIN: True,
			},
		},
	},
}


def read() -> dict:
	global security_recs
	security_recs = temp_recs
	return security_recs


def needs_recs(fn):
	@wraps(fn)
	def wrapper(*args, **kwards):
		global security_recs
		if not security_recs:
			security_recs = read()
		return fn(*args, **kwargs)
	return wrapper

@needs_recs
def read_feature(feature_name: str) -> dict:
	if feature_name in security_recs:
		return security_recs[feature_name]
	else:
		return None