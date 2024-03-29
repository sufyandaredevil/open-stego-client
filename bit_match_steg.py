from PIL import Image, PngImagePlugin
import requests
import json
import random

PORT = '8080'
URL = "http://127.0.0.1:" + PORT

PngImagePlugin.MAX_TEXT_CHUNK = 100 * (1024**2)
_2Bit_Dict = {"11" :[], "00" : [], "01" :[], "10" :[]}
_2BRGBINMAP = []
pix_vals = []
cs = ['r','g','b']
cs_map = {'r':0, 'g':1, 'b':2}

def to_binary(string):
    binary_string = ""
    for i in string:
        ascii_value = ord(i)
        binary_string += str(bin(ascii_value)[2:].zfill(8))
    return binary_string

def to_string(binstring):
    string = ""
    for i in range(0, len(binstring), 8):
        ascii_value = int(binstring[i:i+8], 2)
        string += chr(ascii_value)
    return string

def send_map():
    mapfile_name = input("Enter map file name(with extension): ")
    file = {'map': open(mapfile_name, 'rb')}
    url = URL+'/sendmap'

    try:
        r = requests.post(url, files = file)
        status = r.status_code
        r = json.loads(r.text)
        if status == 200:
            print("\nMap file sent successfully\n")
            print("TOKEN RECEIVED FROM SERVER: ", r['token']+'\n')
    except:
        print("\nError occurred while uploading map\n")

def receive_map():
    token = input("Enter token: ")
    url = URL+'/receivemap'
    data = {'token': token}
    try:
        r = requests.post(url, data = data)
        status = r.status_code
        r = json.loads(r.text)
        if status == 200:
            with open(token+'.json', "w") as outfile:
                j_data = json.dumps(r)
                outfile.write(j_data)
            print("\nMap file received successfully\n")
        else:
            print("\nMap file not found\n")
    except:
        print("\nError occurred while receiving map file\n")

def find_2bit_matches(pix_vals):
    for pixel_index, pixel in enumerate(pix_vals):
        for j in range(len(pixel)):
            mapp(pixel_index, cs[j], pixel[j])

def mapp(pixel_index, cs, pj):
    for i in range(0, len(pj), 2):
        _2Bit_Dict[pj[i:i+2]].append(str(pixel_index)+":"+cs+":"+str(i))

def map_string_to2bitdict(bin_secret_msg):
    for i in range(0, len(bin_secret_msg), 2):
        _2BRGBINMAP.append(random.choice(_2Bit_Dict[bin_secret_msg[i:i+2]]))

def secret_bit_extraction(_2BRGBINMAP, pix_vals):
    secret_bits = ""
    for i in range(len(_2BRGBINMAP)):
        pixel_index, cs, cs_bit_index = _2BRGBINMAP[i].split(":")
        secret_bits += pix_vals[int(pixel_index)][cs_map[cs]][int(cs_bit_index):int(cs_bit_index)+2]
    return secret_bits

if __name__ == '__main__':
    while True:
        print('(1) Map secret text with image')
        print('(2) Upload mapfile to StegoServer')
        print('(3) Download mapfile from StegoServer')
        print('(4) Extract secret text from image using mapfile')
        print('(5) Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            image_name = input('Image name(with extension): ')
            secret_file_name = input('Secret text file name(with extension): ')

            im = Image.open(image_name, 'r')
            pix_vals = list(im.getdata())

            with open(secret_file_name, 'r') as f:
                message = f.read()
            message_in_bin = to_binary(message)

            for i in range(len(pix_vals)):
                r = bin(pix_vals[i][0])[2:].zfill(8)
                g = bin(pix_vals[i][1])[2:].zfill(8)
                b = bin(pix_vals[i][2])[2:].zfill(8)
                pix_vals[i] = [r, g, b]

            find_2bit_matches(pix_vals)
            map_string_to2bitdict(message_in_bin)

            with open("2BRGBINMAP.json", "w") as outfile:
                j_data = json.dumps(_2BRGBINMAP)
                outfile.write(j_data)

            print('\nMap file saved as 2BRGBINMAP.json\n')

        if choice == '2':
            send_map()
        if choice == '3':
            receive_map()
        if choice == '4':
            filename = input('Enter map file name(with extension): ')
            image_name = input('Image name(with extension): ')

            im = Image.open(image_name, 'r')
            pix_vals = list(im.getdata())

            with open(filename, "r") as read_file:
                _2BRGBINMAP= json.load(read_file)

            for i in range(len(pix_vals)):
                r = bin(pix_vals[i][0])[2:].zfill(8)
                g = bin(pix_vals[i][1])[2:].zfill(8)
                b = bin(pix_vals[i][2])[2:].zfill(8)
                pix_vals[i] = [r, g, b]

            ext_secret_text = to_string(secret_bit_extraction(_2BRGBINMAP, pix_vals))

            with open("extracted_secret.txt", "w") as outfile:
                j_data = json.dumps(ext_secret_text)
                outfile.write(j_data)
                print('\nSecret text extracted successfully & saved as extracted_secret.txt\n')
        elif choice == '5':
            exit()
