from email.mime.text import MIMEText
import smtplib
import sys
import os
import requests
import codecs

from bs4 import BeautifulSoup
from smtplib import SMTP


file_name = 'data.txt'
site_url = 'https://freelance.habr.com/'
get_tasks_url = 'https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_bots%2Cdevelopment_scripts%2Cdevelopment_other'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_response(url):
    tasks_response = requests.get(url, headers=header)
    if tasks_response.status_code != 200:
        raise Exception(f'HTTP ERROR {tasks_response.status_code}')
    return tasks_response


def get_list_items(tasks_response):
    page = BeautifulSoup(tasks_response.text, 'html.parser')
    list = page.find('ul', attrs={'class': 'content-list'})
    list_items = list.findAll('li', attrs={'class': 'content-list__item'})
    return list_items


def get_task_title_div(list_item):
    task_title_div = list_item.find('div', attrs={'class': 'task__title'})
    return task_title_div


def print_to_file(text, file_name):
    with codecs.open(file_name, 'a', 'utf-8') as f:
        print(text, file=f)


def print_task_text(list_item):
    task_title_div = get_task_title_div(list_item)
    task_text = task_title_div['title']
    print_to_file(task_text, file_name)


def print_task_link(list_item):
    task_url = site_url + get_task_url(list_item)
    print_to_file(task_url, file_name)


def get_task_url(list_item):
    task_title_div = get_task_title_div(list_item)
    task_url = task_title_div.find('a')['href']
    return task_url


def print_description(list_item):
    task_url = get_task_url(list_item)
    url = site_url + task_url
    desc_response = get_response(url)
    if desc_response.status_code != 200:
        return
    page = BeautifulSoup(desc_response.text, 'html.parser')
    desc = page.find('div', attrs={'class': 'task__description'})
    # Replacing break lines
    for br in desc.find_all('br'):
        br.replace_with('\n')
    print_to_file(desc.text, file_name)


def print_views(list_item):
    views = list_item.find(
        'span', attrs={'class': 'params__views'}).find('i').text
    views = f'{views} просмотра'
    print_to_file(views, file_name)


def print_tasks_response(list_item):
    tasks_response = list_item.find(
        'span', attrs={'class': 'params__responses'})
    if tasks_response:
        tasks_response = tasks_response.find('i').text
        tasks_response = f'{tasks_response} отклика'
        print_to_file(tasks_response, file_name)


def print_time_ago(list_item):
    time_ago = list_item.find(
        'span', attrs={'class': 'params__published-at'}).find('span').text
    print_to_file(time_ago, file_name)


def print_cost(list_item):
    cost = list_item.find('span', attrs={'class': 'count'})
    if cost:
        cost = cost.text
        print_to_file(cost, file_name)
    else:
        print_to_file('Договорная', file_name)


def print_separator():
    separator = ''
    for i in range(100):
        separator += '='
    print_to_file('', file_name)
    print_to_file(separator, file_name)
    print_to_file('', file_name)


def get_task_column(list_item):
    task_column = list_item.find('div', attrs={'class': 'task__column_desc'})
    return task_column


def is_have_one_of_tags(list_item, tags):
    for tag in tags:
        task_tags = list_item.find(
            'ul', attrs={'class': 'tags tags_short'}).findAll('li')
        for task_tag in task_tags:
            if tag in task_tag.text:
                return True
    return False


def parse_tasks(filter_tags):
    try:
        os.remove(file_name)
    except OSError:
        pass
    tasks_response = get_response(get_tasks_url)
    list_items = get_list_items(tasks_response)
    for list_item in list_items:
        if not is_have_one_of_tags(list_item, filter_tags):
            continue
        print_task_text(list_item)
        print_task_link(list_item)
        print_description(list_item)
        print_description(list_item)
        print_views(list_item)
        print_time_ago(list_item)
        print_cost(list_item)
        print_separator()


def send_mail():
    with open(file_name, 'rb') as fp:
        msg = MIMEText(fp.read)
    msg['Subject'] = f'The contents of {file_name}'
    me = 'test'
    you = 'nklnsk708@gmail.com'
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], 'msg.as_string()')
    s.quit

def main(argv):
    tags = argv[1:]
    send_mail()
    #parse_tasks(tags)


if __name__ == '__main__':
    main(sys.argv)
