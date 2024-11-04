import requests
from bs4 import BeautifulSoup
from math import ceil,floor
from playwright.sync_api import sync_playwright
from download import download_file


def get_episodes(page = 1):
    url = f"https://animepahe.ru/api?m=release&id=98d28613-8f08-7fb7-4ace-dcd74e7c5153&sort=episode_asc&page={page}"

    payload = {}
    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
    'cookie': '__ddg9_=197.136.134.5; __ddgid_=ozNiTkP7FYibP3Ux; __ddgmark_=DYwPbAsMFkmTjq9X; __ddg2_=RAEPDvPN0M4yRYX6; __ddg1_=BQCBpEFzC7wH8txqDmHt; SERVERID=janna; __ddg8_=SRLD9T6br5cM473k; __ddg10_=1730713847; XSRF-TOKEN=eyJpdiI6IncvdWNrdGg1V2FEaGx3WlpxSmIwbnc9PSIsInZhbHVlIjoiTjIvQUkyNjErTGYxbVozSjlFa2QvdkY1VmVUcEpLMEk0bEg2SHBSV0VjZ3BJR21tRVptZ3F3TW9vNjBkN21ZRUdWVXZEckVhajFSdE1rVnIwcURmbE9CUStXS2hvUnF1MDlGYWE2OVZkbVpNYXhwVksza2c1TlNWY0tOYWZEQjgiLCJtYWMiOiJlYjQ0OGE2NzA3YzU4NGI4NDFlNzIwOGFjN2Y1ODkxNjJmZjQ5YTcyMzA3ZWRjYTg2MDljZmVlOTE3YzEzYzg3IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IkgrMTlLY0ZocW5CSlpjRmhhS042Y3c9PSIsInZhbHVlIjoiN2VRSjdYRnRWZVppVWZnSUdSd2ZFNFl6aGZSaXgwWWdTQVJiUnFEeXh1QS80Tmw3ejQ5VzFFeS8xSklOSUFCRzR0MVpvRFVaYWwzOTNnOFdRcVRwczliaTUwOUJLWHBLWGZ2cUpKVFFhL0hvVUdzK3FYakhCK1JvQ25OenAzQ1QiLCJtYWMiOiI3YjZjZjM5MzY3NWQzZGI0N2I3ZGIyNTIwNGY2NTkwYjA2ZmYwMmVlMWNmYTYwZWM4ZTMzOWIxZGY4MjQ1MGI1IiwidGFnIjoiIn0%3D',
    'priority': 'u=1, i',
    'referer': 'https://animepahe.ru/anime/98d28613-8f08-7fb7-4ace-dcd74e7c5153',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.json())
    return response.json()

