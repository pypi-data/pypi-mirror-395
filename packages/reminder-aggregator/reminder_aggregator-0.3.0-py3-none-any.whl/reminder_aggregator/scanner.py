import json
import re
import xml.etree.ElementTree as ET
from hashlib import md5
from pathlib import Path
from re import Pattern
from typing import Any, Counter

from pathspec import GitIgnoreSpec


class Scanner:
    def __init__(self, scan_dir: Path, out_file: Path | None, out_format: str, ignore_file: Path | None = None) -> None:
        self.scan_dir: Path = scan_dir
        self.out_format: str = out_format

        if out_file is None:
            extension_map = {
                "json": "json",
                "codeclimate": "json",
                "junitxml": "xml",
            }
            self.out_file = Path(f"report.{extension_map[out_format]}")
        else:
            self.out_file = out_file

        self.ignore_spec: GitIgnoreSpec = self._load_ignorespec(ignore_file)

        self.BASE_PATTERN: str = r"[\:\ ]*(TODO|FIXME|HACK|OPTIMIZE|REVIEW).*"

        self.comment_patterns: dict[Pattern, Pattern] = {
            re.compile(r".*\.(ya?ml|py|json|toml)$"): re.compile(f"#+{self.BASE_PATTERN}"),
            re.compile(r".*\.html?$"): re.compile(f"(<!--){self.BASE_PATTERN}(-->)"),
        }

    def scan(self) -> None:
        matches: list[dict[str, Any]] = []

        for file in self.scan_dir.rglob("*"):
            if not file.is_file():
                continue

            if self.ignore_spec.match_file(file):
                continue

            match: list[dict[str, Any]] = self._parse_file(file)

            if len(match) == 0:
                continue

            matches.extend(match)

        self.matches: list[dict[str, Any]] = matches

    def create_report(self) -> None:
        match self.out_format:
            case "json":
                self._create_json_report(self.out_file)
            case "codeclimate":
                self._create_codeclimate_report(self.out_file)
            case "junitxml":
                self._create_junitxml_report(self.out_file)
            case _:
                return

    def _create_junitxml_report(self, out_file: Path) -> None:
        testsuite = ET.Element("testsuite", name="ReminderAggregator", tests=str(len(self.matches)))

        for match in self.matches:
            testcase = ET.SubElement(testsuite, "testcase", classname=match["file"], name=f"Line {match['line']}")

            failure = ET.SubElement(
                testcase,
                "failure",
                message=f"Found {match['type']} tag",
                type=match["type"],
            )
            failure.text = match["comment"]

        tree = ET.ElementTree(testsuite)
        tree.write(out_file, encoding="utf-8", xml_declaration=True)

    def _create_json_report(self, out_file: Path) -> None:
        counter = Counter(match["type"].upper() for match in self.matches)
        summary = dict(counter)
        summary["total"] = sum(counter.values())

        report = {
            "summary": summary,
            "details": self.matches,
        }

        with open(out_file, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)

    def _create_codeclimate_report(self, out_file: Path) -> None:
        report: list[dict[str, Any]] = []

        for match in self.matches:
            comment_text = match["comment"].split(match["type"], 1)[-1].lstrip(":").strip()
            description = f"Usage of {match['type']} tag"
            fingetprint = md5(f"{match['file']}:{match['line']}:{match['type']}".encode()).hexdigest()

            report.append(
                {
                    "type": "issue",
                    "check_name": match["type"].upper(),
                    "description": description,
                    "content": {
                        "body": comment_text or match["comment"],
                    },
                    "categories": ["Style"],
                    "location": {
                        "path": match["file"],
                        "lines": {
                            "begin": match["line"],
                        },
                    },
                    "severity": "info",
                    "fingerprint": fingetprint,
                }
            )

        with open(out_file, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)

    def _parse_file(self, file_path: Path) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        cwd: Path = Path.cwd()

        if file_path.is_relative_to(cwd):
            display_path: Path = file_path.relative_to(cwd)
        elif file_path.is_relative_to(self.scan_dir):
            display_path: Path = file_path.relative_to(self.scan_dir)
        else:
            display_path: Path = file_path

        comment_pattern: Pattern | None = self._get_comment_pattern(file_path)

        if comment_pattern is None:
            return matches

        try:
            for line_number, line in enumerate(open(file_path)):
                line = line.strip()

                if match := re.search(comment_pattern, line):
                    matches.append(
                        {
                            "type": match.group(1),
                            "file": str(display_path),
                            "line": line_number + 1,
                            "comment": line.strip(),
                        }
                    )

        except UnicodeDecodeError:
            print(f"Error reading {file_path}")

        return matches

    def _get_comment_pattern(self, file_path: Path) -> Pattern | None:
        for file_pattern, comment_pattern in self.comment_patterns.items():
            if file_pattern.match(str(file_path)):
                return comment_pattern

        return None

    def _load_ignorespec(self, ignore_file: Path | None = None) -> GitIgnoreSpec:
        DEFAULT_PATTERNS = [
            ".git/",
        ]

        all_patterns = DEFAULT_PATTERNS.copy()

        if ignore_file and ignore_file.is_file():
            try:
                extra_patterns: list[str] = ignore_file.read_text(encoding="utf-8").splitlines()
                extra_patterns: list[str] = [p.strip() for p in extra_patterns]

                all_patterns.extend(extra_patterns)
            except (OSError, UnicodeDecodeError) as e:
                print(f"Could not read ignore file {ignore_file}: {e}")

        return GitIgnoreSpec.from_lines(all_patterns)
