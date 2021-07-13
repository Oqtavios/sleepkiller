from ctypes import windll

# WINDOWS CONSTANTS
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_AWAYMODE_REQUIRED = 0x00000040  # not used
ES_DISPLAY_REQUIRED = 0x00000002


def updatePreventionState(state=None, requireDisplay=True):
    if state:
        if requireDisplay:
            threadExecState = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        else:
            threadExecState = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    else:
        threadExecState = ES_CONTINUOUS

    windll.kernel32.SetThreadExecutionState(threadExecState)
