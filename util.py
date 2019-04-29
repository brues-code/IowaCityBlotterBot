

# f = open("logs/2019/04/21.txt", "r")
# fe = open("04-21-2019.txt", "a")
# if f.readable():
#     text: str = f.read()
#     splitText = text.split("\n")
#     for line in splitText:
#         if "Fetching https://www.iowa-city.org/icgovapps/police/details?dispatchNumber=" in line:
#             dispatch = line.split('=').pop()
#             fe.write("%s," % (dispatch))
# fe.close()
# f.close()

# Pythono3 code to rename multiple
# files in a directory or folder

# importing os module
import os

rootDir = "logs/"

for yearFolder in os.listdir(rootDir):
    yearDir = rootDir + yearFolder + "/"
    for monthFolder in os.listdir(yearDir):
        srcDir = yearDir + monthFolder + "/"
        for logFile in os.listdir(srcDir):
           if(len(logFile) == 6):
                src = srcDir + logFile
                date = logFile.split(".").pop(0)
                newFileName = "%s%s-%s-%s.txt" % (srcDir, monthFolder, date, yearFolder)
                print(newFileName)
                #os.rename(src, newFileName)
