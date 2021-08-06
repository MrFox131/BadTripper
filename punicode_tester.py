def punicode(name):
    name = name.decode("idna").split(".")[:-1]
    is_ascii_used = False
    is_unicode_used = False
    for y in name:
        for x in y:
            if ord(x)>255:
                is_unicode_used = True
            else:
                is_ascii_used = True
    if is_unicode_used and is_ascii_used:
        return True
