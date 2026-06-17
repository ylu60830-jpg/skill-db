#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宿舍信息管理系统 - 终端交互式前端 (TUI)
基于 MySQL dormitory_system 数据库
菜单导航式 CRUD 操作
"""

import mysql.connector
import os
import sys
import re
import io

# 强制 UTF-8 输出（兼容 GBK 终端）
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stdin.encoding != "utf-8":
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
from textwrap import fill as twfill

# -- 字符宽度工具（中文=2, 英文=1）-----------------------
def dwidth(s):
    """终端显示宽度: CJK=2, ASCII=1"""
    w = 0
    for ch in str(s):
        if '一' <= ch <= '鿿' or '　' <= ch <= '〿' or '＀' <= ch <= '￯':
            w += 2
        else:
            w += 1
    return w


def dpad(s, width, align='left'):
    """按显示宽度填充"""
    s = str(s)
    cur = dwidth(s)
    if cur >= width:
        return s
    pad = width - cur
    if align == 'center':
        lp, rp = pad // 2, pad - pad // 2
        return ' ' * lp + s + ' ' * rp
    elif align == 'right':
        return ' ' * pad + s
    return s + ' ' * pad


# -- 数据库配置 -------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "dormitory_system",
    "charset": "utf8mb4",
    "autocommit": True,
}

# -- 终端显示常量 -----------------------------------------
COL_WIDTHS = {  # 列名 → 显示宽度
    # student
    "学号": 14, "姓名": 8, "性别": 4, "电话": 13,
    "班级": 18, "院系": 12, "辅导员": 8, "辅导员电话": 13,
    "宿舍楼": 8, "宿舍号": 6, "入学日期": 10,
    # counselor
    "辅导员ID": 8, "邮箱": 26, "办公室": 12, "创建时间": 19,
    # class
    "班级ID": 6, "班级名称": 18, "年级": 6,
    # dormitory
    "宿舍ID": 6, "总床位": 6, "已入住": 6, "空余床位": 8, "状态": 6,
    "宿舍类型": 8, "楼栋名称": 8,
    # stats
    "学生人数": 8, "管理班级数": 10, "管理学生数": 10,
}


def get_conn():
    """获取数据库连接"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print(f"\n  [ERR] 数据库连接失败: {e}")
        print("  请确认 MySQL 服务已启动\n")
        sys.exit(1)


def clear():
    """清屏"""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    """打印标题栏"""
    print()
    bar = "=" * 56
    print(f"  +{bar}+")
    print(f"  |  {dpad(title, 52, 'center')}  |")
    print(f"  +{bar}+")


def print_table(rows, cols, title=None):
    """格式化打印表格"""
    if title:
        print(f"\n  -- {title} --")
    if not rows:
        print("  (无数据)")
        return

    # 用显示宽度计算列宽
    widths = {}
    for c in cols:
        max_data = max((dwidth(str(row.get(c, ""))) for row in rows), default=0)
        widths[c] = max(COL_WIDTHS.get(c, 8), dwidth(c), max_data)

    # 顶框
    def hline(ch="+"):
        return "  +" + ch.join("-" * widths[c] for c in cols) + "+"

    top = hline("+")
    sep = hline("+")
    bot = hline("+")

    print(top)
    # 表头
    header = "  |" + "|".join(dpad(c, widths[c], 'center') for c in cols) + "|"
    print(header)
    print(sep)
    # 数据行
    for row in rows:
        line = "  |" + "|".join(
            dpad(str(row.get(c, '')) if row.get(c) is not None else '(未分配)', widths[c], 'left') for c in cols
        ) + "|"
        print(line)
    print(bot)
    print(f"  共 {len(rows)} 条记录")


def input_field(label, default=None, validate=None, allow_empty=False):
    """交互式输入字段"""
    hint = f" [{default}]" if default else ""
    while True:
        val = input(f"  {label}{hint}: ").strip()
        if not val and default:
            val = default
        if not val and not allow_empty:
            print("    WARN: 不能为空")
            continue
        if validate and val:
            if not re.match(validate, val):
                print("    WARN: 格式不正确")
                continue
        return val


def confirm(prompt):
    """确认操作"""
    return input(f"  {prompt} (y/N): ").strip().lower() == "y"


# ===========================================================
#  学生管理
# ===========================================================

