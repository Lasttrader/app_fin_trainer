from django import template
import re

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(token):
    """
    string: значение, к которому нужно применить фильтр
    собственный фильтр censor, 
    который заменяет буквы нежелательных слов в заголовках и текстах статей на символ «*».
    """
    forbidden_words = ["Art", "трейдинг", "drug", "casino",]

    pat = re.compile("|".join(re.escape(w) for w in forbidden_words), flags=re.I)
    # Возвращаемое функцией значение подставится в шаблон.
    return pat.sub(lambda g: "*" * len(g.group(0)), token)
