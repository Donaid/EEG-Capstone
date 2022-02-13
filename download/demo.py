from mindwavelsl import MindwaveLSL
from mindwavelsl.logger import MindwaveLogger
import time
import csv
import threading
import sys, os

mwlsl = MindwaveLSL('localhost', 13854)

mwlsl.setup()
mwlsl.write('{"enableRawOutput": true, "format": "Json"}')

RECORD_DURATION = 8
FILE_PATH = "./demo_output/"
remainingTime = 0
sample = []
status = 0
log = MindwaveLogger("mindwave-connector")
# filename_count = 0

def timerThread():
  global remainingTime
  while(remainingTime != 0):
    time.sleep(1)
    remainingTime -= 1
    print(f"remaining time: {remainingTime}")

def exportRaw(rawList):
  print(f"raw list length: {len(rawList)}")
  # global filename_count
  # fileformat = ".csv"
  # filename_iterative = FILE_PATH + str(filename_count) + fileformat

  filename_demo = FILE_PATH + "demo.csv"
  filenameRaw = "demo.csv"
  with open(filenameRaw, 'w', newline='') as file:
    write = csv.writer(file)
    write.writerow(['rawEeg'])
    write.writerows(rawList)
  print(f"csv created")
  # filename_count = filename_count + 1

def exportStatus(currentStatus):
  writeStatus = ''
  if(currentStatus == 0):
    writeStatus = 'disconnected'
  elif(currentStatus == 1):
    writeStatus = 'connected'
  
  filename_status = FILE_PATH + "status.txt"
  filenameStatus = "status.txt"
  with open(filenameStatus, 'w', newline='') as filestatus:
    filestatus.write(writeStatus)

def main():
  global sample
  global remainingTime
  global status
  threadSaveStatus = threading.Thread(target=exportStatus, args=(0,))
  threadSaveStatus.start()

  while(True):
    response = None
    response = mwlsl.read()
    if (response is None):
      continue
    
    if 'rawEeg' in response:
      if(remainingTime == 0):
        threadSaveRaw = threading.Thread(target=exportRaw, args=(sample[:],))
        threadSaveRaw.start()
        sample = []

        remainingTime = RECORD_DURATION
        threadTimer = threading.Thread(target=timerThread)
        threadTimer.start()

      raw = response.get('rawEeg')
      sampleTest = []
      sampleTest.append(raw)
      sample.append(sampleTest)

      # sample.append(raw)
    else:
      if 'poorSignalLevel' in response:
        if(response.get('poorSignalLevel') != 0 and status == 1):
          status = 0
          threadSaveStatus = threading.Thread(target=exportStatus, args=(status,))
          threadSaveStatus.start()
          print("")
          log.info("status: disconnected / poor signal")
          print("")
          # print("status: disconnected / poor signal")
        elif(response.get('poorSignalLevel') == 0 and status ==0):
          status = 1
          threadSaveStatus = threading.Thread(target=exportStatus, args=(status,))
          threadSaveStatus.start()
          print("")
          log.info("status: connected")
          print("")
          # print("status: connected")

      if 'status' in response:
        print(f"status: {response.get('status')}, {response}")
      else:
        print(f"response: {response}")


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    exportStatus(0)
    log.info("Exit")
    mwlsl.stop()
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
