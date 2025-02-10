import fitz

def merge_nametags(input_file, output_file):
    doc = fitz.open(input_file)
    new_doc = fitz.open()
    
    original_width, original_height = doc[0].rect.width, doc[0].rect.height
    
    # A4 dimensions in landscape orientation
    a4_height, a4_width = fitz.paper_size("a4")
    
    # Calculate margins
    margin_x = (a4_width - 2 * original_width) / 3
    margin_y = (a4_height - 2 * original_height) / 3
    
    # Define positions for 4 nametags on A4 landscape
    positions = [
        (margin_x, margin_y),
        (2 * margin_x + original_width, margin_y),
        (margin_x, 2 * margin_y + original_height),
        (2 * margin_x + original_width, 2 * margin_y + original_height)
    ]
    
    for i in range(0, len(doc), 4):
        new_page = new_doc.new_page(width=a4_width, height=a4_height)
        
        for j in range(4):
            if i + j < len(doc):
                page = doc[i + j]
                src_rect = page.rect
                dst_rect = fitz.Rect(positions[j][0], positions[j][1], 
                                     positions[j][0] + original_width, 
                                     positions[j][1] + original_height)
                new_page.show_pdf_page(dst_rect, doc, i + j, clip=src_rect)
    
    new_doc.save(output_file)
    doc.close()
    new_doc.close()

merge_nametags("nametags.pdf", "nametag-merged.pdf")
