#!/bin/bash
# Inspiration: https://github.com/brablc/clit/blob/master/tmutil-safe-nas-backup

function tmrunning() {
    return $([ $(tmutil currentphase) != 'BackupNotRunning' ])
}

function echostate() {
    DATE=$(date +"%Y-%m-%d %H:%M:%S")
    STATE=$1
    shift
    OPT=""
    if [ "$STATE" = "-n" ]; then 
        OPT=$STATE
        STATE=$1
        shift
    fi
    echo $OPT "-$STATE|$DATE|" $* 
}

function terminatecaffeinate() {
    echostate I "Terminating caffeinate."
    ps -ef | grep caffeinate | awk '{print $2}' | xargs kill 2> /dev/null
}

function tmrun() {
    # End caffeinate if already running in another script
    hash caffeinate 2>/dev/null
    CAFFEINATE_RUNNING=$?
    if [ $CAFFEINATE_RUNNING ]; then
        terminatecaffeinate
    fi

    echostate I "Start caffeinate"
    caffeinate &

    echostate I "Preventing sleep while backup is running"
    PHASE=""
    while tmrunning; do
        NEWPHASE=$(tmutil currentphase)
        if [ "$PHASE" != "$NEWPHASE" ]; then
            echostate I "Current phase: $NEWPHASE"
            PHASE=$NEWPHASE
        fi 
        sleep 10
    done

    terminatecaffeinate
}

if tmrunning; then
    tmrun
else
    echostate W "Backup is not running. Exiting ..."
    exit 1
fi