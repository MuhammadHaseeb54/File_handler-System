from file_handling import read_file, write_file, compress, decompress
from huffman_tree import build_huffman_tree, generate_codes
from collections import Counter

def compress_file(input_file, output_file):
    # Read the file
    file_data = read_file(input_file)
    
    # Calculate frequency of each character
    frequency = Counter(file_data)
    
    # Build Huffman Tree
    root = build_huffman_tree(frequency)
    
    # Generate Huffman codes
    huffman_codes = generate_codes(root)
    
    # Encode the data
    encoded_data = ''.join(huffman_codes[char] for char in file_data)
    
    # Add padding to make binary data byte-aligned
    padding_length = (8 - len(encoded_data) % 8) % 8
    encoded_data = f"{padding_length:08b}" + encoded_data + "0" * padding_length
    
    # Convert binary string to bytes and save to file
    byte_data = int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder="big")
    write_file(output_file, byte_data)
    print(f"File successfully compressed as {output_file}")
