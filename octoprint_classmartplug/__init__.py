from __future__ import absolute_import, unicode_literals
import octoprint.plugin
import time
import broadlink

class ClasSmartPlugin(octoprint.plugin.StartupPlugin, 
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.SimpleApiPlugin):
    
    def on_after_startup(self):
        self._logger.info("Wassup my n-words bbbbb?")
        self.devices = broadlink.discover(timeout=5, discover_ip_address='192.168.1.255')
        for device in self.devices:
            if device.name.startswith(self._settings.get(["name"])):
                self.unit = device
        self.unit.auth()
        self._logger.info(f"Added unit: {self.unit}")
        self.powered = self.unit.check_power()

    def get_api_commands(self):
        return dict(
            turnOn=[],
            turnOff=[]
        )

    def on_api_get(self, request):
        self.toggle()

    def get_settings_defaults(self):
        return dict(name="Roger")

    def get_assets(self):
        return dict(
            js=["js/ClasSmartPlugin.js"]
        )

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]
    
    def toggle(self):
        self.powered = not self.powered
        self._logger.info("Toggled baby, ", self.powered)
        self.unit.set_power(self.powered)
        if self.powered:
            time.sleep(10)
            self._printer.connect()


__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = ClasSmartPlugin()