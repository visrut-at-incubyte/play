import fitz  # PyMuPDF
import os

# Define the compression ratio
COMPRESS_RATIO = 0.5  # Adjust this value as needed

# Open the input PDF
input_pdf_path = "./input.pdf"
output_pdf_path = "output.pdf"



# Check if the input file exists
if not os.path.exists(input_pdf_path):
    raise FileNotFoundError(f"The file {input_pdf_path} does not exist.")

# Open the input PDF
doc = fitz.open(input_pdf_path)

# Compress the PDF
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    images = page.get_images(full=True)
    
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_pix = fitz.Pixmap(image_bytes)

        # Compress the image by rescaling
        if image_pix.n > 4:  # this is GRAY+ALPHA or RGB+ALPHA
            image_pix = fitz.Pixmap(fitz.csRGB, image_pix)  # convert to RGB

        new_width = int(image_pix.width * COMPRESS_RATIO)
        new_height = int(image_pix.height * COMPRESS_RATIO)
        image_pix_rescaled = image_pix.rescale(new_width, new_height)
        
        # Replace the image with the compressed version
        new_xref = doc.add_image(image_pix_rescaled.tobytes())
        page.replace_image(xref, new_xref)

# Save the compressed PDF
doc.save(output_pdf_path)
doc.close()

print(f"Compressed PDF saved as {output_pdf_path}")
