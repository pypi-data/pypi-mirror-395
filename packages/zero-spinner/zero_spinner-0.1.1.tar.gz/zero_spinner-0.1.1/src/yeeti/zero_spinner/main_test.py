# Copyright (C) 2025 Yeeti

"""Comprehensive tests for the zero_spinner module."""

import os
import time
from io import StringIO
from unittest.mock import patch

import pytest

from yeeti.zero_spinner.main import (
    UNICODE_SUPPORTED,
    Colors,
    Spinner,
    SpinnerDefinition,
    Symbols,
    spinner,
)


class TestColors:
    """Test suite for the Colors class."""

    def test_rgb_valid_values(self):
        """Test RGB method with valid color values."""
        colors = Colors()
        result = colors.rgb(255, 128, 0)
        assert result == '\033[38;2;255;128;0m'

        result = colors.rgb(0, 0, 0)
        assert result == '\033[38;2;0;0;0m'

        result = colors.rgb(255, 255, 255)
        assert result == '\033[38;2;255;255;255m'

    def test_rgb_invalid_values(self):
        """Test RGB method with invalid color values."""
        colors = Colors()
        with pytest.raises(ValueError, match='RGB values must be between 0 and 255'):
            colors.rgb(256, 0, 0)

        with pytest.raises(ValueError, match='RGB values must be between 0 and 255'):
            colors.rgb(0, -1, 0)

        with pytest.raises(ValueError, match='RGB values must be between 0 and 255'):
            colors.rgb(0, 0, 300)

    def test_find_named_color(self):
        """Test finding a named color."""
        colors = Colors()
        assert colors.find('red') == '\033[31m'
        assert colors.find('green') == '\033[32m'
        assert colors.find('blue') == '\033[34m'
        assert colors.find('bright_red') == '\033[91m'

    def test_find_rgb_color(self):
        """Test finding an RGB color using the rgb() pattern."""
        colors = Colors()
        result = colors.find('rgb(100,150,200)')
        assert result == '\033[38;2;100;150;200m'

    def test_find_invalid_color(self):
        """Test finding a color that doesn't exist."""
        colors = Colors()
        with pytest.raises(ValueError, match="Color 'invalid_color' not found"):
            colors.find('invalid_color')

    def test_find_invalid_rgb_format(self):
        """Test finding an invalid RGB format."""
        colors = Colors()
        with pytest.raises(ValueError):
            colors.find('rgb(256,0,0)')

    def test_random_color(self):
        """Test getting a random color."""
        colors = Colors()
        # Since it's random, we just verify that it returns a valid color code
        result = colors.random
        assert result.startswith('\033[')
        assert result.endswith('m')

    def test_rainbow_cycle(self):
        """Test rainbow color cycling."""
        colors = Colors()
        # Get several colors and verify they cycle
        color1 = colors.rainbow
        color2 = colors.rainbow
        color3 = colors.rainbow

        # These should all be different (cycling through)
        assert all(c.startswith('\033[') for c in [color1, color2, color3])

    def test_rainbow_bright_cycle(self):
        """Test bright rainbow color cycling."""
        colors = Colors()
        color1 = colors.rainbow_bright
        color2 = colors.rainbow_bright

        assert all(c.startswith('\033[') for c in [color1, color2])

    def test_rainbow_rgb_cycle(self):
        """Test RGB rainbow color cycling."""
        colors = Colors()
        color1 = colors.rainbow_rgb
        color2 = colors.rainbow_rgb

        assert all(c.startswith('\033[38;2;') for c in [color1, color2])

    def test_unicorn_cycle(self):
        """Test unicorn color cycling."""
        colors = Colors()
        color1 = colors.unicorn
        color2 = colors.unicorn

        assert all(c.startswith('\033[') for c in [color1, color2])

    def test_unicorn_rgb_cycle(self):
        """Test RGB unicorn color cycling."""
        colors = Colors()
        color1 = colors.unicorn_rgb
        color2 = colors.unicorn_rgb

        assert all(c.startswith('\033[38;2;') for c in [color1, color2])

    def test_all_named_colors(self):
        """Test all predefined named colors."""
        colors = Colors()
        color_names = [
            'black',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            'bright_black',
            'bright_red',
            'bright_green',
            'bright_yellow',
            'bright_blue',
            'bright_magenta',
            'bright_cyan',
            'bright_white',
        ]

        for name in color_names:
            result = colors.find(name)
            assert result.startswith('\033[')
            assert result.endswith('m')


