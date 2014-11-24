=======
Rolodex
=======

Rolodex is a directory of people and the organizations they belong to. It's also a space where you can model relationships.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add rolodex and the django rest framework to your INSTALLED_APPS setting:

```python
    INSTALLED_APPS = (
        ...
        'rolodex',
	'rest_framework',
    )
```

2. Include the rolodex and rest framework auth URLconf in your project urls.py:

```python
    url(r'^rolodex/', include('rolodex.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
```

3. If you'd like to restrict views to only logged in users, set the variable in settings.py:

```python
    ROLODEX_SECURE = True 
```

It's also recommended you set django rest framework's auth to the django model permission in settings.py. You may also add anonymous read only like this:

```python
	REST_FRAMEWORK = {
	    # Use Django's standard `django.contrib.auth` permissions,
	    # or allow read-only access for unauthenticated users.
	    'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	    ]
	}
```

4. Optionally, you may set a `'rolodex'` database in DATABASES settings or pass a `ROLODEX_DB` environment variable to route to a dedicated database. 

5. Run `python manage.py migrate` (or `python manage.py migrate --database=rolodex` if you set up routing)to create the models and load fixtures.

