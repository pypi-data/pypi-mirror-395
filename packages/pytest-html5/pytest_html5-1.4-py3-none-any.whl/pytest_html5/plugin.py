import bisect
import datetime
import sys
from datetime import timedelta
import importlib
import json
import os
import re
import time
from base64 import b64decode, b64encode
from collections import defaultdict
from collections import OrderedDict
from functools import lru_cache
from html import escape
from os.path import isfile
import random
import pytest
from _pytest.logging import _remove_ansi_escape_sequences
from py.xml import html
from py.xml import raw
import pyecharts
from . import __pypi_url__
from . import extras
from lxml import etree
from itertools import zip_longest
import shutil
from PIL import ImageGrab

gen_html = True
@lru_cache()
def ansi_support():
    try:
        return importlib.import_module("ansi2html")
    except ImportError:
        pass


def pytest_addhooks(pluginmanager):
    from . import hooks

    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--html",
        action="store",
        dest="htmlpath",
        metavar="path",
        default=None,
        help="create html report file at given path.",
    )
    group.addoption(
        "--url",
        action="store",
        dest='page_url',
        metavar=None,
        default="No url given. Please configure by --url",
        help="test url of web page.",
    )
    group.addoption(
        "--name",
        action="store",
        dest='name',
        metavar=None,
        default='***',
        help="user name of your test system",
    )
    group.addoption(
        "--password",
        action="store",
        dest='password',
        metavar=None,
        default='***',
        help="user password of your test system",
    )
    group.addoption(
        "--browser",
        action="store",
        dest='browser',
        metavar=None,
        default='Chrome',
        help="browser of used",
    )
    group.addoption(
        "--css",
        action="append",
        metavar="path",
        default=[],
        help="append given css file content to report style file.",
    )
    parser.addini(
        "render_collapsed",
        type="bool",
        default=False,
        help="Open the report with all rows collapsed. Useful for very large reports",
    )
    parser.addini(
        "max_asset_filename_length",
        default=255,
        help="set the maximum filename length for assets "
             "attached to the html report.",
    )


def pytest_configure(config):
    htmlpath: str = config.getoption("htmlpath")
    if htmlpath:
        # 确认运行层级
        if run_in_level:
            if not os.path.exists(htmlpath):  # run_in_level=1
                htmlpath = htmlpath.replace('../', '', 1)
                if not os.path.exists(htmlpath):
                    print('路径错误，请检查：' + htmlpath)
        missing_css_files = []
        for csspath in config.getoption("css"):
            if not os.path.exists(csspath):
                missing_css_files.append(csspath)

        if missing_css_files:
            oserror = (
                f"Missing CSS file{'s' if len(missing_css_files) > 1 else ''}:"
                f" {', '.join(missing_css_files)}"
            )
            raise OSError(oserror)

        if not hasattr(config, "workerinput"):
            config._html = HTMLReport(htmlpath, config)
            config.pluginmanager.register(config._html)
    else:
        global gen_html
        gen_html = False


