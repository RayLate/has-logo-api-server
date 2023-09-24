import tldextract
from xdriver.xutils.PhishIntentionWrapper import PhishIntentionWrapper
from knowledge_expansion.utils import *
from datetime import date, timedelta, datetime
import warnings
from db.db import *
import socket
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.functional")


class MyLogger:
    def __init__(self,file_path):
        self.file_path = file_path
        
    def log(self,message):
        timestamp = datetime.now().strftime('%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] {str(message)}'
        with open(self.file_path,'a') as file:
            file.write(log_message + '\n')

logger = MyLogger('runtime.log.txt')

app = Flask(__name__)
app.name='dynaphish server'

def has_logo_test(screenshot_path):
    phishintention_config_path = './field_study_logo2brand/configs.yaml'
    PhishIntention = PhishIntentionWrapper(config_path=phishintention_config_path,reload_targetlist=False)

    # Has a logo or not?
    has_logo, in_target_list = PhishIntention.has_logo(
        screenshot_path=screenshot_path)
    print('Has logo? {} Is in targetlist? {}'.format(has_logo, in_target_list))
    return has_logo, in_target_list


def get_html_title(url):
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            return title
        return ''
    except:
        return ''


def get_domain(url):
    # Function to extract the domain from a URL
    domain = tldextract.extract(url).domain + '.' + \
        tldextract.extract(url).suffix
    return domain

def get_container_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def forbidden_words_test(url):
    # Function to check for forbidden words in a URL
    domain = ''
    title = ''
    try:
        domain = get_domain(url) or ''
        title = get_html_title(url) or ''
        print('Domain:', domain, 'Title:', title)
        if domain in title.lower() or re.search(OnlineForbiddenWord.WEBHOSTING_TEXT, title, re.IGNORECASE):
            print('Hit forbidden words')
            return True, domain, title
        print('No forbidden words')
        return False, domain, title
    except Exception as e:
        print(e)
        return True, domain, title


print(has_logo_test('./datasets/accounts.g.cdcde.com/shot.png'))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=5000)







