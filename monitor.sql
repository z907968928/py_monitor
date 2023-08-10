CREATE DATABASE monitor;
USE monitor;

CREATE TABLE `monitor_history` (
  `id` bigint(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `monitor_key` varchar(100) NOT NULL DEFAULT '' COMMENT '监控key',
  `monitor_datetime` datetime NOT NULL DEFAULT '1971-01-01 00:00:00' COMMENT '监控时间',
  `monitor_group` varchar(100) NOT NULL DEFAULT '' COMMENT '监控组',
  `case_name`  varchar(100) NOT NULL DEFAULT '' COMMENT 'case名称',
  `is_succ` tinyint(4) NOT NULL DEFAULT '1' COMMENT '是否成功',
  `param` varchar(1000) NOT NULL DEFAULT '' COMMENT '监控参数',
  `result` text COMMENT '监控返回',
  `err_msg` text COMMENT '错误消息',
  PRIMARY KEY (`id`),
  KEY `idx_monitor_query` (`monitor_key`,`monitor_datetime`,`is_succ`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='数据监控历史';

CREATE TABLE `monitor_notice` (
  `id` bigint(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '标题',
  `monitor_key` varchar(100) NOT NULL DEFAULT '' COMMENT '监控key',
  `case_name` varchar(100) NOT NULL DEFAULT '' COMMENT 'case名称',
  `content` text COMMENT '内容',
  `create_time` datetime NOT NULL DEFAULT '1971-01-01 00:00:00' COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT '1971-01-01 00:00:00' COMMENT '修改时间',
  `is_succ` tinyint(4) NOT NULL DEFAULT '1' COMMENT '是否成功',
  `is_show` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否展示',
  `deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='数据监控公告';