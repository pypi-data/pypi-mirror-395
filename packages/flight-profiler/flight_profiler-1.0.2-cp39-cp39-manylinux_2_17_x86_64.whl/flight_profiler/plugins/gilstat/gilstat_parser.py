
def valid(params):
    if len(params) < 1 or ((params[0] != "on" and params[0] != "off")):
        return False
    return True
