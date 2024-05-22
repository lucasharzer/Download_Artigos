from bs4 import BeautifulSoup
import requests
import re
import os


class Navigation:
    def __init__(self):
        # Main variables
        self.link = "https://journal.seriousgamessociety.org/index.php/IJSG/issue/archive"
        self.folder = os.path.join(os.getcwd(), "files")
        self.titles_file = "titles.txt"

    def create_folder(self):
        # Create download folder
        try:
            os.mkdir(self.folder)
        except FileExistsError:
            pass
    
    def access_url(self, url=""):
        if len(url) == 0:
            url = self.link
        
        while True:
            try:
                # Page content
                page_response = requests.get(url)
                page_response.raise_for_status()

                # HTML content
                soup = BeautifulSoup(page_response.content, 'html.parser')
                return soup
            except requests.exceptions.HTTPError as e:
                return 0
            except Exception as e:
                print(f"Ocorreu um erro: {e}")

    def download_file(self, url, title):
        soup = self.access_url(url)
        if soup != 0:
            # PDF link
            download_link = soup.find('a', class_='download')['href']
            if not download_link.startswith('http'):
                download_link = requests.compat.urljoin(url, download_link)

            # PDF Download
            pdf_response = requests.get(download_link)
            pdf_response.raise_for_status()

            # Save PDF
            file_path = os.path.join(self.folder, title)
            with open(file_path, 'wb') as file:
                file.write(pdf_response.content)
            return True
        else:
            return False
    
    def access_volumes(self, soup, pos):
        item = total_items = 0

        with open(self.titles_file, "a", encoding="utf-8") as txt_file:
            volumes = soup.find_all("a", class_="title")
            print(f"Accessing {len(volumes)} volumes, wait some seconds...")
            # Get total items
            for volume in volumes:
                soup_volumes = self.access_url(volume["href"])
                articles = soup_volumes.find_all("a", class_="obj_galley_link pdf")
                total_items += len(articles)

            # Access each volume
            for volume in volumes:
                soup_volumes = self.access_url(volume["href"])
                articles = soup_volumes.find_all("a", class_="obj_galley_link pdf")

                # Access each link
                for article in articles:
                    item += 1
                    title = str(soup_volumes.find(
                        "a", id=re.search(r"article-\d+", article["id"]).group()
                    ).get_text()).strip().split("\n")[0]

                    file_name = re.sub(r'[<>:"/\\|?*]', "", title) + ".pdf"

                    print(f"[{item}/{total_items}] - {title[:30]+'...'}", end="\r")
                    
                    if self.download_file(article['href'], file_name):
                        pos += 1
                        txt_file.write(f"{pos}.{title}\n")
                        txt_file.flush()

        return pos
    
    def paginator(self, pos):
        while True:
            try:
                # Access page
                print(f"Accessing the link: {self.link}")
                soup = self.access_url()
                pos = self.access_volumes(soup, pos)
                # Next page
                self.link = soup.find("a", class_="next")["href"]
            except TypeError:
                print("\nEnd of pages")
                break

    def list_files(self):
        files = len(os.listdir(self.folder))
        print(f"{files} files downloaded")


if __name__ == "__main__":
    try:
        pos = 0
        site = Navigation()
        site.create_folder()
        site.paginator(pos)
        site.list_files()
    except KeyboardInterrupt:
        pass
