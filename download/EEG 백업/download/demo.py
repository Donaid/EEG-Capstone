from mindwavelsl import MindwaveLSL
import time
import csv
import threading

mwlsl = MindwaveLSL('localhost', 13854)
# mwlsl = MindwaveLSL('localhost', 13854, file_outlet_path='./demo_output', run_lsl=False)

# Setup the LSL outlet and the ThinkGear connection
mwlsl.setup()
mwlsl.write('{"enableRawOutput": true, "format": "Json"}')

# Run the service
# mwlsl.run()

remainingTime = 0
sample = []
filename_count = 0

def timerThread():
  global remainingTime
  print("thread start")
  while(remainingTime != 0):
    time.sleep(1)
    remainingTime-=1
    print(f"remaining time: {remainingTime}")

def exportSample(rawList):
  print(f"raw list length: {len(rawList)}")
  global filename_count
  filename1 = "./demo_output/"
  filename3 = ".csv"
  #filename = filename1+str(filename_count)+filename3
  filename = "demo.csv"
  with open(filename, 'w', newline='') as file:
    write = csv.writer(file)
    write.writerow(['rawEeg'])
    write.writerows(rawList)
  print(f"csv created")
  filename_count = filename_count + 1

def main():
  global sample
  global remainingTime
  while(True):
    response = None
    response = mwlsl.read()
    if (response is None):
      continue
    
    if 'rawEeg' in response:
      if(remainingTime == 0):
        print(f"sample before reset: {(len(sample))}")
        threadSave = threading.Thread(target=exportSample, args=(sample[:],))
        threadSave.start()
        sample = []
        print(f"sample after reset: {(len(sample))}")

        remainingTime = 15
        threadTimer = threading.Thread(target=timerThread)
        threadTimer.start()

      raw = response.get('rawEeg')
      sampleTest = []
      sampleTest.append(raw)
      sample.append(sampleTest)

      # sample.append(raw)
    else:
      if 'status' in response:
        print(f"status: {response.get('status')}, {response}")
      else:
        print(f"response: {response}")

main()

print("process end")

