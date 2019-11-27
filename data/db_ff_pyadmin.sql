/*
 Navicat Premium Data Transfer

 Source Server         : .
 Source Server Type    : MySQL
 Source Server Version : 50630
 Source Host           : 127.0.0.1:3306
 Source Schema         : db_ff_pyadmin

 Target Server Type    : MySQL
 Target Server Version : 50630
 File Encoding         : 65001

 Date: 26/11/2019 23:05:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ff_asn
-- ----------------------------
DROP TABLE IF EXISTS `ff_asn`;
CREATE TABLE `ff_asn`  (
  `asn` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键, ASN(Autonomous System Number)',
  `asn_desc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ASN 描述',
  PRIMARY KEY (`asn`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 667 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ff_asn
-- ----------------------------
INSERT INTO `ff_asn` VALUES (666, '示例内容, 请忽略.');

-- ----------------------------
-- Table structure for ff_bgp
-- ----------------------------
DROP TABLE IF EXISTS `ff_bgp`;
CREATE TABLE `ff_bgp`  (
  `bgp_ip_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `bgp_ip` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'BGP 管理 IP',
  `bgp_asn` int(11) NOT NULL COMMENT 'BGP 所属 ASN',
  `bgp_desc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'BGP 服务器描述',
  `bgp_update` datetime(0) NULL DEFAULT NULL COMMENT '最后更新成功时间',
  PRIMARY KEY (`bgp_ip_id`) USING BTREE,
  UNIQUE INDEX `bgp_ip`(`bgp_ip`) USING BTREE,
  INDEX `ix_ff_bgp_bgp_update`(`bgp_update`) USING BTREE,
  INDEX `ix_ff_bgp_bgp_asn`(`bgp_asn`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ff_bgp
-- ----------------------------
INSERT INTO `ff_bgp` VALUES (1, '10.1.1.1', 666, '示例 BGP', NULL);

-- ----------------------------
-- Table structure for ff_log
-- ----------------------------
DROP TABLE IF EXISTS `ff_log`;
CREATE TABLE `ff_log`  (
  `log_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `log_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '日志写入时间',
  `log_action` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '操作, BGP 更新状态',
  `log_operator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '操作者姓名, BGP IP',
  `log_status` smallint(6) NOT NULL DEFAULT 1 COMMENT '操作是否成功',
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `ix_ff_log_log_operator`(`log_operator`) USING BTREE,
  INDEX `ix_ff_log_log_time`(`log_time`) USING BTREE,
  INDEX `ix_ff_log_log_status`(`log_status`) USING BTREE,
  INDEX `ix_ff_log_log_action`(`log_action`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for ff_role
-- ----------------------------
DROP TABLE IF EXISTS `ff_role`;
CREATE TABLE `ff_role`  (
  `role_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色标识, 如: admin, readonly',
  `role_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色名称, 如: 管理员, 只读权限',
  `role_allow` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '允许的权限列表(蓝图/视图函数名), 逗号分隔',
  `role_deny` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '禁止的权限(视图函数名), 最高优先级, 逗号分隔',
  PRIMARY KEY (`role_id`) USING BTREE,
  UNIQUE INDEX `role`(`role`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ff_role
-- ----------------------------
INSERT INTO `ff_role` VALUES (1, 'Admin', '管理员', 'asn,bgp,user,role,log', '');
INSERT INTO `ff_role` VALUES (2, 'QA', '质量管理', 'asn,bgp,log', 'asn_add,bgp_add');

-- ----------------------------
-- Table structure for ff_user
-- ----------------------------
DROP TABLE IF EXISTS `ff_user`;
CREATE TABLE `ff_user`  (
  `job_number` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键, 工号',
  `realname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '姓名',
  `mobile` varchar(23) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '手机号',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色标识',
  `status` smallint(6) NULL DEFAULT 0 COMMENT '状态: 1 正常, 0 禁用',
  PRIMARY KEY (`job_number`) USING BTREE,
  INDEX `ix_ff_user_status`(`status`) USING BTREE,
  INDEX `ix_ff_user_role`(`role`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10000 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ff_user
-- ----------------------------
INSERT INTO `ff_user` VALUES (777, 'QA', '13000000000', '', 0);
INSERT INTO `ff_user` VALUES (7777, 'Fufu', '', 'Admin', 1);
INSERT INTO `ff_user` VALUES (9999, 'BDDTester', '', 'Admin', 1);

SET FOREIGN_KEY_CHECKS = 1;
