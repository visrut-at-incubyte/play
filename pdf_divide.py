import PyPDF2

def split_pdf(input_pdf, output_pdf1, output_pdf2):
    # Open the input PDF file
    with open(input_pdf, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        total_pages = len(reader.pages)

        if total_pages < 4:
            raise ValueError("Input PDF must have at least 4 pages")

        # Create writer objects for the two new PDFs
        writer1 = PyPDF2.PdfWriter()
        writer2 = PyPDF2.PdfWriter()

        # Add the specified pages to the writers
        writer1.add_page(reader.pages[0])  # Page 1
        writer1.add_page(reader.pages[1])  # Page 2

        writer2.add_page(reader.pages[2])  # Page 2
        writer2.add_page(reader.pages[3])  # Page 3

        # Write the pages to the new PDF files
        with open(output_pdf1, 'wb') as outfile1:
            writer1.write(outfile1)

        with open(output_pdf2, 'wb') as outfile2:
            writer2.write(outfile2)

    print(f"Created {output_pdf1} with pages 1 and 2")
    print(f"Created {output_pdf2} with pages 2 and 3")

# Example usage
input_pdf = 'input.pdf'
output_pdf1 = 'first.pdf'
output_pdf2 = 'second.pdf'

split_pdf(input_pdf, output_pdf1, output_pdf2)