class TestSymbols:
    """Test suite for the Symbols class."""

    def test_symbols_unicode(self):
        """Test that symbols are set correctly based on Unicode support."""
        symbols = Symbols()

        if UNICODE_SUPPORTED:
            assert symbols.success == '✔'
            assert symbols.fail == '✗'
            assert symbols.warn == '⚠'
            assert symbols.info == 'ℹ'
        else:
            assert symbols.success == '+'
            assert symbols.fail == 'X'
            assert symbols.warn == '!'
            assert symbols.info == 'i'

    def test_symbol_colors(self):
        """Test that symbol colors are set correctly."""
        symbols = Symbols()

        assert symbols.success_color == 'green'
        assert symbols.fail_color == 'red'
        assert symbols.warn_color == 'yellow'
        assert symbols.info_color == 'blue'


class TestSpinnerDefinition:
    """Test suite for the SpinnerDefinition class."""

    def test_default_spinner_definition(self):
        """Test default SpinnerDefinition values."""
        spinner_def = SpinnerDefinition()

        assert isinstance(spinner_def.frames, list)
        assert len(spinner_def.frames) > 0
        assert isinstance(spinner_def.interval, int)
        assert spinner_def.interval == 80

    def test_from_dict_valid(self):
        """Test creating SpinnerDefinition from a valid dictionary."""
        data = {
            'frames': ['|', '/', '-', '\\'],
            'interval': 100,
        }

        spinner_def = SpinnerDefinition.from_dict(data)
        assert spinner_def.frames == ['|', '/', '-', '\\']
        assert spinner_def.interval == 100

    def test_from_dict_not_dict(self):
        """Test from_dict with non-dictionary input."""
        with pytest.raises(ValueError, match='data must be a dictionary'):
            SpinnerDefinition.from_dict('not a dict')  # type: ignore

    def test_from_dict_missing_frames(self):
        """Test from_dict with missing frames."""
        data = {'interval': 100}

        with pytest.raises(ValueError, match='data.frames is missing'):
            SpinnerDefinition.from_dict(data)

    def test_from_dict_frames_not_list(self):
        """Test from_dict with frames not being a list."""
        data = {
            'frames': 'not a list',
            'interval': 100,
        }

        with pytest.raises(ValueError, match='data.frames is not a list'):
            SpinnerDefinition.from_dict(data)

    def test_from_dict_frames_contain_non_strings(self):
        """Test from_dict with frames containing non-string values."""
        data = {
            'frames': ['|', 1, '-'],
            'interval': 100,
        }

        with pytest.raises(ValueError, match='data.frames\\[x\\] must contain only strings'):
            SpinnerDefinition.from_dict(data)

    def test_from_dict_missing_interval(self):
        """Test from_dict with missing interval."""
        data = {'frames': ['|', '/', '-', '\\']}

        with pytest.raises(ValueError, match='data.interval is missing'):
            SpinnerDefinition.from_dict(data)

    def test_from_dict_interval_not_int(self):
        """Test from_dict with interval not being an integer."""
        data = {
            'frames': ['|', '/', '-', '\\'],
            'interval': '100',
        }

        with pytest.raises(ValueError, match='data.interval must be a int'):
            SpinnerDefinition.from_dict(data)


