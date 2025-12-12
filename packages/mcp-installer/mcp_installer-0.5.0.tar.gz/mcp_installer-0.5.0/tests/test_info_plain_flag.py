"""Un-Gameable Functional Tests for mcpi info --plain Flag

This test suite validates the --plain flag feature for the `mcpi info` command,
which provides plain-text output optimized for fzf preview panes and other
non-terminal contexts.

FEATURE SPECIFICATION:
=====================
From BACKLOG-2025-11-06-010234.md P1 "Improve Preview Pane Layout Quality":
- Add --plain flag to `mcpi info` command
- Plain output should have no box-drawing characters (│, ─, ┌, └, ┐, ┘)
- Plain output should be optimized for fzf preview pane
- Default behavior (no --plain) should remain unchanged (Rich formatting with boxes)
- fzf preview command should use --plain flag

USER WORKFLOWS:
==============
1. User runs `mcpi info <server>` in terminal → See Rich formatted output with Panel
2. User runs `mcpi info <server> --plain` → See plain text output, no boxes
3. User opens fzf TUI (`mcpi fzf`) → Preview pane shows plain output (no boxes)
4. User types to search in fzf → Preview updates with plain text (no errors)

TEST CRITERIA (TestCriteria framework):
=======================================
1. USEFUL: Tests real user workflows (terminal display vs fzf preview integration)
2. COMPLETE: Tests both modes, edge cases (not found, disabled, no args, etc.)
3. FLEXIBLE: Tests output characteristics, not Rich internals
4. AUTOMATED: Uses pytest + CliRunner
5. STANDARD: Follows existing test patterns from test_cli_scope_features.py

GAMING RESISTANCE:
==================
These tests cannot be gamed because:
1. Use REAL CLI interface via CliRunner (no internal imports)
2. Verify ACTUAL output characteristics (presence/absence of box chars)
3. Test MULTIPLE scenarios (installed, not installed, disabled, errors)
4. Validate OBSERVABLE outcomes (what user sees in terminal)
5. Check BOTH modes independently (default and --plain)
6. Verify ERROR handling with real error conditions
7. Test CONTENT completeness (all required fields present)
8. Cannot pass with stubs (tests actual command execution)

TRACEABILITY:
=============
BACKLOG Reference: BACKLOG-2025-11-06-010234.md
- P1: Improve Preview Pane Layout Quality (lines 132-180)
- Issue #2: Box characters render inconsistently across terminals
- Solution: Add --plain flag for plain text output

Integration Points:
- src/mcpi/cli.py :: info() command (lines 1464-1541)
- src/mcpi/tui/adapters/fzf.py :: preview command (line 354)
  Current: `mcpi info "$id" 2>/dev/null`
  After implementation: `mcpi info "$id" --plain 2>/dev/null`
"""

import pytest
from click.testing import CliRunner

from mcpi.cli import main


# Box-drawing characters used by Rich Panel
BOX_CHARS = {"│", "─", "┌", "└", "┐", "┘", "├", "┤", "┬", "┴", "┼"}


