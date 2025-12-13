import os
import re
from dataclasses import dataclass
from io import BytesIO
from typing import NamedTuple, Optional

from adb_shell import constants, exceptions
from adb_shell.adb_device import AdbDevice, _open_bytesio
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.constants import DEFAULT_READ_TIMEOUT_S
from adb_shell.hidden_helpers import _FileSyncTransactionInfo
from adb_shell.transport.tcp_transport import TcpTransport
from PIL import Image, UnidentifiedImageError

try:
    from adb_shell.transport.usb_transport import UsbTransport
except (ImportError, OSError):
    UsbTransport = None

from .exceptions import AdbError


class WindowSize(NamedTuple):
    width: int
    height: int


@dataclass
class RunningAppInfo:
    package: str
    activity: str
    pid: int = 0


class XsharkADBDevice(AdbDevice):
    def __call__(self, *args, **kwds):
        return self

    def pull(
        self,
        device_path,
        local_path,
        progress_callback=None,
        transport_timeout_s=None,
        read_timeout_s=DEFAULT_READ_TIMEOUT_S,
    ):
        if not device_path:
            raise exceptions.DevicePathInvalidError(
                "Cannot pull from an empty device path"
            )
        if not self.available:
            raise exceptions.AdbConnectionError(
                "ADB command not sent because a connection to the device has not been established."
                "  (Did you call `AdbDevice.connect()`?)"
            )

        opener = _open_bytesio if isinstance(local_path, BytesIO) else open
        with opener(local_path, "wb") as stream:
            adb_info = self._open(b"sync:", transport_timeout_s, read_timeout_s, None)
            filesync_info = _FileSyncTransactionInfo(
                constants.FILESYNC_PULL_FORMAT, maxdata=self._maxdata
            )

            try:
                self._pull(
                    device_path, stream, progress_callback, adb_info, filesync_info
                )
            finally:
                # self._clse(adb_info)
                pass

    def _screenshot(self, display_id: Optional[int] = None) -> Image.Image:
        try:
            cmd = "screencap -p"
            if display_id is not None:
                _id = self._get_real_display_id(display_id)
                cmd += f" -d {_id}"

            png_bytes = self.shell(cmd, decode=False)
            pil_image = Image.open(BytesIO(png_bytes))
            if pil_image.mode == "RGBA":
                pil_image = pil_image.convert("RGB")

            return pil_image
        except UnidentifiedImageError as e:
            raise AdbError("screencap error") from e

    def _get_real_display_id(self, display_id: int) -> str:
        # adb shell dumpsys SurfaceFlinger --display-id
        # Display 4619827259835644672 (HWC display 0): port=0 pnpId=GGL displayName="EMU_display_0"
        output = self.shell("dumpsys SurfaceFlinger --display-id")
        _RE = re.compile(r"Display (\d+) ")
        ids = _RE.findall(output)
        if not ids:
            raise AdbError(
                "No display found, debug with 'dumpsys SurfaceFlinger --display-id'"
            )

        if display_id >= len(ids):
            raise AdbError("Invalid display_id", display_id)

        return ids[display_id]

    def screenshot(
        self,
        filename: Optional[str] = None,
        format="pillow",
        display_id: Optional[int] = None,
    ):
        pil_img = self._screenshot()
        if filename:
            pil_img.save(filename)
            return

        if format == "pillow":
            return pil_img
        elif format == "opencv":
            pil_img = pil_img.convert("RGB")
            import cv2
            import numpy as np

            return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        elif format == "raw":
            return pil_img.tobytes()

    def rotation(self) -> int:
        for line in self.shell("dumpsys display").splitlines():
            m = re.search(r".*?orientation=(?P<orientation>\d+)", line)
            if not m:
                continue

            o = int(m.group("orientation"))
            return int(o)

        raise AdbError("rotation get failed")

    def _wm_size(self) -> WindowSize:
        output = self.shell("wm size")
        o = re.search(r"Override size: (\d+)x(\d+)", output)
        if o:
            w, h = o.group(1), o.group(2)
            return WindowSize(int(w), int(h))

        m = re.search(r"Physical size: (\d+)x(\d+)", output)
        if m:
            w, h = m.group(1), m.group(2)
            return WindowSize(int(w), int(h))

        raise AdbError("wm size output unexpected", output)

    def window_size(self) -> WindowSize:
        wsize = self._wm_size()
        horizontal = self.rotation() % 2 == 1
        return WindowSize(wsize.height, wsize.width) if horizontal else wsize

    def app_current(self) -> RunningAppInfo:
        _focusedRE = re.compile(
            r"mCurrentFocus=Window{.*\s+(?P<package>[^\s]+)/(?P<activity>[^\s]+)\}"
        )
        m = _focusedRE.search(self.shell("dumpsys window windows"))
        if m:
            return RunningAppInfo(
                package=m.group("package"), activity=m.group("activity")
            )

        # search mResumedActivity
        # https://stackoverflow.com/questions/13193592/adb-android-getting-the-name-of-the-current-activity
        package = None
        output = self.shell("dumpsys activity activities")
        _recordRE = re.compile(
            r"mResumedActivity: ActivityRecord\{.*?\s+(?P<package>[^\s]+)/(?P<activity>[^\s]+)\s.*?\}"
        )
        m = _recordRE.search(output)
        if m:
            package = m.group("package")

        # try: adb shell dumpsys activity top
        _activityRE = re.compile(
            r"ACTIVITY (?P<package>[^\s]+)/(?P<activity>[^/\s]+) \w+ pid=(?P<pid>\d+)"
        )
        output = self.shell("dumpsys activity top")
        ms = _activityRE.finditer(output)
        ret = None
        for m in ms:
            ret = RunningAppInfo(
                package=m.group("package"),
                activity=m.group("activity"),
                pid=int(m.group("pid")),
            )
            if ret.package == package:
                return ret

        if ret:
            return ret

        raise AdbError("Couldn't get focused app")

    def dump_hierarchy(self) -> str:
        target = "/sdcard/tmp/uidump.xml"
        output = self.shell(f"rm -f {target};uiautomator dump {target} && echo success")
        if "ERROR" in output or "success" not in output:
            raise AdbError("uiautomator dump failed", output)

        local = os.path.join("/tmp", os.path.basename(target))
        if os.path.exists(local):
            os.remove(local)

        self.pull(target, local)
        with open(local, "r") as f:
            return f.read()

    def click(self, x, y):
        self.shell(f"input tap {x} {y}")
        print(f"click axis ({x}, {y})")


