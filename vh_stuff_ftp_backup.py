from shutil import copytree
from datetime import datetime
from os import listdir, mkdir, path
from ftplib import FTP
import json

CONFIG_FILE = './vhbuconfig.json'

def read_config_file():
    #read config json
    with open(CONFIG_FILE) as file:
        config_json = json.load(file)
    return config_json

conf = read_config_file()

host = conf["host"]
port = conf["port"]
username = conf["username"]
password = conf["password"]

#set up local folders
# vh user data location
vh_user_data_dir = r"C:\Users\johnh\AppData\LocalLow\IronGate\Valheim"

# where to put character and world backups
vh_backup_root_dir = r"C:\Users\johnh\OneDrive\Valheim\local_vh_backup"

#full paths to char and world folders
vh_char_path = path.join(vh_user_data_dir, "characters")
vh_world_path = path.join(vh_user_data_dir, "worlds")

#build backup dir paths with datetime
vh_backup_dir = str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S-%f"))
vh_backup_fullpath = path.join(vh_backup_root_dir, vh_backup_dir)

#make backup parent dir
mkdir(vh_backup_fullpath)

vh_char_backup_fullpath = (path.join(vh_backup_fullpath + "/character"))
vh_world_backup_fullpath =  (path.join(vh_backup_fullpath + "/world"))
vh_ftp_world_backup_fullpath = (path.join(vh_backup_fullpath + "/mixer_crew_server"))

#make directory for ftp files
mkdir(vh_ftp_world_backup_fullpath)

#print("Backup up from: " + vh_user_data_dir + " to: " + vh_backup_fullpath)

#actually copy
copytree(vh_char_path, vh_char_backup_fullpath)
copytree(vh_world_path, vh_world_backup_fullpath)

#Copy FTP server files from g-portal
ftp = FTP()
#connect
ftp.connect(host, port)
ftp.login(username, password)
#change dir
ftp.cwd("save/worlds")

#list files and put filenames in an array
listings = []
filenames = []
ftp.retrlines('LIST', listings.append)
for listing in listings:
    f = listing.split(None, 8)
    fname = f[8]
    filenames.append(fname)

#find the files that match the server string
files_to_download = []
for match in filenames:
    if "mixer" in match:
        files_to_download.append(match)

f = files_to_download[0] #replace with loop for all matching files
for f in files_to_download:
    local_filename = path.join(vh_ftp_world_backup_fullpath, f)
    lf = open(local_filename, "wb")
    ftp.retrbinary("RETR " + f, lf.write)
    lf.close()

#close connection
ftp.quit()