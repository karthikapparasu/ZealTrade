#!c:\users\pcuser1.pcuser1-pc\appdata\local\programs\python\python38\python.exe
#Request_token need to be update daily. once a day.
def rtk():
    rt = open('request_token.txt', 'r').read()
    return rt
#Access_token
def att():
    at = open('access_token.txt', 'r').read()
    return at
#API_KEY
def atp():
    ap = '7d3io9rdvacxeslm'
    return ap
#API_SECRET_KEY
def sec():
    se = 'rdgmoxdos3y6p69ry2spekwq7ft532wm'
    return se




