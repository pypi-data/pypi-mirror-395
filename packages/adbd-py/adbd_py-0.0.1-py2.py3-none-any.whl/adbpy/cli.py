import os

import click

from adbpy import ADBDevice, __version__

from .constants import VENDORID


@click.version_option(version=__version__)
@click.group(
    context_settings=dict(help_option_names=["-h", "--help"]),
)
def main():
    pass


@main.command(name="shell")
@click.option(
    "-i",
    "--info",
    help="android device connect info, e.g. 172.20.10.14:7777 or serial no.",
    required=True,
)
@click.option("-c", "--cmd", help="android shell command", required=True)
def shell(info, cmd):
    "execute shell command in android device"
    d = ADBDevice(info)
    d.connect(rsa_keys=[ADBDevice.gen_adbkey()], auth_timeout_s=0.1)
    print(d.shell(cmd))


@main.command(name="pull")
@click.option(
    "-i",
    "--info",
    help="android device connect info, e.g. 172.20.10.14:7777 or serial no.",
    required=True,
)
@click.option("-r", "--remote_path", help="path in android device", required=True)
@click.option("-l", "--local_path", help="local path", default=None)
def pull(info, remote_path, local_path):
    "pull android device's file to local"
    d = ADBDevice(info)
    d.connect(rsa_keys=[ADBDevice.gen_adbkey()], auth_timeout_s=0.1)
    if local_path is None:
        local_path = os.path.basename(remote_path)

    d.pull(remote_path, local_path)


@main.command(name="screenshot")
@click.option(
    "-i",
    "--info",
    help="android device connect info, e.g. 172.20.10.14:7777 or serial no.",
    required=True,
)
@click.option(
    "-f", "--file", help="local screenshot file path", default="screenshot.png"
)
def screenshot(info, file):
    "get android device's screenshot and save to local"
    d = ADBDevice(info)
    d.connect(rsa_keys=[ADBDevice.gen_adbkey()], auth_timeout_s=0.1)
    d.screenshot(filename=file)

@main.command(name="click")
@click.option(
    "-i",
    "--info",
    help="android device connect info, e.g. 172.20.10.14:7777 or serial no.",
    required=True,
)
@click.option("-x", "--axisx", help="x-axis", default=0)
@click.option("-y", "--axisy", help="x-axis", default=0)
def adb_click(info, axisx, axisy):
    "click the axis in screen"
    d = ADBDevice(info)
    d.connect(rsa_keys=[ADBDevice.gen_adbkey()], auth_timeout_s=0.1)
    d.click(axisx, axisy)


@main.command(name="devices")
def devices():
    "get android device's serial no."
    try:
        import usb1
    except ImportError:
        click.echo(
            click.style(
                "To enable USB support you must install this package via `pip install adb-py[usb]`",
                fg="red",
                bold=True,
            )
        )
        return

    with usb1.USBContext() as context:
        for device in context.getDeviceList(skip_on_error=True):
            if VENDORID.get(device.getVendorID()):
                click.echo(click.style(device.getSerialNumber(), fg="cyan", bold=True))
