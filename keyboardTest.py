import subprocess


def asRun(aScript):
    """
    Run the given AppleScript and 
    return the standard output and error.
    """
    osa = subprocess.Popen(['osascript', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
    return osa.communicate(bytes(aScript, 'UTF-8'))[0]


def asQuote(aStr):
    """
    Return the AppleScript equivalent of the given string.
    """
    aStr = aStr.replace('"', '" & quote & "')
    return '"{}"'.format(aStr)


pdScript = '''
tell application "System Events"
    key code 123 using {control down}
end tell
'''

ndScript = '''
tell application "System Events"
    key code 124 using {control down}
end tell
'''

asRun(ndScript)
