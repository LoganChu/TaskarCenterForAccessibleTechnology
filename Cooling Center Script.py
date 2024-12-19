import requests
from bs4 import BeautifulSoup

url = "https://search.wa211.org/search?query=TH-2600.1900-180&query_label=Extreme+Heat+Cooling+Centers&query_type=taxonomy&location=Seattle&radius=10&lat=47.603832&lon=-122.330062&query_language=en"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    elements = soup.find_all(class_="sc-b752dc62-0 fnWJZd")
    
    values = [element.get_text() for element in elements if element.get_text().strip()]
    comma_separated_list = ', '.join(values)
    
    print(comma_separated_list)
    print("hello")
else:
    print("Failed to retrieve the webpage.")