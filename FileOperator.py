import binascii
import sys
dict_file_head={
    ("ff", "d8", "ff"): "jpg/jpeg",
    ("89", "50", "4e", "47"): "png",
    ("47", "49", "46", "38"): "gif",
    ("49", "49", "2a", "00"): "tif",
    ("42", "4d"): "bmp",
    ("41", "43", "31", "30"): "CAD",
    ("38", "42", "50", "53"): "psd",
    ("7b", "5c", "72", "74", "66"): "rtf",
    ("3c", "3f", "78", "6d", "6c"): "xml",
    ("68", "74", "6d", "6c", "3e"): "html",
    ("44", "65", "6c", "69", "76", "65", "72", "79", "2d", "64", "61", "74", "65", "3a"): "eml",
    ("cf", "ad", "12", "fe", "c5", "fd", "74", "6f"): "dbx",
    ("21", "42", "44", "4e"): "pst",
    ("d0", "cf", "11", "e0"): "xls or doc",
    ("53", "74", "61", "6e", "64", "61", "72", "64", "20", "4a"): "mdb",
    ("ff", "57", "50", "43"): "wpd",
    ("ac", "93", "bd", "8f"): "qdf",
    ("e3", "82", "85", "96"): "pwl",
    ("57", "41", "56", "45"): "wav",
    ("41", "56", "49", "20"): "avi",
    ("2e", "72", "61", "fd"): "ram",
    ("2e", "52", "4d", "46"): "rm",
    ("00", "00", "01", "ba"): "mpg",
    ("00", "00", "01", "ba"): "mpeg",
    ("6d", "6f", "6f", "76"): "mov",
    ("30", "26", "b2", "75", "8e", "66", "cf", "11"): "asf",
    ("4d", "54", "68", "64"): "mid",
    ("50", "4b", "03", "04", "14"): "zip",
    ("52", "61", "72", "21", "1a"): "rar",
    ("49", "44", "33", "03", "00"): "mp3",
    ("52", "49", "46", "46", "18"): "wav",
    ("4d", "5a", "90", "00", "03"): "pe",
    ("25", "50", "44", "46", "2d", "31", "2e"): "pdf"

}

def preprocess(filename):                 #对文件进行预处理，将其转换为16进制流
    file = open(filename, "rb")
    bin_text = file.read()
    hex_str_list = str(binascii.b2a_hex(bin_text)).split("'")
    del hex_str_list[0]
    del hex_str_list[-1]
    hex_str = str(hex_str_list[0])
    hex_list_single = list(hex_str)
    hex_list=[]
    for i in range(len(hex_list_single)):
        if i%2 == 0:
            hexnum=hex_list_single[i]+hex_list_single[i+1]
            hex_list.append(hexnum)
    return hex_list
def write_to_file(filename):        #若需要分析文件的16进制则可选择将其写入文件hex中
    file = open("hex.txt","w+")
    hex_list=preprocess(filename)
    k=0
    for j in range(len(hex_list)):
        file.write(hex_list[j] + "\t")
        k+=1
        if k == 16:
            file.write("\n")
            k=0
    file.close()
    print("Done, please check C://Users/sunday/Desktop/科研训练/new/hex.txt")
def modify_file(filename):
    write_to_file(filename)
    print("please modify this file and exit with 'quit'")
    while True:
        if input() == "quit":
            file_r = open("C://Users/sunday/Desktop/科研训练/new/hex.txt","r")
            hex_text = file_r.readlines()
            file_r.close()
            hex_str=""
            for i in range(len(hex_text)):
                hex_str+=hex_text[i]
            hex_str=hex_str.replace("\t", "").replace("\n", "")
            #hex_str="b'"+hex_str+"'"
            hex_str = hex_str.strip('\n')
            bin_str=binascii.a2b_hex(hex_str)
            file_new_name=filename+".new"
            file_w = open(file_new_name,"wb+")
            file_w.write(bin_str)
            file_w.close()
            break
        else:
            continue
def file_belong(filename):           #通过查询字典判断文件类型
    text=preprocess(filename)[0:16]
    flag=False
    for key in dict_file_head.keys():
        compare = 0
        for i in range(len(key)):
            if key[i]==text[i]:
                compare+=1
        if compare==len(key):
            flag=True
            print('file:"'+filename+'"'+"'s format is "+dict_file_head[key])
    if flag == False:
        print('file:"'+filename+'"'+"'s format can not be define, it may be encrypted")
