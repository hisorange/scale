echo 'Downloading the payloads\n'

wget https://github.com/hisorange/scale/releases/download/V_TAG/scale
wget https://github.com/hisorange/scale/releases/download/V_TAG/checksum.md5
wget https://github.com/hisorange/scale/releases/download/V_TAG/scale.asc
wget https://github.com/hisorange/scale/releases/download/V_TAG/scale.gpg.key

if ! [ -f scale ]; then
    exit 2
fi

md5sum -c checksum.md5 scale

if ! [ $? -eq 0 ]; then
    exit 2
fi

gpg --import scale.gpg.key
gpg --verify scale.asc scale

if ! [ $? -eq 0 ]; then
    exit 3
fi

chmod +x scale
mv scale /usr/bin/scale