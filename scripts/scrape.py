from bs4 import BeautifulSoup
import os
from security import safe_requests

def download_chapters(book_name, start_chapter, end_chapter, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for chapter_number in range(start_chapter, end_chapter + 1):
        url = f"https://novelfull.com/{book_name}/chapter-{chapter_number}.html"
        response = safe_requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to download chapter {chapter_number} of {book_name}.")
            continue

        soup = BeautifulSoup(response.text, 'lxml')

        # Find the div that contains the chapter text
        chapter_text_div = soup.find('div', id='chapter-content')

        # Check if the chapter text was found
        if chapter_text_div is None:
            print(f"Failed to find text for chapter {chapter_number} of {book_name}.")
            continue

        # Find the chapter title
        chapter_title = chapter_text_div.find(['h2', 'h3'])
        if chapter_title is not None:
            chapter_title = chapter_title.text
        else:
            chapter_title = f"Chapter {chapter_number}"

        # Find all paragraph elements that are descendants of the chapter_text_div
        paragraphs = chapter_text_div.find_all('p')

        # Save the chapter text to a file in the specified folder
        with open(os.path.join(folder, f'chapter_{chapter_number}.html'), 'w') as f:
            # Write the chapter title to the file
            f.write("<h1>" + chapter_title + "</h1>\n")

            for paragraph in paragraphs:
                if paragraph.text.strip():  # Ignore empty paragraphs
                    f.write("<p>" + paragraph.text + "</p>\n")  # Write the paragraph text, wrapped in <p> tags

# Call the function
download_chapters("god-rank-upgrade-system", 1, 500, "god-rank-upgrade-system")