def changekey(key):
    key_list=[]
    while len(key) % 4 != 0:
        key+="0"
    xorTime=int(len(key)/4)
    for i in range(len(key)):
        key_list.append(ord(key[i]))
    for i in range(1,xorTime):
        key_list[0] = key_list[0] ^ key_list[4 * i]
        key_list[1] = key_list[1] ^ key_list[4 * i + 1]
        key_list[2] = key_list[2] ^ key_list[4 * i + 2]
        key_list[3] = key_list[3] ^ key_list[4 * i + 3]
    FinalKey=key_list[0:4]
    return FinalKey
def encrypt_file(filename,key):
    k=changekey(key)
    h=[]
    hex_list = preprocess(filename)
    while len(hex_list) % 4 != 0:
        hex_list.append('00')
    for i in range(len(hex_list)):
        h.append(int.from_bytes(binascii.a2b_hex(hex_list[i]),byteorder='big', signed=False))
    for i in range(len(h)):
        h[i]=h[i]^k[i%4]
        h[i]=h[i].to_bytes(1,'big')
    encrypt_file_name=filename+".enc"
    f_write=open(encrypt_file_name,"wb+")
    for i in range(len(h)):
        f_write.write(h[i])
    f_write.close()
    print(filename + " has been encrypted,you can find it named <"+filename+".enc>")
def decrypt_file(filename,key):
    k = changekey(key)
    h = []
    hex_list = preprocess(filename)
    while len(hex_list) % 4 != 0:
        key.append('00')
    for i in range(len(hex_list)):
        h.append(int.from_bytes(binascii.a2b_hex(hex_list[i]), byteorder='big', signed=False))
    for i in range(len(h)):
        h[i] = h[i] ^ k[i % 4]
        h[i] = h[i].to_bytes(1, 'big')
    encrypt_file_name = filename + ".dec"
    f_write = open(encrypt_file_name, "wb+")
    for i in range(len(h)):
        f_write.write(h[i])
    f_write.close()
    print(filename + " has been decrypted,you can find it named <" + filename + ".dec>")


if __name__=="__main__":
    file_belong("h.exe")
    #write_to_file("helloworld.exe.enc.dec")
    encrypt_file("1.png","sundayLHN9824")
    file_belong("1.png")
    file_belong("1.png.enc")
    #decrypt_file("1.png.enc","sundayLHN9824")
'''
    if len(sys.argv) == 2 and sys.argv[1]=="-h": #输入一个参数且参数为-h则提供帮助目录
        print("python FileOperator.py + \n")
        print("                          -h                        #for help")
        print("                          -w [filename]             #write hex to 'hex.txt'")
        print("                          -m [filename]             #modify the file")
        print("                          -f [filename]             #find the format of the file")
        print("                          -e [filename] [password]  #encrypt the file")
        print("                          -d [filename] [password]  #decrypt the file")
    elif len(sys.argv) == 3 and sys.argv[1] == "-f": #输入为两个参数且参数为-f则查找文件类型
        try:
            file_belong(sys.argv[2])
        except FileNotFoundError: #若文件路径不存在则抛出异常
            print("file does not exists, please check and rerun")
    elif len(sys.argv) == 3 and sys.argv[1] == "-w": #输入为两个参数且参数为-w则将文件写入hex.txt
        try:
            write_to_file(sys.argv[2])
        except FileNotFoundError: #若文件路径不存在则抛出异常
            print("file does not exists, please check and rerun")
    elif len(sys.argv) == 3 and sys.argv[1] == "-m": #输入为两个参数且参数为-m则令使用者修改hex.txt并重新写回文件中
        try:
            modify_file(sys.argv[2])
        except FileNotFoundError: #若文件路径不存在则抛出异常
            print("file does not exists, please check and rerun")
    elif len(sys.argv) == 4 and sys.argv[1] == "-e": #输入为三个参数且参数为-e则通过输入的密码对文件进行加密
        try:
            encrypt_file(sys.argv[2],sys.argv[3])
        except FileNotFoundError: #若文件路径不存在则抛出异常
            print("file does not exists, please check and rerun")
    elif len(sys.argv) == 4 and sys.argv[1] == "-d": #输入为三个参数且参数为-d则通过输入的密码对文件进行解密
        try:
            decrypt_file(sys.argv[2],sys.argv[3])
        except FileNotFoundError: #若文件路径不存在则抛出异常
            print("file does not exists, please check and rerun")
    else:
        print('Parameter error,please input "-h" for help')#无输入或其他输入则提示参数错误'''