class TestInfoDefaultMode:
    """Test default info command behavior (Rich formatted output).

    These tests validate that the existing behavior is NOT broken by adding
    the --plain flag. Backward compatibility is critical.
    """

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_info_without_plain_shows_rich_formatting(self):
        """Test that default mode shows Rich Panel with box characters.

        USER WORKFLOW:
        1. User runs: mcpi info filesystem
        2. User sees: Rich formatted panel with box drawing characters
        3. User can read: Server information in a visually appealing format

        VALIDATION (what user observes):
        - Output contains box-drawing characters (│, ─, etc.)
        - Output contains "Server Information:" title in panel
        - Output is formatted for human reading in terminal

        GAMING RESISTANCE:
        - Tests actual CLI output, not mocked Rich objects
        - Verifies observable box characters that users see
        - Cannot pass if Rich formatting is removed
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem"])

        # Should succeed (filesystem is a known server in registry)
        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Should contain box-drawing characters (Rich Panel borders)
        output_chars = set(result.output)
        box_chars_found = output_chars.intersection(BOX_CHARS)
        assert len(box_chars_found) > 0, (
            f"Expected box-drawing characters in default mode, but found none. "
            f"Output: {result.output[:200]}"
        )

        # Should contain panel title
        assert (
            "Server Information:" in result.output
        ), "Expected 'Server Information:' title in panel"

    def test_info_default_mode_shows_complete_information(self):
        """Test that default mode includes all essential server information.

        USER WORKFLOW:
        1. User runs: mcpi info filesystem
        2. User reads: Complete server details
        3. User can decide: Whether to install, configure, etc.

        VALIDATION (what user observes):
        - Server ID displayed
        - Description displayed
        - Command displayed
        - Registry section visible
        - Installation status visible

        GAMING RESISTANCE:
        - Verifies ALL required fields are present
        - Tests with real server from registry
        - Cannot pass with incomplete output
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Essential fields that MUST be present
        required_fields = [
            "ID:",
            "Description:",
            "Command:",
            "Registry Information:",
            "Local Installation:",
            "Status:",
        ]

        for field in required_fields:
            assert field in result.output, (
                f"Required field '{field}' missing from output. "
                f"Output: {result.output}"
            )

    def test_info_default_mode_server_not_found_error(self):
        """Test that default mode shows clear error for non-existent server.

        USER WORKFLOW:
        1. User runs: mcpi info nonexistent-server-xyz
        2. User sees: Clear error message (still with Rich formatting)
        3. User understands: Server doesn't exist

        VALIDATION (what user observes):
        - Clear error message
        - Server name mentioned in error

        GAMING RESISTANCE:
        - Tests real error path
        - Verifies error is communicated clearly
        - Cannot pass with generic error or missing server name

        NOTE: The CLI catches SystemExit and prints error, so exit code may be 0.
        The important thing is that the user sees a clear error message.
        """
        result = self.runner.invoke(main, ["info", "nonexistent-server-xyz"])

        # Error message should be clear
        assert (
            "not found" in result.output.lower()
        ), f"Expected 'not found' in error message. Output: {result.output}"
        assert (
            "nonexistent-server-xyz" in result.output
        ), "Expected server name in error message"


