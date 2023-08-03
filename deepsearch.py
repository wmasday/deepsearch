from time import sleep
from random import random
from multiprocessing import Process
import requests, re
from multiprocessing.dummy import Pool

headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
timeout = 10
verifySSL = True
extensions_needed = ['jpg', 'png', 'jpeg', 'docx', 'pdf', 'php', 'phtml', 'phar', 'php3', 'php5', 'php7', 'pht', 'txt']

def findExtensions(url, response):
    for ext in extensions_needed:
        extension = '.'+ ext
        if extension in response:
            open('deepsearch_'+ ext +'.txt', 'a').write(url +'\n')
        else:pass
        
def files(url, response):
    try:
        findExtensions(url, response)
        
        if 'alt="[TXT]">' in response and 'file-text.svg' in response:
            resources_php = re.findall(r'file-text.svg" alt="[TXT]">(.*?).php</a>', response)
        else:
            resources_php = re.findall(r'.php">(.*?).php</a>', response)

        for is_file in resources_php:
            is_url = url + is_file + '.php'
            is_url = is_url.replace(' ', '')  # Replace Blank Or Space
            check = requests.get(is_url, headers=headers, timeout=timeout)
            if 'FilesMan' in check.text:
                open(f"wso.txt", "a").write(f"{is_url}\n")
            elif 'type="file"' in check.text or "type='file'" in check.text:
                open(f"uploader.txt", "a").write(f"{is_url}\n")
            elif '<form' in check.text and check.status_code != 404:
                open(f"form.txt", "a").write(f"{is_url}\n")
            else:
                pass
    except:
        pass
    
    try:
        if 'alt="[TXT]">' in response and 'file-text.svg' in response:
            resources_phtml = re.findall(r'file-text.svg" alt="[TXT]">(.*?).phtml</a>', response)
        else:
            resources_phtml = re.findall(r'.phtml">(.*?).phtml</a>', response)

        for is_file in resources_phtml:
            is_url = url + is_file + '.phtml'
            is_url = is_url.replace(' ', '')  # Replace Blank Or Space
            check = requests.get(is_url, headers=headers, timeout=timeout)
            if 'FilesMan' in check.text:
                open(f"wso.txt", "a").write(f"{is_url}\n")
            elif 'type="file"' in check.text or "type='file'" in check.text:
                open(f"uploader.txt", "a").write(f"{is_url}\n")
            elif '<form' in check.text and check.status_code != 404:
                open(f"form.txt", "a").write(f"{is_url}\n")
            else:
                pass
    except:
        pass
        
def path_handle(url, response):
    try:
        pages = re.findall(r'/">(.*?)/</a></td><td align="right">', response)
        if len(pages) == 0:
            pages = re.findall(r'<a href="/(.*?)"><img class="icon" src="/_autoindex/assets/icons/folder-fill.svg" alt="Directory">', response)
        else:pass
        
        if len(pages) == 0:
            pages = re.findall(r'&nbsp;</td><td><a href="(.*?)/">', response)
        else:pass
            
        if len(pages) == 0:
            print (f'[!] PATH : {url} Failed To Get Directory...')
            print (f'[!] PATH : {url} Getting Files...')
            return files(url, response)
        else:pass
        
        for page in pages:
            if page == '':
                next(pages)
            else:pass
            
            path_url = url +'/'+ page
            check = requests.get(path_url, headers=headers, timeout=timeout, verify=verifySSL).text
            if 'Index of' in check:
                print(f'[!] PATH : Index Of Found {path_url}')
                files(path_url, check)
                path_handle(path_url, check)
            else:
                print(f'[!] PATH : Index Of Not Found {path_url}')
    except Exception as err:
        print(f'[!] PATH ERROR : {url}')
    
def lab(url):
    if 'http://' not in url:
        url = 'http://'+ url
    else:pass
    
    try:
        print (f'[!] Checking {url}')
        print (f'[!] {url} Getting Directory...')
        check = requests.get(url, headers=headers, timeout=timeout, verify=verifySSL).text
        pages = re.findall(r'/">(.*?)/</a></td><td align="right">', check)
        if len(pages) == 0:
            pages = re.findall(r'<a href="/(.*?)"><img class="icon" src="/_autoindex/assets/icons/folder-fill.svg" alt="Directory">', check)
        else:pass
        
        if len(pages) == 0:
            pages = re.findall(r'&nbsp;</td><td><a href="(.*?)/">', check)
        else:pass
        
        if len(pages) == 0:
            print (f'[!] {url} Failed To Get Directory...')
            print (f'[!] {url} Getting Files...')
            return files(url, check)
        else:pass
        
        print (f'[!] {url} Success Get Directory...')
        for page in pages:
            if page == '':
                next(pages)
            else:pass
            
            path_url = url +'/'+ page
            dirCheck = requests.get(path_url, headers=headers, timeout=timeout, verify=verifySSL).text
            print(f'[!] LAB : {url}/{page}')
            files(path_url, dirCheck)
            path_handle(path_url, dirCheck)
    except Exception as err:
        print(f'[!] LAB ERROR : {url}')

def init():
    try:
        target = input('[?] Target : ')
        if len(target) == 0:
            return init()
            
        lab(target)
    except:
        pass


if __name__ == '__main__':
    init()