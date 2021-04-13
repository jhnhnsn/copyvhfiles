from shutil import copytree
from datetime import datetime
from os import listdir, mkdir, path
from ftplib import FTP
import json

## Edit and rename vhbuconfig-SAMPLE.json
CONFIG_FILE = './vhbuconfig.json'

#read config file and initialize
try:
    with open(CONFIG_FILE) as file:
        conf = json.load(file)
except:
    print("Oopsy. Couldn't fine the config file.")

#initialize vars with config file values
host = conf["host"]
port = conf["port"]
username = conf["username"]
password = conf["password"]
ftp_substring = conf["ftp_substring"]
ftp_subdir = conf["ftp_subdir"]
vh_user_data_dir = conf["vh_user_data_dir"]
vh_backup_root_dir = conf["vh_backup_root_dir"]

#full paths to char and world folders
vh_char_path = path.join(vh_user_data_dir, "characters")
vh_world_path = path.join(vh_user_data_dir, "worlds")

#build backup dir paths with datetime
vh_backup_dir = str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S-%f"))
vh_backup_fullpath = path.join(vh_backup_root_dir, vh_backup_dir)

#make backup parent dir
print("Making directory: " + vh_backup_fullpath)
mkdir(vh_backup_fullpath)

vh_char_backup_fullpath = (path.join(vh_backup_fullpath + "/character"))
vh_world_backup_fullpath =  (path.join(vh_backup_fullpath + "/local_world"))
vh_ftp_world_backup_fullpath = (path.join(vh_backup_fullpath + "/server_world"))

#make directory for ftp files
print("Making directory: " + vh_ftp_world_backup_fullpath)
mkdir(vh_ftp_world_backup_fullpath)

#actually copy
print("Backing up local files from: " + vh_user_data_dir + " to: " + vh_backup_fullpath)
try:
    copytree(vh_char_path, vh_char_backup_fullpath)
    copytree(vh_world_path, vh_world_backup_fullpath)
except:
    print("Couldn't copy local backup files. Check that the config file is correct")

#Copy FTP server files from g-portal
try:
    ftp = FTP()
    #connect
    print("Connecting to ftp server: " + host)
    ftp.connect(host, port)
    ftp.login(username, password)
    #change dir
    ftp.cwd(ftp_subdir)

    #list files and put filenames in an array
    listings = []
    filenames = []
    ftp.retrlines('LIST', listings.append)
    for listing in listings:
        f = listing.split(None, 8)
        fname = f[8]
        filenames.append(fname)

    #find the files that match the server string
    print("Downloading all files matching substring " + ftp_substring)
    files_to_download = []
    for match in filenames:
        if ftp_substring in match:
            files_to_download.append(match)

    f = files_to_download[0] #replace with loop for all matching files
    for f in files_to_download:
        local_filename = path.join(vh_ftp_world_backup_fullpath, f)
        lf = open(local_filename, "wb")
        ftp.retrbinary("RETR " + f, lf.write)
        lf.close()

    #close connection
    ftp.quit()

except:
    print("FTP step failed. Check config file settings and try again.")

print("All done.")
    