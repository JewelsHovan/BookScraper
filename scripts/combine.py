import os

def combine_chapters(start_chapter, end_chapter, folder, output_file):
    with open(output_file, 'w') as outfile:
        # Write the HTML header
        outfile.write("<html>\n<body>\n")

        for chapter_number in range(start_chapter, end_chapter + 1):
            chapter_file = os.path.join(folder, f'chapter_{chapter_number}.html')
            if os.path.exists(chapter_file):
                with open(chapter_file, 'r') as infile:
                    # Append the contents of the chapter file to the output file
                    outfile.write(infile.read())
                    # Add a separator between chapters
                    outfile.write("<p>########</p>\n")  # Separator in a new paragraph
                    outfile.write("\n\n\n")  # Add a newline to separate chapters

        # Write the HTML footer
        outfile.write("</body>\n</html>\n")

# Call the function
combine_chapters(1, 500, "god-rank-upgrade-system", "god-rank-upgrade-system.html")
