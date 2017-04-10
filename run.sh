#!/bin/bash

#author:patrickstary

RED='\e[1;91m'
GREEN='\e[1;92m'
WITE='\e[1;97m'
NC='\e[0m'

SOLR_SYNC_HOME="."
PID_DIR="./run"
mkdir -p $PID_DIR
chmod 777 $PID_DIR
LOG_DIR="/var/log/solr_sync"
mkdir -p $LOG_DIR
chmod 777 $LOG_DIR
STDOUT="$LOG_DIR/stdout"

CONFIG_FILE="$SOLR_SYNC_HOME/config.py"
SOLR_SYNC_FILE="$SOLR_SYNC_HOME/solr_sync.py"
if [ ! -f $CONFIG_FILE ]; then
    echo "Config.py not found!"
    exit 1
fi
if [ ! -f $SOLR_SYNC_FILE ]; then
    echo "solr_sync.py not found!"
    exit 1
fi

PID_FILE="$PID_DIR/solr_sync.pid"
if [ ! -f $PID_FILE ]; then
    echo -e $RED"pid file not exist, create it."$NC
    touch $PID_FILE
    chmod 777 $PID_FILE
fi

function start_service() {
    PIDS=$(ps -ef | grep -F "python ./solr_sync" | grep -v grep | awk '{print $2}')
    if [[ "$PIDS" != "" ]]; then
        echo -e $RED"service is running."$NC
        return
    fi
    LAST_POS=$(ls -al $STDOUT  | awk '{print $5}')
    echo "=======================start service============================" >> $STDOUT
    echo $(date '+%F %T') >> $STDOUT
    python $SOLR_SYNC_FILE 2>&1 1>>$STDOUT &
    echo $! > $PID_FILE
    PID=$!
    echo "process pid:$PID"
    for (( i=0;i<100;i++ )); do
        if [ $PID != "" ]; then
            if [ $(tail -n 2 $STDOUT | grep -c -F "start ok") -gt 0 ]; then
                CUR_POS=$(ls -al $STDOUT  | awk '{print $5}')
                tail -c $(expr $CUR_POS - $LAST_POS) $STDOUT
                echo
                echo -e $GREEN"start service."$NC
                return
            fi
        fi
        printf "."
        sleep 0.5
    done

    echo
    CUR_POS=$(ls -al $STDOUT  | awk '{print $5}')
    tail -c $(expr $CUR_POS - $LAST_POS) $STDOUT
    echo -e $RED"Service start failed."$NC
    exit 1
}

function stop_service() {
    echo "=======================stop service============================" >> $STDOUT
    echo $(date '+%F %T') >> $STDOUT
    PID=$(cat $PID_FILE)
    EXEC=$(ps -ef | awk -v "PID=$PID" '{if( $2 == PID ) {print $9}}')
    if [[ "$EXEC" == "" ]]; then
        echo -e $RED"service is not running."$NC
        echo "" > $PID_FILE
        return
    elif [[ "$EXEC" =~ "solr_sync" ]]; then
        kill -9 $PID
        echo -e $GREEN"stop service successfully."$NC
        echo "" > $PID_FILE
        return
    else
        echo -e $RED"not found service. somthing error."$NC
        echo "exec:$EXEC"
        return
    fi
    echo
    echo -e $RED"stop service failed."$NC
    exit 1
}



function stop_all_service() {
    LIST=$(ps -ef | grep -F "solr_sync" | grep -v grep | awk '{print $2}')
    for pid in LIST
    do
        kill -9 $pid
    done
    echo -e $GREEN"stop all service successfully."$NC
    echo "" > $PID_FILE
}

function status_service() {
    PID=$(cat $PID_FILE)
    echo "pid:$PID"
    EXEC=$(ps -ef | awk '{if($2==$PID){print $8}}')
    echo "exec:$EXEC"
    if [[ "$EXEC" == "" ]]; then
        echo -e $RED"server is not running."$NC
    elif [[ "$EXEC" =~ "solr_sync" ]]; then
        echo -e $RED"service is running."$NC
        exit 1
    else
        echo -e $RED"service is not running."$NC
    fi
}

MODE=$1
case $MODE in
    "start")
        start_service
        ;;
    "restart")
        stop_service
        start_service
        ;;
    "stop")
        stop_service
        ;;
    "status")
        status_service
        ;;
    "stopall")
        stop_all_service
        ;;
    *)
        echo -e "Usage: $0 { start | stop | restart | status}"
        exit 1
        ;;
esac