def student_list(conn):
    """查询所有学生（完整视图）"""
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM v_student_full")
    rows = cur.fetchall()
    cols = ["学号", "姓名", "性别", "电话", "班级", "院系", "辅导员", "宿舍楼", "宿舍号"]
    print_table(rows, cols, "学生完整信息")
    cur.close()


def student_search(conn):
    """搜索学生"""
    kw = input("  输入学号或姓名关键字: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM v_student_full WHERE 学号 LIKE %s OR 姓名 LIKE %s",
        (f"%{kw}%", f"%{kw}%"),
    )
    rows = cur.fetchall()
    cols = ["学号", "姓名", "性别", "电话", "班级", "院系", "辅导员", "宿舍楼", "宿舍号"]
    print_table(rows, cols, f"搜索结果: '{kw}'")
    cur.close()


def student_add(conn):
    """添加学生"""
    print("\n  -- 添加学生 --")
    cur = conn.cursor(dictionary=True)

    # Step 1: 选班级（自动带出辅导员）
    print("\n  [1/5] 选择班级:")
    cur.execute("""
        SELECT c.class_id, c.class_name, c.department, c.grade,
               co.counselor_id, co.counselor_name
        FROM class c JOIN counselor co ON c.counselor_id = co.counselor_id
        ORDER BY c.class_id
    """)
    classes = cur.fetchall()
    print_table(classes, ["class_id", "class_name", "department", "grade", "counselor_id", "counselor_name"], "可选班级")
    class_id = input_field("班级ID", validate=r"^\d+$")
    selected = next((c for c in classes if str(c["class_id"]) == class_id), None)
    if selected:
        print(f"     -> {selected['class_name']} ({selected['department']}), 辅导员: {selected['counselor_name']}")
        counselor_id = str(selected["counselor_id"])
        print(f"     -> 辅导员ID 自动填入: {counselor_id}")
    else:
        # 手动指定辅导员
        print("\n  [2/5] 选择辅导员:")
        cur.execute("SELECT counselor_id, counselor_name, phone FROM counselor ORDER BY counselor_id")
        counselors = cur.fetchall()
        print_table(counselors, ["counselor_id", "counselor_name", "phone"], "可选辅导员")
        counselor_id = input_field("辅导员ID", validate=r"^\d+$")

    # Step 2: 基本信息
    print("\n  [3/5] 学生基本信息:")
    sid = input_field("学号", validate=r"^\d{8,12}$")
    name = input_field("姓名")
    gender = input_field("性别 (男/女)", validate=r"^[男女]$")
    phone = input_field("电话", validate=r"^\d{11}$", allow_empty=True)
    enroll = input_field("入学日期 (YYYY-MM-DD)", default="2024-09-01")

    # Step 3: 分配宿舍（可选）
    print("\n  [4/5] 分配宿舍 (可跳过):")
    cur.execute("""
        SELECT d.dorm_id, d.building_name AS 宿舍楼, d.dorm_no AS 宿舍号,
               d.bed_count AS 总床位, d.occupied AS 已入住,
               (d.bed_count - d.occupied) AS 空余床位
        FROM dormitory d
        WHERE d.occupied < d.bed_count
        ORDER BY d.building_name, d.dorm_no
    """)
    available_dorms = cur.fetchall()
    if available_dorms:
        print_table(available_dorms, ["dorm_id", "宿舍楼", "宿舍号", "总床位", "已入住", "空余床位"], "有空位的宿舍")
    else:
        print("  (暂无可分配宿舍)")
    dorm_id = input_field("宿舍ID (留空跳过)", allow_empty=True)

    # Step 4: 确认
    print(f"\n  [5/5] 确认信息:")
    print(f"    学号: {sid}  姓名: {name}  性别: {gender}")
    print(f"    班级ID: {class_id}  辅导员ID: {counselor_id}")
    print(f"    宿舍ID: {dorm_id or '(未分配)'}  入学: {enroll}")
    if not confirm("  确认添加?"):
        print("  已取消"); cur.close(); return

    try:
        cur.execute(
            """INSERT INTO student (student_id, student_name, gender, phone,
               class_id, counselor_id, dorm_id, enrollment_date)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (sid, name, gender, phone or None, int(class_id),
             int(counselor_id), int(dorm_id) if dorm_id else None, enroll),
        )
        print(f"  [OK] 学生 '{name}' 添加成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 添加失败: {e}")
    cur.close()


def student_edit(conn):
    """修改学生"""
    sid = input("  输入要修改的学号: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM v_student_full WHERE 学号 = %s", (sid,))
    row = cur.fetchone()
    if not row:
        print(f"  [ERR] 学号 '{sid}' 不存在")
        cur.close(); return
    print_table([row], ["学号", "姓名", "性别", "电话", "班级", "院系", "辅导员", "宿舍楼", "宿舍号"])

    print("\n  输入新值 (留空=不变):")
    name = input("  姓名: ").strip()
    gender = input("  性别 (男/女): ").strip()
    phone = input("  电话: ").strip()
    dorm_id = input("  宿舍ID (输入0=清空): ").strip()

    updates = []
    params = []
    if name: updates.append("student_name=%s"); params.append(name)
    if gender: updates.append("gender=%s"); params.append(gender)
    if phone: updates.append("phone=%s"); params.append(phone)
    if dorm_id == "0": updates.append("dorm_id=NULL")
    elif dorm_id: updates.append("dorm_id=%s"); params.append(int(dorm_id))

    if not updates:
        print("  未做任何修改"); cur.close(); return

    params.append(sid)
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE student SET {','.join(updates)} WHERE student_id=%s", params)
        print(f"  [OK] 学号 '{sid}' 更新成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 更新失败: {e}")
    cur.close()


def student_delete(conn):
    """删除学生"""
    sid = input("  输入要删除的学号: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT 学号, 姓名 FROM v_student_full WHERE 学号 = %s", (sid,))
    row = cur.fetchone()
    if not row:
        print(f"  [ERR] 学号 '{sid}' 不存在"); cur.close(); return
    print(f"\n  将删除: {row['学号']} {row['姓名']}")
    if not confirm("  确认删除?"):
        print("  已取消"); cur.close(); return
    try:
        cur.execute("DELETE FROM student WHERE student_id=%s", (sid,))
        print(f"  [OK] 学号 '{sid}' 已删除")
    except mysql.connector.Error as e:
        print(f"  [ERR] 删除失败: {e}")
    cur.close()


def student_menu(conn):
    """学生管理菜单"""
    while True:
        clear()
        print_header("学生管理")
        print("  [1] 查看所有学生")
        print("  [2] 搜索学生")
        print("  [3] 添加学生")
        print("  [4] 修改学生")
        print("  [5] 删除学生")
        print("  [0] 返回主菜单")
        choice = input("\n  请选择: ").strip()
        if choice == "1": student_list(conn)
        elif choice == "2": student_search(conn)
        elif choice == "3": student_add(conn)
        elif choice == "4": student_edit(conn)
        elif choice == "5": student_delete(conn)
        elif choice == "0": break
        if choice != "0": input("\n  按回车继续...")


# ===========================================================
#  宿舍管理
# ===========================================================

def dorm_list(conn):
    """查看所有宿舍"""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT d.dorm_id, d.building_name AS 宿舍楼, d.dorm_no AS 宿舍号,
               d.bed_count AS 总床位, d.occupied AS 已入住,
               (d.bed_count - d.occupied) AS 空余床位,
               CASE WHEN d.occupied >= d.bed_count THEN '已满' ELSE '有空位' END AS 状态
        FROM dormitory d ORDER BY d.building_name, d.dorm_no
    """)
    rows = cur.fetchall()
    print_table(rows, ["dorm_id", "宿舍楼", "宿舍号", "总床位", "已入住", "空余床位", "状态"], "宿舍入住情况")
    cur.close()


