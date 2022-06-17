from PIL import Image
import json
import random

_2Bit_Dict = {"11" :[], "00" : [], "01" :[], "10" :[]}
_2BRGBINMAP = []
pix_vals = []
cs = ['r','g','b']
cs_map = {'r':0, 'g':1, 'b':2}

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

def find_2bit_matches(pix_vals):
    for pixel_index, pixel in enumerate(pix_vals):
        # print(pixel_index, pixel)
        for j in range(len(pixel)):
            # print(pixel_index, cs[j], pixel[j])
            mapp(pixel_index, cs[j], pixel[j])

def mapp(pixel_index, cs, pj):
    for i in range(0, len(pj), 2):
        # print(pixel_index, cs, i)
        _2Bit_Dict[pj[i:i+2]].append(str(pixel_index)+":"+cs+":"+str(i))
    # print(_2Bit_Dict)
    # print(pixel_index, cs[csj], p[i:i+2])

def map_string_to2bitdict(bin_secret_msg):
    for i in range(0, len(bin_secret_msg), 2):
        _2BRGBINMAP.append(random.choice(_2Bit_Dict[bin_secret_msg[i:i+2]]))

# <pixel_index(0 to last_pixel_of_image)>:
# <colorspace(r/g/b)>:
# <colorspace_bit_index>

# image_name = input('Image name(with extension): ')
# secret_file_name = input('Secret text file name(with extension): ')

image_name = 'autumn.png'
secret_file_name = 'secret_text.txt'

# read the image
im = Image.open(image_name, 'r')
pix_vals = list(im.getdata())

# read the secret message
with open(secret_file_name, 'r') as f:
    message = f.read()
message_in_bin = to_binary(message)
# print(message_in_bin)

for i in range(len(pix_vals)):
    r = bin(pix_vals[i][0])[2:].zfill(8)
    g = bin(pix_vals[i][1])[2:].zfill(8)
    b = bin(pix_vals[i][2])[2:].zfill(8)
    pix_vals[i] = [r, g, b]

find_2bit_matches(pix_vals)
map_string_to2bitdict(message_in_bin)

# save 2BRGBINMAP.json as a file
with open("2BRGBINMAP.json", "w") as outfile:
    j_data = json.dumps(_2BRGBINMAP)
    outfile.write(j_data)

def secret_bit_extraction(_2BRGBINMAP, pix_vals):
    secret_bits = ""
    for i in range(len(_2BRGBINMAP)):
        pixel_index, cs, cs_bit_index = _2BRGBINMAP[i].split(":")
        # print(pixel_index, cs, cs_bit_index)
        secret_bits += pix_vals[int(pixel_index)][cs_map[cs]][int(cs_bit_index):int(cs_bit_index)+2]
    return secret_bits

# open 2BRGBINMAP.json file
with open("2BRGBINMAP.json", "r") as read_file:
    _2BRGBINMAP= json.load(read_file)
    # print(_2BRGBINMAP)

ext_secret_text = to_string(secret_bit_extraction(_2BRGBINMAP, pix_vals))

# save extracted secret text to a file
with open("extracted_secret.txt", "w") as outfile:
    j_data = json.dumps(ext_secret_text)
    outfile.write(j_data)
    print('Secret text extracted successfully!')
