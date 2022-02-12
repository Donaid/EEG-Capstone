import threading
import time
import csv

remainingTime = 0
sample = []

def main():
  global remainingTime
  global sample
  count = 0
  while(True):
    if(remainingTime == 0):
      threadSave = threading.Thread(target=exportSample, args=(sample[:],))
      threadSave.start()
      sample = []
      count=0
      print(f"sample from thread: {(len(sample))}")

      remainingTime = 5
      threadTimer = threading.Thread(target=timerThread)
      threadTimer.start()
    
    count += 1
    sampleTest = []
    sampleTest.append(count)
    sample.append(sampleTest)
  
def timerThread():
  global remainingTime
  global sample
  print("thread start")
  while(remainingTime != 0):
    time.sleep(1)
    remainingTime-=1
    print(f"remaining time: {remainingTime}")

def exportSample(rawList):
  print(f"raw list: {len(rawList)}")
  with open('./demo_output/playground.csv', 'w', newline='') as file:
    write = csv.writer(file)
    write.writerow(['rawEeg'])
    write.writerows(rawList)

  print(f"csv created")

main()
