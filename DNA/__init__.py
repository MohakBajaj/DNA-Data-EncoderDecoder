class DNA_Data_Storage:
    def __init__(self, process_type: str, is_file: bool, data=None, file_path=None, save_file=False, encrypt=False, decrypt=False):
        self.process_type = process_type
        self.is_file = is_file
        self.data = data
        self.file_path = file_path
        self.DNA_Encoded = None
        self.DNA_Decoded = None
        self.enc = encrypt
        self.dec = decrypt
        if is_file:
            self.data = self.read_file(file_path)

        if self.enc:
            self.data = self.encrypt(self.data)

        self.binary_str = ''.join(format(x, '08b') for x in bytearray(self.data, 'utf-8'))

        if process_type == "encode":
            self.DNA_Encoded = self.Encoding()
        elif process_type == "decode":
            self.DNA_Decoded = self.Decoding()
            if self.dec:
                self.DNA_Decoded = self.decrypt(self.DNA_Decoded)

        if self.process_type == "encode":
            print(self.DNA_Encoded)
        if self.process_type == "decode":
            print(self.DNA_Decoded)

        if save_file:
            self.write_file()
            print("File Saved")

    def read_file(self, file_path):
        with open(file_path, "r") as file:
            return file.read()
    
    def Encoding(self):
        binary_list = [self.binary_str[i: i+2] for i in range(0, len(self.binary_str), 2)]
        DNA_encoding = {
            "00": "A",
            "01": "G",
            "10": "C",
            "11": "T"
        } 
        DNA_list = []
        for num in binary_list:
            for key in list(DNA_encoding.keys()):
                if num == key:
                    DNA_list.append(DNA_encoding.get(key))
        return "".join(DNA_list)

    def Decoding(self):
        DNA_decoding = {
            "A": "00",
            "G": "01",
            "C": "10",
            "T": "11"
        }
        Decoded_list = []
        for letter in self.data:
            for key in list(DNA_decoding.keys()):
                if letter == key:
                    Decoded_list.append(DNA_decoding.get(key))
        Decoded_str = "".join(Decoded_list)
        Decoded_str = "".join(chr(int(Decoded_str[i*8:i*8+8],2)) for i in range(len(Decoded_str)//8))

        return Decoded_str
    
    def write_file(self):
        if self.is_file:
            if self.process_type == "encode":
                with open(self.file_path + ".dna", "w") as file:
                    file.write(self.DNA_Encoded)
            elif self.process_type == "decode":
                with open(self.file_path + ".txt", "w") as file:
                    file.write(self.DNA_Decoded)
        else:
            if self.process_type == "encode":
                with open("data" + ".dna", "w") as file:
                    file.write(self.DNA_Encoded)
            elif self.process_type == "decode":
                with open("data" + ".txt", "w") as file:
                    file.write(self.DNA_Decoded)
    
    def encrypt(self, s):
        import random
        l = len(s)
        r = random.randint(1, l)
        return ''.join(chr(ord(c) + r + i) for i, c in enumerate(s[::-1]))+str(r)
    
    def decrypt(self, s):
        r = int(s[-1])
        return ''.join(chr(ord(c) - r - i) for i, c in enumerate(s))[::-1][1:]

    def __del__(self):
        print(f"{self.process_type} Complete")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DNA Encoding and Decoding", prog="DNA")
    parser.add_argument("-t", "--type", help="Type of process", choices=["encode", "decode"], required=True)
    parser.add_argument("-f", "--file", help="File to process", action="store_true")
    parser.add_argument("-d", "--data", help="Data to process")
    parser.add_argument("-p", "--path", help="Path to file")
    parser.add_argument("-e", "--encrypt", help="Encrypt data", action="store_true")
    parser.add_argument("-de", "--decrypt", help="Decrypt data", action="store_true")
    parser.add_argument("-s", "--save", help="Save file", action="store_true")
    args = parser.parse_args()
    if args.file:
        if args.encrypt:
            DNA_Data_Storage(args.type, args.file, file_path=args.path, save_file=args.save, encrypt=args.encrypt)
        elif args.decrypt:
            DNA_Data_Storage(args.type, args.file, file_path=args.path, save_file=args.save, decrypt=args.decrypt)
        else:
            DNA_Data_Storage(args.type, args.file, file_path=args.path, save_file=args.save)
    else:
        if args.encrypt:
            DNA_Data_Storage(args.type, args.file, data=args.data, save_file=args.save, encrypt=args.encrypt)
        elif args.decrypt:
            DNA_Data_Storage(args.type, args.file, data=args.data, save_file=args.save, decrypt=args.decrypt)
        else:
            DNA_Data_Storage(args.type, args.file, data=args.data, save_file=args.save)

# I'm not sure if this is the best way to do it, but it works. I'm open to suggestions on how to improve it.