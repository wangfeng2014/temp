#! /bin/sh
# Short-Description: control the temperature & huminity detect sensor
do_start(){
        sudo /home/pi/sensor/temp.py >&2 &
}

do_stop() {
        pid=$(ps -ef|grep temp.py|grep -v grep|head -1|awk {'print $2'})
        if [ $pid ] ; then
                echo "kill process $pid"
                sudo kill $pid
        else
            echo "no precess is running"
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
