INSERT INTO `tbl_users` (`userId`, `email`, `password`, `name`, `mobile`, `roleId`, `isDeleted`, `createdBy`, `createdDtm`, `updatedBy`, `updatedDtm`, `api_key`, `api_secret`, `auto_trade`) VALUES (1, 'admin@example.com', '$2y$10$kb0u/30KKcGkwBIvWhAhK.xy29uJBcLW4V22qLV2Kn7oEaoHXVyd6', 'System Administrator', '1234567890', 1, 0, 0, '2015-07-01 18:56:49', 1, '2019-06-23 17:27:44', '23224', '435', 1);
INSERT INTO `tbl_users` (`userId`, `email`, `password`, `name`, `mobile`, `roleId`, `isDeleted`, `createdBy`, `createdDtm`, `updatedBy`, `updatedDtm`, `api_key`, `api_secret`, `auto_trade`) VALUES (2, 'manager@example.com', '$2y$10$O7jjcIKV4iLmMJDu8No/b.uD2XpCAsxt5g.bkKDCYUtO.Fz6O3Ooq', 'Manager', '9890098900', 2, 0, 1, '2016-12-09 17:49:56', 2, '2018-10-30 14:11:01', NULL, NULL, 0);
INSERT INTO `tbl_users` (`userId`, `email`, `password`, `name`, `mobile`, `roleId`, `isDeleted`, `createdBy`, `createdDtm`, `updatedBy`, `updatedDtm`, `api_key`, `api_secret`, `auto_trade`) VALUES (3, 'employee@example.com', '$2y$10$O7jjcIKV4iLmMJDu8No/b.uD2XpCAsxt5g.bkKDCYUtO.Fz6O3Ooq', 'Employee', '9890098900', 3, 1, 1, '2016-12-09 17:50:22', 1, '2019-01-04 20:19:11', NULL, NULL, 0);
INSERT INTO `tbl_users` (`userId`, `email`, `password`, `name`, `mobile`, `roleId`, `isDeleted`, `createdBy`, `createdDtm`, `updatedBy`, `updatedDtm`, `api_key`, `api_secret`, `auto_trade`) VALUES (4, 'hung@gmail.com', '$2y$10$kb0u/30KKcGkwBIvWhAhK.xy29uJBcLW4V22qLV2Kn7oEaoHXVyd6', NULL, NULL, 3, 0, 0, '2021-12-26 10:54:33', NULL, NULL, NULL, NULL, 0);
