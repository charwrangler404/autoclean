cat "export PATH=$PATH:$HOME/.local/bin/" >> $HOME/.bashrc
mkdir -p $HOME/.local/bin/autoclean
mkdir -p $HOME/.config/autoclean.d

cp -r src/* $HOME/.local/bin/autoclean/
cp requirements.txt $HOME/.local/bin/autoclean/
pushd $HOME/.local/bin/autoclean
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
popd
cp autoclean.d/downloads.ini $HOME/.config/autoclean.d/downloads.ini
echo "You will need to modify the downloads.ini file in $HOME/.config/autoclean.d/ to match your desired configuration"