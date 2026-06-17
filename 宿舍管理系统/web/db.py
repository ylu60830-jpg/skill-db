# -*- coding: utf-8 -*-
"""数据库操作封装"""

import mysql.connector
from config import DB_CONFIG


def get_conn():
    return mysql.connector.connect(**DB_CONFIG)


def query(sql, params=None):
    """执行 SELECT，返回字典列表"""
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def query_one(sql, params=None):
    """执行 SELECT，返回单条字典或 None"""
    rows = query(sql, params)
    return rows[0] if rows else None


def execute(sql, params=None):
    """执行 INSERT/UPDATE/DELETE，返回影响行数"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    rowcount = cur.rowcount
    conn.close()
    return rowcount
