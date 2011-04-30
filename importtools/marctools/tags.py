TAGS = {
}

def meaning(tag, subfield=""):
    if subfield:
        key = "%s.%s" % (tag, subfield)
    else:
        key = tag
    return TAGS.get(key)
    