from flask import Flask, request, jsonify
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

app = Flask(__name__)

async def divert_to_next_link(driver, newLinks, pre, index, limit): 
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
        if driver.current_url != pre and index < limit:
            pre = driver.current_url
            print(driver.current_url +" "+ pre)
            print(len(newLinks))
            print()
            await divert_to_next_link(driver, newLinks, pre, index+1, limit)

async def new_model_to_crowl(driver, newLinks, index, limit, channel_name): 
    javascript_code = f"""
    document.getElementById("searchInput").value = "{channel_name}";
    document.getElementById("btnSearch").click();
    """

    # page_next
    driver.execute_script(javascript_code)
    pre = driver.current_url
    # get All links from page 
    await divert_to_next_link(driver, newLinks, pre, 1, limit)

@app.route('/')
async def hello_world():
    model = request.args.get('model')
    limit = request.args.get('limit')
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to Google Images
    driver.get(f"https://fr.pornhub.com")

    time.sleep(2)
    channel_name = model
    newLinks = []
    await new_model_to_crowl(driver, newLinks, 1, int(limit), channel_name)

    # file_name = f"assets/url.txt"  # You can change the file name and extension as needed

    # with open(file_name, "w") as file:
    #     for link in newLinks:
    #         file.write(link + "\n")

    # Close the browser
    driver.quit()

    data = {
        f"{channel_name}": newLinks
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()
