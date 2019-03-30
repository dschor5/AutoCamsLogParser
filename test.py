from AutoCAMS.CAMSArchive import *
from AutoCAMS.CAMSConstants import *

ARCHIVE_DIR = "./SampleData/"



a = Archive(ARCHIVE_DIR + "192.168.0.14_0014.txt")
b = Archive(ARCHIVE_DIR + "130.149.150.152_0012.txt")
#a.plotCabinInfo()
#b.plotCabinInfo()
#plt.show()

temp = b[...][b[I_ERROR_PHASE] == E_RED]

temp2 = temp.getConnectionCheck()

print(temp.size)
print(temp2.size)