
t=`date +%s`
log=logs/log.${t}

date > ${log}
/usr/bin/python3 update_seaweedfs.py >> ${log}
date >> ${log}

