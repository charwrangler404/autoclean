from pathlib import PosixPath
import os
import time
import configparser
import notify2

def read_etc_config():
    config = configparser.ConfigParser()
    config.read("/etc/autoclean/config.ini")
    user = config['USER']
    #system = config['SYSTEM']
    return user#, system

def read_dir_config(configdir):
    directories = []
    p = PosixPath(configdir)
    for x in p.iterdir():
        if x.is_file():
            newconfig = configparser.ConfigParser()
            newconfig.read(str(x))
            directories.append(newconfig["FOLDER"])

    return directories

def move_file(file, destfolder):
    if file.exists():
        os.rename(str(file), f"{destfolder}/{file.name}" )

def remove_file(file):
    if file.exists():
        os.remove(str(file))

def notify(title, message):
    notification = notify2.Notification(title, message, "notification-message-im")
    notification.show()

def check_purge(dir_config):
    dir = dir_config['Target']
    archive1_age =  time.clock_gettime(time.CLOCK_REALTIME) - float(int(dir_config['Archive1']) * 24 * 60 * 60)
    archive2_age = time.clock_gettime(time.CLOCK_REALTIME) - float(int(dir_config['Archive2']) * 24 * 60 * 60 )
    archive3_age = time.clock_gettime(time.CLOCK_REALTIME) - float(int(dir_config['Archive3']) * 24 * 60 * 60 )
    maxage = time.clock_gettime(time.CLOCK_REALTIME) - float(int(dir_config['MaxAge']) * 24 * 60 * 60)
    p = PosixPath(dir)
    files_archive_1 = 0
    files_archive_2 = 0
    files_archive_3 = 0
    files_deleted = 0
    for x in p.iterdir():
        if x.is_file():
            stat = os.stat(x)
            if stat.st_atime > archive1_age:
                # Rotate file to Archive1_New folder
                move_file(x, f"{dir}/Archive1_Recent/{x.name}")
                files_archive_1 += 1
            elif stat.st_atime > archive2_age:
                # Rotate file to Archive2_Recent folder
                move_file(x, f"{dir}/Archive2_Old/{x.name}")
                files_archive_2 += 1
            elif stat.st_atime > archive3_age:
                # Rotate file to Archive3_Old_About_to_be_deleted folder
                move_file(x, f"{dir}/Archive3_AboutToBeDeleted")
                files_archive_3 += 1
            elif stat.st_atime > maxage:
                remove_file(x)
                files_deleted += 1

    notify(dir, f"{files_archive_1} files moved to Archive1_Recent")
    notify(dir, f"{files_archive_2} files moved to Archive2_Old")
    notify(dir, f"{files_archive_3} files moved to Archive3_AboutToBeDeleted")

if __name__ == "__main__":
    userconfig = read_etc_config()
    configdir = userconfig['ConfigDir']
    username = userconfig['User']
    directories = read_dir_config(configdir)
    for directory in directories:
        check_purge(directory)