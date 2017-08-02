import math
import re
from django.utils.html import strip_tags

def words_count(html_content):
    stripped = strip_tags(html_content)
    words = re.findall(r'\w+', stripped)
    return len(words)

def read_time(html_content):
    words = words_count(html_content)
    time_in_min = math.ceil(words/220) # assume 220 words per minute
    return int(time_in_min)