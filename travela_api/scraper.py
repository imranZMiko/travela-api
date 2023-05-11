from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import re
import time

def getDestinations(search_term):
    result = []

    # configure headless Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")

    # create a Firefox webdriver instance with headless options
    driver = webdriver.Firefox(options=firefox_options)

    # navigate to the TripAdvisor homepage
    driver.get(f"https://www.tripadvisor.com/Search?q={search_term}")

    # # wait for the search box to load
    # search_box = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.NAME, "q"))
    # )

    # driver.execute_script(f"return document.querySelector(\"input[name='q']\").value=\"{search_term}\"")
    # driver.execute_script("return document.querySelector(\"input[name='q']\").value")
    # returned = driver.execute_script("return document.querySelector(\".riJbp._G._H.B-._S.t.u.j.Cj.PGlrP\").click()")

    # wait for the search results page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "result-title"))
    )

    # create a Beautiful Soup object from the search results page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # # find all the hotels on the search results page
    hotel_listings = soup.find_all("div", class_="prw_search_search_result_poi")


    # extract information from each hotel listing
    for hotel in hotel_listings:
        name = hotel.find("div", class_="result-title").text.strip()
        address = hotel.find("div", class_="address-text").text.strip()
        image = hotel.find("div", class_="thumbnail").find("div", class_="inner").get("style")
        image = re.findall(r'\((.*?)\)', image)
        image = image[0]
        tag = hotel.find("div", class_="thumbnail").find("span", class_="thumbnail-overlay-tag").text.strip()
        if tag in ["Hotels", "Castles", "Religious Sites", "Ancient Ruins", "Historic Sites","Bodies of Water","Mountains","Forests","Parks","Activities","Architectural Buildings","Points of Interest & Landmarks","Scenic Walking Areas","Restaurants"]:
            result.append({"name":name, "address":address, "image":[image], "tag":tag, "description":None})
        # print(f"Name: {name}\nAddress: {address}\nImage: {image}")

    # # close the browser
    driver.quit()

    # print(result)
    return result

def getDestinationDetails(search_term):
    # configure headless Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")

    # create a Firefox webdriver instance with headless options
    driver = webdriver.Firefox(options=firefox_options)

    # navigate to the TripAdvisor homepage
    driver.get(f"https://www.tripadvisor.com/Search?q={search_term}")

    # wait for the search results page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "result-title"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    hotel = soup.find("div", class_="prw_search_search_result_poi")
    name = hotel.find("div", class_="result-title").text.strip()
    address = hotel.find("div", class_="address-text").text.strip()
    tag = hotel.find("div", class_="thumbnail").find("span", class_="thumbnail-overlay-tag").text.strip()

    try:
        returned = driver.execute_script("return document.querySelector('[data-widget-type=\"TOP_RESULT\"]').querySelector('.result-title').getAttribute(\"onclick\")")
        returned = re.findall("[^']*\.html", returned)
    except:
        returned = driver.execute_script("return document.querySelector('.prw_search_search_result_poi').querySelector('.result-title').getAttribute(\"onclick\")")
        returned = re.findall("[^']*\.html", returned)
    
    returned = returned[0]

    driver.get(f"https://www.tripadvisor.com{returned}")

    if tag == "Hotels":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "HEADING"))
        )

        # create a Beautiful Soup object from the search results page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            description = soup.find("div", class_="fIrGe _T").text.strip()
        except:
            description = None
        imageUrls = []
        images = soup.find("div", class_="rXyAo").find_all("img")
        for image in images:
            url = image.get("srcset")
            if url is not None:
                url = url.split()[0]
                url = re.sub(r'w=\d+0', 'w=1800', url)
                imageUrls.append(url)
    elif tag in ["Castles", "Religious Sites", "Ancient Ruins", "Historic Sites","Bodies of Water","Mountains","Forests","Parks"] :
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "eIegw"))
        )

        # create a Beautiful Soup object from the search results page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            description = soup.find("div", class_="_d MJ").find("div", class_="KxBGd").text.strip()
        except:
            description = None
        imageUrls = []
        images = soup.find("div", class_="yNgTB").find_all("img")
        for image in images:
            url = image.get("src")
            if url is not None:
                url = url.split()[0]
                url = re.sub(r'w=\d+0', 'w=1800', url)
                imageUrls.append(url)
    elif tag == "Activities":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "EVnyE"))
        )

        # create a Beautiful Soup object from the search results page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            temp = soup.find("div", class_="biGQs _P pZUbB roAGK KxBGd")
            if temp is None:
                temp = soup.find("div", class_="biGQs _P pZUbB KxBGd")
                description = temp.find("div", class_="_d").text.strip()
            else:
                description = temp.find("div", class_="_d").text.strip()
        except:
            description = None
        
        imageUrls = []
        images = soup.find_all("img")
        for image in images:
            url = image.get("src")
            if url.startswith("https://media-cdn.tripadvisor.com") or url.startswith("https://dynamic-media-cdn.tripadvisor.com/media/"):
                url = url.split()[0]
                url = re.sub(r'w=\d+0', 'w=1800', url)
                imageUrls.append(url)
    elif tag == "Restaurants":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "EVnyE"))
        )

        # create a Beautiful Soup object from the search results page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        description = None

        imageUrls = []
        images = soup.find("div", class_="mosaic_photos").find_all("img")
        for image in images:
            url = image.get("data-lazyurl")
            if url is not None:
                if url.startswith("https://media-cdn.tripadvisor.com") or url.startswith("https://dynamic-media-cdn.tripadvisor.com/media/"):
                    url = url.split()[0]
                    url = re.sub(r'w=\d+0', 'w=1800', url)
                    imageUrls.append(url)
    #yNgTB
    elif tag in ["Architectural Buildings","Points of Interest & Landmarks","Scenic Walking Areas"]:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "EVnyE"))
        )

        # create a Beautiful Soup object from the search results page
        soup = BeautifulSoup(driver.page_source, "html.parser")

        description = None

        imageUrls = []
        images = soup.find("div", class_="yNgTB").find_all("img")
        for image in images:
            url = image.get("src")
            if url is not None:
                if url.startswith("https://media-cdn.tripadvisor.com") or url.startswith("https://dynamic-media-cdn.tripadvisor.com/media/"):
                    url = url.split()[0]
                    url = re.sub(r'w=\d+0', 'w=1800', url)
                    imageUrls.append(url)

    result = {"name":name, "address":address, "image":imageUrls, "tag":tag, "description":description}

    # close the browser
    driver.quit()

    # print(result)
    return result

def getDestinationLocation(search_term):
    # configure headless Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")

    # create a Firefox webdriver instance with headless options
    driver = webdriver.Firefox(options=firefox_options)

    # navigate to the TripAdvisor homepage
    driver.get(f"https://www.google.com/maps?hl=en")

    # wait for the search results page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchboxinput"))
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchbox-searchbutton"))
    )

    driver.execute_script(f"return document.querySelector(\"input[id='searchboxinput']\").value=\"{search_term}\"")
    # driver.execute_script("return document.querySelector(\"input[name='searchboxinput']\").value")
    driver.execute_script("return document.querySelector(\"button[id='searchbox-searchbutton']\").click()")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".k7jAl.lJ3Kh.miFGmb"))
    )

    time.sleep(1)

    url = driver.current_url

    matches = url.split('/')
    result = [s for s in matches if s.startswith("@")]

    strings = result[0].split(',')
    strings[0] = strings[0].removeprefix('@')

    result = {"latitude":strings[0], "longitude":strings[1]}

    # close the browser
    driver.quit()

    # print(result)
    return result