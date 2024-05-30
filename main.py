from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup
import requests
import platform
import aiohttp
import asyncio
import re
import os


class Navigation:
    def __init__(self):
        load_dotenv(find_dotenv())
        # Main variables
        self.link = os.getenv("LINK")
        self.folder = os.path.join(os.getcwd(), os.getenv("FOLDER"))
        self.titles_file = os.getenv("TITLES")
        self.pos_lock = asyncio.Lock()
        # HTML variables
        self.a_tag = "a"
        self.div_tag = "div"
        self.h2_tag = "h2"
        self.contents_class = "sc-dxZgTM iYdecD toc_article"
        self.download_attr = "Download PDF"
        self.next_attr = "Next"

    def create_folder(self):
        # Create download folder
        try:
            os.mkdir(self.folder)
        except FileExistsError:
            pass

    async def access_url(self, url=""):
        if len(url) == 0:
            url = self.link
        
        while True:
            try:
                # Page content
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                }
                response = requests.get(url, headers=headers)
                # # HTML content
                soup = BeautifulSoup(response.text, "html.parser")
                return soup 
            except requests.exceptions.RequestException as e:
                return 0             
            except Exception as e:
                print(f"Ocorreu um erro: {type(e)}")
                # Wait 3 seconds to repet the request after some error
                await asyncio.sleep(3)

    async def download_file(self, download_link, file_name):
        # PDF Download
        async with aiohttp.ClientSession() as session:
            async with session.get(download_link) as pdf_response:
                pdf_response.raise_for_status()
                pdf_content = await pdf_response.read()

        # Save PDF
        file_path = os.path.join(self.folder, file_name)
        with open(file_path, "wb") as file:
            file.write(pdf_content)
        
    async def access_articles(self, soup, pos):
        item = total_items = 0
        
        with open(self.titles_file, "a", encoding="utf-8") as txt_file:
            contents = soup.find_all(self.div_tag, class_=self.contents_class)
            total_items = len(contents)
            tasks = list()
            for content in contents:
                title = content.find(self.h2_tag).get_text().split("\n")[0]
                # PDF link
                download_url = content.find(self.a_tag, attrs={"aria-label": self.download_attr})["href"]
                async with self.pos_lock:
                    pos += 1
                    file_name = f"{pos}-" + re.sub(r'[<>:"/\\|?*]', "", title) + ".pdf"
                
                item += 1
                print(f"[{item}/{total_items}] - \033[94m{title[:30]+'...'}\033[0m", end="\r")

                tasks.append((self.download_file(download_url, file_name), title, pos))
            
            results = await asyncio.gather(*[task[0] for task in tasks])
            for result, task in zip(results, tasks):
                _, title, current_pos = task
                # Save PDF in text file
                txt_file.write(f"{current_pos}.{title}\n")
                txt_file.flush()

        return pos

    async def paginator(self, pos):
        while True:
            try:
                # Access page
                print(f"Accessing the link: \033[92m{self.link}\033[0m")
                soup = await self.access_url()
                pos = await self.access_articles(soup, pos)
                # Next page
                self.link = str(soup.find(self.a_tag, attrs={"aria-label": self.next_attr})["href"])
                # Wait 3 seconds to avoid "Too Many Requests" error
                await asyncio.sleep(3)
                if self.link == "#/":
                    print("End of pages" + " "*35)
                    break
            except Exception as e:
                print(f"Ocorreu um erro: {e}")    

    def list_files(self):
        files = len(os.listdir(self.folder))
        print(f"\033[92m{files} files downloaded\033[0m")

    async def main(self, pos):
        await self.paginator(pos)
        self.list_files()


if __name__ == "__main__":
    pos = 0
    site = Navigation()
    site.create_folder()

    try:
        if platform.system().lower() == "windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(site.main(pos))
    except KeyboardInterrupt:
        pass