def dorm_add(conn):
    """添加宿舍"""
    print("\n  -- 添加宿舍 --")
    dno = input_field("宿舍号 (如101)")
    bld = input_field("楼栋名称 (如学一楼)")
    floor = input_field("楼层", validate=r"^\d+$")
    beds = input_field("床位总数", default="4", validate=r"^\d+$")
    dtype = input_field("宿舍类型 (男/女)", validate=r"^[男女]$")
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO dormitory (dorm_no, building_name, floor, bed_count, dorm_type) VALUES (%s,%s,%s,%s,%s)",
            (dno, bld, int(floor), int(beds), dtype),
        )
        print(f"  [OK] 宿舍 '{bld} {dno}' 添加成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 添加失败: {e}")
    cur.close()


def dorm_edit(conn):
    """修改宿舍"""
    did = input("  输入宿舍ID: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT dorm_id, building_name, dorm_no, floor, bed_count, dorm_type "
        "FROM dormitory WHERE dorm_id = %s", (did,)
    )
    row = cur.fetchone()
    if not row:
        print(f"  [ERR] 宿舍ID '{did}' 不存在"); cur.close(); return
    print_table([row], ["dorm_id", "building_name", "dorm_no", "floor", "bed_count", "dorm_type"])

    dno = input("  宿舍号 (留空=不变): ").strip()
    bld = input("  楼栋名称 (留空=不变): ").strip()
    floor = input("  楼层 (留空=不变): ").strip()
    beds = input("  床位总数 (留空=不变): ").strip()
    dtype = input("  宿舍类型 男/女 (留空=不变): ").strip()

    updates, params = [], []
    if dno: updates.append("dorm_no=%s"); params.append(dno)
    if bld: updates.append("building_name=%s"); params.append(bld)
    if floor: updates.append("floor=%s"); params.append(int(floor))
    if beds: updates.append("bed_count=%s"); params.append(int(beds))
    if dtype: updates.append("dorm_type=%s"); params.append(dtype)

    if not updates: print("  未做任何修改"); cur.close(); return
    params.append(int(did))
    try:
        cur.execute(f"UPDATE dormitory SET {','.join(updates)} WHERE dorm_id=%s", params)
        print(f"  [OK] 宿舍ID '{did}' 更新成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 更新失败: {e}")
    cur.close()


