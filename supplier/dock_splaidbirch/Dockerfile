FROM nsjail:18.04

RUN useradd -m -d /home/user -s /bin/bash -u 1000 user
COPY splaid_birch /home/user/splaid_birch
COPY flag /home/user/flag
COPY libsplaid.so.1 /usr/lib/libsplaid.so.1
CMD su user -c 'nsjail -Ml --port 31000 --chroot / --user 1000 --group 1000 /home/user/splaid_birch'
EXPOSE 31000