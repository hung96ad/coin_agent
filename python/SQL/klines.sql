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

 Date: 12/01/2022 13:29:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for klines
-- ----------------------------
DROP TABLE IF EXISTS `klines`;
CREATE TABLE `klines`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_symbol` int NULL DEFAULT NULL,
  `Close_time` bigint NULL DEFAULT NULL,
  `Open` double NULL DEFAULT NULL,
  `High` double NULL DEFAULT NULL,
  `Low` double NULL DEFAULT NULL,
  `Close` double NULL DEFAULT NULL,
  `Volume` double NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `index`(`id_symbol`, `Close_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 175274 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
