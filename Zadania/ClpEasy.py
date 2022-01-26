from clp3 import clp
from Library import CLP_ON
if CLP_ON:
    from clp3 import clp
    import clp_settings

def CLPBasicWord(s):
    id = clp(s)
    if len(id) > 0:
        list_p = clp.forms(id[0])
        if len(list_p) > 0:
            s = list_p[0]
    return s