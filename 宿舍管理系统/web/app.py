# -*- coding: utf-8 -*-
"""宿舍信息管理系统 - Web 前端（Flask 后端）"""

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import SECRET_KEY
from db import query, query_one, execute

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ═══════════════════════════════════════════════
#  首页 - 仪表盘
# ═══════════════════════════════════════════════
@app.route("/")
def index():
    stats = {
        "students":   query_one("SELECT COUNT(*) AS n FROM student")["n"],
        "dorms":      query_one("SELECT COUNT(*) AS n FROM dormitory")["n"],
        "classes":    query_one("SELECT COUNT(*) AS n FROM class")["n"],
        "counselors": query_one("SELECT COUNT(*) AS n FROM counselor")["n"],
    }
    dorm_occ = query("SELECT * FROM v_dorm_occupancy")
    class_stats = query("SELECT * FROM v_class_stats")
    return render_template("index.html",
                           stats=stats,
                           dorms=dorm_occ,
                           classes=class_stats)


# ═══════════════════════════════════════════════
#  学生管理 CRUD
# ═══════════════════════════════════════════════
@app.route("/student")
def student_list():
    q = request.args.get("q", "").strip()
    if q:
        rows = query(
            "SELECT * FROM v_student_full "
            "WHERE 学号 LIKE %s OR 姓名 LIKE %s OR 班级 LIKE %s "
            "ORDER BY 学号",
            (f"%{q}%", f"%{q}%", f"%{q}%")
        )
    else:
        rows = query("SELECT * FROM v_student_full ORDER BY 学号")
    return render_template("student/list.html", students=rows, query=q)


@app.route("/student/add", methods=["GET", "POST"])
def student_add():
    if request.method == "GET":
        classes = query(
            "SELECT c.class_id, c.class_name, c.department, c.grade, "
            "co.counselor_id, co.counselor_name "
            "FROM class c JOIN counselor co ON c.counselor_id = co.counselor_id "
            "ORDER BY c.class_id"
        )
        dorms = query(
            "SELECT dorm_id, building_name, dorm_no, bed_count, occupied, "
            "(bed_count - occupied) AS available "
            "FROM dormitory WHERE occupied < bed_count "
            "ORDER BY building_name, dorm_no"
        )
        counselors = query("SELECT counselor_id, counselor_name FROM counselor ORDER BY counselor_id")
        return render_template("student/form.html",
                               student=None, classes=classes,
                               dorms=dorms, counselors=counselors)

    # POST: 处理添加
    try:
        execute(
            "INSERT INTO student (student_id, student_name, gender, phone, "
            "class_id, counselor_id, dorm_id, enrollment_date) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (request.form["student_id"].strip(),
             request.form["student_name"].strip(),
             request.form["gender"],
             request.form.get("phone", "").strip() or None,
             int(request.form["class_id"]),
             int(request.form["counselor_id"]),
             int(request.form["dorm_id"]) if request.form.get("dorm_id") else None,
             request.form.get("enrollment_date", "").strip() or None)
        )
        flash("[成功] 学生添加成功！", "success")
        return redirect("/student")
    except mysql.connector.Error as e:
        flash(f"[错误] 添加失败: {e}", "error")
        return redirect("/student/add")


@app.route("/student/<student_id>/edit", methods=["GET", "POST"])
def student_edit(student_id):
    if request.method == "GET":
        student = query_one(
            "SELECT * FROM student WHERE student_id = %s", (student_id,))
        if not student:
            flash("[错误] 学生不存在", "error")
            return redirect("/student")
        classes = query(
            "SELECT c.class_id, c.class_name, c.department, c.grade, "
            "co.counselor_id, co.counselor_name "
            "FROM class c JOIN counselor co ON c.counselor_id = co.counselor_id "
            "ORDER BY c.class_id"
        )
        dorms = query(
            "SELECT dorm_id, building_name, dorm_no, bed_count, occupied, "
            "(bed_count - occupied) AS available "
            "FROM dormitory "
            "ORDER BY building_name, dorm_no"
        )
        counselors = query(
            "SELECT counselor_id, counselor_name FROM counselor ORDER BY counselor_id"
        )
        return render_template("student/form.html",
                               student=student, classes=classes,
                               dorms=dorms, counselors=counselors)

    # POST: 处理编辑
    try:
        new_dorm = int(request.form["dorm_id"]) if request.form.get("dorm_id") else None
        execute(
            "UPDATE student SET student_name=%s, gender=%s, phone=%s, "
            "class_id=%s, counselor_id=%s, dorm_id=%s, enrollment_date=%s "
            "WHERE student_id=%s",
            (request.form["student_name"].strip(),
             request.form["gender"],
             request.form.get("phone", "").strip() or None,
             int(request.form["class_id"]),
             int(request.form["counselor_id"]),
             new_dorm,
             request.form.get("enrollment_date", "").strip() or None,
             student_id)
        )
        flash("[成功] 学生信息更新成功！", "success")
        return redirect("/student")
    except mysql.connector.Error as e:
        flash(f"[错误] 更新失败: {e}", "error")
        return redirect(f"/student/{student_id}/edit")


