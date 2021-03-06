from django.template.defaultfilters import stringfilter
from django.template import Library
from django.utils.safestring import mark_safe
from django.utils.html import urlize

register = Library()

def html_urlize(value, autoescape=None):
    """Converts URLs in html into clickable links."""
    from BeautifulSoup import BeautifulSoup
    ignored_tags = ['a', 'code', 'pre']
    soup = BeautifulSoup(value)
    tags = soup.findAll(True)
    text_all = soup.contents
    for text in text_all:
        if text not in tags:
            parsed_text = urlize(text, nofollow=True, autoescape=autoescape)
            text.replaceWith(parsed_text)
    for tag in tags:
        if not tag.name in ignored_tags:
            soup_text = BeautifulSoup(str(tag))
            if len(soup_text.findAll()) > 1:
                for child_tag in tag.contents:
                    child_tag.replaceWith(html_urlize(str(child_tag)))
            elif len(soup_text.findAll()) > 0:
                text_list = soup_text.findAll(text=True)
                for text in text_list:
                    parsed_text = urlize(text, nofollow=True, autoescape=autoescape)
                    text.replaceWith(parsed_text)
                try:
                    tag.replaceWith(str(soup_text))
                except:
                    pass
    return mark_safe(str(soup))

html_urlize.is_safe = True
html_urlize.needs_autoescape = True
html_urlize = stringfilter(html_urlize)
register.filter(html_urlize)