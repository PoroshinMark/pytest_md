import os
import math
import mlflow
from mlflow.tracking import MlflowClient
import pytest
from pathlib import Path
from collections import defaultdict
import datetime
import json

from pytest_md.fixtures import extras, extras_stash_key


class MarkDownReport:

    def __init__(self, report_path, report_data, report_template, project_name=None):
        self._report_path = (
            Path.cwd() / Path(os.path.expandvars(report_path)).expanduser()
        )
        self._reports = defaultdict(dict)
        self._report = report_data
        self._report_template = report_template
        self.project_name = project_name
        self._mlflow_client = self._get_mlflow_client()

    @pytest.hookimpl(trylast=True)
    def pytest_runtest_logreport(self, report):
        key = (report.when, report.outcome)
        if report.outcome == "rerun":
            if key not in self._reports[report.nodeid]:
                self._reports[report.nodeid][key] = list()
            self._reports[report.nodeid][key].append(report)
        else:
            self._reports[report.nodeid][key] = [report]
        
        self._report.total_duration += report.duration

        finished = report.when == "teardown" and report.outcome != "rerun"
        if not finished:
            return
        
        # Calculate total duration for a single test.
        # This is needed to add the "teardown" duration
        # to tests total duration.
        test_duration = 0
        for key, reports in self._reports[report.nodeid].items():
            _, outcome = key
            if outcome != "rerun":
                test_duration += reports[0].duration
        
        for key, reports in self._reports[report.nodeid].items():
            when, _ = key
            for each in reports:
                dur = test_duration if when == "call" else each.duration
                self._process_report(each, dur)
                self._log_node_to_mlflow(report.nodeid, each, dur)
    
    @pytest.hookimpl(trylast=True)
    def pytest_sessionstart(self, session):
        self._report.running_state = "started"
        self._report.collected_items = len(session.items)
    
    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session):
        self._report.running_state = "finished"
        self._generate_report()


    def _get_mlflow_client(self) -> MlflowClient | None:
        """
        Configure and verify access to the MLflow Tracking server.
        Raises RuntimeError on any connectivity or authentication failure.
        """
        if os.getenv("MLFLOW_TRACKING_URI") is None or self.project_name is None:
            return None
        client = MlflowClient()
        # quick check that credentials & server are working
        try:
            client.search_experiments(max_results=1)
        except Exception as e:
            return None
        return client
    
    def _log_node_to_mlflow(self, nodeid, report, duration):
        """
        Log the test node to MLflow.
        """
        if not self._mlflow_client:
            return
        if report.when != "call":
            return
        experiment = self._mlflow_client.get_experiment_by_name(f"{self.project_name}-{nodeid}")
        if not experiment:
            experiment_id = self._mlflow_client.create_experiment(f"{self.project_name}-{nodeid}")
        else:
            experiment_id = experiment.experiment_id

        metrics = self._process_metrics(report)
        
        with mlflow.start_run(experiment_id=experiment_id, run_name=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) as run:
            mlflow.log_param("outcome", report.outcome)
            mlflow.log_metric("duration", duration)
            
            for metric in metrics:
                mlflow.log_metric(metric[0], metric[1])

    def _process_report(self, report, duration):
        if report.when != "call":
            return
        outcome = self._process_outcome(report)
        test_id = report.nodeid
        data = {
            "extras": self._process_extras(report, test_id),
            "metrics": self._process_metrics(report),
        }
        processed_logs = _process_logs(report)
        self._report.add_test(data, report, outcome, processed_logs)
        # Increment the outcome counter
        self._report.outcomes = outcome.lower()

    def _process_extras(self, report, test_id):
        test_index = hasattr(report, "rerun") and report.rerun + 1 or 0
        report_extras = getattr(report, "extras", [])
        return report_extras
    
    def _process_metrics(self, report):
        test_index = hasattr(report, "rerun") and report.rerun + 1 or 0
        report_metrics = getattr(report, "metrics", [])
        return report_metrics

    def _process_outcome(self, report):
        if _is_error(report):
            return "Error"
        if hasattr(report, "wasxfail"):
            if report.outcome in ["passed", "failed"]:
                return "XPassed"
            if report.outcome == "skipped":
                return "XFailed"

        return report.outcome.capitalize()

    def _generate_report(self):
        generated = datetime.datetime.now()
        test_data = self._report.data["tests"]

        rendered_report = self._report_template.render(
            title=self._report.title,
            date=generated.strftime("%d-%b-%Y"),
            time=generated.strftime("%H:%M:%S"),
            run_count=self._run_count(),
            running_state=self._report.running_state,
            outcomes=self._report.outcomes,
            test_data=test_data,
            additional_summary=self._report.additional_summary,
            total_duration=self._report.total_duration,
        )
        self._write_report(rendered_report)
        self._log_final_report_to_mlflow()

    def _log_final_report_to_mlflow(self):
        """
        Log the final report to MLflow.
        """
        if not self._mlflow_client:
            return
        experiment = self._mlflow_client.get_experiment_by_name(f"{self.project_name} Final Report")
        if not experiment:
            experiment_id = self._mlflow_client.create_experiment(f"{self.project_name} Final Report")
        else:
            experiment_id = experiment.experiment_id
        
        # Create a new run for the final report
        with mlflow.start_run(experiment_id=experiment_id, run_name=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) as run:
            mlflow.log_artifact(str(self._report_path), artifact_path="final_report")

    def _write_report(self, rendered_report):
        # Ensure the parent directory exists
        self._report_path.parent.mkdir(parents=True, exist_ok=True)
        # Write the rendered report to the file
        with open(self._report_path, "w", encoding="utf-8") as f:
            f.write(rendered_report)

    def _run_count(self):
        relevant_outcomes = ["passed", "failed", "xpassed", "xfailed"]
        counts = 0
        for outcome in self._report.outcomes.keys():
            if outcome in relevant_outcomes:
                counts += self._report.outcomes[outcome]["value"]

        plural = counts > 1
        duration = self._format_duration(self._report.total_duration)

        if self._report.running_state == "finished":
            return f"{counts} {'tests' if plural else 'test'} took {duration}."
        elif self._report.running_state == "started":
            collected = self._report.collected_items or 0
            return f"{counts}/{collected} {'tests' if collected > 1 else 'test'} done."
        else:
            return f"{counts} {'tests' if counts > 1 else 'test'} collected."

    def _format_duration(self, duration):
        if duration < 1:
            return "{} ms".format(round(duration * 1000))

        hours = math.floor(duration / 3600)
        remaining_seconds = duration % 3600
        minutes = math.floor(remaining_seconds / 60)
        remaining_seconds = remaining_seconds % 60
        seconds = round(remaining_seconds)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def _is_error(report):
    return (
        report.when in ["setup", "teardown", "collect"] and report.outcome == "failed"
    )


def _process_logs(report):
    log = []
    if report.longreprtext:
        log.append(report.longreprtext + "\n")
    # Don't add captured output to reruns
    if report.outcome != "rerun":
        for section in report.sections:
            header, content = section
            log.append(f"{' ' + header + ' ':-^80}\n{content}")

            # weird formatting related to logs
            if "log" in header:
                log.append("")
                if "call" in header:
                    log.append("")
    if not log:
        log.append("No log output captured.")
    return log