import os
print(os.popen("ls -l && pwd").read())