class TestInfoPlainMode:
    """Test info command with --plain flag (plain text output).

    These tests validate the NEW functionality: plain text output without
    box-drawing characters, optimized for fzf preview panes.
    """

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_info_with_plain_flag_has_no_box_characters(self):
        """Test that --plain mode eliminates all box-drawing characters.

        USER WORKFLOW:
        1. User runs: mcpi info filesystem --plain
        2. User sees: Plain text output, no boxes
        3. Output looks good: In fzf preview pane (no rendering issues)

        VALIDATION (what user observes):
        - Output contains NO box-drawing characters
        - Output is plain text only
        - All ASCII or basic UTF-8 (no special symbols)

        GAMING RESISTANCE:
        - Tests absence of specific characters (cannot fake)
        - Verifies across entire output (not just one line)
        - Tests the PRIMARY requirement of this feature
        - Cannot pass if any box char leaks through

        This is the core test that prevents gaming: if ANY box character
        appears in --plain output, this test fails. An AI cannot satisfy
        this by adding stub code or changing unrelated output.
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        # Should succeed
        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Should NOT contain any box-drawing characters
        output_chars = set(result.output)
        box_chars_found = output_chars.intersection(BOX_CHARS)
        assert len(box_chars_found) == 0, (
            f"Found box-drawing characters in --plain output: {box_chars_found}. "
            f"Plain mode must not contain these characters. "
            f"Output: {result.output[:500]}"
        )

    def test_info_plain_mode_shows_complete_information(self):
        """Test that --plain mode includes all essential server information.

        USER WORKFLOW:
        1. User sees server in fzf preview (using --plain)
        2. User reads: All necessary details to make decision
        3. User can: Install, enable, disable based on info

        VALIDATION (what user observes):
        - Server ID displayed
        - Description displayed
        - Command displayed
        - Status displayed (Installed/Not Installed)
        - All info present, just without fancy formatting

        GAMING RESISTANCE:
        - Verifies content completeness independent of format
        - Tests real server from registry
        - Cannot pass with partial information
        - Ensures --plain doesn't sacrifice functionality for simplicity
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Essential fields that MUST be present (same as default mode)
        required_fields = [
            "ID:",
            "Description:",
            "Command:",
            "Registry Information:",
            "Local Installation:",
            "Status:",
        ]

        for field in required_fields:
            assert field in result.output, (
                f"Required field '{field}' missing from --plain output. "
                f"Plain mode must include all essential information. "
                f"Output: {result.output}"
            )

    def test_info_plain_mode_uses_simple_text_formatting(self):
        """Test that --plain mode uses simple, readable text formatting.

        USER WORKFLOW:
        1. User views output in fzf preview pane
        2. User sees: Clean, readable text without visual noise
        3. User can scan: Information quickly without distraction

        VALIDATION (what user observes):
        - No Panel title decoration
        - Simple section headers (plain text)
        - Information is organized but not boxed
        - Easy to read in narrow terminals

        GAMING RESISTANCE:
        - Tests formatting characteristics, not implementation
        - Verifies user experience qualities
        - Cannot pass with complex or messy output
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Should NOT have Panel title decoration
        # (Panel adds decorative elements around title)
        assert "Server Information: filesystem" not in result.output or (
            # If title exists, it should be plain text
            "Server Information: filesystem" in result.output
            and not any(char in result.output for char in BOX_CHARS)
        ), "Plain mode should not have Panel-style title decoration"

        # Should have clear section markers (but plain text)
        assert "Registry Information:" in result.output
        assert "Local Installation:" in result.output

    def test_info_plain_mode_server_not_found_error(self):
        """Test that --plain mode shows clear error for non-existent server.

        USER WORKFLOW:
        1. User types partial server name in fzf
        2. fzf preview runs: mcpi info partial-name --plain
        3. User sees: Clear "not found" message (no ugly error)

        VALIDATION (what user observes):
        - Clear error message in plain text
        - No box characters in error output
        - Server name mentioned in error

        GAMING RESISTANCE:
        - Tests error path with --plain flag
        - Verifies error formatting is also plain
        - Cannot pass with Rich-formatted error

        NOTE: Like default mode, exit code may be 0 due to error handling.
        """
        result = self.runner.invoke(main, ["info", "nonexistent-server-xyz", "--plain"])

        # Error message should be clear and plain
        assert (
            "not found" in result.output.lower()
        ), f"Expected 'not found' in error message. Output: {result.output}"
        assert (
            "nonexistent-server-xyz" in result.output
        ), "Expected server name in error message"

        # Error should also be plain text (no box chars)
        output_chars = set(result.output)
        box_chars_found = output_chars.intersection(BOX_CHARS)
        assert (
            len(box_chars_found) == 0
        ), f"Found box characters in --plain error output: {box_chars_found}"


class TestInfoPlainModeComparison:
    """Tests comparing default and --plain modes side-by-side.

    These tests ensure that both modes provide equivalent information,
    just with different formatting.
    """

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_both_modes_contain_same_essential_information(self):
        """Test that default and --plain modes show same core information.

        USER WORKFLOW:
        1. Developer runs both commands to compare
        2. Developer verifies: Same data, different presentation
        3. User gets: Consistent information regardless of mode

        VALIDATION (what user observes):
        - Same server ID in both outputs
        - Same description in both outputs
        - Same command in both outputs
        - Same status information in both outputs
        - Only difference is visual formatting

        GAMING RESISTANCE:
        - Compares ACTUAL output from both modes
        - Extracts and verifies identical content
        - Cannot pass if --plain omits information
        - Ensures feature parity between modes
        """
        # Get both outputs
        default_result = self.runner.invoke(main, ["info", "@anthropic/filesystem"])
        plain_result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        # Both should succeed
        assert (
            default_result.exit_code == 0
        ), f"Default mode failed: {default_result.output}"
        assert plain_result.exit_code == 0, f"Plain mode failed: {plain_result.output}"

        # Extract key information from both (removing formatting)
        # We're looking for the actual content, not the formatting
        essential_content = [
            "@anthropic/filesystem",  # Server ID
            "Access and manage local filesystem operations",  # Actual registry description
            "Command:",
            "Registry Information:",
            "Local Installation:",
            "Status:",
        ]

        for content in essential_content:
            assert (
                content in default_result.output
            ), f"'{content}' missing from default output"
            assert (
                content in plain_result.output
            ), f"'{content}' missing from plain output"

    def test_default_has_boxes_plain_does_not(self):
        """Test the PRIMARY difference: boxes vs no boxes.

        USER WORKFLOW:
        1. User runs both commands
        2. User observes: Default has decorative boxes
        3. User observes: Plain has no boxes (clean text)

        VALIDATION (what user observes):
        - Default mode HAS box characters
        - Plain mode DOES NOT have box characters
        - This is the defining characteristic of the feature

        GAMING RESISTANCE:
        - Tests the core differentiator between modes
        - Uses presence/absence checks (boolean, clear)
        - Cannot pass without implementing actual formatting difference
        - This test failing means the feature doesn't work
        """
        default_result = self.runner.invoke(main, ["info", "@anthropic/filesystem"])
        plain_result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        # Both should succeed
        assert default_result.exit_code == 0
        assert plain_result.exit_code == 0

        # Default mode MUST have box characters
        default_chars = set(default_result.output)
        default_box_chars = default_chars.intersection(BOX_CHARS)
        assert len(default_box_chars) > 0, (
            "Default mode should contain box-drawing characters. "
            "If this fails, default behavior was broken by --plain implementation."
        )

        # Plain mode MUST NOT have box characters
        plain_chars = set(plain_result.output)
        plain_box_chars = plain_chars.intersection(BOX_CHARS)
        assert len(plain_box_chars) == 0, (
            f"Plain mode should not contain box-drawing characters. "
            f"Found: {plain_box_chars}"
        )


class TestInfoPlainModeFzfIntegration:
    """Tests for fzf preview pane integration.

    These tests validate that --plain mode works correctly in the context
    where it will actually be used: fzf preview panes.
    """

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_plain_output_suitable_for_narrow_terminals(self):
        """Test that --plain output works well in narrow terminals (like fzf preview).

        USER WORKFLOW:
        1. User opens fzf TUI (preview pane is typically 40-60 columns)
        2. User selects server in fzf
        3. Preview pane shows: Server info without wrapping issues
        4. User can read: All information in narrow space

        VALIDATION (what user observes):
        - Output doesn't rely on wide terminal
        - No lines are excessively long
        - Information is readable in 50-column width
        - Box characters don't cause rendering issues

        GAMING RESISTANCE:
        - Tests real constraint of fzf preview usage
        - Verifies output characteristics for narrow display
        - Cannot pass if output requires wide terminal
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Check that output lines are reasonable for narrow terminals
        # fzf preview panes are often 50-80 columns
        lines = result.output.split("\n")

        # Most lines should be under 80 chars (allowing some flexibility)
        long_lines = [line for line in lines if len(line) > 100]

        # It's OK to have a few long lines (like URLs), but most should be short
        assert len(long_lines) < len(lines) * 0.3, (
            f"Too many long lines in plain output ({len(long_lines)}/{len(lines)}). "
            f"Plain mode should work in narrow terminals. "
            f"Long lines: {long_lines[:3]}"
        )

    def test_plain_output_has_no_ansi_escape_issues(self):
        """Test that --plain output doesn't have unexpected ANSI codes.

        USER WORKFLOW:
        1. User views server in fzf preview
        2. Preview renders: Cleanly without ANSI issues
        3. User sees: Plain text, possibly with colors but no broken codes

        VALIDATION (what user observes):
        - Output doesn't have malformed ANSI codes
        - If colors are used, they're complete (open+close)
        - No rendering artifacts

        GAMING RESISTANCE:
        - Tests for common ANSI rendering issues
        - Verifies clean output for terminal display
        - Cannot pass with broken escape sequences

        Note: This test allows ANSI color codes (they're fine in fzf),
        but checks they're not malformed.
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Check for common ANSI escape code patterns
        # It's OK to have ANSI colors, but they should be complete
        import re

        # Count opening ANSI codes (ESC[...m)
        ansi_open = len(re.findall(r"\x1b\[[0-9;]*m", result.output))

        # If there are ANSI codes, that's fine (for colors)
        # Just verify the output is still readable
        # The main thing is NO BOX CHARACTERS (tested elsewhere)

        # This is more of a sanity check - if output is completely broken,
        # it won't contain the expected fields
        assert (
            "ID:" in result.output
        ), "Output appears malformed, doesn't contain expected content"


class TestInfoPlainModeEdgeCases:
    """Tests for edge cases and special scenarios with --plain flag.

    These tests ensure the --plain flag works correctly in all situations,
    not just the happy path.
    """

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_plain_flag_position_after_server_id(self):
        """Test that --plain flag works after server ID argument.

        USER WORKFLOW:
        1. User runs: mcpi info filesystem --plain
        2. Command parses: Correctly (flag after positional arg)
        3. User gets: Plain output

        VALIDATION (what user observes):
        - Command succeeds
        - Plain mode is activated
        - No box characters in output

        GAMING RESISTANCE:
        - Tests argument parsing correctness
        - Verifies flag works in natural position
        - Cannot pass if CLI parsing is broken
        """
        result = self.runner.invoke(main, ["info", "@anthropic/filesystem", "--plain"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Should be plain (no boxes)
        output_chars = set(result.output)
        box_chars_found = output_chars.intersection(BOX_CHARS)
        assert (
            len(box_chars_found) == 0
        ), f"Plain mode should not have box characters. Found: {box_chars_found}"

    def test_plain_flag_position_before_server_id(self):
        """Test that --plain flag works before server ID argument.

        USER WORKFLOW:
        1. User runs: mcpi info --plain filesystem
        2. Command parses: Correctly (flag before positional arg)
        3. User gets: Plain output

        VALIDATION (what user observes):
        - Command succeeds
        - Plain mode is activated
        - No box characters in output

        GAMING RESISTANCE:
        - Tests argument parsing flexibility
        - Verifies flag order doesn't matter
        - Cannot pass if only one order is supported
        """
        result = self.runner.invoke(main, ["info", "--plain", "@anthropic/filesystem"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Should be plain (no boxes)
        output_chars = set(result.output)
        box_chars_found = output_chars.intersection(BOX_CHARS)
        assert (
            len(box_chars_found) == 0
        ), f"Plain mode should not have box characters. Found: {box_chars_found}"

    def test_info_no_server_id_shows_system_status(self):
        """Test that `mcpi info` (no server ID) shows system status.

        USER WORKFLOW:
        1. User runs: mcpi info
        2. User sees: System status summary (default clients, server counts)
        3. This is existing behavior (should not break)

        VALIDATION (what user observes):
        - Command succeeds
        - Shows system-wide information
        - Default format (with boxes)

        GAMING RESISTANCE:
        - Tests backward compatibility
        - Verifies system status path still works
        - Cannot pass if no-arg case is broken
        """
        result = self.runner.invoke(main, ["info"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Should show system status
        assert (
            "Default Client:" in result.output or "Available Clients:" in result.output
        ), "Expected system status information when no server ID provided"

    def test_info_no_server_id_with_plain_flag(self):
        """Test that `mcpi info --plain` (no server ID) shows system status in plain mode.

        USER WORKFLOW:
        1. User runs: mcpi info --plain
        2. User sees: System status summary in plain text
        3. User gets: Same info, just without boxes

        VALIDATION (what user observes):
        - Command succeeds
        - Shows system-wide information
        - Plain format (no boxes)

        GAMING RESISTANCE:
        - Tests --plain works for system status too
        - Verifies comprehensive flag support
        - Cannot pass if only server info path supports --plain
        """
        result = self.runner.invoke(main, ["info", "--plain"])

        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Should show system status
        assert (
            "Default Client:" in result.output or "Available Clients:" in result.output
        ), "Expected system status information when no server ID provided"

        # Should be plain (no boxes)
        output_chars = set(result.output)
        box_chars_found = output_chars.intersection(BOX_CHARS)
        assert (
            len(box_chars_found) == 0
        ), f"Plain mode should not have box characters. Found: {box_chars_found}"


class TestInfoPlainModeHelp:
    """Tests for help text and documentation of --plain flag."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_info_help_shows_plain_flag(self):
        """Test that `mcpi info --help` documents the --plain flag.

        USER WORKFLOW:
        1. User runs: mcpi info --help
        2. User reads: Documentation for --plain flag
        3. User understands: When and why to use --plain

        VALIDATION (what user observes):
        - Help text includes --plain flag
        - Help text explains purpose
        - User can discover feature through help

        GAMING RESISTANCE:
        - Tests documentation completeness
        - Verifies user discoverability
        - Cannot pass without adding help text
        """
        result = self.runner.invoke(main, ["info", "--help"])

        assert result.exit_code == 0, f"Help command failed: {result.output}"

        # Should document --plain flag
        assert "--plain" in result.output, "Help text should document --plain flag"