@app.route("/student/<student_id>/delete", methods=["POST"])
def student_delete(student_id):
    try:
        execute("DELETE FROM student WHERE student_id = %s", (student_id,))
        flash("[成功] 学生已删除", "success")
    except mysql.connector.Error as e:
        flash(f"[错误] 删除失败: {e}", "error")
    return redirect("/student")


# ═══════════════════════════════════════════════
#  宿舍管理 CRUD
# ═══════════════════════════════════════════════
@app.route("/dormitory")
def dorm_list():
    rows = query(
        "SELECT dorm_id, building_name, dorm_no, floor, bed_count, occupied, "
        "dorm_type, (bed_count - occupied) AS available, "
        "CASE WHEN occupied >= bed_count THEN '已满' ELSE '有空位' END AS status "
        "FROM dormitory ORDER BY building_name, dorm_no"
    )
    return render_template("dormitory/list.html", dorms=rows)


@app.route("/dormitory/add", methods=["GET", "POST"])
def dorm_add():
    if request.method == "GET":
        return render_template("dormitory/form.html", dorm=None)

    try:
        execute(
            "INSERT INTO dormitory (building_name, dorm_no, floor, bed_count, dorm_type) "
            "VALUES (%s,%s,%s,%s,%s)",
            (request.form["building_name"].strip(),
             request.form["dorm_no"].strip(),
             int(request.form["floor"]),
             int(request.form["bed_count"]),
             request.form["dorm_type"])
        )
        flash("[成功] 宿舍添加成功！", "success")
        return redirect("/dormitory")
    except mysql.connector.Error as e:
        flash(f"[错误] 添加失败: {e}", "error")
        return redirect("/dormitory/add")


@app.route("/dormitory/<int:dorm_id>/edit", methods=["GET", "POST"])
def dorm_edit(dorm_id):
    if request.method == "GET":
        dorm = query_one("SELECT * FROM dormitory WHERE dorm_id = %s", (dorm_id,))
        if not dorm:
            flash("[错误] 宿舍不存在", "error")
            return redirect("/dormitory")
        return render_template("dormitory/form.html", dorm=dorm)

    try:
        execute(
            "UPDATE dormitory SET building_name=%s, dorm_no=%s, floor=%s, "
            "bed_count=%s, dorm_type=%s WHERE dorm_id=%s",
            (request.form["building_name"].strip(),
             request.form["dorm_no"].strip(),
             int(request.form["floor"]),
             int(request.form["bed_count"]),
             request.form["dorm_type"],
             dorm_id)
        )
        flash("[成功] 宿舍信息更新成功！", "success")
        return redirect("/dormitory")
    except mysql.connector.Error as e:
        flash(f"[错误] 更新失败: {e}", "error")
        return redirect(f"/dormitory/{dorm_id}/edit")


@app.route("/dormitory/<int:dorm_id>/delete", methods=["POST"])
def dorm_delete(dorm_id):
    try:
        execute("DELETE FROM dormitory WHERE dorm_id = %s", (dorm_id,))
        flash("[成功] 宿舍已删除", "success")
    except mysql.connector.Error as e:
        flash(f"[错误] 删除失败: {e}", "error")
    return redirect("/dormitory")


# ═══════════════════════════════════════════════
#  班级管理 CRUD
# ═══════════════════════════════════════════════
@app.route("/class")
def class_list():
    rows = query(
        "SELECT c.class_id AS 班级ID, c.class_name AS 班级名称, "
        "c.department AS 所属院系, c.grade AS 年级, "
        "co.counselor_name AS 辅导员, "
        "COUNT(s.student_id) AS 学生人数 "
        "FROM class c "
        "JOIN counselor co ON c.counselor_id = co.counselor_id "
        "LEFT JOIN student s ON c.class_id = s.class_id "
        "GROUP BY c.class_id, c.class_name, c.department, c.grade, co.counselor_name "
        "ORDER BY c.class_id"
    )
    return render_template("class/list.html", classes=rows)


@app.route("/class/add", methods=["GET", "POST"])
def class_add():
    counselors = query("SELECT counselor_id, counselor_name FROM counselor ORDER BY counselor_id")
    if request.method == "GET":
        return render_template("class/form.html", cls=None, counselors=counselors)

    try:
        execute(
            "INSERT INTO class (class_name, department, grade, counselor_id) "
            "VALUES (%s,%s,%s,%s)",
            (request.form["class_name"].strip(),
             request.form["department"].strip(),
             request.form.get("grade", "").strip() or None,
             int(request.form["counselor_id"]))
        )
        flash("[成功] 班级添加成功！", "success")
        return redirect("/class")
    except mysql.connector.Error as e:
        flash(f"[错误] 添加失败: {e}", "error")
        return redirect("/class/add")


