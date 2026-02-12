def split_text(text,chunks_size,overlaps):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunks_size
        chunk = text[start : end]
        chunks.append(chunk)
        start = end - overlaps
        

    return chunks



##def split_text(text, chunk_size, overlap):
##    chunks = []
##    start = 0
##    text_length = len(text)
##
##    while start < text_length:
##        end = start + chunk_size
##        chunk = text[start:end]
##        chunks.append(chunk)
##
##        start = end - overlap  # IMPORTANT
##
##    return chunks