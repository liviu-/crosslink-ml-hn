from subprocess import Popen, PIPE


TOOL = 'crosslinking_bot'


def run_tool(args=[]):
    p = Popen([TOOL] + args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = (out.decode('utf-8') for out in p.communicate())
    return p, stdout, stderr

def test_simple_call():
    p, stdout, stderr = run_tool()
    assert p.returncode == 0


