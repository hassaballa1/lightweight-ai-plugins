import unittest

from core.orchestrator import Orchestrator
from core.plugin_manager import discover_plugins, load_plugin
from core.resource_selector import decide
from interfaces.monitor_interface import SystemStatus


def status(cpu=20.0, ram=8.0, battery=None, gpu=False):
    return SystemStatus(cpu_percent=cpu, available_ram_gb=ram, battery_percent=battery, gpu_available=gpu)


class DecideTests(unittest.TestCase):
    def test_low_battery_is_light(self):
        self.assertEqual(decide(status(battery=20, gpu=True)), "light")

    def test_low_ram_is_light(self):
        self.assertEqual(decide(status(ram=1.5)), "light")

    def test_high_cpu_is_light(self):
        self.assertEqual(decide(status(cpu=95)), "light")

    def test_gpu_with_headroom_is_heavy(self):
        self.assertEqual(decide(status(gpu=True, battery=90)), "heavy")

    def test_otherwise_medium(self):
        self.assertEqual(decide(status()), "medium")
        self.assertEqual(decide(status(gpu=True, cpu=70)), "medium")


class PluginTests(unittest.TestCase):
    def test_all_tiers_discovered(self):
        self.assertEqual(set(discover_plugins()), {"light", "medium", "heavy"})

    def test_dummy_run(self):
        plugin = load_plugin("medium")
        plugin.load_model()
        self.assertEqual(plugin.run("x")["model"], "medium")

    def test_unknown_plugin(self):
        with self.assertRaises(ValueError):
            load_plugin("giant")

    def test_orchestrator_swaps(self):
        orch = Orchestrator()
        self.assertEqual(orch.ensure_plugin("light").name, "light")
        self.assertEqual(orch.ensure_plugin("heavy").name, "heavy")
        orch.reload()
        self.assertEqual(orch.plugin.name, "heavy")


if __name__ == "__main__":
    unittest.main()
