# Check the requirements for the installation
# Installation needs root privileges
if [ $UID -ne 0 ]; then
    echo "This script requires root privileges."
    echo "Please run the script as root."
    exit 1
fi

echo "Downloading the payloads\n"

wget https://github.com/hisorange/scale/releases/download/V_TAG/scale
wget https://github.com/hisorange/scale/releases/download/V_TAG/checksum.md5
wget https://github.com/hisorange/scale/releases/download/V_TAG/scale.asc
wget https://github.com/hisorange/scale/releases/download/V_TAG/scale.gpg.key

if [ -f scale ]; then
    echo "Scale downloaded\n"
else
    echo "Scale not downloaded\n"
    exit 2
fi

echo "Verifying the checksum\n"

md5sum -c checksum.md5

if [ $? -eq 0 ]; then
    echo "Checksum is correct\n"
else
    echo "Checksum is not correct\n"
    exit 2
fi

echo "Verifying the GPG signature\n"

gpg --import --batch scale.gpg.key
gpg --verify scale.asc scale

if [ $? -eq 0 ]; then
    echo "Signature is correct\n"
else
    echo "Signature is not correct\n"
    exit 3
fi

echo "Making the binary executable\n"

chmod +x scale

echo "Moving to the global path\n"

mv scale /usr/bin/scale

rm -f checksum.md5 scale.asc scale.gpg.key

echo "\nInstallation is ready!\n"
