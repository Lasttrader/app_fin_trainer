{% extends "account/email/base_message.txt" %}
{% load account %}
{% load i18n %}

{% block content %}{% autoescape off %}{% user_display user as user_display %}{% blocktrans with site_name=current_site.name site_domain=current_site.domain %}Вы получили это сообщение, потому что пользователь {{ user_display }} указал этот email при регистрации на сайте {{ site_domain }}.

Для подтверждения регистрации пройдите по ссылке {{ activate_url }}

Хорошего дня!
{% endblocktrans %}{% endautoescape %}
{% endblock %}