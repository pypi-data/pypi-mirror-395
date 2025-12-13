from userAgentManager import *
uaMgr = UserAgentManager(randomAll=True)
for i in range(10):
    input(uaMgr.get_user_agent())
