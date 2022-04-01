import requests
from bs4 import BeautifulSoup
import os

urls = []
while True:
    i = 1
    urls += requests.get(f'https://cheb.ws/str.htm?page={i}')
    i += 1
print(urls)