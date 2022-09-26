from distutils.text_file import TextFile
from email.mime.text import MIMEText
import requests
import codecs
import smtplib
from email.message import EmailMessage

from cmath import cos
from bs4 import BeautifulSoup


def parse():
    url = 'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_bots%2Cdevelopment_scripts%2Cdevelopment_other'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    response = requests.get(url, headers=header)

    if response.status_code == 200:
        with codecs.open('data.txt', 'w', 'utf-16') as f:
            page = BeautifulSoup(response.text, 'html.parser')
            list = page.find('ul', attrs={'class': 'content-list'})
            list_items = list.findAll('li', attrs={'class': 'content-list__item'})
            for list_item in list_items:
                site_url = 'https://freelance.habr.com/'  
                
                task_title_div = list_item.find('div', attrs={'class': 'task__title'})
                
                task_text = task_title_div['title']
                print(task_text, file=f)
                
                task_link = task_title_div.find('a')['href']
                task_link = site_url + task_link
                print(task_link, file=f)
                
                # Parse description
                desc_response = requests.get(task_link, headers=header)
                if desc_response.status_code == 200:
                    page = BeautifulSoup(desc_response.text, 'html.parser')
                    desc = page.find('div', attrs={'class': 'task__description'})
                    # Replacing break lines
                    for br in desc.find_all('br'):
                        br.replace_with('\n')
                    print(desc.text, file=f)
                
                views = list_item.find('span', attrs={'class': 'params__views'}).find('i').text
                print(f'{views} просмотра', file=f)
                
                response = list_item.find('span', attrs={'class': 'params__responses'})
                if response:
                    response = response.find('i').text
                    print(f'{response} отклика', file=f)
                
                time_ago = list_item.find('span', attrs={'class': 'params__published-at'}).find('span').text
                print(f'{time_ago}', file=f)
                
                cost = list_item.find('span', attrs={'class': 'count'})
                if cost:
                    cost = cost.text
                    print(cost, file=f)
                else:
                    print('Договорная', file=f)
                
                separator = ''
                for i in range(100):
                    separator += '='
                print(file=f)
                print(separator, file=f)
                print(file=f)
            # with open(f, 'rb') as fp:
            #     msg = EmailMessage()
            #     msg.set_content(fp.read())
            # msg['Subject'] = f'The contents of {f}'
            # msg['From'] = 'kek'
            # msg['To'] = 'nklnsk708@gmail.com'
            # s = smtplib.SMTP('localhost')
            # s.send_message(msg)
            # s.quit()

parse()
