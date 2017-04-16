import xbmc, xbmcaddon, xbmcgui
import sys, os, time

if sys.version_info < (2, 7):
    import simplejson as json
else:
    import json

osmc_net = xbmcaddon.Addon('script.module.osmcsetting.networking')
sys.path.append(xbmc.translatePath( os.path.join(osmc_net.getAddonInfo('path'), 'resources', 'lib')))

from osmc_bluetooth import is_bluetooth_available,toggle_bluetooth_state,is_bluetooth_enabled, connect_device, is_device_connected, disconnect_device

default_audio_device = "PI:HDMI"
bluetooth_audio_device = "ALSA:pulse"
connected_bt_device_addr = "C4:B3:01:E5:44:C0"
max_connect_attempt_count = 5
sleep_time_after_turn_on = 2
sleep_time_between_attemps = 5

dialog = xbmcgui.Dialog()

def log(message):
    xbmc.log("### " + str(message), level=xbmc.LOGNOTICE)

def show_notification(heading, message = "", time = 1000):
    dialog.notification(heading,message,xbmcgui.NOTIFICATION_INFO,time)

def get_current_audio_device():
    return json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"audiooutput.audiodevice"},"id":1}'))["result"]["value"]

def change_audio_device(device_name):
    return json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"audiooutput.audiodevice","value":"' + device_name + '"},"id":1}'))["result"]

if ((is_device_connected(connected_bt_device_addr) and get_current_audio_device() == bluetooth_audio_device)):
    log("Device connected, disconnecting")
    show_notification("Disconnecting device")
    disconnect_device(connected_bt_device_addr)
else:
    log("Device not connected, starting connecting")
    if is_bluetooth_enabled() == False:
        log("Bluetooth turn on")
        show_notification("Bluetooth", "Turning on")
        toggle_bluetooth_state(True)
        time.sleep(sleep_time_after_turn_on)
    if is_device_connected(connected_bt_device_addr) == False:
        for attempt in range(max_connect_attempt_count):
            log("Connecting to device:" + str(connected_bt_device_addr))
            show_notification("Connecting to device",str(attempt+1) + ". try")
            connect_result = connect_device(connected_bt_device_addr)
            if (connect_result or is_device_connected(connected_bt_device_addr)):
                log("Device connected!")
                show_notification("Connecting to device","Successfully connected")
                break
            time.sleep(sleep_time_between_attemps)

if is_device_connected(connected_bt_device_addr) == True:
    log("Device connected, checking output")
    if get_current_audio_device() != bluetooth_audio_device:
        log("Changing output to " + str(bluetooth_audio_device))
        show_notification("Audio device", "Changing to: " + bluetooth_audio_device)
        change_audio_device(bluetooth_audio_device)
else:
    if is_bluetooth_enabled() == True:
        log("Bluetooth turn off")
        show_notification("Bluetooth", "Turning off")
        toggle_bluetooth_state(False)
    if get_current_audio_device() != default_audio_device:
        log("Changing output to " + str(default_audio_device))
        show_notification("Audio device", "Changing to: " + default_audio_device)
        change_audio_device(default_audio_device)

# if sys.argv[1] == "toggle":