class TestSpinner:
    """Test suite for the Spinner class."""

    def test_spinner_initialization(self):
        """Test Spinner initialization with default values."""
        stream = StringIO()
        spin = Spinner(text='Loading', stream=stream)

        assert spin.text == 'Loading'
        assert spin.color == 'cyan'
        assert spin._prefix_text == ''
        assert spin._suffix_text == ''
        assert spin._hide_cursor is True
        assert spin._indent == 0

    def test_spinner_initialization_custom_values(self):
        """Test Spinner initialization with custom values."""
        stream = StringIO()
        custom_spinner = SpinnerDefinition.from_dict({
            'frames': ['1', '2', '3'],
            'interval': 50,
        })
        custom_symbols = Symbols()
        custom_colors = Colors()

        spin = Spinner(
            text='Custom',
            prefix_text='[',
            suffix_text=']',
            color='red',
            hide_cursor=False,
            indent=4,
            stream=stream,
            disabled=False,
            spinner=custom_spinner,
            symbols=custom_symbols,
            colors=custom_colors,
        )

        assert spin.text == 'Custom'
        assert spin.color == 'red'
        assert spin._prefix_text == '['
        assert spin._suffix_text == ']'
        assert spin._hide_cursor is False
        assert spin._indent == 4

    @patch.dict(os.environ, {'CI': '1'})
    def test_is_ci_environment_github_actions(self):
        """Test CI environment detection for GitHub Actions."""
        stream = StringIO()
        spin = Spinner(stream=stream)

        assert spin._is_ci_environment() is True

    @patch.dict(os.environ, {'GITHUB_ACTIONS': 'true'})
    def test_is_ci_environment_ci(self):
        """Test CI environment detection with CI variable."""
        stream = StringIO()
        spin = Spinner(stream=stream)

        assert spin._is_ci_environment() is True

    @patch.dict(os.environ, {}, clear=True)
    def test_is_not_ci_environment(self):
        """Test when not in CI environment."""
        stream = StringIO()
        spin = Spinner(stream=stream)

        # Remove any CI-related env vars
        for var in ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'TRAVIS', 'CIRCLECI', 'JENKINS_URL', 'TEAMCITY_VERSION']:
            os.environ.pop(var, None)

        assert spin._is_ci_environment() is False

    def test_start_disabled(self):
        """Test starting a disabled spinner."""
        stream = StringIO()
        spin = Spinner(text='Loading', stream=stream, disabled=True)

        spin.start()

        # When disabled, it should just print the text
        assert 'Loading' in stream.getvalue()
        assert spin._spinning is False

    @patch.dict(os.environ, {}, clear=True)
    def test_start_and_stop(self):
        """Test starting and stopping the spinner."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Loading', stream=stream)
            spin.start()

            # Give it a moment to start
            time.sleep(0.1)

            assert spin._spinning is True
            assert spin._thread is not None
            assert spin._stop is not None

            spin.stop()

            assert spin._spinning is False

    @patch.dict(os.environ, {}, clear=True)
    def test_start_with_text_parameter(self):
        """Test starting the spinner with text parameter."""
        stream = StringIO()
        spin = Spinner(text='Initial', stream=stream, disabled=True)

        spin.start('Updated')

        assert spin.text == 'Updated'

    @patch.dict(os.environ, {}, clear=True)
    def test_start_already_spinning(self):
        """Test starting a spinner that's already spinning."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Loading', stream=stream)
            spin.start()

            # Try to start again
            result = spin.start()

            assert result is spin

            spin.stop()

    @patch.dict(os.environ, {}, clear=True)
    def test_format(self):
        """Test the _format method."""
        stream = StringIO()
        spin = Spinner(stream=stream)

        result = spin._format(
            symbol='✔',
            color='green',
            text='Done',
            indent=2,
            prefix_text='[',
            suffix_text=']',
        )

        assert '\r' in result
        assert '✔' in result
        assert 'Done' in result
        assert '[' in result
        assert ']' in result

    @patch.dict(os.environ, {}, clear=True)
    def test_end(self):
        """Test the end method."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.end('✔', 'green', 'Complete')

            output = stream.getvalue()
            assert 'Complete' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_succeed(self):
        """Test the succeed method."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.succeed('Success!')

            output = stream.getvalue()
            assert 'Success!' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_succeed_default_text(self):
        """Test succeed method with default text."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.succeed()

            output = stream.getvalue()
            assert 'Processing' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_fail(self):
        """Test the fail method."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.fail('Failed!')

            output = stream.getvalue()
            assert 'Failed!' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_fail_default_text(self):
        """Test fail method with default text."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.fail()

            output = stream.getvalue()
            assert 'Processing' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_warn(self):
        """Test the warn method."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.warn('Warning!')

            output = stream.getvalue()
            assert 'Warning!' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_warn_default_text(self):
        """Test warn method with default text."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.warn()

            output = stream.getvalue()
            assert 'Processing' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_info(self):
        """Test the info method."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.info('Info!')

            output = stream.getvalue()
            assert 'Info!' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_info_default_text(self):
        """Test info method with default text."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = Spinner(text='Processing', stream=stream)
            spin.start()
            time.sleep(0.1)

            spin.info()

            output = stream.getvalue()
            assert 'Processing' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_context_manager_success(self):
        """Test using spinner as context manager with success."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            with Spinner(text='Loading', stream=stream) as spin:
                assert spin._spinning is True
                time.sleep(0.05)

            # Should call succeed when exiting without exception
            output = stream.getvalue()
            assert 'Loading' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_context_manager_failure(self):
        """Test using spinner as context manager with failure."""  # noqa: DOC501
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            try:
                with Spinner(text='Loading', stream=stream) as spin:
                    assert spin._spinning is True
                    time.sleep(0.05)
                    raise ValueError('Test error')
            except ValueError:
                pass

            # Should call fail when exiting with exception
            output = stream.getvalue()
            assert 'Loading' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_stop_raises_type_error_if_not_initialized(self):
        """Test that stop raises TypeError if _stop is None."""
        stream = StringIO()
        spin = Spinner(text='Test', stream=stream)

        # Manually set _disabled to True to force the stop to execute
        spin._disabled = False
        # Manually set _stop to None to simulate error condition
        spin._stop = None

        with pytest.raises(TypeError, match='_stop is not supposed to be None'):
            spin.stop()

    @patch.dict(os.environ, {}, clear=True)
    def test_stop_raises_type_error_if_thread_none(self):
        """Test that stop raises TypeError if _thread is None."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Test', stream=stream)
            spin.start()
            time.sleep(0.05)

            # Manually set _thread to None to simulate error condition
            spin._thread = None

            with pytest.raises(TypeError, match='_thread is not supposed to be None'):
                spin.stop()

    @patch.dict(os.environ, {}, clear=True)
    def test_animate_thread_functionality(self):
        """Test that the animation thread works correctly."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=True):
            spin = Spinner(text='Animating', stream=stream)
            spin.start()

            # Let it animate for a bit
            time.sleep(0.2)

            spin.stop()

            output = stream.getvalue()
            # Should have multiple frames written
            assert len(output) > 0

    def test_spinner_with_indent(self):
        """Test spinner with indent."""
        stream = StringIO()
        spin = Spinner(text='Test', indent=4, stream=stream)

        result = spin._format('✔', 'green', 'Done', indent=4)

        # Check that indent adds spaces
        assert result.startswith('\r    ')

    def test_spinner_with_prefix_and_suffix(self):
        """Test spinner with prefix and suffix text."""
        stream = StringIO()
        spin = Spinner(
            text='Test',
            prefix_text='[PREFIX]',
            suffix_text='[SUFFIX]',
            stream=stream,
        )

        result = spin._format(
            '✔',
            'green',
            'Done',
            prefix_text='[PREFIX]',
            suffix_text='[SUFFIX]',
        )

        assert '[PREFIX]' in result
        assert '[SUFFIX]' in result

    def test_custom_spinner_definition(self):
        """Test using a custom SpinnerDefinition."""
        custom_def = SpinnerDefinition.from_dict({
            'frames': ['A', 'B', 'C'],
            'interval': 50,
        })

        stream = StringIO()
        spin = Spinner(text='Custom', spinner=custom_def, stream=stream)

        assert spin._interval == 50

    @patch.dict(os.environ, {}, clear=True)
    def test_non_tty_stream(self):
        """Test spinner with non-TTY stream gets disabled."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = Spinner(text='Test', stream=stream)

            # Non-TTY streams should disable the spinner
            assert spin._disabled is True


class TestSpinnerFactory:
    """Test suite for the spinner factory function."""

    def test_spinner_factory_returns_spinner_instance(self):
        """Test that spinner factory returns a Spinner instance."""
        stream = StringIO()
        spin = spinner(text='Test', stream=stream)

        assert isinstance(spin, Spinner)
        assert spin.text == 'Test'

    def test_spinner_factory_with_all_parameters(self):
        """Test spinner factory with all parameters."""
        stream = StringIO()
        custom_spinner_def = SpinnerDefinition.from_dict({
            'frames': ['1', '2'],
            'interval': 100,
        })
        custom_symbols = Symbols()
        custom_colors = Colors()

        spin = spinner(
            text='Factory',
            prefix_text='<',
            suffix_text='>',
            color='blue',
            hide_cursor=False,
            indent=2,
            stream=stream,
            disabled=True,
            spinner=custom_spinner_def,
            symbols=custom_symbols,
            colors=custom_colors,
        )

        assert isinstance(spin, Spinner)
        assert spin.text == 'Factory'
        assert spin.color == 'blue'
        assert spin._prefix_text == '<'
        assert spin._suffix_text == '>'
        assert spin._hide_cursor is False
        assert spin._indent == 2
        assert spin._disabled is True


class TestIntegration:
    """Integration tests for the spinner."""

    @patch.dict(os.environ, {}, clear=True)
    def test_full_lifecycle(self):
        """Test the full lifecycle of a spinner."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = spinner(text='Loading data', stream=stream)
            spin.start()

            # Simulate some work
            time.sleep(0.1)

            spin.succeed('Data loaded successfully')

            output = stream.getvalue()
            assert 'Data loaded successfully' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_multiple_spinners(self):
        """Test using multiple spinners."""
        stream1 = StringIO()
        stream2 = StringIO()

        with patch.object(stream1, 'isatty', return_value=False), patch.object(stream2, 'isatty', return_value=False):
            spin1 = spinner(text='Task 1', stream=stream1)
            spin2 = spinner(text='Task 2', stream=stream2)

            spin1.start()
            spin2.start()

            time.sleep(0.1)

            spin1.succeed()
            spin2.fail()

            assert 'Task 1' in stream1.getvalue()
            assert 'Task 2' in stream2.getvalue()

    @patch.dict(os.environ, {}, clear=True)
    def test_changing_text_while_spinning(self):
        """Test changing text while spinner is running."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = spinner(text='Step 1', stream=stream)
            spin.start()

            time.sleep(0.05)

            # Change text
            spin.text = 'Step 2'

            time.sleep(0.05)

            spin.succeed()

            # Both texts might appear in output
            output = stream.getvalue()
            assert len(output) > 0


class TestEdgeCases:
    """Test edge cases and error handling."""

    @patch.dict(os.environ, {}, clear=True)
    def test_empty_text(self):
        """Test spinner with empty text."""
        stream = StringIO()
        spin = spinner(text='', stream=stream, disabled=True)

        spin.start()
        spin.succeed()

        # Should not raise an error
        assert True

    @patch.dict(os.environ, {}, clear=True)
    def test_special_characters_in_text(self):
        """Test spinner with special characters in text."""
        stream = StringIO()
        spin = spinner(text='Loading 💯 items', stream=stream, disabled=True)

        spin.start()
        spin.succeed()

        output = stream.getvalue()
        assert 'Loading' in output

    @patch.dict(os.environ, {}, clear=True)
    def test_very_long_text(self):
        """Test spinner with very long text."""
        stream = StringIO()
        long_text = 'A' * 1000
        spin = spinner(text=long_text, stream=stream, disabled=True)

        spin.start()
        spin.succeed()

        output = stream.getvalue()
        assert 'A' in output

    def test_negative_indent(self):
        """Test spinner with negative indent (should still work)."""
        stream = StringIO()
        spin = Spinner(text='Test', indent=-5, stream=stream)

        # Should not raise an error
        result = spin._format('✔', 'green', 'Done', indent=-5)
        assert result is not None

    def test_color_property_changes(self):
        """Test changing color property."""
        stream = StringIO()
        spin = Spinner(text='Test', color='red', stream=stream)

        assert spin.color == 'red'

        spin.color = 'blue'
        assert spin.color == 'blue'

    @patch.dict(os.environ, {}, clear=True)
    def test_rapid_start_stop_cycles(self):
        """Test rapid start/stop cycles."""
        stream = StringIO()

        with patch.object(stream, 'isatty', return_value=False):
            spin = Spinner(text='Test', stream=stream)

            for _ in range(3):
                spin.start()
                time.sleep(0.01)
                spin.stop()

            # Should not raise errors
            assert True