def pytest_unconfigure(config):
    html = getattr(config, "_html", None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if not gen_html:
        return
    pytest_html = item.config.pluginmanager.getplugin("html")
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            if file_name:
                screen_img = _screenshot_(item)
                html_ = (
                        '<div><img src="%s" alt="screenshot" style="width:465px;height:245px;" '
                        'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                )
                extra.append(pytest_html.extras.html(html_))
    doc = str(item.function.__doc__)
    if len(doc) > 180:
        doc = doc[:177] + '...'
    report.description = doc
    report.extra = extra


@pytest.fixture
def extra(pytestconfig):
    pytestconfig.extras = []
    yield pytestconfig.extras
    del pytestconfig.extras[:]


def data_uri(content, mime_type="text/plain", charset="utf-8"):
    data = b64encode(content.encode(charset)).decode("ascii")
    return f"data:{mime_type};charset={charset};base64,{data}"


def download_js(save_path):
    """下载好js，如果某些公司没有外网，那就自己手动配了
    现在源码里自带echarts。js
    """
    try:
        ori_js = os.path.join(os.path.dirname(__file__), "sttc", "echarts.min.js")
        shutil.copy(ori_js, save_path)
    except Exception:
        ...


__color__ = ['6cb1e1', 'ffb06a', '74d974', 'cb91ff', 'ff8ddc', 'ff8a8a', 'feff00', '17becf',
             '32cd99', '7093db', '8af38a', 'd4ed31']
# 两种运行方式：当前测试脚本里执行（用于调试运行）；在根目录执行（用于定时任务）
base_path = os.getcwd()  # 如果是根目录命令行运行
run_in_level = 2  # 默认是日常调试里的运行层级，二级
for case_type in ['test_case', 'test_cases', 'testcase', 'testcases']:  # 标准命名只有这几个
    if case_type in base_path:
        base_path = base_path[:base_path.rindex(case_type)]
        break
else:
    run_in_level = 0
sys.path.append(base_path)
output_dir = os.path.join(base_path, "output")
report_path = os.path.join(output_dir, 'report')
html_report_path = os.path.join(report_path, "report.html")
assets_path = os.path.join(report_path, "assets")
pfs_json = os.path.join(assets_path, "pfs.json")
e1_html_path = os.path.join(assets_path, "e1.html")
e2_html_path = os.path.join(assets_path, "e2.html")
report_path = report_path
screenshot_dir = os.path.join(report_path, "screenshots")
replaced_js_path = os.path.join(report_path, "assets", "echarts.min.js")
replace_js = replaced_js_path if os.path.exists(replaced_js_path) else None


class HTMLReport:
    def __init__(self, logfile, config):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.abspath(logfile)
        self.test_logs = []
        self.title = os.path.basename(self.logfile)
        self.results = []
        self.errors = self.failed = 0
        self.passed = self.skipped = 0
        self.xfailed = self.xpassed = 0
        has_rerun = config.pluginmanager.hasplugin("rerunfailures")
        self.rerun = 0 if has_rerun else None
        self.config = config
        self.reports = defaultdict(list)
        self.view = pyecharts
        self.__pfs_color__ = ['#74d974', '#fd5a3e', '#ffd050']

        for _ in [report_path, screenshot_dir, assets_path]:
            if not os.path.exists(_):
                os.makedirs(_)
        if not os.path.exists(replaced_js_path):
            download_js(replaced_js_path)

    class TestResult:
        __pfs_color__ = ['#74d974', '#fd5a3e', '#ffd050']
        cl = random.choice(__color__)

        def __init__(self, outcome, report, logfile, config):
            self.test_id = report.nodeid
            if getattr(report, "when", "call") != "call":
                self.test_id = "::".join([report.nodeid, report.when])
            self.time = getattr(report, "duration", 0.0)
            self.formatted_time = self._format_time(report)
            self.outcome = outcome
            self.additional_html = []
            self.links_html = []
            self.max_asset_filename_length = int(
                config.getini("max_asset_filename_length")
            )
            self.logfile = logfile
            self.config = config
            self.row_table = self.row_extra = None

            test_index = hasattr(report, "rerun") and report.rerun + 1 or 0

            for extra_index, extra in enumerate(getattr(report, "extra", [])):
                self.append_extra_html(extra, extra_index, test_index)

            self.append_log_html(
                report,
                self.additional_html,
                config.option.capture,
                config.option.showcapture,
            )

            cells = [
                html.td(self.outcome, class_="col-result"),
                html.td(self.test_id, class_="col-name"),
                html.td(self.formatted_time, class_="col-duration"),
                html.td(self.links_html, class_="col-links"),
            ]

            self.pytest_html_results_table_row(report=report, cells=cells)

            self.config.hook.pytest_html_results_table_html(
                report=report, data=self.additional_html
            )

            if len(cells) > 0:
                tr_class = None
                if self.config.getini("render_collapsed"):
                    tr_class = "collapsed"
                self.row_table = html.tr(cells)
                self.row_extra = html.tr(
                    html.td(self.additional_html, class_="extra", colspan=len(cells)),
                    class_=tr_class,
                )

        def c_time(self, star):
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(star))

        def pytest_html_results_table_row(self, report, cells):
            try:
                cells.insert(2, html.td(report.description))
                cells.insert(3, html.td(self.c_time(report.start), class_='col-time'))
            except AttributeError:
                ...
            cells.pop()
            for i in range(len(cells)):
                cells[i].attr.__setattr__('style', 'border:0.2px solid #%s' % self.cl)

        def __lt__(self, other):
            order = (
                "Error",
                "Failed",
                "Rerun",
                "XFailed",
                "XPassed",
                "Skipped",
                "Passed",
            )
            return order.index(self.outcome) < order.index(other.outcome)

        def create_asset(
                self, content, extra_index, test_index, file_extension, mode="w"
        ):
            asset_file_name = "{}_{}_{}.{}".format(
                re.sub(r"[^\w\.]", "_", self.test_id),
                str(extra_index),
                str(test_index),
                file_extension,
            )[-self.max_asset_filename_length:]
            asset_path = os.path.join(
                os.path.dirname(self.logfile), "assets", asset_file_name
            )

            os.makedirs(os.path.dirname(asset_path), exist_ok=True)

            relative_path = f"assets/{asset_file_name}"

            kwargs = {"encoding": "utf-8"} if "b" not in mode else {}
            with open(asset_path, mode, **kwargs) as f:
                f.write(content)
            return relative_path

        def append_extra_html(self, extra, extra_index, test_index):
            href = None
            if extra.get("format_type") == extras.FORMAT_IMAGE:
                self._append_image(extra, extra_index, test_index)

            elif extra.get("format_type") == extras.FORMAT_HTML:
                self.additional_html.append(html.div(raw(extra.get("content"))))

            elif extra.get("format_type") == extras.FORMAT_JSON:
                content = json.dumps(extra.get("content"))
                href = self.create_asset(
                    content, extra_index, test_index, extra.get("extension")
                )

            elif extra.get("format_type") == extras.FORMAT_TEXT:
                content = extra.get("content")
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
                href = self.create_asset(
                    content, extra_index, test_index, extra.get("extension")
                )

            elif extra.get("format_type") == extras.FORMAT_URL:
                href = extra.get("content")

            elif extra.get("format_type") == extras.FORMAT_VIDEO:
                self._append_video(extra, extra_index, test_index)

            if href is not None:
                self.links_html.append(
                    html.a(
                        extra.get("name"),
                        class_=extra.get("format_type"),
                        href=href,
                        target="_blank",
                    )
                )
                self.links_html.append(" ")

        def _format_time(self, report):
            duration = getattr(report, "duration", None)
            if duration is None:
                return ""

            duration_formatter = getattr(report, "duration_formatter", None)
            string_duration = str(duration)
            if duration_formatter is None:
                if "." in string_duration:
                    split_duration = string_duration.split(".")
                    split_duration[1] = split_duration[1][0:2]

                    string_duration = ".".join(split_duration)

                return string_duration
            else:
                formatted_milliseconds = "00"
                if "." in string_duration:
                    milliseconds = string_duration.split(".")[1]
                    formatted_milliseconds = milliseconds[0:2]

                duration_formatter = duration_formatter.replace(
                    "%f", formatted_milliseconds
                )
                duration_as_gmtime = time.gmtime(report.duration)
                return time.strftime(duration_formatter, duration_as_gmtime)

        def _populate_html_log_div(self, log, report):
            if report.longrepr:
                text = report.longreprtext or report.full_text
                for line in text.splitlines():
                    separator = line.startswith("_ " * 10)
                    if separator:
                        log.append(line[:80])
                    else:
                        exception = line.startswith("E   ")
                        if exception:
                            log.append(html.span(raw(escape(line)), class_="error"))
                        else:
                            log.append(raw(escape(line)))
                    log.append(html.br())

            for section in report.sections:
                header, content = map(escape, section)
                log.append(f" {header:-^80} ")
                log.append(html.br())

                if ansi_support():
                    converter = ansi_support().Ansi2HTMLConverter(
                        inline=False, escaped=False
                    )
                    content = converter.convert(content, full=False)
                else:
                    content = _remove_ansi_escape_sequences(content)

                log.append(raw(content))
                log.append(html.br())

        def append_log_html(
                self,
                report,
                additional_html,
                pytest_capture_value,
                pytest_show_capture_value,
        ):
            log = html.div(class_="log")

            should_skip_captured_output = pytest_capture_value == "no"
            if report.outcome == "failed" and not should_skip_captured_output:
                should_skip_captured_output = pytest_show_capture_value == "no"
            if not should_skip_captured_output:
                self._populate_html_log_div(log, report)

            if len(log) == 0:
                log = html.div(class_="empty log")
                log.append("No log output captured.")

            additional_html.append(log)

        def _make_media_html_div(
                self, extra, extra_index, test_index, base_extra_string, base_extra_class
        ):
            content = extra.get("content")
            try:
                is_uri_or_path = content.startswith(("file", "http")) or isfile(content)
            except ValueError:
                is_uri_or_path = False
            if is_uri_or_path:
                html_div = html.a(
                    raw(base_extra_string.format(extra.get("content"))), href=content
                )
            else:
                content = b64decode(content.encode("utf-8"))
                href = src = self.create_asset(
                    content, extra_index, test_index, extra.get("extension"), "wb"
                )
                html_div = html.a(
                    raw(base_extra_string.format(src)),
                    class_=base_extra_class,
                    target="_blank",
                    href=href,
                )
            return html_div

        def _append_image(self, extra, extra_index, test_index):
            image_base = '<img src="{}"/>'
            html_div = self._make_media_html_div(
                extra, extra_index, test_index, image_base, "image"
            )
            self.additional_html.append(html.div(html_div, class_="image"))

        def _append_video(self, extra, extra_index, test_index):
            video_base = '<video controls><source src="{}" type="video/mp4"></video>'
            html_div = self._make_media_html_div(
                extra, extra_index, test_index, video_base, "video"
            )
            self.additional_html.append(html.div(html_div, class_="video"))

    def _appendrow(self, outcome, report):
        result = self.TestResult(outcome, report, self.logfile, self.config)
        if result.row_table is not None:
            index = bisect.bisect_right(self.results, result)
            self.results.insert(index, result)
            tbody = html.tbody(
                result.row_table,
                class_="{} results-table-row".format(result.outcome.lower()),
            )
            if result.row_extra is not None:
                tbody.append(result.row_extra)
            self.test_logs.insert(index, tbody)

    def append_passed(self, report):
        if report.when == "call":
            if hasattr(report, "wasxfail"):
                self.xpassed += 1
                self._appendrow("XPassed", report)
            else:
                self.passed += 1
                self._appendrow("Passed", report)

    def append_failed(self, report):
        if getattr(report, "when", None) == "call":
            if hasattr(report, "wasxfail"):
                self.xpassed += 1
                self._appendrow("XPassed", report)
            else:
                self.failed += 1
                self._appendrow("Failed", report)
        else:
            self.errors += 1
            self._appendrow("Error", report)

    def append_rerun(self, report):
        self.rerun += 1
        self._appendrow("Rerun", report)

    def append_skipped(self, report):
        if hasattr(report, "wasxfail"):
            self.xfailed += 1
            self._appendrow("XFailed", report)
        else:
            self.skipped += 1
            self._appendrow("Skipped", report)

    def _color_(self):
        _ = random.choice(__color__)
        if len(__color__) > 1:
            __color__.remove(_)
        return _

    def pytest_html_results_table_header(self, cells):
        cells[0].attr.width = '10%'
        cells[1].attr.width = '30%'
        cells.insert(2, html.th("Description", width='35%'))
        cells.insert(3, html.th("Time", class_="sortable time", col="time", width='13%'))
        cells[4].attr.width = '12%'
        cells.pop()
        for i in range(len(cells)):
            cells[i].attr.__setattr__('style', 'border:3px solid #%s' % self._color_())

    @staticmethod
    def pytest_html_report_title(report):
        report.title = 'TEST REPORT'

    def _generate_report(self, session):
        suite_stop_time = time.time()
        suite_time_delta = suite_stop_time - self.suite_start_time
        numtests = self.passed + self.failed + self.xpassed + self.xfailed
        generated = datetime.datetime.now()

        with open(
                os.path.join(os.path.dirname(__file__), "sttc", "style.css")
        ) as style_css_fp:
            self.style_css = style_css_fp.read()

        if ansi_support():
            ansi_css = [
                "\n/******************************",
                " * ANSI2HTML STYLES",
                " ******************************/\n",
            ]
            ansi_css.extend([str(r) for r in ansi_support().style.get_styles()])
            self.style_css += "\n".join(ansi_css)

        for path in self.config.getoption("css"):
            self.style_css += "\n/******************************"
            self.style_css += "\n * CUSTOM CSS"
            self.style_css += f"\n * {path}"
            self.style_css += "\n ******************************/\n\n"
            with open(path) as f:
                self.style_css += f.read()

        css_href = "assets/style.css"
        html_css = html.link(href=css_href, rel="stylesheet", type="text/css")
        head = html.head(
            html.meta(charset="utf-8"), html.title("Test Report"), html_css
        )

        class Outcome:
            def __init__(
                    self, outcome, total=0, label=None, test_result=None, class_html=None
            ):
                self.outcome = outcome
                self.label = label or outcome
                self.class_html = class_html or outcome
                self.total = total
                self.test_result = test_result or outcome

                self.generate_checkbox()
                self.generate_summary_item()

            def generate_checkbox(self):
                checkbox_kwargs = {"data-test-result": self.test_result.lower()}
                if self.total == 0:
                    checkbox_kwargs["disabled"] = "true"

                self.checkbox = html.input(
                    type="checkbox",
                    checked="true",
                    onChange="filterTable(this)",
                    name="filter_checkbox",
                    class_="filter",
                    hidden="true",
                    **checkbox_kwargs,
                )

            def generate_summary_item(self):
                self.summary_item = html.span(
                    f"{self.total} {self.label}", class_=self.class_html
                )

        outcomes = [
            Outcome("passed", self.passed),
            Outcome("skipped", self.skipped),
            Outcome("failed", self.failed),
            Outcome("error", self.errors, label="errors"),
            Outcome("xfailed", self.xfailed, label="expected failures"),
            Outcome("xpassed", self.xpassed, label="unexpected passes"),
        ]

        if self.rerun is not None:
            outcomes.append(Outcome("rerun", self.rerun))

        summary = [
            html.p(f"{numtests} tests ran in {suite_time_delta:.2f} seconds. "),
            html.p(
                "(Un)check the boxes to filter the results.",
                class_="filter",
                hidden="true",
            ),
        ]

        for i, outcome in enumerate(outcomes, start=1):
            summary.append(outcome.checkbox)
            summary.append(outcome.summary_item)
            if i < len(outcomes):
                summary.append(", ")

        cells = [
            html.th("Result", class_="sortable result initial-sort", col="result"),
            html.th("Test", class_="sortable", col="name"),
            html.th("Duration", class_="sortable", col="duration"),
            html.th("Links", class_="sortable links", col="links"),
        ]
        self.pytest_html_results_table_header(cells=cells)

        results = [
            html.h2("Results"),
            html.table(
                [
                    html.thead(
                        html.tr(cells),
                        html.tr(
                            [
                                html.th(
                                    "No results found. Try to check the filters",
                                    colspan=len(cells),
                                )
                            ],
                            id="not-found-message",
                            hidden="true",
                        ),
                        id="results-table-head",
                    ),
                    self.test_logs,
                ],
                id="results-table",
            ),
        ]

        with open(
                os.path.join(os.path.dirname(__file__), "sttc", "main.js")
        ) as main_js_fp:
            main_js = main_js_fp.read()

        self.pytest_html_report_title(report=self)

        body = html.body(
            html.script(raw(main_js)),
            html.h1(self.title),
            html.p(
                "Report generated on {} at {} by ".format(
                    generated.strftime("%d-%b-%Y"), generated.strftime("%H:%M:%S")
                ),
                html.a("pytest-report", href=__pypi_url__),
            ),
            onLoad="init()",
        )

        body.extend(self._generate_environment(session.config))
        summary_prefix, summary_postfix = [], []
        body.extend([html.h2("Summary")] + summary_prefix + summary + summary_postfix)
        body.extend(results)
        doc = html.html(head, body)
        unicode_doc = "<!DOCTYPE html>\n{}".format(doc.unicode(indent=2))
        unicode_doc = unicode_doc.encode("utf-8", errors="xmlcharrefreplace")
        return unicode_doc.decode("utf-8")

    def _generate_environment(self, config):
        if not hasattr(config, "_metadata") or config._metadata is None:
            return []

        metadata = config._metadata
        environment = [html.h2("Environment")]
        rows = []

        keys = [k for k in metadata.keys()]
        if not isinstance(metadata, OrderedDict):
            keys.sort()

        for key in keys:
            value = metadata[key]
            if isinstance(value, str) and value.startswith("http"):
                value = html.a(value, href=value, target="_blank")
            elif isinstance(value, (list, tuple, set)):
                value = ", ".join(str(i) for i in sorted(map(str, value)))
            elif isinstance(value, dict):
                sorted_dict = {k: value[k] for k in sorted(value)}
                value = json.dumps(sorted_dict)
            raw_value_string = raw(str(value))
            rows.append(html.tr(html.td(key), html.td(raw_value_string)))

        environment.append(html.table(rows, id="environment"))
        return environment

    def _save_report(self, report_content):
        dir_name = os.path.dirname(self.logfile)
        assets_dir = os.path.join(dir_name, "assets")

        os.makedirs(dir_name, exist_ok=True)

        with open(self.logfile, "w", encoding="utf-8") as f:
            f.write(report_content)
        style_path = os.path.join(assets_dir, "style.css")
        with open(style_path, "w", encoding="utf-8") as f:
            f.write(self.style_css)

    def _post_process_reports(self):
        for test_name, test_reports in self.reports.items():
            outcome = "passed"
            wasxfail = False
            failure_when = None
            full_text = ""
            extras = []
            duration = 0.0

            for test_report in test_reports:
                if test_report.outcome == "rerun":
                    self.append_rerun(test_report)
                else:
                    full_text += test_report.longreprtext
                    extras.extend(getattr(test_report, "extra", []))
                    duration += getattr(test_report, "duration", 0.0)

                    if (
                            test_report.outcome not in ("passed", "rerun")
                            and outcome == "passed"
                    ):
                        outcome = test_report.outcome
                        failure_when = test_report.when

                    if hasattr(test_report, "wasxfail"):
                        wasxfail = True

            test_report.outcome = outcome
            test_report.when = "call"
            test_report.nodeid = test_name
            test_report.longrepr = full_text
            test_report.extra = extras
            test_report.duration = duration

            if wasxfail:
                test_report.wasxfail = True

            if test_report.outcome == "passed":
                self.append_passed(test_report)
            elif test_report.outcome == "skipped":
                self.append_skipped(test_report)
            elif test_report.outcome == "failed":
                test_report.when = failure_when
                self.append_failed(test_report)

    def pytest_runtest_logreport(self, report):
        self.reports[report.nodeid].append(report)

    def pytest_collectreport(self, report):
        if report.failed:
            self.append_failed(report)

    def pytest_sessionstart(self, session):
        self.suite_start_time = time.time()

    def pytest_sessionfinish(self, session):
        self._post_process_reports()
        report_content = self._generate_report(session)
        self._save_report(report_content)

        _Utils.clear_by_mtime(screenshot_dir)
        # 兼容seliky
        log_dir = os.path.join(output_dir, "logs")
        if os.path.exists(log_dir):
            _Utils.clear_by_mtime(log_dir)
        self._sub_html_()

        self._get_pfs_data_()
        with open(pfs_json, "r", encoding="utf-8") as ff:
            data = json.loads(ff.read())

        self._draw_by_echarts_(data)
        self._draw_by_echarts2_(data)
        self._replace_js_()
        _Utils().preset(output_dir)  # 报告备份，grid并行运行必须在结束时备份，开始时备份不行

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep("-", f"generated html file: file://{self.logfile}")

    def _draw_by_echarts_(self, data):
        p, f, s, x, label = self._get_view1_data(data)
        try:
            rate = round(p / (p + f + s) * 100, 2)
        except ZeroDivisionError:
            rate = 0
        c = (
            self.view.charts.Pie(init_opts=self.view.options.InitOpts(width="380px", height="280px"))
                .add(
                "",
                [list(z) for z in zip(label, x)],
                radius=["35%", "55%"], center=["45%", "55%"],
            )
                .set_global_opts(
                title_opts=self.view.options.TitleOpts(title=f"{rate} %", pos_right="45%", pos_top="48%"),
                legend_opts=self.view.options.LegendOpts(is_show=False)
            )
                .set_series_opts(label_opts=self.view.options.LabelOpts(formatter="{b}: {c}"))
                .set_colors(self.__pfs_color__)
        )
        c.page_title = '成功率'
        c.render(path=e1_html_path)

    def _draw_by_echarts2_(self, data):
        """
        :param data: {"Demo": (8, 1), "结构化": (9, 3), "零部件": (12, 0)}
        """

        def radius(color_index: int, border_radius: list):
            return {
                "normal": {
                    "color": self.view.commons.utils.JsCode(
                        """new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'%s'},{offset:1,color:'%s'}],false)""" % (
                            self.__pfs_color__[color_index], self.__pfs_color__[color_index])
                    ),
                    "barBorderRadius": border_radius,
                }
            }

        x, y1, y2, y3 = [], [], [], []
        for k, v in data.items():
            x.append(k)
            v1, v2, v3 = v
            if not v1:
                v1 = ""
            if not v2:
                v2 = ""
            if not v3:
                v3 = ""
            y1.append(v1)  # 所有的成功
            y2.append(v2)  # 所有的失败
            y3.append(v3)  # 所有的跳过

        # 后面的height高度值配置iframe的高度调整，7个模块没问题，再往上会不好看
        bar = self.view.charts.Bar(init_opts=self.view.options.InitOpts(width="500px", height=f"{195 + len(x) * 22}px"))
        bar.add_xaxis(x)

        bar.add_yaxis(series_name='成功', y_axis=y1, stack="stack1", color=self.__pfs_color__[0], category_gap="33%",
                      itemstyle_opts=radius(0, [6, 3, 3, 6]), label_opts={"show": True, "color": "black"})
        bar.add_yaxis(series_name='跳过', y_axis=y3, stack="stack1", color=self.__pfs_color__[2], category_gap="33%",
                      itemstyle_opts=radius(2, [0, 0, 0, 0]), label_opts={"show": True, "color": "black"})
        bar.add_yaxis(series_name='失败', y_axis=y2, stack="stack1", color=self.__pfs_color__[1], category_gap="33%",
                      itemstyle_opts=radius(1, [3, 6, 6, 3]), label_opts={"show": True, "color": "black"})

        try:
            max_ = sum(data.values())
        except TypeError:  # 多模块运行情况
            max_ = []
            for i in list(data.values()):
                max_.append(sum(i))
            max_ = max(max_)

        bar.set_global_opts(
            # min/max 控制长短，inverse：左右对调，调试时把show打开。min最多为-2，最少为-0.2；max为总数
            xaxis_opts={"show": False, "inverse": False, "min": -0.2 - max_ / 5, "max": max_},
            yaxis_opts={"show": True, "splitLine": {"show": False}, "axisLine": {"show": False}, "axisTick": {
                "show": False}, "offset": -50},  # offset 控制偏移多少
            legend_opts={"show": False},
        )
        bar.set_series_opts()
        bar.reversal_axis()
        bar.page_title = "模块图"
        bar.render(e2_html_path)

    @staticmethod
    def _get_view1_data(data):
        p = f = s = 0
        for k, v in data.items():
            v1, v2, v3 = v
            p = p + v1
            f = f + v2
            s = s + v3
        x = [p, f]
        label = ['成功', '失败']
        if s:
            x.append(s)
            label.append('跳过')
        return p, f, s, x, label

    def _get_pfs_data_(self):
        with open(html_report_path, 'r', encoding='utf-8') as f:
            con = f.read()
        con = etree.HTML(con)
        pfs_xpath = '//tbody[contains(@class,"%s")]//td[@class="col-name"]'
        p = con.xpath(pfs_xpath % 'passed')
        f = con.xpath(pfs_xpath % 'failed')
        s = con.xpath(pfs_xpath % 'skipped')

        def _cal_(pfs):
            _md = dict()
            if not pfs:
                return _md
            for _ in pfs:
                e = _.text.rindex('/')
                try:
                    md = _.text[_.text.rindex('/', 0, e) + 1:e]
                except ValueError:
                    md = _.text[e + 1:_.text.rindex('.')]
                if _md.get(md):
                    _md[md] += 1
                else:
                    _md[md] = 1
            return _md

        pmd = _cal_(p)
        fmd = _cal_(f)
        smd = _cal_(s)
        self.module_num = max(len(pmd), len(fmd))
        rates = dict()  # 各模块的pfs
        for p, f, s in zip_longest(pmd, fmd, smd):
            key = p or f or s
            pp = pmd.get(key, 0)
            ff = fmd.get(key, 0)
            ss = smd.get(key, 0)
            try:
                rates[key] = (pp, ff, ss)
            except ZeroDivisionError:
                rates[p] = 100

        with open(pfs_json, "w", encoding="utf-8") as f:
            f.write(json.dumps(rates))

    def _sub_html_(self):
        with open(html_report_path, 'r', encoding='utf-8') as f:
            con = f.read()
        res = re.sub('<p>Report generated.*</p>', '', con)
        re_waste = r'<p>\d+ tests ran in*.*</p>'
        waste = re.findall(re_waste, res)
        if not waste:
            re_waste = r'</span>\d+ tests ran in*.*</div>'
            waste = re.findall(re_waste, res)
        if waste:
            waste = waste[0][3:-4]
        else:
            waste = 0.6
        res = re.sub(re_waste, '', res)
        res = re.sub(r'<p>*.*\(Un\)check the boxes .+\.</p>', '', res)
        res = re.sub(r'<input checked="true"',
                     '<span style="height:40px; color:black; font-weight:bold; font-size:120%">Filter : </span>'
                     '<input checked="true"',
                     res, count=1)
        res = re.sub(r'0 errors</span>*.*unexpected passes</span>', '0 errors</span>', res)
        res = re.sub(r'<h2>Results</h2>', '', res)
        index_url = self.config.getoption("page_url")
        name = self.config.getoption("name")
        password = self.config.getoption("password")
        browser = self.config.getoption("browser")
        link = f'<div style="height:30px; color:green; padding:15px 0px 0px 0px">' \
               f'<span style="color:black;font-weight:bold; font-size:120%">Test Url : </span>' \
               f'<a href={index_url} style="color:green">{index_url}</a></div>' \
               f'<div style="height:30px; color:green">' \
               f'<span style="color:black;font-weight:bold; font-size:120%">Test By : </span>' \
               f'name: {name} &nbsp &nbsp | &nbsp &nbsp password: {password} </div>' \
               f'<div style="height:30px; color:green">' \
               f'<span style="color:black;font-weight:bold; font-size:120%">Test Browser : </span>{browser}</div>' \
               f'<div style="height:30px; color:green">' \
               f'<span style="color:black;font-weight:bold; font-size:120%">Test Consuming : </span>{waste}</div>'
        res = re.sub('<h2>Summary</h2>', link, res)
        with open(html_report_path, 'w', encoding='utf-8') as f:
            f.write(res)

    def _replace_js_(self):
        if replace_js:
            js_name = replace_js.rsplit(os.sep)[-1]
            for i in (e1_html_path, e2_html_path):
                with open(i, 'r', encoding='utf-8') as f:
                    con = f.read()
                res = re.sub('https://assets.pyecharts.org/assets/v5/echarts.min.js', js_name, con)
                with open(i, 'w', encoding='utf-8') as f:
                    f.write(res)

        with open(html_report_path, 'r', encoding='utf-8') as f:
            con = f.read()
        res = re.sub('seconds. </div>',
                     'seconds. </div>'
                     '<iframe style="width:30%;height:300px;margin:-215px 0px 0px 30.5%" width="100%" height="100%" '
                     'frameborder="no" border="0" src="assets/e1.html"></iframe>'
                     f'<iframe style="width:33%;height:{300 + self.module_num * 10}px;margin:-290px 0px 0px 59.5%" width="100%" height="100%" '
                     'frameborder="no" border="0" src="assets/e2.html"></iframe>'  # 33% 兼容了小屏
                     '<div style="margin:-80px 0px 0px 0px"></div>',  # 上下部分缝合
                     con)
        with open(html_report_path, 'w', encoding='utf-8') as f:
            f.write(res)


class _Utils:
    cur_time = property(lambda self: datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

    @staticmethod
    def clear_by_mtime(dir_path, days=4, count=0, by='mtime', remove: list = None):
        if not remove:
            remove = []
        if not by:
            files_date = [
                (file, datetime.datetime.fromtimestamp(os.stat(os.path.join(dir_path, file)).st_file_attributes))
                for file in os.listdir(dir_path) if file not in remove]
        else:
            files_date = [(file, datetime.datetime.fromtimestamp(os.stat(os.path.join(dir_path, file)).st_mtime))
                          for file in os.listdir(dir_path) if file not in remove]
        sorted_file = [(os.path.join(dir_path, x[0]), x[1]) for x in
                       sorted(files_date, key=lambda x: x[0], reverse=True)]
        if count:
            sorted_file = sorted_file[count:]

        for i in sorted_file:
            file, date = i
            if date < datetime.datetime.today() - timedelta(days=days) or count:
                try:
                    os.remove(file)
                except PermissionError:
                    shutil.rmtree(file)

    def clear_by_count(self, dir_path, count=10):
        return self.clear_by_mtime(dir_path=dir_path, count=count, by='', remove=['logs', 'report'])

    @staticmethod
    def clear_by_type(dir_path, end='.jpg'):
        for i in [os.path.join(dir_path, i) for i in os.listdir(dir_path)]:
            if i.endswith(end):
                os.remove(i)

    def preset(self, dir_path):
        """输出文件夹清理 + 报告备份"""
        for i in os.listdir(dir_path):
            i_path = os.path.join(dir_path, i)
            if 'report' == i:
                bake_report_path = os.path.join(dir_path, 'report_' + self.cur_time[4:-4])
                shutil.copytree(i_path, bake_report_path)
                # shutil.rmtree(i_path)  # 有时是grid并行在跑，一个跑完了一个没跑完，把它删了会影响另一个的报告。优化为不删仅复制，删除超过一天的截图
                screenshot_path = os.path.join(i_path, 'screenshots')
                if os.path.exists(screenshot_path):
                    self.clear_by_mtime(screenshot_path, days=1)
                break
        self.clear_by_count(dir_path)  # 根据数量清理


def _screenshot_(item):
    file_name = _Utils().cur_time + '.png'
    file_path = os.path.join(screenshot_dir, file_name)
    shot = False
    # 通常获取driver的方式，虽然没什么用
    if "driver" in item.funcargs:
        driver = item.funcargs["driver"]
        try:
            shot = driver.save_screenshot(screenshot_dir)
        except:
            ...
    else:
        # 反射来获取，我才是真nb
        vars = dir(item.cls)
        instance = ''
        for i in vars:
            if not (i.startswith('_') or 'setup' in i or 'teardown' in i or 'test' in i):
                instance = i
        if instance:
            try:
                driver = getattr(item.cls, instance).page
                shot = driver.save_screenshot(screenshot_dir)
            except:
                ...

    if not shot:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.destroy()

        ImageGrab.grab(bbox=(0, 0, w, h)).save(file_path)
    file_path = './screenshots/' + file_name
    return file_path