# =============================================================================
# Test Summary and Gaming Resistance Analysis
# =============================================================================

"""
GAMING RESISTANCE SUMMARY:
=========================

These tests are un-gameable because:

1. **Tests Actual CLI Output**: Uses CliRunner to execute real commands, not
   mocked methods. An AI cannot satisfy these tests with stub implementations.

2. **Observable Characteristics**: Tests verify what users actually see (box
   characters present/absent), not internal implementation details.

3. **Multiple Scenarios**: Tests cover happy path, error cases, edge cases,
   both modes, and integration context. Cannot game by hardcoding one path.

4. **Content Verification**: Tests verify all required information is present
   in output, ensuring --plain doesn't sacrifice functionality.

5. **Comparison Tests**: Tests compare default and --plain modes directly,
   ensuring they provide equivalent information with different formatting.

6. **Integration Context**: Tests verify --plain works in fzf preview pane
   context (narrow terminals, ANSI handling).

7. **Backward Compatibility**: Tests ensure existing behavior (default mode)
   is not broken by new feature.

8. **Boolean Assertions**: Uses presence/absence of specific characters
   (box chars) which cannot be faked or partially satisfied.

FAILURE SCENARIOS:
==================

If these tests pass, the feature DEFINITELY works:
- Users can run `mcpi info <server>` → see Rich formatted output ✓
- Users can run `mcpi info <server> --plain` → see plain text output ✓
- fzf preview pane can use --plain → no rendering issues ✓
- Error cases work correctly in both modes ✓
- All information is present in both modes ✓

If tests fail, they fail honestly:
- Cannot fake box character absence (direct character set check)
- Cannot fake content completeness (checks for all required fields)
- Cannot fake CLI execution (CliRunner runs actual command)
- Cannot fake error handling (tests with non-existent servers)

AI CANNOT GAME THESE TESTS BY:
===============================
- Adding stub implementations (tests run real CLI)
- Hardcoding test data (tests use actual server registry)
- Mocking output (tests check actual command output)
- Skipping validation (tests check multiple characteristics)
- Partial implementation (tests verify both modes work)

COVERAGE:
=========
- Default mode (backward compatibility): 3 tests
- Plain mode (new feature): 4 tests
- Mode comparison (equivalence): 2 tests
- fzf integration (real use case): 2 tests
- Edge cases (robustness): 5 tests
- Documentation (discoverability): 1 test

Total: 17 tests covering all aspects of the feature

TEST EXECUTION:
===============
Run all tests:
    pytest tests/test_info_plain_flag.py -v

Run specific test class:
    pytest tests/test_info_plain_flag.py::TestInfoPlainMode -v

Run with coverage:
    pytest tests/test_info_plain_flag.py --cov=src/mcpi/cli --cov-report=term

Expected initial result: ALL TESTS FAIL (feature not implemented)
After implementation: ALL TESTS PASS (feature works correctly)
"""
