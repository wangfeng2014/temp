#! /bin/sh
### BEGIN INIT INFO
# Provides:          sensor
# Required-Start:    $local_fs
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: control the temperature & huminity detect sensor
### END INIT INFO
do_start(){
        sudo /home/pi/sensor/temp.py >&2 &
}

do_stop() {
        pid = $(ps -ef|grep temp.py|grep -v grep|head -1|awk {'print $2'})
        echo $pid
        if [[ $pid ]] ; then
                echo "not kill"
                sudo kill $pid
        fi
}

case "$1" in
  start)
        do_start
        ;;
  restart)
        do_stop
        do_start
        ;;		
  stop)
        do_stop        
        ;;
  *)
        echo "Usage: $0 start|stop|restart" >&2
	echo  '\n\n'
	q
        
        ;;
esac

exit 0
~
