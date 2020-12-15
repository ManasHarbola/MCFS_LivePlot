import time
from random import randint

inFile = open('DIGISIM_dcpdp_log_1.log')
outFile = open('logfile.log', 'a')

for line in inFile:
    outFile.write(line)
    outFile.flush()
    time.sleep(0.15)

outFile.close()
