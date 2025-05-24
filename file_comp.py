import heapq 
import os     

# This class creates a binary tree node that stores a character and its frequency
class BinaryTree:
    def __init__(self, value, freq):
        self.value = value  
        self.freq = freq   
        self.left = None    
        self.right = None   

    # Tells heapq how to compare nodes based on frequency i.e. (min frequency)
    def __lt__(self, other):
        return self.freq < other.freq


# Main class to handle compression and decompression
class HuffmanCode:
    def __init__(self, path):
        self.path = path  
        self.__heap = []  
        self.__code = {}  
        self.__reverse_code = {}  

    # Step 1: Count frequency of each character in the text
    def __frequency_from_text(self, text):
        freq_dict = {}
        for char in text:
            if char not in freq_dict:
                freq_dict[char] = 0
            freq_dict[char] += 1
        return freq_dict

    # Step 2: Add all characters as nodes into a min-heap
    def __build_heap(self, freq_dict):
        for char, freq in freq_dict.items():
            node = BinaryTree(char, freq)
            heapq.heappush(self.__heap, node)

    # Step 3: Build the Huffman tree using heap
    def __build_binary_tree(self):
        while len(self.__heap) > 1:
            node1 = heapq.heappop(self.__heap)  # smallest frequency
            node2 = heapq.heappop(self.__heap)  # second smallest
            merged = BinaryTree(None, node1.freq + node2.freq)  # create new internal node
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.__heap, merged)  # push back to heap

    # Step 4 (Helper): assigns codes to characters
    def __build_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = current_code
            self.__reverse_code[current_code] = root.value
            return
        self.__build_codes_helper(root.left, current_code + "0")
        self.__build_codes_helper(root.right, current_code + "1")

    # Step 5: Call helper to assign Huffman codes to each character
    def __build_codes(self):
        root = heapq.heappop(self.__heap)
        self.__build_codes_helper(root, "")

    # Step 6: Replace each character in text with its Huffman code
    def __get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.__code[char]
        return encoded_text

    # Step 7: Add padding to encoded text to make it byte-aligned (multiples of 8)
    def __pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8  # how many 0s we need to add
        padded_info = "{0:08b}".format(extra_padding)  # convert padding length to 8-bit binary
        encoded_text += "0" * extra_padding  # add padding
        return padded_info + encoded_text  

    # Step 8: Convert bit string to bytes (8 bits at a time)
    def __get_byte_array(self, padded_text):
        byte_array = []
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i+8]
            byte_array.append(int(byte, 2))  # convert 8 bits to integer
        return byte_array

    # Main function to compress the file
    def compress(self):
        print("Compression started...")

        filename, _ = os.path.splitext(self.path) 
        output_path = filename + ".bin"  

        with open(self.path, 'r') as file:
            text = file.read()
            text = text.rstrip()  

        # Step-by-step process
        # Freq count fro each character
        freq_dict = self.__frequency_from_text(text)
        # store it in a freq dict 
        self.__build_heap(freq_dict)
        # min heap from two min freq constrcut binary tree from heap 
        self.__build_binary_tree()
        # construct code for binary tree and store it is dict 
        self.__build_codes()
        # for making encoded text 
        encoded_text = self.__get_encoded_text(text)
        # padding for encoded text for completing 8 bit no by adding zeroes 
        padded_text = self.__pad_encoded_text(encoded_text)
        # returning binary file as output 
        byte_array = self.__get_byte_array(padded_text)

        # Write compressed data to binary file
        with open(output_path, 'wb') as output:
            output.write(bytes(byte_array))

        print("Compression completed successfully.")
        return output_path

    # Step to remove padding from bit string
    def __remove_padding(self, padded_text):
        padded_info = padded_text[:8]  # first 8 bits tell us how many extra zeros we added
        extra_padding = int(padded_info, 2)
        padded_text = padded_text[8:]  # remove padded_info part
        return padded_text[:-extra_padding]  # remove the extra zeros from the end

    # Step to decode the text using reverse code dictionary
    def __decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.__reverse_code:
                character = self.__reverse_code[current_code]
                decoded_text += character
                current_code = ""  # reset after each successful match

        return decoded_text

    # Main function to decompress the file
    def decompress(self, input_path):
        filename, _ = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"  

        with open(input_path, 'rb') as file:
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)  # convert byte to integer
                bits = bin(byte)[2:].rjust(8, '0')  # convert to 8-bit binary string
                bit_string += bits
                byte = file.read(1)

        # Remove padding and decode the text
        encoded_text = self.__remove_padding(bit_string)
        decompressed_text = self.__decode_text(encoded_text)

        with open(output_path, 'w') as output:
            output.write(decompressed_text)

        print("Decompression completed successfully.")
        return output_path


# Asking user for file and running compression and decompression
if __name__ == "__main__":
    path = input("Enter the file path: ")
    h = HuffmanCode(path)
    compressed_file = h.compress()
    h.decompress(compressed_file)

         