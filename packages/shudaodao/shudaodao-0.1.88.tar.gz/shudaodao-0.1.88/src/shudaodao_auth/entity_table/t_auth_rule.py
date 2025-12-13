#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @License  ：(C)Copyright 2025, 数道智融科技
# @Author   ：李锋
# @Software ：PyCharm
# @Date     ：2025/9/17 上午11:06
# @Desc     ：

from sqlalchemy import Column, Integer, String

from ..package_config import PackageConfig

Base = PackageConfig.Registry.generate_base()


class AuthRule(Base):
    __tablename__ = "t_auth_rule"
    __table_args__ = {"schema": PackageConfig.SchemaTable, "comment": "访问控制规则表"}

    id = Column(Integer, primary_key=True, comment="主键")
    ptype = Column(String(255), comment="类型")
    v0 = Column(String(255), comment="角色/用户")
    v1 = Column(String(255), comment="资源/角色")
    v2 = Column(String(255), comment="动作")
    v3 = Column(String(255), comment="租户")
    v4 = Column(String(255))
    v5 = Column(String(255))

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ", ".join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))
