import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def login(username, password):
    login_url = "https://studentportal.ipb.ac.id/Account/Login"
    session = requests.Session()
    response = session.get(login_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    csrf_token_login = soup.find("input", {"name": "__RequestVerificationToken"})
    csrf_token_login_value = csrf_token_login.get("value")

    login_data = {
        "ReturnUrl": "",
        "Username": username,
        "Password": password,
        "__RequestVerificationToken": csrf_token_login_value,
        "RememberMe": "false"
        
    }
    headers_login = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "origin": "https://studentportal.ipb.ac.id",
    "referer": "https://studentportal.ipb.ac.id/Account/Login",
    }
    response_login = session.post(login_url, headers=headers_login, data=login_data, allow_redirects=False)
    #print(BeautifulSoup(response_login.text,"html.parser").prettify())

    if response_login.status_code == 302:
        print("Login Success")
        #print(response_login.cookies.get_dict())
        return response_login.cookies.get_dict()
    else:
        print(f"Login Failed with status code: {response_login.status_code}")
        print("Response Content:", response_login.text)
        print("Response Headers:", response_login.headers)
        return None


def submitForm(username, password):
    cookies = login(username, password)
    url = "https://studentportal.ipb.ac.id/Kegiatan/AktivitasKampusMerdeka"
    session = requests.Session()
    
    response = session.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    endpoint = soup.find("a", {"class": "btn btn-info"})
    endpoint_value = endpoint.get("href")
    
    response = session.get("https://studentportal.ipb.ac.id"+endpoint_value,headers=headers,cookies=cookies)
    


submitForm("example", "example")