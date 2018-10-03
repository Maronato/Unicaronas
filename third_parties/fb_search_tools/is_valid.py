import re


def is_valid(item):
    """Is Valid
    True if is a offering and not full. False otherwise
    """
    message = item['message']
    return re.search('ofereco', message) and not re.search('lotad', message)
