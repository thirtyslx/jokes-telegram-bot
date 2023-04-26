def use_html_tag(text: str, tag: str) -> str:
    return f'<{tag}>{text}</{tag}>'


def b(text: str) -> str:
    return use_html_tag(text, 'b')


def i(text: str) -> str:
    return use_html_tag(text, 'i')


def u(text: str) -> str:
    return use_html_tag(text, 'u')


def code(text: str) -> str:
    return use_html_tag(text, 'code')


def href(url: str, text: str) -> str:
    return f'<a href="{url}">{text}</a>'
