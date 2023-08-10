# 数据监控脚本
### python 2.7
#### 目录结构
 * **check** *检测case目录*
    * check.py *主文件*

 * **config** *配置目录(case,base,....yaml)*
    * base *case conf base conf*
    * case *case conf*
    * case_default.yaml *case默认配置*
    * cmd.yaml  *cmd配置*
    * const.yaml *常量配置*
    * databases.yaml *Db配置*
    * redis.yaml *Monitor_Redis配置*

 * **core** *依赖*
    * Model.py *数据库操作*
    * Redis.py *Redis操作*

 * **init** *初始化*
    * case *初始化case目录*
    * init_base.py *初始化conf*
    * init_case.py *初始化case*

 * **log** *日志目录*

 * **model** *DB操作类存放目录*
    * monitor.py *监控history&notice方法*

 * **tool** *工具类*
    * _print.py *打印方法类*
    * assertions.py *断言类*
    * http.py *HTTP 请求类*
    * log.py *写日志方法(比较简单)*
    * notice.py *通知类*
    * tool_conf.py *conf 工具*

#### 运行demo
 * python main.py
 * python main.py --monitor_type=mysql *单独跑mysql_case*