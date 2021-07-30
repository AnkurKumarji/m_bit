from datetime import datetime
from time import sleep
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers,login_data = {},[]

def Variable_ini():
    global headers,login_data
    print('[+] Developer ..Ankur Kumar..@yesankur')
    with open('Cookies.ql', 'a') as f: pass
    with open('Accounts.txt', 'a') as f: pass
    with open('Login_data.txt','r+') as f: login_data = f.read().splitlines()
    headers = {'Host': 'www.instagram.com', 'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html',
               'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip',
               'X-Instagram-AJAX': 'f1259423883b','X-IG-App-ID': '936619743392459',
               'Content-Type': 'application/x-www-form-urlencoded','X-Requested-With': 'XMLHttpRequest'}
    return True
Variable_ini()

def login():
    print(login_data)
    cookies = requests.get('https://www.instagram.com/', headers=headers).cookies.get_dict()
    use_cookie = {'ig_did': cookies['ig_did'], 'mid': cookies['mid']}
    headers['X-CSRFToken'] = cookies['csrftoken']
    time = int(datetime.now().timestamp())
    data = {"username": login_data[0], "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{time}:{login_data[1]}","queryParams": "{}", "optIntoOneTap": "false"}
    res = requests.post("https://www.instagram.com/accounts/login/ajax/", headers=headers, cookies=cookies, data=data)
    new_cookie = res.cookies.get_dict()
    try:
        if res.json()['authenticated'] == True:
            use_cookie.update(new_cookie)
            with open('Cookies.ql','w') as f: f.write(str(use_cookie))
            return True
        else: return False
    except:
        print('[x] Login Details Are Incorrect...')
        return False


def task(type,acc):
    make = 'follow'
    with open('Cookies.ql', 'r') as f: main_cookie = eval(f.read().splitlines()[0])
    headers['X-CSRFToken'] = main_cookie['csrftoken']
    if type=='follow' or type=='f' or type=='fol': make = 'follow'
    elif type=='unfollow' or type=='unf' or type=='unfol': make = 'unfollow'
    res = requests.post(f'https://www.instagram.com/web/friendships/{acc}/{make}/', headers=headers,cookies=main_cookie).json()
    if res['status']=='ok': return True
    else: return False

def cookie_check():
    cooki_dta = task('fol','5907224148')
    if cooki_dta == False: login()
    elif cooki_dta == True: return cooki_dta
    return task('fol','5907224148')

def insta_id(username):
    UserData = {}
    ids = requests.get(f"https://www.instagram.com/web/search/topsearch/?query={username}",headers={"User-Agent": "Mozilla/5.0"}).json()
    for id in range(170):
        try:
            if ids['users'][id]['user']['username'] == username:
                UserData['id'] = ids['users'][id]['user']['pk']
                UserData['name'] = ids['users'][id]['user']['full_name']
                UserData['username'] = ids['users'][id]['user']['username']
                UserData['profile_pic'] = ids['users'][id]['user']['profile_pic_url']
                return UserData
        except: pass
    return {'id': 'Invalid UserName'}


# print(cookie_check())
# cookie_check()
while True:
    login()
    try:
        cookie_check()
        Acc_ids = []
        with open('Accounts.txt','r') as f: Accounts = f.read().splitlines()
        for Acc in Accounts: Acc_ids.append(insta_id(Acc)['id'])
        print(Accounts,'\n',Acc_ids)
        while True:
            for Acc_id in Acc_ids:
                print('Follow ',task('fol',Acc_id))
                sleep(60)
            sleep(40*60)
            for Acc_id in Acc_ids:
                print('UnFollow ',task('unfol',Acc_id))
                sleep(60)
            print('------------')
    except: pass


# print(insta_id('yesankur'))
# task('fol','173560420')
# # print(login())