def dorm_delete(conn):
    """删除宿舍"""
    did = input("  输入宿舍ID: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT dorm_id, building_name, dorm_no FROM dormitory WHERE dorm_id=%s", (did,))
    row = cur.fetchone()
    if not row: print(f"  [ERR] 不存在"); cur.close(); return
    print(f"\n  将删除: {row['building_name']} {row['dorm_no']}")
    if not confirm("  确认删除?"): print("  已取消"); cur.close(); return
    try:
        cur.execute("DELETE FROM dormitory WHERE dorm_id=%s", (did,))
        print(f"  [OK] 已删除")
    except mysql.connector.Error as e:
        print(f"  [ERR] 删除失败: {e}")
    cur.close()


def dorm_menu(conn):
    """宿舍管理菜单"""
    while True:
        clear()
        print_header("宿舍管理")
        print("  [1] 查看宿舍入住情况")
        print("  [2] 添加宿舍")
        print("  [3] 修改宿舍")
        print("  [4] 删除宿舍")
        print("  [0] 返回主菜单")
        choice = input("\n  请选择: ").strip()
        if choice == "1": dorm_list(conn)
        elif choice == "2": dorm_add(conn)
        elif choice == "3": dorm_edit(conn)
        elif choice == "4": dorm_delete(conn)
        elif choice == "0": break
        if choice != "0": input("\n  按回车继续...")


# ===========================================================
#  班级管理
# ===========================================================

