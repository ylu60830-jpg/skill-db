/* -*- coding: utf-8 -*- */
/* 宿舍信息管理系统 - 前端交互脚本 */

/* 删除确认 */
function confirmDelete(msg) {
    return confirm(msg || '确定要删除吗？此操作不可撤销。');
}

/* 表单提交前验证 */
document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('form[data-validate]');
    if (form) {
        form.addEventListener('submit', function(e) {
            var required = form.querySelectorAll('[required]');
            var ok = true;
            required.forEach(function(el) {
                if (!el.value.trim()) {
                    el.style.borderColor = '#e74c3c';
                    ok = false;
                } else {
                    el.style.borderColor = '#d5dce6';
                }
            });
            if (!ok) {
                e.preventDefault();
                alert('请填写所有必填字段。');
            }
        });
    }
});

/* 班级-辅导员联动：选择班级后自动填入辅导员 */
function setupClassCounselorLink(classSelectId, counselorSelectId) {
    var classSelect = document.getElementById(classSelectId);
    var counselorSelect = document.getElementById(counselorSelectId);
    if (!classSelect || !counselorSelect) return;

    classSelect.addEventListener('change', function() {
        var opt = classSelect.selectedOptions[0];
        if (opt && opt.dataset.counselorId) {
            counselorSelect.value = opt.dataset.counselorId;
        }
    });
}

/* 初始化联动 */
document.addEventListener('DOMContentLoaded', function() {
    setupClassCounselorLink('class_id', 'counselor_id');
});
