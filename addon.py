import xbmc, xbmcaddon, xbmcgui
import sys, os

osmc_net = xbmcaddon.Addon('script.module.osmcsetting.networking')
sys.path.append(xbmc.translatePath( os.path.join(osmc_net.getAddonInfo('path'), 'resources', 'lib')))

from osmc_bluetooth import is_bluetooth_available,toggle_bluetooth_state,is_bluetooth_enabled, connect_device, is_device_connected, disconnect_device

device_conn = "C4:B3:01:E5:44:C0"

def log(message):
    xbmc.log("### " + str(message), level=xbmc.LOGNOTICE)

log("Funguje!" + str(sys.argv))

# log(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettings", "params":{"level": "expert", "filter":{"id":"audiooutput.audiodevice"}},"id":1}'))
# log(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"audiooutput.audiodevice"},"id":1}'))

if sys.argv[1] == "toggle":
        dialog = xbmcgui.Dialog()
        log("Available: " + str(is_bluetooth_available()))
        log("Enabled: " + str(is_bluetooth_enabled()))
        if is_device_connected(device_conn):
                dialog.notification("Bluetooth se vypina..", "Disconneting..")
                disconnect_device(device_conn)
        log(toggle_bluetooth_state(not is_bluetooth_enabled()))
        log("Enabled: " + str(is_bluetooth_enabled()))
        if is_bluetooth_enabled():
                dialog.notification("Bluetooth pusteno..", "Conneting..")
                result = connect_device(device_conn)
                log("Connect: " + str(result))
                dialog.notification("Bluetooth pusteno..", "Vysledek spojeni: " + str(result) + ". Output na ALSA")
                device_name = 'ALSA:pulse'
        else:
                dialog.notification("Bluetooth vypnuto..", "Output na HDMI")
                device_name = 'PI:HDMI'
        log(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"audiooutput.audiodevice","value":"' + device_name + '"},"id":1}'))