@app.route("/class/<int:class_id>/edit", methods=["GET", "POST"])
def class_edit(class_id):
    counselors = query("SELECT counselor_id, counselor_name FROM counselor ORDER BY counselor_id")
    if request.method == "GET":
        cls = query_one("SELECT * FROM class WHERE class_id = %s", (class_id,))
        if not cls:
            flash("[错误] 班级不存在", "error")
            return redirect("/class")
        return render_template("class/form.html", cls=cls, counselors=counselors)

    try:
        execute(
            "UPDATE class SET class_name=%s, department=%s, grade=%s, "
            "counselor_id=%s WHERE class_id=%s",
            (request.form["class_name"].strip(),
             request.form["department"].strip(),
             request.form.get("grade", "").strip() or None,
             int(request.form["counselor_id"]),
             class_id)
        )
        flash("[成功] 班级信息更新成功！", "success")
        return redirect("/class")
    except mysql.connector.Error as e:
        flash(f"[错误] 更新失败: {e}", "error")
        return redirect(f"/class/{class_id}/edit")


@app.route("/class/<int:class_id>/delete", methods=["POST"])
def class_delete(class_id):
    try:
        execute("DELETE FROM class WHERE class_id = %s", (class_id,))
        flash("[成功] 班级已删除", "success")
    except mysql.connector.Error as e:
        flash(f"[错误] 删除失败（可能该班级下仍有学生）: {e}", "error")
    return redirect("/class")


# ═══════════════════════════════════════════════
#  辅导员管理 CRUD
# ═══════════════════════════════════════════════
@app.route("/counselor")
def counselor_list():
    rows = query(
        "SELECT co.counselor_id AS 辅导员ID, co.counselor_name AS 姓名, "
        "co.gender AS 性别, co.phone AS 电话, co.email AS 邮箱, "
        "co.office AS 办公室, "
        "COUNT(DISTINCT c.class_id) AS 管理班级数, "
        "COUNT(DISTINCT s.student_id) AS 管理学生数 "
        "FROM counselor co "
        "LEFT JOIN class c ON co.counselor_id = c.counselor_id "
        "LEFT JOIN student s ON co.counselor_id = s.counselor_id "
        "GROUP BY co.counselor_id, co.counselor_name, co.gender, "
        "co.phone, co.email, co.office "
        "ORDER BY co.counselor_id"
    )
    return render_template("counselor/list.html", counselors=rows)


@app.route("/counselor/add", methods=["GET", "POST"])
def counselor_add():
    if request.method == "GET":
        return render_template("counselor/form.html", counselor=None)

    try:
        execute(
            "INSERT INTO counselor (counselor_name, gender, phone, email, office) "
            "VALUES (%s,%s,%s,%s,%s)",
            (request.form["counselor_name"].strip(),
             request.form["gender"],
             request.form.get("phone", "").strip() or None,
             request.form.get("email", "").strip() or None,
             request.form.get("office", "").strip() or None)
        )
        flash("[成功] 辅导员添加成功！", "success")
        return redirect("/counselor")
    except mysql.connector.Error as e:
        flash(f"[错误] 添加失败: {e}", "error")
        return redirect("/counselor/add")


@app.route("/counselor/<int:counselor_id>/edit", methods=["GET", "POST"])
def counselor_edit(counselor_id):
    if request.method == "GET":
        c = query_one(
            "SELECT * FROM counselor WHERE counselor_id = %s", (counselor_id,))
        if not c:
            flash("[错误] 辅导员不存在", "error")
            return redirect("/counselor")
        return render_template("counselor/form.html", counselor=c)

    try:
        execute(
            "UPDATE counselor SET counselor_name=%s, gender=%s, phone=%s, "
            "email=%s, office=%s WHERE counselor_id=%s",
            (request.form["counselor_name"].strip(),
             request.form["gender"],
             request.form.get("phone", "").strip() or None,
             request.form.get("email", "").strip() or None,
             request.form.get("office", "").strip() or None,
             counselor_id)
        )
        flash("[成功] 辅导员信息更新成功！", "success")
        return redirect("/counselor")
    except mysql.connector.Error as e:
        flash(f"[错误] 更新失败: {e}", "error")
        return redirect(f"/counselor/{counselor_id}/edit")


@app.route("/counselor/<int:counselor_id>/delete", methods=["POST"])
def counselor_delete(counselor_id):
    try:
        execute("DELETE FROM counselor WHERE counselor_id = %s", (counselor_id,))
        flash("[成功] 辅导员已删除", "success")
    except mysql.connector.Error as e:
        flash(f"[错误] 删除失败（可能该辅导员仍管理班级）: {e}", "error")
    return redirect("/counselor")


# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  宿舍信息管理系统 Web 前端")
    print("  http://localhost:5000")
    print("=" * 50)
    print()
    app.run(debug=True, host="127.0.0.1", port=5000)
