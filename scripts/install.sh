wget https://github.com/hisorange/scale/releases/download/V_TAG/scale && \
wget https://github.com/hisorange/scale/releases/download/V_TAG/checksum.md5 && \
wget https://github.com/hisorange/scale/releases/download/V_TAG/scale.asc && \
wget https://github.com/hisorange/scale/releases/download/V_TAG/scale.gpg.key && \
md5sum -c checksum.md5 scale && \
gpg --import scale.gpg.key && \
gpg --verify scale.asc scale && \
chmod +x scale && \
mv scale /usr/bin/scale

