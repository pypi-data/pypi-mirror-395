"""Test suite to scripts"""

import logging
import subprocess
import sys
import unittest
import os

_logger = logging.getLogger(__name__)


class TestScriptsHelp(unittest.TestCase):
    def executeCommandLine(self, command_line, env):
        """Execute a command line.

        Log output as debug in case of bad return code.
        """
        _logger.info("Execute: %s", " ".join(command_line))
        p = subprocess.Popen(
            command_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )
        out, err = p.communicate()
        _logger.info("Return code: %d", p.returncode)
        try:
            out = out.decode("utf-8")
        except UnicodeError:
            pass
        try:
            err = err.decode("utf-8")
        except UnicodeError:
            pass

        if p.returncode != 0:
            _logger.info("stdout:")
            _logger.info("%s", out)
            _logger.info("stderr:")
            _logger.info("%s", err)
        else:
            _logger.debug("stdout:")
            _logger.debug("%s", out)
            _logger.debug("stderr:")
            _logger.debug("%s", err)
        self.assertEqual(p.returncode, 0)

    def executeAppHelp(self, script_name, module_name):
        test_script = ScriptTest()
        script = test_script.script_path(script_name, module_name)
        env = test_script.get_test_env()
        if script.endswith(".exe"):
            command_line = [script]
        else:
            command_line = [sys.executable, script]
        command_line.append("--help")
        self.executeCommandLine(command_line, env)

    def testAxis(self):
        self.executeAppHelp("axis", "tomwer.app.axis")

    def testCanvas(self):
        self.executeAppHelp("axis", "tomwer.app.canvas")

    def testDarkRef(self):
        self.executeAppHelp("darkref", "tomwer.app.darkref")

    def testDarkRefPath(self):
        self.executeAppHelp("darkrefpatch", "tomwer.app.darkrefpatch")

    def testDiffFrame(self):
        self.executeAppHelp("diffFrame", "tomwer.app.diffframe")

    def testImageKeyEditor(self):
        self.executeAppHelp("image-key-editor", "tomwer.app.imagekeyeditor")

    def testImageKeyUpgrader(self):
        self.executeAppHelp("image-key-upgrader", "tomwer.app.imagekeyupgrader")

    def testIntensityNormalization(self):
        self.executeAppHelp(
            "intensity-normalization", "tomwer.app.intensitynormalization"
        )

    def testMulticor(self):
        self.executeAppHelp("multicor", "tomwer.app.multicor")

    def testMultiPag(self):
        self.executeAppHelp("multipag", "tomwer.app.multipag")

    def testNabu(self):
        self.executeAppHelp("nabu", "tomwer.app.nabuapp")

    def testNxTomoEditor(self):
        self.executeAppHelp("nxtomo-editor", "tomwer.app.nxtomoeditor")

    def testPatchRawDarkflat(self):
        self.executeAppHelp("patch-raw-dark-flat", "tomwer.app.patchrawdarkflat")

    def testRadioStack(self):
        self.executeAppHelp("radiostack", "tomwer.app.radiostack")

    def testReduceDarkFlat(self):
        self.executeAppHelp("reduce-dark-flat", "tomwer.app.reducedarkflat")

    def testRSync(self):
        self.executeAppHelp("rsync", "tomwer.app.rsync")

    def testSampleMoved(self):
        self.executeAppHelp("samplemoved", "tomwer.app.samplemoved")

    def testScanviewer(self):
        self.executeAppHelp("scanviewer", "tomwer.app.scanviewer")

    def testSinogramViewer(self):
        self.executeAppHelp("sinogramviewer", "tomwer.app.sinogramviewer")

    def testSliceStack(self):
        self.executeAppHelp("slicestack", "tomwer.app.slicestack")

    def testStopDataListener(self):
        self.executeAppHelp("stop-data-listener", "tomwer.app.stopdatalistener")

    def testZStitching(self):
        self.executeAppHelp("zstitching", "tomwer.app.zstitching")


class ScriptTest:
    """
    Class providing useful stuff for preparing script tests.
    """

    def get_test_env(self):
        """
        Returns an associated environment with a working project.
        """
        env = dict((str(k), str(v)) for k, v in os.environ.items())
        env["PYTHONPATH"] = os.pathsep.join(sys.path)
        return env

    def script_path(self, script_name, module_name):
        """Returns the script path according to it's location"""
        import importlib

        module = importlib.import_module(module_name)
        script = module.__file__
        return script

    def get_installed_script_path(self, script):
        """
        Returns the path of the executable and the associated environment

        In Windows, it checks availability of script using .py .bat, and .exe
        file extensions.
        """
        paths = os.environ.get("PATH", "").split(os.pathsep)
        for base in paths:
            # clean up extra quotes from paths
            if base.startswith('"') and base.endswith('"'):
                base = base[1:-1]
        # script not found
        _logger.warning("Script '%s' not found in paths: %s", script, ":".join(paths))
        script_path = script
        return script_path
