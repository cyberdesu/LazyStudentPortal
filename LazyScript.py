import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder



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

    headers_form = {
        "content-type": "multipart/form-data; boundary=---------------------------138331498894928001678762203",
        "origin": "https://studentportal.ipb.ac.id",
        "referer": "https://studentportal.ipb.ac.id/Kegiatan/LogAktivitasKampusMerdeka/Tambah",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "accept": "*/*",
        "accept-language": "id,en-US;q=0.9,en;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
        
    }
    cookies = login(username, password)
    url = "https://studentportal.ipb.ac.id/Kegiatan/AktivitasKampusMerdeka"
    session = requests.Session()
    
    response = session.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    #endpoint = soup.find("a", {"class": "btn btn-info"})
    #endpoint_value = endpoint.get("href")
    #print(endpoint_value)
    elements = soup.find_all("a", {"class": "btn btn-info"})

    # Buat daftar untuk menyimpan nilai href dari setiap elemen
    href_list = []

    # Loop melalui setiap elemen dan tambahkan nilai href ke dalam daftar
    for element in elements:
        href_value = element.get("href")
        href_list.append(href_value)

    # Tampilkan daftar nilai href
    for i, href in enumerate(href_list, start=1):
        print(f"{i}. {href}")

    # Buat input pilihan
    selected_option = int(input("Pilih nomor opsi: "))

    # Lakukan sesuatu dengan opsi yang dipilih (misalnya, buka URL)
    selected_url = href_list[selected_option - 1]
    print(f"Anda memilih opsi {selected_option}: {selected_url}")
    response = session.get("https://studentportal.ipb.ac.id"+selected_url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    endpoint = soup.find("a", {"class": "btn btn-default btn-tool"})
    endpoint_value = endpoint.get("onclick")
    endpoint_value = endpoint_value.split("'")[1]

    # Set the start and end dates
    start_date = datetime(2023, 8, 7)
    end_date = datetime(2023, 8, 10) # hanya dikirim senin-jumat aja

    # Array of activities
    kegiatan_array = [
        "Pembagian Jobdesc dari pihak kantor",
        "Mencari Referensi data untuk project yang akan dibuat",
        "mencari referensi terkait mikrotik",
        "belajar dasar front end di dicoding"
        # Add more activities as needed
    ]
    foto_kegiatan_array = [
        "1.jpg",
        "2.jpeg",
        "3.jpeg",
        "4.jpeg"
        # Add more activities as needed
    ]
    # Check if the lengths of all arrays are the same
    if len(kegiatan_array) != len(foto_kegiatan_array):
        print("Error: Lengths of 'kegiatan_array' and 'foto_kegiatan_array' are not the same.")
        exit()

    # Calculate the number of days
    num_days = (end_date - start_date).days + 1

    # Check if the lengths of tanggal, kegiatan_array, and foto_kegiatan_array are the same
    if num_days != len(kegiatan_array):
        print("Error: Lengths of 'tanggal', 'kegiatan_array', and 'foto_kegiatan_array' are not the same.")
        exit()
    # Iterate over the dates
    current_date = start_date
    url_form = "https://studentportal.ipb.ac.id/Kegiatan/LogAktivitasKampusMerdeka/Tambah"

    # Iterate over the activities and images
    for i in range(len(kegiatan_array)):
        kegiatan = kegiatan_array[i]
        image = foto_kegiatan_array[i]

        # Check if the current day is Monday to Friday
        if 0 <= current_date.weekday() <= 4:
            try:
                image_folder = "Gambar"
                image_filename = image
                image_path = os.path.join(image_folder, image_filename)

                with open(image_path, "rb") as image_file:
                    response = session.get("https://studentportal.ipb.ac.id" + endpoint_value, headers=headers, cookies=cookies)
                    soup = BeautifulSoup(response.text, "html.parser")
                    AktivitasId = soup.find("input", {"name": "AktivitasId"})
                    AktivitasId_value = AktivitasId.get("value")

                    csrf_token_form = soup.find("input", {"name": "__RequestVerificationToken"})
                    csrf_token_form_value = csrf_token_form.get("value")

                    idDosen = soup.find("input", {"name": "ListDosenPembimbing[0].Key.PembimbingId"})
                    idDosen_value = idDosen.get("value")

                    formatted_date = current_date.strftime("%d/%m/%Y")

                    form_data = {
                        "Id": "",
                        "AktivitasId": AktivitasId_value,
                        "Waktu": formatted_date,
                        "Tmw": "8:00",
                        "Tsw": "16:00",
                        "JenisLogbookKegiatanKampusMerdekaId": "3",
                        "ListDosenPembimbing[0].Key.PembimbingId": idDosen_value,
                        "IsLuring": "",
                        "Lokasi": "Jl. Jeruk Purut Dalam No.33, RT.6/RW.3, Cilandak Tim., Ps. Minggu, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12560",
                        "Keterangan": kegiatan,
                        "__RequestVerificationToken": csrf_token_form_value,
                        "ListDosenPembimbing[0].Value": "true",
                        "File": (image_filename, image_file, "image/jpeg"),
                    }

                    multipart_encoder = MultipartEncoder(fields=form_data)
                    headers_form["Content-Type"] = multipart_encoder.content_type

                    response = session.post(url_form, headers=headers_form, data=multipart_encoder, cookies=cookies)

                    print(f"Tanggal: {current_date.strftime('%A, %d %B %Y')}, Kegiatan: {kegiatan}, Status Code: {response.status_code}")

            except FileNotFoundError:
                print(f"Error: File not found at {image_path}")

            except Exception as e:
                print(f"Error: {e}")

        current_date += timedelta(days=1)

# Example usage
submitForm("example_username", "example_pass") # change this to your username and password