# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import warnings
from collections import defaultdict


class ReportData:
    def __init__(self, config):
        self._config = config

        self._additional_summary = {
            "prefix": [],
            "summary": [],
            "postfix": [],
        }

        self._collected_items = 0
        self._total_duration = 0
        self._running_state = "not_started"

        self._outcomes = {
            "failed": {"label": "Failed", "value": 0},
            "passed": {"label": "Passed", "value": 0},
            "skipped": {"label": "Skipped", "value": 0},
            "xfailed": {"label": "Expected failures", "value": 0},
            "xpassed": {"label": "Unexpected passes", "value": 0},
            "error": {"label": "Errors", "value": 0},
            "rerun": {"label": "Reruns", "value": 0},
        }

        self._results_table_header = [
            '<th class="sortable" data-column-type="result">Result</th>',
            '<th class="sortable" data-column-type="testId">Test</th>',
            '<th class="sortable" data-column-type="duration">Duration</th>',
            "<th>Links</th>",
        ]

        self._data = {
            "environment": {},
            "tests": defaultdict(list),
            "title": "Test Report",
        }

        # Handle missing configuration values gracefully
        try:
            collapsed = config.getini("render_collapsed")
            if collapsed.lower() == "true":
                warnings.warn(
                    "'render_collapsed = True' is deprecated and support "
                    "will be removed in the next major release. "
                    "Please use 'render_collapsed = all' instead.",
                    DeprecationWarning,
                )
                collapsed = "all"
        except ValueError:
            # Configuration value doesn't exist, use default
            collapsed = ""

        self._data["renderCollapsed"] = [
            outcome.lower() for outcome in collapsed.split(",") if outcome
        ]

        try:
            initial_sort = config.getini("initial_sort")
        except ValueError:
            # Configuration value doesn't exist, use default
            initial_sort = "result"
            
        self._data["initialSort"] = initial_sort

    @property
    def additional_summary(self):
        return self._additional_summary

    @additional_summary.setter
    def additional_summary(self, value):
        self._additional_summary = value

    @property
    def collected_items(self):
        return self._collected_items

    @collected_items.setter
    def collected_items(self, count):
        self._collected_items = count

    @property
    def config(self):
        return self._config

    @property
    def data(self):
        return self._data

    @property
    def outcomes(self):
        return self._outcomes

    @outcomes.setter
    def outcomes(self, outcome):
        self._outcomes[outcome.lower()]["value"] += 1

    @property
    def running_state(self):
        return self._running_state

    @running_state.setter
    def running_state(self, state):
        self._running_state = state

    @property
    def table_header(self):
        return self._results_table_header

    @table_header.setter
    def table_header(self, header):
        self._results_table_header = header

    @property
    def title(self):
        return self._data["title"]

    @title.setter
    def title(self, title):
        self._data["title"] = title

    @property
    def total_duration(self):
        return self._total_duration

    @total_duration.setter
    def total_duration(self, duration):
        self._total_duration = duration

    def set_data(self, key, value):
        self._data[key] = value

    def add_test(self, test_data, report, outcome, logs):
        test_id = report.nodeid
        self._data["tests"][test_id] = {
            "duration": getattr(report, "duration", 0.0),
            "result": outcome,
            "extras": test_data.get("extras", []),
            "logs": logs,
        }

    def append_teardown_log(self, report):
        pass
