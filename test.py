def to_binary(string):
    binary_string = ""
    for i in string:
        # convert string to ascii
        ascii_value = ord(i)
        # convert ascii to binary
        binary_string += str(bin(ascii_value)[2:].zfill(8))
    return binary_string

def to_string(binstring):
# select first 8 bits of string
    string = ""
    for i in range(0, len(binstring), 8):
        # convert binary to ascii
        ascii_value = int(binstring[i:i+8], 2)
        # convert ascii to string
        string += chr(ascii_value)
    return string

secret = 'hello #$` 5'
retrieved_string = to_binary(secret)
print(to_string(retrieved_string))

# <pixel_index(0 to last_pixel_of_image)>:
# <colorspace(r/g/b)>:
# <bit_index>
