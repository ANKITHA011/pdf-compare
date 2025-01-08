import fitz  # PyMuPDF

def compare_pdfs(file1, file2, output_file):
    """
    Compares two PDFs and highlights the differences using fitz.

    Args:
        file1 (str): Path to the first PDF file.
        file2 (str): Path to the second PDF file.
        output_file (str): Path to save the output PDF with highlighted differences.
    """
    try:
        # Open the PDF files
        doc1 = fitz.open(file1)
        doc2 = fitz.open(file2)

        # Ensure both PDFs have the same number of pages
        if len(doc1) != len(doc2):
            print(f"Number of pages in {file1} and {file2} do not match.")
            return

        # Create a new PDF document for the output
        output_doc = fitz.open()

        # Iterate through each page pair
        for page_num in range(len(doc1)):
            page1 = doc1[page_num]
            page2 = doc2[page_num]

            # Extract text content from each page
            text1 = page1.get_text("text")
            text2 = page2.get_text("text")

            # Compare texts and highlight differences
            if text1 != text2:
                # Create a new page in the output document
                output_page = output_doc.new_page(
                    width=page1.rect.width, height=page1.rect.height
                )

                # Insert the content of the first page into the output page
                pix = page1.get_pixmap()  # Render the page as an image
                output_page.insert_image(output_page.rect, pixmap=pix)

                # Highlight text differences (basic character-based comparison)
                for i, (char1, char2) in enumerate(zip(text1, text2)):
                    if char1 != char2:
                        # Get the bounding boxes of the differing text
                        bbox = page1.search_for(char1)
                        if bbox:
                            for rect in bbox:
                                # Draw a red rectangle around the differing character
                                output_page.draw_rect(rect, color=(1, 0, 0), width=0.5)

        # Save the output PDF with highlighted differences
        output_doc.save(output_file)
        print(f"Differences saved to {output_file}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file1 = "pdf1.pdf"  # Replace with your uploaded file name
file2 = "pdf2.pdf"  # Replace with your uploaded file name
output_file = "diff_output.pdf"
compare_pdfs(file1, file2, output_file)