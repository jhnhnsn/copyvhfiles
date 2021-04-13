Makes copies of your Valheim character and world files. There's also an option to download world files from an FTP server if you're using a hosting service that supports that kind of thing.

You'll need to create a config file from the sample provided. Just copy vhbuconfig-SAMPLE.json to vhbuconfig.json.

Change the user directory for local character and world files and the directory you want to store the backed up files. 

If you want to backup ftp files change "ftp_backup_enabled": false to "ftp_backup_enabled": true in vhbuconfig.json. You'll also need to provide address, port, username, password, and subdir for where your world files are stored. If you want to only download files with a specific substring (other than "world") you can change that value too. I think "world" is a safe default. I have no idea what happens if it's empty.

Also, I've barely tested this. Please be sure you know what you're doing before you try this. There's a really good chance it could delete everything.
