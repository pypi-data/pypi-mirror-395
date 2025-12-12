import unittest
from unittest.mock import patch, MagicMock, call
import time
import json
import subprocess
from juham_systemstatus.systemstatus import SystemStatusThread, SystemStatus
from masterpiece.mqtt import MqttMsg, Mqtt

# --- Mocking Superclasses for JuhamThread ---
class MasterPieceThread:
    def __init__(self, client=None): 
        self.name = "MasterPieceThread"
    def from_dict(self, data): pass
    def to_dict(self): return {"_class": "MasterPieceThread"}
    def run(self): pass
    def error(self, msg): pass
    def warning(self, msg): pass
    def debug(self, msg): pass
    def publish(self, topic, msg, qos, retain): pass

class JuhamThread(MasterPieceThread):
    def make_topic_name(self, name): return f"juham/{name}"
    def subscribe(self, topic): pass
    def write_point(self, *args, **kwargs): pass
    def instantiate(self, class_id): return MagicMock()
    # --- Needed to avoid AttributeError ---
    def on_connect(self, client, userdata, flags, rc): pass
    def on_message(self, client, userdata, msg): pass

# ------------------------ TESTS ------------------------

class TestSystemStatusThread(unittest.TestCase):

    @patch('time.time', return_value=1000.0)
    @patch('threading.enumerate')
    def setUp(self, mock_enumerate, mock_time):
        self.mock_mqtt = MagicMock(spec=Mqtt)
        self.thread = SystemStatusThread(client=self.mock_mqtt) 
        self.thread.error = MagicMock()
        self.thread.warning = MagicMock()
        self.thread.debug = MagicMock()
        self.thread.init(
            topic="test/sys",
            log_topic="test/log",
            control_topic="test/control",
            interval=10.0,
            location="lab",
            max_uptime=3600.0
        )


    @patch('threading.enumerate')
    def test_get_thread_counts_initial(self, mock_enumerate):
        mock_active_thread = MagicMock(is_alive=lambda: True)
        mock_idle_thread = MagicMock(is_alive=lambda: False)
        mock_enumerate.return_value = [mock_active_thread]*3 + [mock_idle_thread]*2
        self.thread.expected_thread_count = 0
        counts = self.thread.get_thread_counts()
        self.assertEqual(counts["total_threads"], 5)
        self.assertEqual(self.thread.expected_thread_count, 5)
        self.thread.debug.assert_called_once()
        self.assertFalse(self.thread.request_reboot)

    @patch('threading.enumerate')
    def test_get_thread_counts_thread_drop_triggers_reboot(self, mock_enumerate):
        mock_active_thread = MagicMock(is_alive=lambda: True)
        mock_enumerate.return_value = [mock_active_thread]*3
        self.thread.expected_thread_count = 5
        self.thread.request_reboot = False
        self.thread.get_thread_counts()
        self.assertTrue(self.thread.request_reboot)
        self.thread.warning.assert_called_once()

    @patch('juham_systemstatus.systemstatus.psutil.disk_usage')
    @patch('juham_systemstatus.systemstatus.psutil.disk_partitions')
    @patch('juham_systemstatus.systemstatus.psutil.virtual_memory')
    @patch('juham_systemstatus.systemstatus.psutil.cpu_percent', return_value=[5.0])
    def test_get_system_info(self, mock_cpu, mock_mem, mock_parts, mock_usage):
        MockMemory = MagicMock(total=1000, available=800)
        mock_mem.return_value = MockMemory
        MockPartition = MagicMock(device="/dev/sda1", mountpoint="/")
        mock_parts.return_value = [MockPartition]
        MockUsage = MagicMock(total=5000, free=1000, used=4000, percent=80.0)
        mock_usage.return_value = MockUsage
        info = self.thread.get_system_info()
        self.assertEqual(info["cpu_loads"], {"cpu0": 5.0})
        self.assertEqual(info["memory"]["memory_usage"], 80.0)

    
    @patch('time.localtime')
    @patch.object(SystemStatusThread, 'reboot')
    def test_consider_reboot_not_midnight(self, mock_reboot, mock_localtime):
        self.thread.startup_time = 1000.0
        current_time = self.thread.startup_time + 4000.0
        mock_localtime.return_value = time.struct_time((2025,1,1,15,30,0,2,1,0))
        self.thread.consider_reboot(current_time)
        mock_reboot.assert_not_called()
        self.thread.warning.assert_called_once()
        self.assertIn("Delaying reboot until midnight", self.thread.warning.call_args[0][0])

    @patch.object(SystemStatusThread, 'get_system_info', return_value={"cpu_loads": {"cpu0": 5.0}})
    @patch.object(SystemStatusThread, 'get_thread_counts', return_value={"total": 5})
    @patch.object(SystemStatusThread, 'consider_reboot')
    def test_update_method(self, mock_consider, mock_threads, mock_info):
        self.thread.publish = MagicMock()
        with patch('time.time', side_effect=[1000.0,1000.1,1000.2]):
            self.thread.update()
        self.thread.publish.assert_called_once()
        mock_consider.assert_called_once()

# ------------------------ SYSTEMSTATUS TESTS ------------------------

class TestSystemStatus(unittest.TestCase):
    @patch.object(JuhamThread, '__init__', return_value=None)
    def setUp(self, mock_super_init):
        self.sys_status = SystemStatus(name="TestStatus")
        self.sys_status.worker = MagicMock(spec=SystemStatusThread)
        self.sys_status.subscribe = MagicMock()
        self.sys_status.write_point = MagicMock()
        self.sys_status.error = MagicMock()
        self.sys_status.timestamp = MagicMock(return_value=1609459200.0)
        self.sys_status.epoc2utc = MagicMock(return_value="2021-01-01T00:00:00Z")
        self.sys_status.systemstatus_topic = "test/system"

        # Mocks for super() calls
        self.sys_status._super_on_connect = MagicMock()
        self.sys_status._super_on_message = MagicMock()
        self.sys_status.name = "TestStatus"
        self.sys_status.update_interval = 5.0
        self.sys_status.location = "test_loc"
        self.sys_status.max_uptime_before_reboot = 7200.0

    def test_on_connect_success(self):
        msg = MagicMock()
        self.sys_status.on_connect(MagicMock(), None, 0, 0)
        self.sys_status.subscribe.assert_called_once_with(self.sys_status.systemstatus_topic)

    def test_on_connect_failure(self):
        msg = MagicMock()
        self.sys_status.on_connect(MagicMock(), None, 0, 5)
        self.sys_status.subscribe.assert_not_called()


    @patch.object(SystemStatus, 'instantiate')
    def test_run(self, mock_instantiate):
        mock_worker = MagicMock(spec=SystemStatusThread)
        mock_instantiate.return_value = mock_worker
        self.sys_status.worker = None
        self.sys_status.run()
        mock_instantiate.assert_called_once_with("SystemStatusThread")
        
    def test_to_dict_from_dict(self):
        data = {
            "_class": "SystemStatus",
            "_base": {},
            "_object": {},
            "systemstatus": {
                "topic": "new_system",
                "update_interval": 120.0,
                "location": "office"
            }
        }
        self.sys_status.from_dict(data)
        self.assertEqual(self.sys_status.topic, "new_system")
        dict_out = self.sys_status.to_dict()
        self.assertIn("systemstatus", dict_out)
        self.assertEqual(dict_out["systemstatus"]["topic"], "new_system")

if __name__ == '__main__':
    unittest.main()
