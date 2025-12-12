import os
from typing import Any, Optional

from fastmcp import FastMCP
from pydantic import BaseModel

from splunk_appinspect import app_package_handler, checks, validator
from splunk_appinspect.formatters.validation_report_json_formatter import ValidationReportJSONFormatter
from splunk_appinspect.validation_report import ValidationReport

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

mcp = FastMCP(
    "AppInspect MCP Server",
    instructions="This is a set of tools to validate Splunk apps. Use `inspect_app` to validate an app."
    "Treat it as a static analysis tool so prefer to run it when you finish making changes to your app.",
)


class RunInspectionResponse(BaseModel):
    status: Literal["success", "exception"]
    summary: dict[str, int]
    logs: str
    next_steps: list[str]
    validation_results: dict[str, Any]


def run_inspection_inprocess(
    path: str,
    mode: str = "test",
    included_tags: Optional[list] = None,
    excluded_tags: Optional[list] = None,
    max_messages: int = 25,
) -> RunInspectionResponse:
    """Run AppInspect validation in-process and return structured results."""

    try:
        app_package_handler_obj = app_package_handler.AppPackageHandler(path)
        groups_to_validate = checks.groups(included_tags=included_tags, excluded_tags=excluded_tags)
        validation_report: ValidationReport = validator.validate_packages(
            app_package_handler_obj,
            args={
                "included_tags": included_tags,
                "excluded_tags": excluded_tags,
            },
            groups_to_validate=groups_to_validate,
            listeners=[],  # No listeners during validation
        )
        formatter = ValidationReportJSONFormatter()
        reports = formatter.format_application_validation_reports(validation_report, max_messages)
        allowed_check_results = {"failure", "error"}
        allowed_message_results = {"warning", "error", "failure"}
        for app_report in reports:
            filtered_groups = []
            for group in app_report.get("groups", []):
                filtered_checks = []
                for check in group.get("checks", []):
                    if check.get("result") in allowed_check_results:
                        check["messages"] = [
                            m for m in check.get("messages", []) if m.get("result") in allowed_message_results
                        ]
                        filtered_checks.append(check)
                if filtered_checks:
                    group["checks"] = filtered_checks
                    filtered_groups.append(group)
            app_report["groups"] = filtered_groups

        aggregated_groups: list[dict[str, Any]] = []
        for app_report in reports:
            aggregated_groups.extend(app_report.get("groups", []))

        validation_report_summary = validation_report.get_summary()

        failure_count = validation_report_summary.get("failure", 0)
        error_count = validation_report_summary.get("error", 0)

        next_steps: list[str]
        if failure_count > 0:
            next_steps = [
                "Fix all errors in the `validation_results` with result `failure` one by one",
                "Rerun `inspect_app` tool",
            ]
        elif error_count > 0:
            next_steps = [
                "Some checks in `validation_results` failed due to internal errors. This does not necessarily mean there is an issue with your code."
            ]
        else:
            next_steps = ["All validation checks passed. No fixes from AppInspect required."]

        response = RunInspectionResponse(
            status="success",
            summary=validation_report_summary,
            logs=f"Validation completed with {failure_count} failures and {error_count} errors.",
            next_steps=next_steps,
            validation_results={"groups": aggregated_groups},
        )
        return response

    except Exception as e:
        response = RunInspectionResponse(
            status="exception",
            summary={},
            logs=f"Validation failed with error: {str(e)}",
            next_steps=["Unable to run validation. Please check the logs for more information."],
            validation_results={"groups": []},
        )
        return response
    finally:
        if "app_package_handler_obj" in locals():
            app_package_handler_obj.cleanup()


@mcp.tool()
def inspect_app(
    path: str,
) -> RunInspectionResponse:
    """
    Validate an app using AppInspect CLI

    Returns an object with the following fields:
    - status: "success" | "exception"
    - summary: dict[str, int] – Aggregate counts from the validation summary (e.g., failure, error, warning).
    - logs: str – A brief status note about the validation run.
    - next_steps: list[str] – Actionable guidance on what to do next.
    - validation_results: { "groups": [...] } — aggregated across all apps, containing only
      checks with overall result of "failure". Each check includes `messages` with message text and
      optional file/line/code context indicating where the check failed.

    Notes:
    - Use `validation_results` for programmatic reasoning and to present concise, actionable fixes.

    Args:
        path: Absolute path to an app package (.tgz, .tar.gz, .spl) or a directory
    """

    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")

    result = run_inspection_inprocess(
        path=path,
        included_tags=[],
        excluded_tags=[],
        max_messages=100,
    )

    return result


def main():
    mcp.run()


if __name__ == "__main__":
    main()
