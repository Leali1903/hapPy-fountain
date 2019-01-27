import sys
import subprocess

print('hallo')

print('zweites hallo')

subprocess.call([sys.executable, 'hello.py', 'htmlfilename.htm'])
