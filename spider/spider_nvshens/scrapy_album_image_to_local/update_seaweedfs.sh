
t=`date +%s`

date > log.${t}
/usr/bin/python3 update_seaweedfs.py >> log.${t}
date >> log.${t}