class XsharkAdbDeviceTcp(XsharkADBDevice):
    def __init__(self, host, port=5555, default_transport_timeout_s=None, banner=None):
        transport = TcpTransport(host, port)
        super(XsharkAdbDeviceTcp, self).__init__(
            transport, default_transport_timeout_s, banner
        )


class XsharkAdbDeviceUSB(XsharkADBDevice):
    def __init__(
        self, serial=None, port_path=None, default_transport_timeout_s=None, banner=None
    ):
        if UsbTransport is None:
            raise exceptions.InvalidTransportError(
                "To enable USB support you must install this package via `pip install adb-py[usb]`"
            )

        transport = UsbTransport.find_adb(
            serial, port_path, default_transport_timeout_s
        )
        super(XsharkAdbDeviceUSB, self).__init__(
            transport, default_transport_timeout_s, banner
        )


class ADBDevice:
    def __new__(self, info: str, **kwargs) -> None:
        match = re.match(r"(\d+\.\d+\.\d+\.\d+):(\d+)", info, re.I)
        if match:
            return XsharkAdbDeviceTcp(
                match.group(1), port=int(match.group(2)), **kwargs
            )
        else:
            return XsharkAdbDeviceUSB(serial=info, **kwargs)

    @classmethod
    def gen_adbkey(cls) -> PythonRSASigner:
        home = os.path.join(os.path.expanduser("~"), ".config", "adbkey")
        if not os.path.exists(home):
            os.makedirs(home)

        adbkey = os.path.join(home, "adbkey")
        adbpubkey = os.path.join(home, "adbkey.pub")
        if not os.path.exists(adbkey):
            keygen(adbkey)

        with open(adbkey, "r") as f:
            priv = f.read()

        with open(adbpubkey, "r") as f:
            pub = f.read()

        return PythonRSASigner(pub, priv)
