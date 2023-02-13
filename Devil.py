import requests
import re
import concurrent.futures
import argparse
import time

def find_php_links_on_page(url):
    response = requests.get(url)
    html_content = response.text
    links = re.findall(r'href=[\'"]?([^\'" >]+)', html_content)
    return [link for link in links if link.endswith('.php') and 'id=' in link]

def find_php_links(url, depth=1, max_depth=5):
    links = find_php_links_on_page(url)
    log_file.write("[+] Found - {}\n".format(url))
    if links:
        for link in links:
            log_file.write("- {}\n".format(link))
        if depth < max_depth:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                future_to_link = {executor.submit(find_php_links_on_page, link): link for link in links}
                for future in concurrent.futures.as_completed(future_to_link):
                    link = future_to_link[future]
                    try:
                        sublinks = future.result()
                    except Exception as exc:
                        log_file.write('%r generated an exception: %s\n' % (link, exc))
                    else:
                        find_php_links(link, depth + 1, max_depth)
    else:
        log_file.write("[-] Not Found - {}\n".format(url))

if __name__ == "__main__":
    print("Welcome to the Advanced Network Scan Tool!\nDeveloped by RoD Programming Section")
    parser = argparse.ArgumentParser(description="Scan for .php links on a website")
    parser.add_argument("-u", "--url", type=str, required=True, help="URL to scan")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads to use (max 5)")
    parser.add_argument("-d", "--depth", type=int, default=5, help="Max search depth")
    args = parser.parse_args()

    url = args.url
    num_threads = min(args.threads, 5)
    max_depth = args.depth

    log_file = open("scan_log.txt", "w")
    log_file.write("Scan started at {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    find_php_links(url, max_depth=max_depth)
    log_file.write("Scan finished at {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    log_file.close()
