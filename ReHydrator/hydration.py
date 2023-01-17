import random
import ast
import os
from datetime import datetime
import time
import tweepy 
import json
import csv
import sys

import time
import mmap
import random
from collections import defaultdict

# Usage: hydration.py [api_keys_file] [input] [key_no]

api = None
def read_api_keys():
  all_keys = []
  with open(sys.argv[1], "r") as inptr:
    for i in range(78):
      inptr.readline()
      consumer_key=inptr.readline().lstrip("consumer_key=\"").rstrip("\"\n")
      consumer_secret=inptr.readline().lstrip("consumer_secret=\"").rstrip("\"\n")
      access_key=inptr.readline().lstrip("access_key=\"").rstrip("\"\n")
      access_secret=inptr.readline().lstrip("access_secret=\"").rstrip("\"\n")
      inptr.readline()

      all_keys.append([consumer_key, consumer_secret, access_key, access_secret])
  
  return all_keys

def setup_tweepy():
  global api

  api_keys = read_api_keys()
  key_num = int(sys.argv[3]) - 1

  # assign the values accordingly 
  consumer_key=api_keys[key_num][0].lstrip().rstrip()
  consumer_secret=api_keys[key_num][1].lstrip().rstrip()
  access_key=api_keys[key_num][2].lstrip().rstrip()
  access_secret=api_keys[key_num][3].lstrip().rstrip()
  
  # authorization of consumer key and consumer secret 
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
  # set access to user's access key and access secret  
  auth.set_access_token(access_key, access_secret) 
    
  # calling the api  
  api = tweepy.API(auth, wait_on_rate_limit = True)

# def reformat(data):
#   data = data.split("},")
#   ans = []
#   for i in range(len(data)-1):
#     tweet = data[i]
#     try:
#       tweet = tweet + "}"
#       ans.append(json.loads(tweet))
#     except:
#       print("Error in reformat ", tweet, i, len(data), data[i-1])
#       exit()
#   return ans

def convert_line_to_dict(line): 
  # return ast.literal_eval(ast.literal_eval(line))
  d = {}
  id_str = "\'ID\': "
  id_start = line.find(id_str)
  id_end_indx = id_start + len(id_str)

  label_str = ", \'label\': "
  label_start = line.find(label_str)
  label_end_indx = label_start + len(label_str)

  text_str = ", \'text\': "
  text_start = line.find(text_str)
  text_end_indx = text_start + len(text_str)

  d['ID'] = line[id_end_indx: label_start].lstrip('\'').rstrip('\'')
  d['label'] = line[label_end_indx: text_start].lstrip('\'').rstrip('\'')
  d['text'] = line[text_end_indx: -2].lstrip('\'').rstrip('\'')

  return d

def getTweet(tweet_id):
  status = None
  global api
  try:
    status = api.get_status(tweet_id) 
  except Exception as e:
    if(str(e).find("Could not authenticate you") != -1 or str(e).find("Authentication") != -1 or str(e).find("token") != -1):
      print(str(e))
      time.sleep(60)
      os.remove("./RunningLog/" + sys.argv[3] + ".txt")
      exit()
    return {"error": str(e)}

  # d = {}
  # d["tweet_id"] = status._json["id"]
  # d["created_at"] = status._json["created_at"]
  # d["user_id"] = status._json["user"]["id"]
  # d["geo_source"] = status._json["geo_source"]
  # d["user_location"] = status._json["user_location"]
  # d["geo"] = status._json["geo"]
  # d["place"] = status._json["place"]
  # d["tweet_locations"] = status._json["tweet_locations"]
  d = status._json
  json_obj = json.dumps(d)

  return json_obj

def classify(tweet_id):
  status = None
  global api
  try:
    status = api.get_status(tweet_id) 
  # except tweepy.RateLimitError as e:
  #   print("Rate limit error exceed waiting for 15 mins")
  #   print(datetime.now())
  #   time.sleep(60 * 15)
  #   return ("Rate limit", "")
  except Exception as e:
    if(str(e).find("Could not authenticate you") != -1 or str(e).find("Authentication") != -1 or str(e).find("token") != -1):
      print(str(e))
      time.sleep(60)
      os.remove("./RunningLog/" + sys.argv[3] + ".txt")
      exit()
    return {"id": tweet_id, "error": str(e), "tweet_id": tweet_id}

  text = status.text.strip('\n').strip('\r')
  d = status._json
  # print(text)
  if (status.in_reply_to_status_id != None):
    d["label"] = "reply"
  elif (text.find("RT @") != -1 or (hasattr(d, 'retweeted_d'))):
    d["label"] = "retweet"
  else:
    d["label"] = "source"
  return d

# def has_US_location(tweet):
#   # change it to consider only user_location
#   return str(tweet).find("\'us\', \'state\'") != -1

def mapcount(filename):
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
      lines += 1
    return lines

def create_folder_if_doesnt_exit(d):
  isExist = os.path.exists(d)
  if not isExist:
    # Create a new directory because it does not exist 
    os.makedirs(d)

  # for dir in all_dirs:
  #   cur_dir = global_dir + dir + "/"

  #   file_names = [f for f in os.listdir(cur_dir) if isfile(join(cur_dir, f))]
    
def main():
  with open("./RunningLog/" + sys.argv[3] + ".txt", "w") as outptr:
    print("Running key #", sys.argv[3], file = outptr)
  time.sleep(10)

  # what percentage do you want to rehydrate
  target = 1 / 100

  input_file = sys.argv[2]

  # without the input folder
  indx = input_file.find("split_")
  if indx == -1:
    print("Error for file")
    os.remove("./RunningLog/" + sys.argv[3] + ".txt")
    time.sleep(60)
    exit()
  
  output_folder = "./GitDatasetOutput/"
  create_folder_if_doesnt_exit(output_folder)
  output_file = output_folder + input_file[indx:]
  
  total = mapcount(input_file)
  print(sys.argv)
  print("Total = ", total)

  setup_tweepy()

  filtered_num = 0
  processed_num = 0
  index = {}
  mode = "w"
  if (os.path.exists(output_file)):
    with open(output_file) as inptr:
      lines = 0 #mapcount("./Output/" + json_file + "_categorized.csv")
      reader = csv.reader(inptr)
      for row in reader:
        lines += 1

      print("Indexed ", lines, " lines")
      processed_num += lines

      mode = "a"

  print(total, processed_num)

  with open(input_file) as inptr, \
   open(output_file, mode) as outptr:
    try:
      count = 0
      for line in inptr:
        # Skip already done ones
        count += 1
        if (count < processed_num):
          continue
          
        # stop once done
        # if(processed_num / total >= target):
        if (processed_num == total):
          print("Target hit = ", processed_num, " / ", total, " = ", processed_num / total)
          os.remove("./RunningLog/" + sys.argv[3] + ".txt")
          time.sleep(60)
          exit()

        id = line
        
        processed_num += 1
        print(getTweet(id), file = outptr)
        
        if(count % 1000 == 0 or processed_num % 1000 == 0):
          print(count, " Processed: ", processed_num, " Filtered: ", filtered_num)
    except Exception as e:
      print ("Error = ", e)
      os.remove("./RunningLog/" + sys.argv[3] + ".txt")
      time.sleep(60)
      exit()

  print('250')
  time.sleep(60)


if __name__ == '__main__':
  if (len(sys.argv) != 4):
    print("# Usage: hydration.py [api_keys_file] [input] [key_no]")    
    time.sleep(60)
    exit()
  main()
