advLockExportador = 100
advLockPyMeuRH = 101
advLockPyRPA = 102

from nsj_pyRPA.resources.envConfig import getDb

def advisory_lock():
    try:
        _execute = getDb().execute_query("select pg_try_advisory_lock(:identificador) resultado", identificador=advLockPyRPA)

        if len(_execute) > 0:
            return _execute[0]["resultado"]
        else :
            return False
    except:
        return False
    

def advisory_unlock():
    try:
        _execute = getDb().execute_query("select pg_advisory_unlock(:identificador) resultado", identificador=advLockPyRPA)

        if len(_execute) > 0:
            return _execute[0]["resultado"]
        else :
            return False
    except:
        return False
    

def advisory_unlock_all():
    try:
        _execute = getDb().execute("select pg_advisory_unlock_all()")
    except:
        return False
