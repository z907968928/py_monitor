if [ ! -n "`pip show redis`" ];
then
    pip install redis --trusted-host didiyum.sys.xiaojukeji.com -i http://didiyum.sys.xiaojukeji.com/didiyum/pip/simple/
fi

if [ ! -n "`pip show requests`" ];
then
    pip install requests --trusted-host didiyum.sys.xiaojukeji.com -i http://didiyum.sys.xiaojukeji.com/didiyum/pip/simple/
fi

nohup python main.py &