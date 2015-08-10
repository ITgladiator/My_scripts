#/bin/sh
#cut nginx access log by day
#by gc @ 2014.12.16

LOG_DIR=/app/logs
PID=`cat /app/logs/nginx.pid`
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

/bin/mv ${LOG_DIR}/file.fairvo.com_access.log ${LOG_DIR}/file.fairvo.com_access_${YESTERDAY}.log
/bin/mv ${LOG_DIR}/video.fairvo.com_access.log ${LOG_DIR}/video.fairvo.com_access_${YESTERDAY}.log

kill -USR1 $PID
