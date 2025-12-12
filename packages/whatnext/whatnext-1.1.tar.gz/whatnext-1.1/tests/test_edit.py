from datetime import date

from whatnext.cli import get_editor
from whatnext.models import MarkdownFile


class TestGetEditor:
    def test_whatnext_editor_takes_priority(self, monkeypatch):
        monkeypatch.setenv("WHATNEXT_EDITOR", "whatnext-editor")
        monkeypatch.setenv("VISUAL", "visual-editor")
        monkeypatch.setenv("EDITOR", "editor")
        assert get_editor() == "whatnext-editor"

    def test_visual_is_second_priority(self, monkeypatch):
        monkeypatch.delenv("WHATNEXT_EDITOR", raising=False)
        monkeypatch.setenv("VISUAL", "visual-editor")
        monkeypatch.setenv("EDITOR", "editor")
        assert get_editor() == "visual-editor"

    def test_editor_is_third_priority(self, monkeypatch):
        monkeypatch.delenv("WHATNEXT_EDITOR", raising=False)
        monkeypatch.delenv("VISUAL", raising=False)
        monkeypatch.setenv("EDITOR", "editor")
        assert get_editor() == "editor"

    def test_none_when_no_editor_set(self, monkeypatch):
        monkeypatch.delenv("WHATNEXT_EDITOR", raising=False)
        monkeypatch.delenv("VISUAL", raising=False)
        monkeypatch.delenv("EDITOR", raising=False)
        assert get_editor() == "vi"


class TestTaskLineNumber:
    def test_tasks_have_correct_line_numbers(self):
        file = MarkdownFile(
            source="example/tasks.md",
            today=date(2025, 1, 1),
        )
        assert len(file.tasks) == 3
        assert file.tasks[0].line == 3
        assert file.tasks[1].line == 4
        assert file.tasks[2].line == 5

    def test_tasks_in_multiple_sections(self):
        file = MarkdownFile(
            source="example/projects/obelisk.md",
            today=date(2025, 1, 1),
        )
        assert len(file.tasks) == 4
        lines = [task.line for task in file.tasks]
        assert lines == [7, 8, 9, 17]
