#!/usr/bin/python3
import os
import sys
import threading
import time
import random


start_time = time.time()

data_path = './data/'
file_list = []
number_of_files = 10

global done
done = False

def print_time(from_time):
    global done
    while not done:
        sys.stdout.write('\r{0} seconds elapsed...'.format('%.4f'%(time.time()-from_time)))
        sys.stdout.flush()
        time.sleep(.5)
    sys.stdout.write('\r{0} seconds elapsed...\n'.format('%.4f'%(time.time()-from_time)))
    sys.stdout.flush()


#t = threading.Thread(target=print_time, args=(start_time,))
#t.start()

for (dirpath, dirnames, filenames) in os.walk(data_path):
    for filename in filenames:
        if filename.endswith('.txt'):
            file_list.append(dirpath+'/'+filename)

random.shuffle(file_list)
with open('input.txt', 'w') as outfile:
    for fname in file_list[:number_of_files]:
        with open(fname) as infile:
            for l in infile:
                outfile.write(l)
done = True
#t.join()

print("input.txt created from {0} files...".format(number_of_files))



print("\nDone in {0} seconds...".format('%.2f'%(time.time()-start_time)))