def class_list(conn):
    """查看班级统计"""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT c.class_id, c.class_name AS 班级, c.department AS 院系,
               co.counselor_name AS 辅导员, COUNT(s.student_id) AS 学生人数
        FROM class c
        JOIN counselor co ON c.counselor_id = co.counselor_id
        LEFT JOIN student s ON c.class_id = s.class_id
        GROUP BY c.class_id, c.class_name, c.department, co.counselor_name
        ORDER BY c.class_id
    """)
    rows = cur.fetchall()
    print_table(rows, ["class_id", "班级", "院系", "辅导员", "学生人数"], "班级统计")
    cur.close()


def class_add(conn):
    """添加班级"""
    print("\n  -- 添加班级 --")
    name = input_field("班级名称")
    dept = input_field("所属院系")
    grade = input_field("年级", default="2024", validate=r"^\d{4}$")
    # 显示辅导员列表
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT counselor_id, counselor_name, phone FROM counselor")
    counselors = cur.fetchall()
    print_table(counselors, ["counselor_id", "counselor_name", "phone"], "可选辅导员")
    cid = input_field("辅导员ID", validate=r"^\d+$")
    try:
        cur.execute(
            "INSERT INTO class (class_name, department, grade, counselor_id) VALUES (%s,%s,%s,%s)",
            (name, dept, grade, int(cid)),
        )
        print(f"  [OK] 班级 '{name}' 添加成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 添加失败: {e}")
    cur.close()


def class_edit(conn):
    """修改班级"""
    cid = input("  输入班级ID: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM class WHERE class_id=%s", (cid,))
    row = cur.fetchone()
    if not row: print(f"  [ERR] 不存在"); cur.close(); return
    print_table([row], ["class_id", "class_name", "department", "grade", "counselor_id"])

    name = input("  班级名称 (留空=不变): ").strip()
    dept = input("  院系 (留空=不变): ").strip()
    grade = input("  年级 (留空=不变): ").strip()
    counselor_id = input("  辅导员ID (留空=不变): ").strip()

    updates, params = [], []
    if name: updates.append("class_name=%s"); params.append(name)
    if dept: updates.append("department=%s"); params.append(dept)
    if grade: updates.append("grade=%s"); params.append(grade)
    if counselor_id: updates.append("counselor_id=%s"); params.append(int(counselor_id))

    if not updates: print("  未修改"); cur.close(); return
    params.append(int(cid))
    try:
        cur.execute(f"UPDATE class SET {','.join(updates)} WHERE class_id=%s", params)
        print(f"  [OK] 班级更新成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 更新失败: {e}")
    cur.close()


def class_delete(conn):
    """删除班级"""
    cid = input("  输入班级ID: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM class WHERE class_id=%s", (cid,))
    row = cur.fetchone()
    if not row: print(f"  [ERR] 不存在"); cur.close(); return
    print(f"\n  将删除: {row['class_name']}")
    if not confirm("  确认删除?"): print("  已取消"); cur.close(); return
    try:
        cur.execute("DELETE FROM class WHERE class_id=%s", (cid,))
        print(f"  [OK] 已删除")
    except mysql.connector.Error as e:
        print(f"  [ERR] 删除失败: {e}")
    cur.close()


def class_menu(conn):
    """班级管理菜单"""
    while True:
        clear()
        print_header("班级管理")
        print("  [1] 查看班级统计")
        print("  [2] 添加班级")
        print("  [3] 修改班级")
        print("  [4] 删除班级")
        print("  [0] 返回主菜单")
        choice = input("\n  请选择: ").strip()
        if choice == "1": class_list(conn)
        elif choice == "2": class_add(conn)
        elif choice == "3": class_edit(conn)
        elif choice == "4": class_delete(conn)
        elif choice == "0": break
        if choice != "0": input("\n  按回车继续...")


# ===========================================================
#  辅导员管理
# ===========================================================

def counselor_list(conn):
    """查看辅导员"""
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT co.counselor_id, co.counselor_name AS 辅导员, co.phone AS 电话,
               COUNT(DISTINCT c.class_id) AS 管理班级数,
               COUNT(DISTINCT s.student_id) AS 管理学生数
        FROM counselor co
        LEFT JOIN class c ON co.counselor_id = c.counselor_id
        LEFT JOIN student s ON co.counselor_id = s.counselor_id
        GROUP BY co.counselor_id, co.counselor_name, co.phone
        ORDER BY co.counselor_id
    """)
    rows = cur.fetchall()
    print_table(rows, ["counselor_id", "辅导员", "电话", "管理班级数", "管理学生数"], "辅导员带班统计")
    cur.close()


def counselor_add(conn):
    """添加辅导员"""
    print("\n  -- 添加辅导员 --")
    name = input_field("姓名")
    gender = input_field("性别 (男/女)", validate=r"^[男女]$")
    phone = input_field("电话", validate=r"^\d{11}$", allow_empty=True)
    email = input_field("邮箱", allow_empty=True)
    office = input_field("办公室", allow_empty=True)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO counselor (counselor_name, gender, phone, email, office) VALUES (%s,%s,%s,%s,%s)",
            (name, gender, phone or None, email or None, office or None),
        )
        print(f"  [OK] 辅导员 '{name}' 添加成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 添加失败: {e}")
    cur.close()


def counselor_edit(conn):
    """修改辅导员"""
    cid = input("  输入辅导员ID: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM counselor WHERE counselor_id=%s", (cid,))
    row = cur.fetchone()
    if not row: print(f"  [ERR] 不存在"); cur.close(); return
    print_table([row], ["counselor_id", "counselor_name", "gender", "phone", "email", "office"])

    name = input_field("姓名", allow_empty=True)
    gender = input_field("性别 男/女 (留空=不变)", allow_empty=True)
    phone = input_field("电话 (留空=不变)", allow_empty=True)
    email = input_field("邮箱 (留空=不变)", allow_empty=True)
    office = input_field("办公室 (留空=不变)", allow_empty=True)

    field_map = {
        "counselor_name": name, "gender": gender,
        "phone": phone, "email": email, "office": office,
    }
    updates = [(k, v) for k, v in field_map.items() if v]
    if not updates: print("  未修改"); cur.close(); return

    sets = ", ".join(f"{k}=%s" for k, _ in updates)
    params = [v for _, v in updates] + [int(cid)]
    try:
        cur.execute(f"UPDATE counselor SET {sets} WHERE counselor_id=%s", params)
        print(f"  [OK] 更新成功")
    except mysql.connector.Error as e:
        print(f"  [ERR] 更新失败: {e}")
    cur.close()


