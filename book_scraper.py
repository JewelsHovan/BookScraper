import requests
from bs4 import BeautifulSoup
import os
import pickle

class Book:
    def __init__(self, title, folder_path):
        self.title = title
        self.folder_path = folder_path
        
class BookScraper:
    NOVELFULL_CHAPTER_URL_TEMPLATE = "https://novelfull.com/{book_name}/chapter-{chapter_number}.html"
    def __init__(self, folder, chapter_url_template = None, chapter_content_id = None):
        self.folder = folder
        self.novels = []
        # seta the url template
        if chapter_url_template is None:
            self.chapter_url_template = BookScraper.NOVELFULL_CHAPTER_URL_TEMPLATE
        else:
            self.chapter_url_template = chapter_url_template
        # set the chapter content id
        if chapter_content_id is None:
            self.chapter_content_id = 'chapter-content'
        else:
            self.chapter_content_id = chapter_content_id

        self.load_books()

    def load_books(self):
        # Load the books from a file if it exists
        if os.path.exists('books.pkl'):
            with open('books.pkl', 'rb') as f:
                self.novels = pickle.load(f)

    def save_books(self):
        # Save the books to a file
        with open('books.pkl', 'wb') as f:
            pickle.dump(self.novels, f)

    def get_all_hot_novels(self):
        page = 1
        all_novel_names = []
        last_novel_names = None

        while True:
            url = f"https://novelfull.net/hot-novel?page={page}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to download page {page} of the hot novels.")
                break

            soup = BeautifulSoup(response.text, 'lxml')
            novel_links = soup.find_all('h3', class_='truyen-title')

            # If there are no more novels, stop
            if not novel_links:
                break

            # Extract the novel names from the links
            novel_names = [link.text.lower().replace(' ', '-')
                           for link in novel_links]

            # If the novel names are the same as the last page, stop
            if novel_names == last_novel_names:
                break

            # Add the novel names to the list and go to the next page
            all_novel_names.extend(novel_names)
            last_novel_names = novel_names
            page += 1

        # Save the novel names in the instance attribute
        self.novels = [Book(name, os.path.join(self.folder, name))
                       for name in all_novel_names]

        # Save the books to a file
        self.save_books()

    def book_exists(self, book_name):
        # Check if the book_name is in the list
        return any(book.title == book_name for book in self.novels)

    def download_book(self, book_name, start_chapter=1, end_chapter=50):
        # convert book_name into valid format
        book_name = book_name.lower().replace(' ', '-')
        # Check if the book exists
        if not self.book_exists(book_name):
            print(f"The book '{book_name}' does not exist.")
            return

        # Download the chapters of the book
        self.download_chapters(book_name, start_chapter, end_chapter)

        # Combine the chapters into a single HTML file
        self.combine_chapters(book_name, start_chapter, end_chapter)

        # download the book cover
        self.download_book_cover(book_name)

    def download_chapters(self, book_name, start_chapter, end_chapter):
        book_folder = os.path.join(self.folder, book_name)
        if not os.path.exists(book_folder):
            os.makedirs(book_folder)

        for chapter_number in range(start_chapter, end_chapter + 1):
            url = self.chapter_url_template.format(book_name=book_name, chapter_number=chapter_number)
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to download chapter {chapter_number} of {book_name}.")
                print(f"URL: {url}")
                print(f"Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'lxml')
            chapter_text_div = soup.find('div', id=self.chapter_content_id)

            if chapter_text_div is None:
                print(f"Failed to find text for chapter {chapter_number} of {book_name}.")
                continue

            chapter_title = chapter_text_div.find(['h2', 'h3'])
            if chapter_title is not None:
                chapter_title = chapter_title.text
                # Append chapter number if not present in title
                if f"Chapter {chapter_number}" not in chapter_title:
                    chapter_title = f"Chapter {chapter_number}: {chapter_title}"
            else:
                chapter_title = f"Chapter {chapter_number}"

            paragraphs = chapter_text_div.find_all('p')

            with open(os.path.join(book_folder, f'chapter_{chapter_number}.html'), 'w') as f:
                f.write("<h1>" + chapter_title + "</h1>\n")
                for paragraph in paragraphs:
                    if paragraph.text.strip():
                        f.write("<p>" + paragraph.text + "</p>\n")

    def combine_chapters(self, book_name, start_chapter, end_chapter):
        book_folder = os.path.join(self.folder, book_name)
        output_file = os.path.join(book_folder, f"{book_name}.html")

        with open(output_file, 'w') as outfile:
            outfile.write("<html>\n<body>\n")

            for chapter_number in range(start_chapter, end_chapter + 1):
                chapter_file = os.path.join(
                    book_folder, f'chapter_{chapter_number}.html')
                if os.path.exists(chapter_file):
                    with open(chapter_file, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write("<p>########</p>\n")
                        outfile.write("\n\n\n")

                    # Delete the individual chapter file
                    os.remove(chapter_file)

            outfile.write("</body>\n</html>\n")

    def print_novels(self):
        if not self.novels:
            print("No novels found.")
            return

        for novel in self.novels:
            # Convert back to a readable format
            novel = novel.replace('-', ' ')
            novel = ' '.join(word.capitalize() for word in novel.split())
            print(novel)

    def search_hot_novel(self, search_term):
        # Convert the search term to the format used in the list
        search_term = search_term.lower().replace(' ', '-')

        # Find all novels that contain the search term
        matching_novels = [
            novel for novel in self.novels if search_term in novel.title]

        if matching_novels:
            print(f"Found novels containing '{search_term}':")
            for novel in matching_novels:
                # Convert back to a readable format
                novel_title = novel.title.replace('-', ' ')
                novel_title = ' '.join(word.capitalize()
                                       for word in novel_title.split())
                print(novel_title)
        else:
            print(f"No novels found containing '{search_term}'")

    def search_novel(self, search_term):
        # Convert the search term to the format used in the URL
        search_term = search_term.lower().replace(' ', '%20')

        # Create the search URL
        url = f"https://novelfull.net/search?keyword={search_term}"

        # Send a GET request to the URL
        response = requests.get(url)

        # If the request was successful, parse the HTML content
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            # Find the div that contains the list of novels
            novels_div = soup.find('div', class_='list list-truyen col-xs-12')

            # If the div was found, extract the novel names
            if novels_div:
                novel_links = novels_div.find_all('h3')

                # Extract the novel names from the links
                novel_names = [link.text for link in novel_links]

                # Print the novel names
                if novel_names:
                    print(f"Found novels with '{search_term}':")
                    for novel in novel_names:
                        print(novel)
                else:
                    print(f"No novels found with '{search_term}'")
            else:
                print("No novels found.")
        else:
            print("Failed to search for novels.")

    def get_book_info_and_cover(self, book_name):
        # Convert the book name to the format used in the URL
        book_name = book_name.lower().replace(' ', '-')
        url = f"https://novelfull.net/{book_name}.html"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to download page for {book_name}.")
            return

        soup = BeautifulSoup(response.text, 'lxml')

        # Get the book cover image
        self.download_book_cover(soup, book_name)

        # Get the book info
        self.print_book_info(soup)

        # Get the book synopsis
        self.print_synopsis(book_name)

    def download_book_cover(self, book_name):
        url = f"https://novelfull.net/{book_name}.html"
        response = requests.get(url)
        print(response.status_code)
        if response.status_code != 200:
            print(f"Failed to download cover for {book_name}.")
            return
        soup = BeautifulSoup(response.text, 'lxml')
        book_div = soup.find('div', class_='book')
        img_tag = book_div.find('img')
        if img_tag is not None:
            img_url = "https://novelfull.net" + img_tag['src']
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                with open(os.path.join(self.folder + f"/{book_name}", f"{book_name}_cover.jpg"), 'wb') as f:
                    f.write(img_response.content)
            else:
                print(f"Failed to download cover image for {book_name}.")

    def print_book_info(self, soup : BeautifulSoup):
        info_div = soup.find('div', class_='info')
        if info_div is not None:
            info = {}
            for div in info_div.find_all('div'):
                key = div.find('h3').text.strip(':')
                value = ', '.join(a.text for a in div.find_all('a'))
                info[key] = value
            print(info)

    def print_synopsis(self, novel_name):
        # Convert the novel name to the format used in the URL
        novel_name = novel_name.lower().replace(' ', '-')

        # Create the novel URL
        url = f"https://novelfull.net/{novel_name}.html"

        # Send a GET request to the URL
        response = requests.get(url)

        # If the request was successful, parse the HTML content
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            # Find the div that contains the synopsis
            synopsis_div = soup.find('div', class_='desc-text')

            # If the div was found, extract and print the synopsis
            if synopsis_div:
                synopsis = synopsis_div.text
                print(f"Synopsis of '{novel_name}':\n{synopsis}")
            else:
                print("No synopsis found.")
        else:
            print("Failed to get the synopsis.")


if __name__ == "__main__":
    # Usage:
    NOVELUSB_TEMPLATE = "https://novelusb.com/novel-book/{book_name}/chapter-{chapter_number}"
    NOVELUSB_chapter_id = "chr-content"
    # intialize the BookScraper
    scraper = BookScraper("novels")

    book_name = "Super Gene"
    scraper.search_novel(book_name)
    #scraper.combine_chapters('super-gene', 1, 1149)



