from bs4 import BeautifulSoup
import aiohttp
import asyncio
import re
import os


class Navigation:
    def __init__(self):
        # Main variables
        self.link = "https://journal.seriousgamessociety.org/index.php/IJSG/issue/archive"
        self.folder = os.path.join(os.getcwd(), "files")
        self.titles_file = "titles.txt"
        self.pos_lock = asyncio.Lock()

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
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        # HTML content
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        return soup
            except aiohttp.ClientResponseError as e:
                return 0
            except Exception as e:
                print(f"Ocorreu um erro: {e}")

    async def download_file(self, url, file_name):
        soup = await self.access_url(url)
        if soup != 0:
            # PDF link
            download_link = soup.find('a', class_='download')['href']
            if not download_link.startswith('http'):
                download_link = aiohttp.helpers.urljoin(url, download_link)

            # PDF Download
            async with aiohttp.ClientSession() as session:
                async with session.get(download_link) as pdf_response:
                    pdf_response.raise_for_status()
                    pdf_content = await pdf_response.read()

            # Save PDF
            file_path = os.path.join(self.folder, file_name)
            with open(file_path, 'wb') as file:
                file.write(pdf_content)
            return True
        else:
            return False

    async def access_volumes(self, soup, pos):
        item = total_items = 0

        with open(self.titles_file, "a", encoding="utf-8") as txt_file:
            volumes = soup.find_all("a", class_="title")
            print(f"Accessing {len(volumes)} volumes, wait some seconds...")
            # Get total items
            for volume in volumes:
                soup_volumes = await self.access_url(volume["href"])
                articles = soup_volumes.find_all("a", class_="obj_galley_link pdf")
                total_items += len(articles)

            # Access each volume
            for volume in volumes:
                soup_volumes = await self.access_url(volume["href"])
                articles = soup_volumes.find_all("a", class_="obj_galley_link pdf")

                # Access each link
                tasks = []
                for article in articles:
                    item += 1
                    title = str(soup_volumes.find(
                        "a", id=re.search(r"article-\d+", article["id"]).group()
                    ).get_text()).strip().split("\n")[0]

                    async with self.pos_lock:
                        pos += 1
                        file_name = f"{pos}-" + re.sub(r'[<>:"/\\|?*]', "", title) + ".pdf"

                    print(f"[{item}/{total_items}] - \033[94m{title[:30]+'...'}\033[0m", end="\r")

                    tasks.append((self.download_file(article['href'], file_name), title, pos))

                results = await asyncio.gather(*[task[0] for task in tasks])
                for result, task in zip(results, tasks):
                    if result:
                        _, title, current_pos = task
                        txt_file.write(f"{current_pos}.{title}\n")
                        txt_file.flush()

        return pos

    async def paginator(self, pos):
        while True:
            try:
                # Access page
                print(f"Accessing the link: \033[92m{self.link}\033[0m")
                soup = await self.access_url()
                pos = await self.access_volumes(soup, pos)
                # Next page
                self.link = soup.find("a", class_="next")["href"]
            except TypeError:
                print("End of pages" + " "*35)
                break

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
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(site.main(pos))
    except KeyboardInterrupt:
        pass
