"""
Code
"""
import re

from html_to_markdown import ConversionOptions, PreprocessingOptions


def get_markdown_from_url(url: str) -> str:
    "Fetch markdown content from a given URL"
    import requests
    from html_to_markdown import convert

    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    res = response.text
    r = re.compile(r'^( *?)- (.*?)$', re.MULTILINE)
    res = r.sub(r'\n\1- \2 \n', res)  # Ensure list items are on separate lines

    r = re.compile(r'^( *?)([0-9]+\.) (.*?)$', re.MULTILINE)
    res = r.sub(r'\n\1\2 \3 \n', res)  # Ensure list items are on separate lines
    print(res)

    options = ConversionOptions(
        heading_style="atx",
        list_indent_width=2,
        bullets="*+-",
        strong_em_symbol="*",
    )
    # options.escape_asterisks = True
    options.code_language = "python"
    options.extract_metadata = True

    # find all html tags and convert them to markdown
    r = re.compile(r'<(pre|code|blockquote|ul|ol|li|h[1-6]|p|a|img|strong|em|table|thead|tbody|tr|th|td|span)(.*?)>(.*?)</\1>', re.DOTALL)
    matches = r.findall(res)
    for match in matches:
        full_tag = '<' + match[0] + match[1] + '>' + match[2] + '</' + match[0] + '>'
        md = convert(full_tag, options)
        res = res.replace(full_tag, md)


    res = res.replace('```', '\n```')  # Ensure code blocks are properly formatted
    # print(res)

    return res

def get_content_from_url(url: str) -> str:
    "Fetch raw content from a given URL"
    import requests

    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    res = response.text
    # Removing <head> content
    r = re.compile(r'<head>(.*?)</head>', re.DOTALL)
    res = r.sub('', res)
    # Removing content of class="entity-meta"
    r = re.compile(r'class="entity-meta">(.*?)</div>', re.DOTALL)
    res = r.sub('', res)
    return res

def define_env(env):
    "Declare environment for jinja2 templates for markdown"

    for fn in [get_markdown_from_url, get_content_from_url]:
        env.macro(fn)
