import argparse
import os
import requests
from requests.exceptions import MissingSchema
import whois
from datetime import datetime


def is_valid_file(argument_path):
    if not os.path.exists(argument_path):
        error_message = 'Путь {} не существует'.format(argument_path)
        raise argparse.ArgumentTypeError(error_message)

    return argument_path


def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file_path',
        type=is_valid_file,
        help='Адрес файла с доменами'
    )
    return parser.parse_args()


def load_urls4check(path):
    with open(path) as file_domains:
        return file_domains.read().splitlines()


def is_server_respond_ok(url):
    try:
        response = requests.get(url)
        return response.ok
    except (requests.ConnectionError, requests.ReadTimeout, MissingSchema):
        return False


def get_domain_expiration_date(domain_name):
    attempt = 1
    while attempt < 4:
        try:
            domain_whois = whois.whois(domain_name)
            if type(domain_whois.expiration_date) is list:
                return domain_whois.expiration_date[0]
            else:
                return domain_whois.expiration_date
        except ConnectionResetError:
            attempt += 1
            continue

    return None


def is_expiration_date_more_days(days, expiration_date):
    if not expiration_date:
        return False
    paid_term = expiration_date - datetime.now()
    return paid_term.days > days


if __name__ == '__main__':
    min_paid_days = 31
    domains_file_path = parsing_arguments().file_path
    domains = load_urls4check(domains_file_path)

    print('\n{:<30} | Ответ сервера | Проплачено более |'.format('Домен'))
    print('{:>44} {:>15}'.format('HTTP 200', 'месяца'))
    for domain in domains:
        domain_expiration_date = get_domain_expiration_date(domain)
        print('{:<30} | {!s:^13} | {!s:^16} |'.format(
            domain,
            is_server_respond_ok(domain),
            is_expiration_date_more_days(min_paid_days, domain_expiration_date)
        ))
