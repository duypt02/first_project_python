import os
import requests
import html
import sys
import re
import subprocess as sp
path = './exploit-db'

programName = "notepad.exe"

def checkDir():
    if not os.path.isdir(path):
        os.mkdir(path)

def help():
    help = """
    usage: exam.py [-h] [--exploit EXPLOIT] [--page PAGE] [--search SEARCH]

    Python Exam

    optional arguments:
    	-h, --help		  show this help message and exit
    	--exploit EXPLOIT	  exploit ID
    	--page PAGE     	  get page
    	--search SEARCH           search keyword
    """
    print(help)

def get_argument():
    args = sys.argv
    try:
        if 1 <= len(args) <= 2:
            return 'Help'
        else:
            if '--exploit' in args:
                rgxUrl = r'((?<=^https://www\.exploit-db\.com/exploits/)(\d+)$)|((?<=^exploit-db\.com/exploits/)(\d+)$)|(^\d+$)'
                id = re.search(rgxUrl, args[args.index('--exploit') + 1])
                if id:
                    return 'exploit ' + id.group() #return "exploit " + id
                else:
                    return 'Help'
            elif '--page' in args:
                pageNumber = args[args.index('--page') + 1]
                if pageNumber.isdigit():
                    if(int(pageNumber) >= 0):
                        return 'page ' + pageNumber #return "page " + số trang
                    else:
                        return 'Help'
                else:
                    return 'Help'
            elif '--search' in args:
                return 'search ' + args[args.index('--search') + 1]  #return "search " + chuỗi
            else:
                return 'Help'
    except:
        return 'Help'

def exploit_func(id):
    l = os.listdir(path)
    if (id +'.txt') in l:
        filepath= path + '/{}.txt'.format(id)
        sp.Popen([programName, filepath])
    else:
        url = 'https://exploit-db.com/exploits/{}'.format(id)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res= requests.get(url, headers = headers)
        exploit = res.text[res.text.find('<code') : res.text.find('</code>')]
        exploit = html.unescape(exploit[exploit.find('">') +2 :])
        if exploit:
            filepath= path + '/{}.txt'.format(id)
            f = open(filepath, 'w')
            f.write(exploit)
            f.close()
            sp.Popen([programName, filepath])
        else:
            print('No Data')

def page_func(id):
    l = os.listdir(path)
    skip = 5 * (id)
    l = sorted(l, key=(lambda x: int(x[:-4])))
    for i in range(skip, skip+5):
        if i < len(l):
            print(l[i])
        else:
            break

def search_func(keyword):
    l = os.listdir(path)
    rgx = r'(?<![\w])(' + '|'.join(keyword) + ')(?![\w])'
    for i in l:
        filepath= path + '/' + i
        f = open(filepath, 'r')
        if re.search(rgx, f.read(), re.IGNORECASE):
            print('./exploit-db/' + i)
        f.close()

if __name__ == '__main__':
    command = get_argument()
    checkDir()
    if 'exploit' in command:
        exploit = command.split()[1]
        exploit_func(exploit)
    elif 'page' in command:
        page = int(command.split()[1])
        page_func(page)
    elif 'search' in command:
        search = command.split()[1:]
        search_func(search)
    else:
        help()




