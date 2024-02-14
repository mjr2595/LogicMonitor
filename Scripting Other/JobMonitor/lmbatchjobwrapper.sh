#!/bin/sh
#
# Copyright (c) 2010, LogicMonitor LLC. All rights reserved.
#
# 
# lmbatchjobwrapper.sh is used to wrap your program. For example, in your
# crontab, there is a line
#
#   0 0 * * * /myfolder/cleanlog.pl /mylogfolder
#
# You can change it to:
#
#   0 0 * * * lmbatchjobwrapper.sh <agentaddr> <hostname> <jobname> /myfolder/cleanlog.pl /mylogfolder
#
# When crond starts lmbatchjobwrapper.sh, it will start cleanlog.pl, monitor
# its execution, and reports the result to the agent that, in turn, reports the
# results back to the server.
# 

# utilitiles ################################################


# usage - show usage info and quit
#
usage() {
    echo "
Usage: lmbatchjobwrapper.sh <agentaddr> <hostname> <jobname> <cmdline>
Examples:
    lmbatchjobwrapper.sh 192.168.1.100:7214 hostfoo jobbar /usr/local/bin/cleanlog.pl /usr/local/tomcat/logs"
    exit 1
}

# time is kept word for shell, use time_ instead
time_() {
    date +%s
}


log_info() {
    msg=${1:?"msg is required"}
    echo "`date +"%Y-%m-%d %H:%M:%S"` - $msg"
}
   



# main entry point
#
if ! type curl >/dev/null;then
    echo "you need curl installed on the host to use this wrapper script"
    exit 2
fi

AGENT_URL="/batchjobhandler/reportEvent"

if [ $# -lt 4 ];then
    usage
fi

AGENT_ADDR=$1
HOST_NAME=$2
JOB_NAME=$3
shift 3
CUSTOM_CMD_LINE=$@
URL="http://$AGENT_ADDR$AGENT_URL"
EXECUTION_NO=`time_`

log_info "Start (agent=$AGENT_ADDR, host=$HOST_NAME, job=$JOB_NAME, seq=$EXECUTION_NO, cmdline=$CUSTOM_CMD_LINE)"

# prepare useragent 
USER_AGENT="LogicMonitor BatchJob Wrapper/0.01"

STATUS_CODE=`curl -o /dev/null -s -w "%{http_code}" --data "type=start&executionNo=$EXECUTION_NO&hostName=$HOST_NAME&batchjobName=$JOB_NAME&epoch=$EXECUTION_NO&cmdLine=$CUSTOM_CMD_LINE" "$URL"`
if [ "$STATUS_CODE" != "200" ];then
    log_info "Failed to report start event to the agent - $STATUS_CODE"
else
    log_info "Reported start event to the agent"
fi

# start the customer job
sleep 2
log_info "Executing the job ..."

TMP_STDERR=`mktemp "lmjobwrapperXXXXXXX"`
STDOUT=`$CUSTOM_CMD_LINE 2>$TMP_STDERR`;
EXIT_CODE=$?
STDERR=`cat $TMP_STDERR`
rm $TMP_STDERR

if [ $EXIT_CODE -eq 0 ];then
    LEVEL='ok'
else
    LEVEL='error'
fi


EPOCH=`time_`
STATUS_CODE=`curl -o /dev/null -s -w "%{http_code}" --data "type=finish&executionNo=$EXECUTION_NO&hostName=$HOST_NAME&batchjobName=$JOB_NAME&epoch=$EPOCH&stdout=$STDOUT&stderr=$STDERR&exitCode=$EXIT_CODE&alertLevel=$LEVEL" "$URL"`
if [ "$STATUS_CODE" != "200" ];then
    log_info "Failed to report start event to the agent - $STATUS_CODE"
else
    log_info "Reported start event to the agent"
fi

log_info "Done (exitCode=$EXIT_CODE)"

exit 0;