def get_episode_html(url):

    print(url)
    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '__ddg9_=197.136.134.5; __ddgid_=ozNiTkP7FYibP3Ux; __ddgmark_=DYwPbAsMFkmTjq9X; __ddg2_=RAEPDvPN0M4yRYX6; __ddg1_=BQCBpEFzC7wH8txqDmHt; SERVERID=janna; res=360; aud=jpn; av1=0; sb_main_8966b6c0380845137e2f0bc664baf7be=1; __ddg8_=osKeARZK8bUTKqmr; __ddg10_=1730714093; XSRF-TOKEN=eyJpdiI6IlNZNjBXS1Y5Y3dkMkhtM1NtRWlxWlE9PSIsInZhbHVlIjoiRndsamd6Y0paUWc2a0pnaUtvVHFBc3RjdXVzeVFqRWFvWWxaRmhLMHFuNGtSd1NCd3VnZEhqV1c4bEZTSFVRN2h1Q1d5YmFQTWViSjJlSDVQWG1Oa0M3ck5ISjdEMjhsODdqUVRBc3BWVE5XOGF2dys3T2xTSzd4dmpSbXNjcVMiLCJtYWMiOiIzYWMzZWY1YzEwNDE5MDYwYTQ5NzI0YjEzYTBjMTdlYWViNzY0ZTFkOGMxZWY3ZTU5Mzg4NWQxOWI2MGFiNDg5IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IkYvaHJ0dVczaDY5U0xUODdWREltTHc9PSIsInZhbHVlIjoiMUIrK2xvMS9vMkJsaFJYMU1hK0IrRW1ndVBlTGFlY1gyS1FJQlNiRCtFbFFFZjBNOWg4czhWamRPa050dWUyaWhSU2ZaMTYrVFB0NWE0c3FmcDd5dElqbnhqbzNBa2dvZ3dTTWhJZlM0MTZyUWdZVEFRZ0dvdkR0MzdGN2F2R2EiLCJtYWMiOiI3NWUwYzk3MmU5ZmY1YmE3N2EwMTdmNmM0ZmNiOThmOTYyODZmMGYzMDBlOTA4ODc5Y2MyNmVjOWRhMGYyYmUwIiwidGFnIjoiIn0%3D; sb_page_8966b6c0380845137e2f0bc664baf7be=2; sb_count_8966b6c0380845137e2f0bc664baf7be=2; sb_onpage_8966b6c0380845137e2f0bc664baf7be=1; XSRF-TOKEN=eyJpdiI6Ild4dGNqV3ZXZlRvYTZEc0I1RTN0WXc9PSIsInZhbHVlIjoiTVk0UzlEOG1zRFBEWUJMRDV2d25IMTJpeXFYVXJLTXdrYkMxU0QvanFRMVorSFNacDZtaUMwbU1Qd0R0Qm9sNVNnR2owcXcrOU11KzA3M0tRV3BHb3c4QlRZTUQ3UGltMGVOODA0dWZoZjFPZkdmT0lwb2N6NTlJT0RkL2J4TDEiLCJtYWMiOiJmN2M0NDc0YWQwZDRjYmM3MTg3MTUzNzYyMDE5MWJjMzhiYjA0NDFmN2Y2Y2Y3N2U3NzY1MzkxNmZlOTkxZjE4IiwidGFnIjoiIn0%3D; __ddg10_=1730713955; __ddg8_=lbeAh3hbhsiYEUEX; __ddg9_=197.136.134.5; laravel_session=eyJpdiI6IlNESUZVUGhCTkg1QStVSTVWMXJUSFE9PSIsInZhbHVlIjoiMktxRnd4aytWZVAyUnExNFZ0VGFDL25xYmNleExBcTlJVEdST2R6bit5dXAzSHNRb0Foc2ZWZmxZSTZFQWxFY21CN2haMGNhckhOdWNqYm40SEs2OVpheXBVTWxqZFMrenBhREc3Q0tTZklLa2RpK3Zlc29NQjByaUFJcENOd2ciLCJtYWMiOiJiMjAyMTI1N2JlY2VkNWY5YjNhM2QyYjQwOTRkYjM1NmU3MThjNzE0M2Q4YWRiMjIzOWQ1OTYzZmQzNzc5ODEyIiwidGFnIjoiIn0%3D',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    # print(response.status_code)
    with open("data.html","w") as file :
        file.write(response.text)
    return response.text


