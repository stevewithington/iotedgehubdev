# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import os
import unittest
from iotedgehubdev import configs
from iotedgehubdev.hostplatform import HostPlatform


class TestGetIniConfig(unittest.TestCase):
    @classmethod
    def cleanup(cls):
        iniFile = HostPlatform.get_setting_ini_path()
        if os.path.exists(iniFile):
            os.remove(iniFile)

    @classmethod
    def update_setting_ini_as_firsttime(cls):
        config = configs._prod_config.config
        config.set('DEFAULT', 'firsttime', 'yes')
        configs._prod_config.update_config()

    @classmethod
    def setUpClass(cls):
        cls.update_setting_ini_as_firsttime()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup()

    def test(self):
        from iotedgehubdev import configs
        iniConfig = configs.get_ini_config()
        self.assertEqual(iniConfig.get('DEFAULT', 'firsttime'), 'yes')


class TestCoreTelemetry(unittest.TestCase):
    def test_suppress_all_exceptions(self):
        self._impl(Exception, 'fallback')
        self._impl(Exception, None)
        self._impl(ImportError, 'fallback_for_import_error')
        self._impl(None, None)

    def _impl(self, exception_to_raise, fallback_return):
        from iotedgehubdev.decorators import suppress_all_exceptions

        @suppress_all_exceptions(fallback_return=fallback_return)
        def _error_fn():
            if not exception_to_raise:
                return 'positive result'
            else:
                raise exception_to_raise()

        if not exception_to_raise:
            self.assertEqual(_error_fn(), 'positive result')
        else:
            self.assertEqual(_error_fn(), fallback_return)
