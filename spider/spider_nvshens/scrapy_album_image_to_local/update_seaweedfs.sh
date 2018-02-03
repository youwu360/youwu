
t=`date +%s`
log=logs/log.${t}



date > ${log}
a=`ps aux | grep "update_seaweedf.py" | grep -v grep |wc -l`
if [ $a -gt 0 ]
then
    echo "update_seaweedf is executing , exit now !"
    exit
fi

/usr/bin/python3 update_seaweedfs.py >> ${log}
date >> ${log}