def get_episode_html_wait(url):
    print(url)
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'cookie': '__ddg9_=197.136.134.5; __ddgid_=ozNiTkP7FYibP3Ux; __ddgmark_=DYwPbAsMFkmTjq9X; __ddg2_=RAEPDvPN0M4yRYX6; __ddg1_=BQCBpEFzC7wH8txqDmHt; SERVERID=janna; res=360; aud=jpn; av1=0; sb_main_8966b6c0380845137e2f0bc664baf7be=1; __ddg8_=osKeARZK8bUTKqmr; __ddg10_=1730714093; XSRF-TOKEN=eyJpdiI6IlNZNjBXS1Y5Y3dkMkhtM1NtRWlxWlE9PSIsInZhbHVlIjoiRndsamd6Y0paUWc2a0pnaUtvVHFBc3RjdXVzeVFqRWFvWWxaRmhLMHFuNGtSd1NCd3VnZEhqV1c4bEZTSFVRN2h1Q1d5YmFQTWViSjJlSDVQWG1Oa0M3ck5ISjdEMjhsODdqUVRBc3BWVE5XOGF2dys3T2xTSzd4dmpSbXNjcVMiLCJtYWMiOiIzYWMzZWY1YzEwNDE5MDYwYTQ5NzI0YjEzYTBjMTdlYWViNzY0ZTFkOGMxZWY3ZTU5Mzg4NWQxOWI2MGFiNDg5IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IkYvaHJ0dVczaDY5U0xUODdWREltTHc9PSIsInZhbHVlIjoiMUIrK2xvMS9vMkJsaFJYMU1hK0IrRW1ndVBlTGFlY1gyS1FJQlNiRCtFbFFFZjBNOWg4czhWamRPa050dWUyaWhSU2ZaMTYrVFB0NWE0c3FmcDd5dElqbnhqbzNBa2dvZ3dTTWhJZlM0MTZyUWdZVEFRZ0dvdkR0MzdGN2F2R2EiLCJtYWMiOiI3NWUwYzk3MmU5ZmY1YmE3N2EwMTdmNmM0ZmNiOThmOTYyODZmMGYzMDBlOTA4ODc5Y2MyNmVjOWRhMGYyYmUwIiwidGFnIjoiIn0%3D; sb_page_8966b6c0380845137e2f0bc664baf7be=2; sb_count_8966b6c0380845137e2f0bc664baf7be=2; sb_onpage_8966b6c0380845137e2f0bc664baf7be=1; XSRF-TOKEN=eyJpdiI6Ild4dGNqV3ZXZlRvYTZEc0I1RTN0WXc9PSIsInZhbHVlIjoiTVk0UzlEOG1zRFBEWUJMRDV2d25IMTJpeXFYVXJLTXdrYkMxU0QvanFRMVorSFNacDZtaUMwbU1Qd0R0Qm9sNVNnR2owcXcrOU11KzA3M0tRV3BHb3c4QlRZTUQ3UGltMGVOODA0dWZoZjFPZkdmT0lwb2N6NTlJT0RkL2J4TDEiLCJtYWMiOiJmN2M0NDc0YWQwZDRjYmM3MTg3MTUzNzYyMDE5MWJjMzhiYjA0NDFmN2Y2Y2Y3N2U3NzY1MzkxNmZlOTkxZjE4IiwidGFnIjoiIn0%3D; __ddg10_=1730713955; __ddg8_=lbeAh3hbhsiYEUEX; __ddg9_=197.136.134.5; laravel_session=eyJpdiI6IlNESUZVUGhCTkg1QStVSTVWMXJUSFE9PSIsInZhbHVlIjoiMktxRnd4aytWZVAyUnExNFZ0VGFDL25xYmNleExBcTlJVEdST2R6bit5dXAzSHNRb0Foc2ZWZmxZSTZFQWxFY21CN2haMGNhckhOdWNqYm40SEs2OVpheXBVTWxqZFMrenBhREc3Q0tTZklLa2RpK3Zlc29NQjByaUFJcENOd2ciLCJtYWMiOiJiMjAyMTI1N2JlY2VkNWY5YjNhM2QyYjQwOTRkYjM1NmU3MThjNzE0M2Q4YWRiMjIzOWQ1OTYzZmQzNzc5ODEyIiwidGFnIjoiIn0%3D',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch headless browser
        page = browser.new_page()

        # Set custom headers
        page.set_extra_http_headers(headers)

        # Navigate to the URL
        page.goto(url)

        # Wait for the JavaScript to render (you can adjust the timeout if needed)
        page.wait_for_timeout(7000)  # Wait for 5 seconds

        # Get the page content
        html = page.content()
        with open ("data.html","w",encoding="utf-8") as file:
            file.write(html)

        browser.close()  # Close the browser

    return html

