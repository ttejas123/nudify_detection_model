from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to Google Images
driver.get(f"https://fr.pornhub.com")

time.sleep(2)
channel_name = sys.argv[1]
javascript_code = f"""
document.getElementById("searchInput").value = "{channel_name}";
document.getElementById("btnSearch").click();
"""

# page_next
driver.execute_script(javascript_code)
newLinks = []
pre = driver.current_url
# get All links from page 
def divert_to_next_link(): 
    global pre
    fetch_links = """
        let links = document.getElementsByTagName('a')
        const urls = []
        for(let i = 0; i < links.length; i++) {
            urls.push(links[i].href)
        }
        return urls
    """
    links = driver.execute_script(fetch_links)
    keyword = "view_video.php"
    for link in links:
        if keyword in link:
            newLinks.append(link)
    next_tab = """
        let next_button = document.getElementsByClassName("page_next")[0]
        if ( next_button.className.includes("disabled") === false ) { next_button.children[0].click(); }
    """
    driver.execute_script(next_tab)
    if driver.current_url != pre:
        pre = driver.current_url
        print(driver.current_url +" "+ pre)
        print(len(newLinks))
        print()
        divert_to_next_link()
divert_to_next_link()

file_name = f"assets/url.txt"  # You can change the file name and extension as needed

with open(file_name, "w") as file:
    for link in newLinks:
        file.write(link + "\n")

# Close the browser
driver.quit()