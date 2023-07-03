import os
import requests
import time
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm


# NOTE: credits=https://github.com/ivangrov/Downloading_Google_Images, I have made some changes on the original code.
#       This module doesn't work properly. It's not downloading all the images.
#       Known issues: 1-Even though module grabs image source url successfully,
#                     requests.get() method doesn't response and it stucks there.
#                     for resolving this issue, timeout parameter is added to requests.get() method.
#                     2-On some searches, module raises NoSuchElementException error.
#                     Couldn't find the reason. XPATHs are correct.


class Scrap:
    """
    Scrap images from Google Images. This module uses Selenium and BeautifulSoup.

    Parameters
    ----------
    query : str
        Query to search on Google Images.
    binary_location : str
        Path to the Google Chrome binary file.(browser location)
    driver_path : str
        Path to the ChromeDriver.
    download_path : str
        Path to the download directory.
    SCROLL_PAUSE_TIME : int, optional
        Pause time between scrolls. The default is 2.
    SCROLL_COUNT : int, optional
        Number of scrolls. The default is 5.
    use_container_len : bool, optional
        If True, it will use the length of the containers. The default is False.
    start_from : bool, optional
        If True, it will ask for the starting point. The default is False. If downloads fails, you can start from the last downloaded image.

    """
    def __init__(self, query, binary_location, driver_path, download_path, SCROLL_PAUSE_TIME=2, SCROLL_COUNT=5, use_container_len=False, start_from=False):
        self.query = query
        self.download_path = download_path
        self.URL = f'https://www.google.com/search?q={query}&tbm=isch'
        self.options = Options()
        self.options.binary_location = binary_location
        self.ser = Service(driver_path)
        self.drvr = webdriver.Chrome(options = self.options, service=self.ser)

        self.start_from = start_from
        self.use_container_len = use_container_len
        self.file_length = 0

        self.SCROLL_PAUSE_TIME = SCROLL_PAUSE_TIME  # Adjust this pause time if needed
        self.SCROLL_COUNT = SCROLL_COUNT  # Adjust this count to control the number of scrolls


    def _makedir(self):
        """
        Create a directory for the images.
        """
        PATH = os.path.join(self.download_path, self.query)
        # print("PATH", PATH)

        if not os.path.exists(PATH):
            print("Creating directory...")
            os.mkdir(PATH)
        # else:
        #     print("Directory already exists.")

        return PATH


    def _download_image(self, PATH, url, num):
        """
        download the image from the given url.
        """

        response = requests.get(url, timeout=15)
        print(response)
        if response.status_code==200:
            with open(os.path.join(PATH, str(num)+".jpg"), 'wb') as file:
                file.write(response.content)


    def _scroll(self):
        """
        Waits for an input to proceed. Then scrolls down the page and grabs the image source urls. 
        Downloads all images from first page.
        """

        self.drvr.maximize_window()
        self.drvr.get(self.URL)
        self.drvr.implicitly_wait(10)


        a = input("Waiting...")
        
        for _ in range(self.SCROLL_COUNT):
            self.drvr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.SCROLL_PAUSE_TIME)

        # Retrieve the updated page source after scrolling
        page_html = self.drvr.page_source
        pageSoup = bs4(page_html, 'html.parser')

        # Find the containers with the images
        containers = pageSoup.findAll('div', {'class': 'isv-r PNCib MSM1fd BUooTd'})
        print("len(containers)", len(containers))

        if self.use_container_len:
            self.file_length = len(containers)
        else:
            self.file_length = 50

        # Starting point for downloading images. If download fails, you can start from the last downloaded image.
        if self.start_from:
            starting_point = int(input("Please enter the starting point: "))
        else:
            starting_point = 1


        count = 0
        for i in tqdm(range(starting_point, self.file_length + 1)):
            if i % 25 == 0:
                continue
            count += 1
            
            if i < 50:
                # This is current XPATH container
                xPath = '//*[@id="islrg"]/div[1]/div[%d]' % (i)
                # This is preview XPATH image element
                previewImageXPath = '//*[@id="islrg"]/div[1]/div[%d]/a[1]/div[1]/img' % (i)
            elif i > 50 and i < 105: ### NOTE: 51 - 104 --> div[51] part
                print("Current image", i)
                if i // 51 > 0:
                    xPath = '//*[@id="islrg"]/div[1]/div[51]/div[%d]' % ((i - 51) + 1)
                    print("xPath", xPath)
                    previewImageXPath = '//*[@id="islrg"]/div[1]/div[51]/div[%d]/a[1]/div[1]/img' % ((i - 51) + 1)
            elif i > 104 and i < 209: ### NOTE: 105 - 208 --> div[52] part
                print("i", i)
                if i // 52 > 0:
                    xPath = '//*[@id="islrg"]/div[1]/div[52]/div[%d]' % ((i - 104))
                    print("xPath", xPath)
                    previewImageXPath = '//*[@id="islrg"]/div[1]/div[52]/div[%d]/a[1]/div[1]/img' % ((i - 104))
            elif i > 208 and i < 313: ### NOTE: 209 - 312 --> div[53] part
                print("i", i)
                if i // 53 > 0:
                    xPath = '//*[@id="islrg"]/div[1]/div[53]/div[%d]' % ((i - 208))
                    print("xPath", xPath)
                    previewImageXPath = '//*[@id="islrg"]/div[1]/div[53]/div[%d]/a[1]/div[1]/img' % ((i - 208))
            elif i > 312 and i < 400: ### NOTE: 313 - 399 --> div[54] part
                print("i", i)
                if i // 54 > 0:
                    xPath = '//*[@id="islrg"]/div[1]/div[54]/div[%d]' % ((i - 312))
                    print("xPath", xPath)
                    previewImageXPath = '//*[@id="islrg"]/div[1]/div[54]/div[%d]/a[1]/div[1]/img' % ((i - 312))

            previewImageElement = self.drvr.find_element(By.XPATH, previewImageXPath)
            previewImageURL = previewImageElement.get_attribute("src")

            self.drvr.find_element(By.XPATH, xPath).click()

            timeStarted = time.time()

            while True:

                WebDriverWait(self.drvr, 10)
                # This is the XPATH of the full res image element (the one after clicking on the image that we want to download)
                # But it's dynamic, so we need to find it every time
                # old example : //*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div[2]/a/img
                imageElement = self.drvr.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')
                

                imageURL = imageElement.get_attribute("src")

                if imageURL != previewImageURL:
                    break

                else:
                    currentTime = time.time()

                    if currentTime - timeStarted >= 10:
                        print("TimeoutError! Will download a lower resolution image and move onto the next one")
                        break
            
            try:
                PATH = self._makedir()
                self._download_image(PATH, imageURL, i)
                print("Downloaded element %d out of %d total. URL: %s" % (i, self.file_length + 1, imageURL))

            except:
                print("Couldn't download an image %d, continuing downloading the next one" % (i))

        print("After passing related searches total number of images are: %d" % (count))

        self.drvr.close()


    def fit(self):      
        self._scroll()

    