def download_episode(url,token,title):

    payload = f'_token={token}'
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'srv=s0; ppu_show_on_4e5e04716f26fd21bf611637f4fb8a46=1; sb_page_e1010ee4b61613b1b253d71d1c531c2e=1; sb_main_e1010ee4b61613b1b253d71d1c531c2e=1; sb_count_e1010ee4b61613b1b253d71d1c531c2e=1; sb_onpage_e1010ee4b61613b1b253d71d1c531c2e=1; ppu_main_4e5e04716f26fd21bf611637f4fb8a46=1; ppu_exp_4e5e04716f26fd21bf611637f4fb8a46=1730718955256; cf_clearance=TAd7k0oO2St1tWfGS23OtwK4mMblwBJSU7fPSfCnHA0-1730715356-1.2.1.1-Eg4buh8A.tYdG09xk5TUJvoZtdPIqOILYsKA_LcZISK0P1Srw.icvwZL11z2osRSmWkvzKfKAcIO.3LTECqZwaRLtgXsBvWTsOXmZba2nYcFYHynnTBw2WsMfVLQrwojwGMCWoYxQm7yIW4QEwyrZsXuUnSUmYSthkCzNsEUwH8NR_8qqDdodjnoTQZJo3gwqkQ83GVeUpvejYdp3ZctUEnVpknyjUP4U0YOIMTMcCtAWIcSGoOV3pvnh8VtyavLaXO1pVTwMZ032hvNND3dzmujr_g.mNisEg49h9A3KzETWcqjt1z2C5gYgYvYV0B4pGQUw4j26y9hY0r5D5ZQMVtD9JCRr5YzFwA9axJVJwrsj7I6JoTgPzMzrO7HgPZGidwAy5ninMxhB5s5OXprhw; total_count_4e5e04716f26fd21bf611637f4fb8a46=2; ppu_sub_4e5e04716f26fd21bf611637f4fb8a46=2; kwik_session=eyJpdiI6Iis3REg2SDBSY0JNMHZqSjc4SmtTVHc9PSIsInZhbHVlIjoiSXM0TjdMT0lGdjA2ZzhxTEZYYnpTZVNPMW4rck9ucDloeGlaV0cyUUdUREFLOVBmNUp5RlJORno2b3dFM0dSRHljbGlhMGV5VnkvY09DMkdhMjdOcng5SDBDbWNCYXh0OW1YUkZMTS9XeDVFdlo1bmYyVFhncFZwM1B3MmtucUUiLCJtYWMiOiJhNzBkOTJlOTI4OTBiNTBjZGUzMGJiYjFmZDYzM2RkYmE3NTgwMGNhZmZmYWM4YzI2MWZiNDZhMzE2ZWMxNDgzIiwidGFnIjoiIn0%3D',
    'origin': 'https://kwik.si',
    'priority': 'u=0, i',
    'referer': 'https://kwik.si/f/{token}',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload, stream= True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a local file in binary write mode
        with open(title, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024*1024):  # Download in 1 MB chunks
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
    else:
        print(f'Failed to retrieve video: status code {response.status_code}')

def main(start=90,end=100):
    json_data = get_episodes()
    max_pages = json_data["last_page"]
    page_size = 30
    id = "98d28613-8f08-7fb7-4ace-dcd74e7c5153"
    links =[]
    
    start_page = floor(start/page_size)
    start_page = max(1,start_page)
    
    end_page = ceil(end/page_size)
    end_page = min(max_pages,end_page)
    
    for page_no in range(start_page,end_page+1):
        json_data = get_episodes(page_no)
        for episode in json_data["data"]:
            if episode["episode"] > start and episode["episode"] < end:
                url = f"https://animepahe.ru/play/{id}/{episode["session"]}"
                links.append(url)
    # print(links)
    for link in links:
        soup = BeautifulSoup(get_episode_html(link),features="html.parser")
        download_link = soup.select_one("div#pickDownload > a")
        link = download_link["href"]
        print("done 1 ")
        
        soup = BeautifulSoup(get_episode_html_wait(link),features="html.parser")
        kwik_link = soup.select_one("body > div.container.my-5 > div > div > div.col-md-8 > div > div:nth-child(1) > a") 
        kwik_link = kwik_link["href"]
        print("done 2")
        download_file(kwik_link)
        # soup = BeautifulSoup(get_episode_html_wait(kwik_link),features="html.parser")
        # kwik_link=soup.select_one("form")["action"]
        # kwik_token = soup.select_one("form > input")["value"]
        # name = soup.select_one("h1.title").text
        # print("done 3")
        # print(kwik_link)
        # print(kwik_token)
        # print(name)
        # download_file(kwik_link)
        
if __name__ == "__main__":
    main()  
