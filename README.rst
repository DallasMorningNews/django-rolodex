=======
Rolodex
=======

Rolodex is a directory of people and the organizations they belong to. It's also a space where you can model relationships.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add rolodex and django rest framework to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rolodex',
	'rest_framework',
    )

2. Include the rolodex and rest framework auth URLconf in your project urls.py like this::

    url(r'^rolodex/', include('rolodex.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

3. Run `python manage.py migrate` to create the models and load fixtures.
