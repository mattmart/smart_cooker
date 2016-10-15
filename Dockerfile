from resin/rpi-raspbian:latest
run apt-get update && apt-get install --yes python2.7 python-pip wget make gcc build-essential postgresql postgresql-server-dev-all python-dev
run wget http://heyu.org/download/heyu-2.10.tar.gz && tar xf heyu-2.10.tar.gz && cd heyu-2.10 && sh ./Configure && make && yes 4 | make install && cp heyu /usr/local/bin
run mkdir /root/.heyu
run echo "TTY /host/dev/ttyUSB0" > /root/.heyu/x10config
run pip install plotly flask psycopg2
add . /root/smart_cooker
