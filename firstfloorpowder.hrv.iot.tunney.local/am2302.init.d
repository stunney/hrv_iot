#!/bin/ash /etc/rc.common

START=100
STOP=1

DIR=/root
DAEMON=$DIR/am2302.py
DAEMON_NAME=AM2302_Monitor
DAEMON_OPTS=""
DAEMON_USER=root

PIDFILE=/var/run/$DAEMON_NAME.pid

start() {
	cd $DIR
	python $DEAMON > $DIR/logs/am2302.log 2>&1 & 
}

stop() {
	echo Goodbye
}