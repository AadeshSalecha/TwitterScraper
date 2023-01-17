import time
import sys
import subprocess
import os
from os.path import isfile, join
import shutil

##########################################################################
#                                                                        #
#  Usage: python3 multi_terminal.py api_keys_file inputs_file to_run.py  # 
#                                                                        #
##########################################################################

def main():
  # Remove running logs
  log_dir = "./RunningLog/"
  shutil.rmtree(log_dir)
  os.mkdir(log_dir)

  # If not enough arguments
  if(len(sys.argv) != 4):
    print("Usage: python3 multi_terminal.py api_keys_file inputs_file to_run.py")
    sys.exit(0)

  # Working keys 
  # invalid   keys = [1, 3, 4, 15, , 13, 9, 11, 40, 48, 49, 50, 77, 78]
  keys = [1, 3, 4, 48, 49, 50]
  keys.sort()

  # Open Inputs
  inputs_file = sys.argv[2]
  inputs = read_inputs(inputs_file)

  program_to_run = sys.argv[3]

  if(len(keys) < len(inputs)):
    print("Not enough keys for all inputs")

  # Open in Terminals
  current_processes = []
  counter = 0  
  while counter < (min(len(keys), len(inputs))):
    command = "gnome-terminal --tab -- " + construct_command(to_run = program_to_run, keys_file = sys.argv[1], key_num = keys[counter], data_file = inputs[counter])
    print(command, counter)
    subprocess.Popen(command, shell = True)
    counter += 1
    time.sleep(1)
  
  while counter < len(inputs):
    for i in range(len(keys)):
      if (not os.path.exists("./RunningLog/" + str(keys[i]) + ".txt")):
        command = "gnome-terminal --tab -- " + construct_command(to_run = program_to_run, keys_file = sys.argv[1], key_num = keys[i], data_file = inputs[counter])
        print(command, counter)
        counter += 1
        subprocess.Popen(command, shell = True)
        time.sleep(10)
    time.sleep(20)

def construct_command(to_run, key_num, keys_file, data_file):
  return "python3 " + to_run + " " + keys_file + " " + data_file + " " + str(key_num)

def read_api_keys(file_name):
  keys = []
  with open(file_name, 'r') as inptr:
    while True:
      comment = inptr.readline()
      consumer_key = inptr.readline().lstrip('consumer_key=').rstrip('\n')
      consumer_secret = inptr.readline().lstrip('consumer_secret=').rstrip('\n')
      access_key = inptr.readline().lstrip('access_key=').rstrip('\n')
      access_secret = inptr.readline().lstrip('access_secret=').rstrip('\n')
      blank_line = inptr.readline()

      if (not comment): ### EOF
        break

      keys.append([consumer_key, consumer_secret, access_key, access_secret])
  return keys

def read_inputs(file_name):
  inputs = []
  with open(file_name, 'r') as inptr:
    inputs = [x.rstrip('\n') for x in inptr.readlines()]
  return inputs

if __name__ == '__main__':
  main()