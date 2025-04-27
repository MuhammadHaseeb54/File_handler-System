from file_handling import read_file, write_file, compress, decompress
from huffman_tree import build_huffman_tree, generate_codes

# Decode binary data based on Huffman tree
def decode_data(encoded_data, huffman_tree, padding_length):
    decoded_text = ""
    node = huffman_tree
    for bit in encoded_data[padding_length:]:
        node = node.left if bit == "0" else node.right
        if node.left is None and node.right is None:
            decoded_text += node.char
            node = huffman_tree
    return decoded_text

def decompress_file(input_file, output_file, huffman_tree, padding_length):
    # Read encoded file
    byte_data = read_file(input_file)
    
    # Convert bytes to binary string
    encoded_data = "".join(f"{byte:08b}" for byte in byte_data)
    # Check if padding length is correct
    if len(encoded_data) % 8 != 0:
        raise ValueError("Encoded data length is not a multiple of 8 bits")
    # Decode the data
    decoded_text = decode_data(encoded_data, huffman_tree, padding_length)
    
    # Write decoded text to output file
    write_file(output_file, decoded_text.encode())
    print(f"File successfully decompressed as {output_file}")