def counselor_delete(conn):
    """删除辅导员"""
    cid = input("  输入辅导员ID: ").strip()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM counselor WHERE counselor_id=%s", (cid,))
    row = cur.fetchone()
    if not row: print(f"  [ERR] 不存在"); cur.close(); return
    print(f"\n  将删除: {row['counselor_name']}")
    if not confirm("  确认删除?"): print("  已取消"); cur.close(); return
    try:
        cur.execute("DELETE FROM counselor WHERE counselor_id=%s", (cid,))
        print(f"  [OK] 已删除")
    except mysql.connector.Error as e:
        print(f"  [ERR] 删除失败 (可能有班级引用此辅导员): {e}")
    cur.close()


def counselor_menu(conn):
    """辅导员管理菜单"""
    while True:
        clear()
        print_header("辅导员管理")
        print("  [1] 查看辅导员统计")
        print("  [2] 添加辅导员")
        print("  [3] 修改辅导员")
        print("  [4] 删除辅导员")
        print("  [0] 返回主菜单")
        choice = input("\n  请选择: ").strip()
        if choice == "1": counselor_list(conn)
        elif choice == "2": counselor_add(conn)
        elif choice == "3": counselor_edit(conn)
        elif choice == "4": counselor_delete(conn)
        elif choice == "0": break
        if choice != "0": input("\n  按回车继续...")


# ===========================================================
#  数据概览
# ===========================================================

def overview(conn):
    """数据概览仪表盘"""
    clear()
    print_header("数据概览")
    cur = conn.cursor(dictionary=True)

    # 各表记录数
    tables = ["student", "dormitory", "class", "counselor"]
    counts = {}
    for t in tables:
        cur.execute(f"SELECT COUNT(*) AS cnt FROM {t}")
        counts[t] = cur.fetchone()["cnt"]

    print(f"""
  +------------------------------------------+
  |  学生总数: {counts['student']:<5}   宿舍总数: {counts['dormitory']:<5}  |
  |  班级总数: {counts['class']:<5}   辅导员数: {counts['counselor']:<5}  |
  +------------------------------------------+
""")

    # 宿舍入住
    cur.execute("SELECT * FROM v_dorm_occupancy")
    print_table(cur.fetchall(), ["宿舍楼", "宿舍号", "总床位", "已入住", "空余床位", "状态"], "宿舍入住详情")

    # 班级统计
    cur.execute("SELECT * FROM v_class_stats")
    print_table(cur.fetchall(), ["班级", "院系", "辅导员", "学生人数"], "班级统计")

    cur.close()


# ===========================================================
#  主菜单
# ===========================================================

def main_menu(conn):
    """主菜单循环"""
    while True:
        clear()
        print_header("宿舍信息管理系统")
        print("  [1]  学生管理      (查看/搜索/增删改)")
        print("  [2]  宿舍管理      (入住情况/增删改)")
        print("  [3]  班级管理      (统计/增删改)")
        print("  [4]  辅导员管理   (统计/增删改)")
        print("  [5]  数据概览      (仪表盘)")
        print("  [0]  退出系统")
        choice = input("\n  请选择: ").strip()

        if choice == "1": student_menu(conn)
        elif choice == "2": dorm_menu(conn)
        elif choice == "3": class_menu(conn)
        elif choice == "4": counselor_menu(conn)
        elif choice == "5": overview(conn); input("\n  按回车返回...")
        elif choice == "0":
            print("\n  再见！\n")
            break


def main():
    """入口"""
    clear()
    print_header("宿舍信息管理系统")
    print("  正在连接数据库...")

    conn = get_conn()
    print("  [OK] 数据库连接成功")
    print(f"  [OK] 数据库: {DB_CONFIG['database']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}")
    input("\n  按回车进入系统...")

    try:
        main_menu(conn)
    except KeyboardInterrupt:
        print("\n\n  再见！\n")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
