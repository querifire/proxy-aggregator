import requests
import re
from urllib.parse import urlparse
import questionary
def read_links_from_file(link_file):
    with open(link_file, 'r') as file:
        lines = set(line.strip() for line in file if line.strip())
    links = [line for line in lines if line.startswith(('http://', 'https://'))]
    dublicates = len(lines) - len(links)
    return links, dublicates

def check_links(links):
    valid_links = []
    for index, link in enumerate(links, 1):
        try:
            response = requests.get(link, timeout=5)
            if response.status_code == 200:
                print(f'[{index}] {link} | Valid')
                valid_links.append(link)
            else:
                print(f'[{index}] {link} | Invalid')
        except requests.RequestException:
            print(f'[{index}] {link} | Invalid')
    return valid_links

def parse_proxies_from_links(valid_links, output_file):
    total_valid_proxies = 0
    proxy_set = set()
    for link in valid_links:
        try:
            response = requests.get(link, timeout=5)
            proxies = response.text.splitlines()
            valid_proxies = [proxy for proxy in proxies if re.match(r"^\d{1,3}(\.\d{1,3}){3}:\d{1,5}$", proxy)]
            proxy_set.update(valid_proxies)
            print(f'{link} - Valid ({len(valid_proxies)})')
        except requests.RequestException:
            print(f'{link} - Failed to retrieve proxies')
    with open(output_file, 'w') as file:
        file.writelines(f"{proxy}\n" for proxy in sorted(proxy_set))
    return len(proxy_set)

def main():
    link_file = questionary.path("What's the path to the proxy file {.txt}?").ask()
    links, dublicates = read_links_from_file(link_file)
    if not links:
        print('Please load valid links')
        return
    print(f"Links loaded: {len(links)} | Duplicates skipped: {dublicates}")

    valid_links = check_links(links)
    print('-' * 20)
    print('Parsing proxies...')
    output_file = 'proxy/proxys.txt'
    total_proxies = parse_proxies_from_links(valid_links, output_file)
    print(f'\nTotal valid proxies saved: [{total_proxies}]')

if __name__ == "__main__":
    main()