# //*[@id="islrg"]/div[1]/div[25]
# //*[@id="islrg"]/div[1]/div[50]


# //*[@id="islrg"]/div[1]/div[2]/a[1]/div[1]/img
# //*[@id="islrg"]/div[1]/div[1]


# //*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]
# //*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]


# 24.image --> //*[@id="islrg"]/div[1]/div[24]/a[1]/div[1]/img
# 26.image --> //*[@id="islrg"]/div[1]/div[26]/a[1]/div[1]/img
               

# 49.image --> //*[@id="islrg"]/div[1]/div[49]/a[1]/div[1]/img
# 51.image --> //*[@id="islrg"]/div[1]/div[51]/div[1]/a[1]/div[1]/img

# 74.image --> //*[@id="islrg"]/div[1]/div[51]/div[24]/a[1]/div[1]/img
# 76.image --> //*[@id="islrg"]/div[1]/div[51]/div[26]/a[1]/div[1]/img


# 104.image --> //*[@id="islrg"]/div[1]/div[51]/div[54]/a[1]/div[1]/img
# NOTE: On 105.image div[51] --> div[52]
# 105.image --> //*[@id="islrg"]/div[1]/div[52]/div[1]/a[1]/div[1]/img

# 124.image --> //*[@id="islrg"]/div[1]/div[52]/div[20]/a[1]/div[1]/img
# 126.image --> //*[@id="islrg"]/div[1]/div[52]/div[22]/a[1]/div[1]/img

# 201.image --> //*[@id="islrg"]/div[1]/div[52]/div[97]/a[1]/div[1]/img
# 205.image --> //*[@id="islrg"]/div[1]/div[52]/div[102]/a[1]/div[1]/img

# 208.image --> //*[@id="islrg"]/div[1]/div[52]/div[104]/a[1]/div[1]/img
# NOTE: On 209.image div[52] --> div[53]
# 209.image --> //*[@id="islrg"]/div[1]/div[53]/div[1]/a[1]/div[1]/img

# 313.image --> //*[@id="islrg"]/div[1]/div[54]/div[1]/a[1]/div[1]/img

# 417.image --> //*[@id="islrg"]/div[1]/div[55]/div[1]/a[1]/div[1]/img


# After div[51] every 104 images div[5x] --> div[5x+1] (51 -> 52 | 52 -> 53 ...)


