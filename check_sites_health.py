import argparse
import os
import requests
from requests.exceptions import MissingSchema
import whois
from datetime import datetime
import time


def is_valid_file(argument_path):
    if not os.path.exists(argument_path):
        error_message = 'Путь {} не существует'.format(argument_path)
        raise argparse.ArgumentTypeError(error_message)

    return argument_path


def load_urls4check(path):
    with open(path) as file_domains:
        return file_domains.read().splitlines()


def is_server_respond_with_200(url):
    try:
        response = requests.get(url, timeout=5)
        return response.ok
    except (requests.ConnectionError, MissingSchema):
        return False


def get_domain_expiration_date(domain_name):
    while True:
        try:
            domain_whois = whois.whois(domain_name)
            return domain_whois.expiration_date[0]
        except TypeError:
            return domain_whois.expiration_date
        except ConnectionResetError:
            continue


def is_expiration_date_more_mounth(expiration_date):
    paid_term = expiration_date - datetime.now()
    days_mounth = 31
    return paid_term.days > days_mounth


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file_path',
        type=is_valid_file,
        help='Адрес файла с доменами'
    )
    domains_file_path = parser.parse_args().file_path
    domains = load_urls4check(domains_file_path)

    print('\n{:<30} | Ответ сервера | Проплачено более |'.format('Домен'))
    print('{:>44} {:>15}'.format('HTTP 200', 'месяца'))
    for domain in domains:
        domain_expiration_date = get_domain_expiration_date(domain)
        print('{:<30} | {!s:^13} | {!s:^16} |'.format(
            domain,
            is_server_respond_with_200(domain),
            is_expiration_date_more_mounth(domain_expiration_date)
        ))
