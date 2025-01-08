from pdf2image import convert_from_path
from PIL import Image, ImageChops, ImageDraw
import pytesseract
import os


def highlight_handwritten_differences(pdf1_path, pdf2_path, output_pdf_path):
    """
    Compare two PDFs (including handwritten text) and highlight the differences.
    """
    # Convert PDFs to images
    images1 = convert_from_path(pdf1_path)
    images2 = convert_from_path(pdf2_path)

    if len(images1) != len(images2):
        print("PDFs have a different number of pages.")
        return

    # Create output folder for temporary images
    temp_folder = "temp_images"
    os.makedirs(temp_folder, exist_ok=True)

    highlighted_images = []

    for i, (img1, img2) in enumerate(zip(images1, images2)):
        # Ensure the images have the same size
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)

        # Convert both images to RGBA
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")

        # Detect differences visually
        diff_image = ImageChops.difference(img1, img2)
        diff_image = diff_image.convert("L")  # Convert to grayscale

        # Apply a threshold to focus on significant changes
        diff_image = diff_image.point(lambda x: 255 if x > 40 else 0)  # Adjust sensitivity
        diff_image = diff_image.convert("1")  # Convert to binary (black & white)

        # Highlight differences in yellow
        yellow_layer = Image.new("RGBA", img2.size, (255, 255, 0, 128))  # Semi-transparent yellow
        highlighted = Image.composite(yellow_layer, img2, diff_image)

        # Perform OCR on both images to detect textual differences
        text1 = pytesseract.image_to_string(img1, lang="eng")
        text2 = pytesseract.image_to_string(img2, lang="eng")

        # Highlight text differences (overlay red boxes for differing text)
        if text1 != text2:
            draw = ImageDraw.Draw(highlighted)
            for line in text2.split("\n"):
                if line.strip() and line not in text1:
                    # Find position of differing text using OCR
                    boxes = pytesseract.image_to_boxes(img2, lang="eng")
                    for b in boxes.splitlines():
                        b = b.split()
                        if line in b:
                            x, y, w, h = map(int, b[1:5])
                            y = img2.height - y  # Adjust for coordinate system
                            h = img2.height - h
                            draw.rectangle([x, h, w, y], outline="red", width=2)

        # Save the highlighted image for merging into a new PDF
        temp_path = os.path.join(temp_folder, f"page_{i + 1}.png")
        highlighted.save(temp_path)
        highlighted_images.append(temp_path)

    # Save the highlighted images as a new PDF
    first_image = Image.open(highlighted_images[0])
    first_image.save(
        output_pdf_path,
        save_all=True,
        append_images=[Image.open(img) for img in highlighted_images[1:]],
    )

    # Clean up temporary files
    for img in highlighted_images:
        os.remove(img)
    os.rmdir(temp_folder)

    print(f"Highlighted differences saved in: {output_pdf_path}")


if __name__ == "__main__":
    # Paths to input PDFs and output PDF
    pdf1_path = "first_pdf.pdf"  # Replace with the path to the first PDF
    pdf2_path = "second_pdf_with_handwritten_text.pdf"  # Replace with the path to the second PDF
    output_pdf_path = "highlighted_differences.pdf"  # Path for the output PDF

    # Highlight handwritten differences and save the result
    highlight_handwritten_differences(pdf1_path, pdf2_path, output_pdf_path)
