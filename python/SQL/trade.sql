/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100421
 Source Host           : localhost:3306
 Source Schema         : coin

 Target Server Type    : MySQL
 Target Server Version : 100421
 File Encoding         : 65001

 Date: 12/01/2022 13:29:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for trade
-- ----------------------------
DROP TABLE IF EXISTS `trade`;
CREATE TABLE `trade`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_symbol` int NULL DEFAULT NULL,
  `close_time` bigint NULL DEFAULT NULL,
  `status` tinyint NULL DEFAULT NULL COMMENT '1 buy -1 sell',
  `gain` double NULL DEFAULT NULL,
  `price` double NULL DEFAULT NULL,
  `id_kline` int NULL DEFAULT NULL,
  `investment` double NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index`(`id_symbol`, `close_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
