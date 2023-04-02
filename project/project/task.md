консоль  
DEBUG и выше
время, уровень сообщения, сообщения
WARNING и выше
время, уровень сообщения, сообщенияб путь к источнику
ERROR CRITICAL
время, уровень сообщения, сообщенияб путь к источнику, стек
логгер - django
фильтр - DEBUG = True

general.log
INFO
времени, уровня логирования, модуль, сообщение
логгер - django
фильтр - DEBUG = False

errors.log
ERROR CRITICAL
время, уровень сообщения, сообщенияб путь к источнику, стек
логгеры - django.request, django.server, django.template, django.db.backends.

security.log
INFO
времени, уровня логирования, модуль, сообщение
логгер - django.security

email
время, уровень сообщения, сообщенияб путь к источнику
логгер - django.request и django.server
фильтр - DEBUG = False

