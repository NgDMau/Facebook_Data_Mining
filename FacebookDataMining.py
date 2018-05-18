
# coding: utf-8

import json
import requests
import facebook
import string
import re
import threading
import sys

def remove_emojis(text):   ## this function removes all the emoticons in the text
    return re.sub('[^a-zA-ZÀ-ʠḀ-ỿ.?!%(&,.-^@:"+=/\) ]+', '', text)
def make_file_name(text):  ## and this converts file's name from its corresponding Page's name.
    return re.sub('[^a-zA-Z]+', '', text)

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',        ## only these Vietnamese characters will be kept later.
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    ## this function remove the accent signs in Vietnamese
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def download_all_posts(object_link,ACCESS_TOKEN):
    base_url      = 'https://graph.facebook.com/v3.0/'
    fields        = 'id,name,posts.limit(25)'        # this field defines what information we can get
    url           = base_url + object_link +'?fields=' + fields + '&access_token=' + ACCESS_TOKEN
    NumberOfPosts = 0                                            # number of posts of each page
    content       = requests.get(url).json()                     #request JSON from facebook
    rough_name    = content['name']                              # take 'name' element in JSON
    file_name     = make_file_name(convert(rough_name)) + ".txt" # make a file name based on page's name
    print("Starting with "+convert(rough_name))
    text_file     = open(file_name,'w')
    for x in range ( len(content['posts']['data']) ):  
        if 'message' in content['posts']['data'][x]:  # some posts have no message but story
            text  = content['posts']['data'][x]['message']
            text_file.write(remove_emojis(text))
            text_file.write("\n")              # take n write post from the first "result page"
            NumberOfPosts = NumberOfPosts +1
    content = requests.get(content['posts']['paging']['next']).json() # go to the next "result page"
    if(content['data'] != None):
        while('next' in content['paging']):  # if there is still a next "result page"
            for x in range ( len(content['data'])):
                if(content['data'][x] != None):
                    if 'message' not in content['data'][x] : # some posts have no message but story
                        NumberOfPosts = NumberOfPosts 
                    else:
                        text= content['data'][x]['message']
                        text_file.write(remove_emojis(text))
                        text_file.write("\n")  # write posts'messages to text file
                        NumberOfPosts = NumberOfPosts +1
            content = requests.get(content['paging']['next']).json() # go to the next "result page"
    print("------------------\n")
    print("Done for "+convert(rough_name)+"\n"+"Number of posts is: "+ str(NumberOfPosts))
    print("------------------")



class myThread (threading.Thread):

    def __init__(self,threadID,object_link,ACCESS_TOKEN):
        threading.Thread.__init__(self)
        self.threadID      = threadID
        self.object_link   = object_link
        self.ACCESS_TOKEN  = ACCESS_TOKEN
        
    def run(self):
        download_all_posts(self.object_link,self.ACCESS_TOKEN)

    
def run_task(Pages_Link_File_Name,access_token):
    with open(str(Pages_Link_File_Name)) as f_in: # read lines in text file containing links
        lines = list(line for line in (l.strip() for l in f_in) if line) 
    print("\nThe posts of these pages below are going to be downloaded:")
    for line in lines:
        print(line)
    thread = []  # make a list of thread
    for i in range (len(lines)):
        thread.append(myThread(i,lines[i],access_token))
        thread[i].start()    

run_task(sys.argv[1],sys.argv[2])  # NOW WE RUN ITTTTT

