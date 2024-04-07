import random, string, uuid, requests, sys, os
from rich.console import Console
from rich.panel import Panel

def print2(t, d, c):
    Console().print(Panel(d, title=t, width=None, padding=(1, 3), style=c))
    # If you're wondering why I didn't use this for error and success printing, it's because if you copy the text, there would be parts of the rich (library) text included. ~ kiryu
    
def clear():
    platform = sys.platform.lower()
    if 'linux' in platform:
        os.system('clear')
    elif 'win' in platform:
        os.system('cls')
    else:
        pass          
    
def obtain(e, p):
    h = {
        'authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',       
        'x-fb-friendly-name': 'Authenticate',
        'x-fb-connection-type': 'Unknown',
        'accept-encoding': 'gzip, deflate',
        'content-type': 'application/x-www-form-urlencoded',
        'x-fb-http-engine': 'Liger'
    }
    d = {
        'adid': ''.join(random.choices(string.hexdigits, k=16)),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'email': e,
        'password': p,
        'generate_analytics_claims': '0',
        'credentials_type': 'password',
        'source': 'login',
        'error_detail_type': 'button_with_disabled',
        'enroll_misauth': 'false',
        'generate_session_cookies': '0',
        'generate_machine_id': '0',
        'fb_api_req_friendly_name': 'authenticate',
    }
    ses = requests.Session()
    ses.headers.update(h)
    submit = ses.post('https://b-graph.facebook.com/auth/login', data=d).json()  
       
    if 'session_key' in submit:
        print(f'\n\033[92m SUCCESS: {submit["access_token"]} \033[0m')
 
    elif 'www.facebook.com' in submit.get('error', {}).get('message', ''):
        print('\n\033[91m FAILED: ACCOUNT IN CHECKPOINT \033[0m')
    
    elif 'SMS' in submit.get('error', {}).get('message', ''):
        print('\n\033[91m FAILED: 2 FACTOR AUTHENTICATION IS ENABLED. PLEASE DISABLE IT BEFORE GETTING TOKEN \033[0m')
        
    elif submit.get('error', {}).get('error_user_title') == 'Wrong Credentials':
        print('\n\033[91m FAILED: WRONG CREDENTIALS \033[0m')
        
    elif submit.get('error', {}).get('error_user_title') == 'Incorrect Username':
        print('\n\033[91m FAILED: ACCOUNT DOES NOT EXIST \033[0M')
        
    elif 'limit' in submit.get('error', {}).get('message', ''):
        print('\n\033[91m FAILED: REQUEST LIMIT. USE VPN OR WAIT \033[0m')
        
    elif 'required' in submit.get('error', {}).get('message', ''):     
        print('\n\033[91m FAILED: PLEASE FILL IN ALL REQUIRED FIELDS \033[0m')
        
    else:
        print(f'\n\033[91m ERROR: {submit}\033[0m')

def main():
    clear()
    logo = """
        ,d8888b d8b
        88P'    ?88         d8P
     d888888P    88b     d888888P
       ?88'      888888b   ?88'
       88P       88P `?8b  88P
      d88       d88,  d88  88b
     d88'      d88'`?88P'  `?8b
                           """
    print2('', logo, 'violet')
    print2('', 'Facebook token getter by Kiryu\n ~ github.com/kiryudev', 'violet')
    e = input('\033[0m [›] Email/Usn :\033[90m ')
    p = input('\033[0m [›] Password  :\033[90m ')
    obtain(e, p)
    
main()
