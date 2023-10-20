# Autoclean

This script watches your configured directories for old files, sorts them for you, and eventually deletes them when enough time has passed.

Use it to keep your downloads folder pristine! Or maybe you want to rotate the files based on your own criteria! That's an option too, with config files 
located in $HOME/.config/autoclean.d/, you can define any number of directories to watch, and the rotation time for each file in days!

To schedule a task, install the program using the install script. This will add the right configuration variables and install the script to your home 
folder. Then, schedule a cronjob using your user crontab with the command crontab -e

    0 * * * * * source $HOME/.local/bin/autoclean/.venv/bin/activate && python $HOME/.local/bin/autoclean/main.py