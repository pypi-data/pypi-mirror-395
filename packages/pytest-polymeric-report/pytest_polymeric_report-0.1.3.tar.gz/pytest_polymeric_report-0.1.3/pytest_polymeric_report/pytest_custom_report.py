# -*- coding: utf-8 -*-
import datetime
import os
import time
import pytest
from jinja2 import Environment, FileSystemLoader

# 全局变量：新增skipped字段统计跳过用例
test_result = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": 0,  # 仅统计执行错误（如setup/teardown失败）
    "skipped": 0,  # 新增：专门统计主动跳过的用例
    "generated_time": "",
    "cases": []
}


def pytest_make_parametrize_id(config, val, argname):
    """为参数化用例生成可读ID"""
    if isinstance(val, dict):
        return val.get('title') or val.get('desc')


def pytest_sessionstart(session):
    """初始化生成时间"""
    global test_result
    test_result["generated_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """收集用例基础信息"""
    outcome = yield
    report = outcome.get_result()

    # 合并额外信息
    fixture_extras = getattr(item.config, "extras", [])
    plugin_extras = getattr(report, "extra", [])
    report.extra = fixture_extras + plugin_extras

    report.file_path = item.location[0]  # 用例所在文件
    # 用例描述（优先参数化ID，其次docstring）
    if hasattr(item, 'callspec'):
        report.case_desc = item.callspec.id or (item._obj.__doc__ or "").strip()
    else:
        report.case_desc = (item._obj.__doc__ or "").strip()
    report.method_name = item.location[2].split('[')[0]  # 方法名
    report.full_id = item.nodeid  # 完整ID


def pytest_runtest_logreport(report):
    """统计用例状态，区分失败、错误、跳过"""
    global test_result
    if report.when == 'call' or report.outcome in ['skipped', 'failed']:
        # 基础case结构
        case = {
            "name": report.method_name,
            "classname": report.file_path,
            "time": f"{float(report.duration):.3f}",
            "status": report.outcome,  # 状态：passed/failed/skipped/error
            "description": report.case_desc,
            "message": "",
            "stack_trace": report.capstderr,
            "log": report.capstdout,
            "screenshot": [],
        }

        # 1. 处理执行失败（call阶段失败）
        if report.when == 'call' and report.outcome == 'failed':
            if hasattr(report, 'longrepr'):
                longrepr_str = str(report.longrepr) if report.longrepr else ""
                longrepr_str_pivotal = longrepr_str.split('\n')[-6:] if longrepr_str else "未知失败"
                longrepr_str_pivotal = "\n".join(longrepr_str_pivotal)
                case["message"] = longrepr_str_pivotal
                case["stack_trace"] = longrepr_str
            test_result["failed"] += 1

        # 2. 处理通过用例
        elif report.outcome == 'passed':
            test_result["passed"] += 1

        # 3. 处理主动跳过（@pytest.mark.skip）
        elif report.outcome == 'skipped':
            case["message"] = f"跳过原因：{str(report.longrepr).strip()}"
            test_result["skipped"] += 1  # 统计到新增的skipped字段

        # 4. 处理执行错误（如setup/teardown阶段失败）
        elif report.when in ['setup', 'teardown'] and report.outcome == 'failed':
            case["status"] = 'error'  # 标记为error状态
            if hasattr(report, 'longrepr'):
                # 修复：提前处理包含\n的字符串，避免f-string语法错误
                longrepr_str = str(report.longrepr) if report.longrepr else ""
                longrepr_str_pivotal = longrepr_str.split('\n')[-6:] if longrepr_str else "未知失败"
                longrepr_str_pivotal = "\n".join(longrepr_str_pivotal)
                case["message"] = longrepr_str_pivotal
                case["stack_trace"] = longrepr_str
            test_result["errors"] += 1

        # 提取用例截图
        for extra in report.extra:
            if isinstance(extra, dict) and (
                    extra.get("format") == "image" or extra.get("format_type") == "image") and extra.get("content"):
                case["screenshot"].append(f"data:{extra.get('mime_type')};base64," + extra.get("content"))
                break

        # 更新用例列表和总数
        test_result["cases"].append(case)
        test_result["total"] = len(test_result["cases"])


def pytest_sessionfinish(session):
    """生成报告（逻辑不变，确保模板接收新字段）"""
    report_output = session.config.getoption('--report')
    title = session.config.getoption('--title')
    desc = session.config.getoption('--desc')
    if not report_output:
        return
    test_result["title"] = title or ""
    test_result["desc"] = desc or ""

    # 处理报告文件名
    if not report_output.endswith('.html'):
        report_filename = f"{report_output}.html"
    else:
        report_filename = f"{report_output}"

    final_report_path = report_filename

    # 加载外部模板
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    try:
        template = env.get_template("test_report_template.html")
    except Exception as e:
        raise FileNotFoundError(f"模板未找到：{template_dir}，错误：{str(e)}")

    # 渲染并写入报告
    rendered_report = template.render(results=test_result)
    with open(final_report_path, "w", encoding="utf-8") as f:
        f.write(rendered_report)

    print(f"\n测试报告已生成：{final_report_path}")


def pytest_addoption(parser):
    group = parser.getgroup("custom_report", "自定义测试报告选项")
    group.addoption(
        "--report",
        action="store",
        metavar="报告名称",
        default=None,
        help="指定HTML报告名称"
    )
    group.addoption(
        "--title",
        action="store",
        metavar="报告标题",
        default="通用测试报告",
        help="自定义报告标题"
    )
    group.addoption(
        "--desc",
        action="store",
        metavar="报告描述",
        default="",
        help="自定义报告描述"
    )
