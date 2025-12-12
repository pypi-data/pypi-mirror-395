import libifstate.exception
from libifstate.log import logger, IfStateLogging
import pyroute2
from pyroute2 import IPRoute, IW, NetNS

from pyroute2 import NetlinkError

try:
    # pyroute2 <0.6
    from pyroute2.ethtool.ioctl import SIOCETHTOOL
except ModuleNotFoundError:
    # pyroute2 >= 0.6
    from pr2modules.ethtool.ioctl import SIOCETHTOOL

import atexit
import socket
import fcntl
import re
import struct
import subprocess
import array
import struct
import tempfile
import typing
import os
import yaml

def _get_of_node(netns, link):
    if netns.netns is not None:
        pyroute2.netns.pushns(netns.netns)

    try:
        return os.path.relpath(os.path.realpath(f"{netns.ipr.sysfs_path}/class/net/{link.get_attr('IFLA_IFNAME')}/of_node", strict=True), start=f"{netns.ipr.sysfs_path}/firmware/devicetree")
    except FileNotFoundError:
        return None
    finally:
        if netns.netns is not None:
            pyroute2.netns.popns()

IDENTIFY_LOOKUPS = {
    "perm_address": lambda netns, link: link.get_attr("IFLA_PERM_ADDRESS"),
    "parent_dev_name": lambda netns, link: link.get_attr("IFLA_PARENT_DEV_NAME"),
    "parent_dev_bus_name": lambda netns, link: link.get_attr("IFLA_PARENT_DEV_BUS_NAME"),
    "phys_port_id": lambda netns, link: link.get_attr("IFLA_PHYS_PORT_ID"),
    "phys_port_name": lambda netns, link: link.get_attr("IFLA_PHYS_PORT_NAME"),
    "phys_switch_id": lambda netns, link: link.get_attr("IFLA_PHYS_SWITCH_ID"),
    "of_node": _get_of_node,
}


REGEX_ETHER_BYTE = re.compile('[a-f0-9]{2}')

RUN_BASE_DIR = '/run/libifstate'

root_ipr = typing.NewType("IPRouteExt", IPRoute)

def filter_ifla_dump(showall, ifla, defaults, prefix="IFLA"):
    dump = {}

    for key, default_value in defaults.items():
        current_value = next(iter(ifla.get_attrs("_".join((prefix, key.upper())))), None)

        if current_value is not None:
            if showall or default_value is None or default_value != current_value:
                dump[key] = current_value

    return dump

def format_ether_address(address):
    """
    Formats a ether address string canonical. Accepted formats:

      xx:xx:xx:xx:xx:xx
      xx-xx-xx-xx-xx-xx
      xxxx.xxxx.xxxx

    The hex digits may be lower and upper case.
    """

    return ':'.join(REGEX_ETHER_BYTE.findall(address.lower()))


def get_run_dir(function, *args):
    """
    Returns a deterministic directory under /run/libifstate for saving state
    informations between ifstate calls. A hierarchy is build from the ifstate
    function and additional distinguishers (i.e. ifname).
    
    The directory will be created if it does not already exists.
    """

    run_dir = os.path.join(RUN_BASE_DIR, function, *args)
  
    try:
        os.makedirs(run_dir, mode=0o700)
    except FileExistsError:
        pass

    return run_dir

def get_netns_run_dir(function, netns, *args):
    """
    Returns a deterministic directory under /run/libifstate for saving state
    informations between ifstate calls. A hierarchy is build from the ifstate
    function, the netns and optional additional distinguishers (i.e. ifname).
    
    The directory will be created if it does not already exists.
    """

    if netns.netns is None:
        run_dir = os.path.join(RUN_BASE_DIR, function, 'root', *args)
    else:
        run_dir = os.path.join(RUN_BASE_DIR, function, 'netns', netns.netns, *args)

    try:
        os.makedirs(run_dir, mode=0o700)
    except FileExistsError:
        pass

    return run_dir

def dump_yaml_file(fn, obj, opener=None):
    """
    Dump obj to a YAML file, create directories if needed and catch file
    I/O errors.
    """
    try:
        os.makedirs(os.path.dirname(fn), mode=0o700)
    except FileExistsError:
        pass

    try:
        with open(fn, "w", opener=opener) as fh:
            yaml.dump(obj, fh)
    except OSError as err:
        logger.error('Writing {} failed: {}'.format(fn, err))

def slurp_yaml_file(fn, default=None):
    """
    Read the content of a YAML file, returns *default* if the file could not be
    found, read or parsed.
    """
    try:
        with open(fn) as fh:
            return yaml.load(fh, Loader=yaml.SafeLoader)
    except OSError as err:
        logger.debug('Reading {} failed: {}'.format(fn, err))
    except yaml.YAMLError as err:
        logger.warning('Parsing {} failed: {}'.format(fn, err))

    return default

def kind_has_identify(kind):
    """
    Return True if the interface kind can be identified by some unique
    properties. These are all types of physical interfaces.
    """
    return kind is None or kind in ['dsa']

def cmp_fields(r1, r2, fields, indent):
    """
    Return True if both dicts r1 and r2 contains the same values for the
    keys in fields.
    """
    for fld in fields:
        if not indent is None:
            logger.debug("{}: {} - {}".format(fld, r1.get(fld), r2.get(fld)), extra={'iface': indent})
        if fld in r1 and fld in r2:
            if r1[fld] != r2[fld]:
                return False
        elif fld in r1 or fld in r2:
            return False
    return True

class IPRouteExt(IPRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sysfs_path = "/sys"

    def get_ifname_by_index(self, index):
        link = next(iter(self.get_links(index)), None)

        if link is None:
            return index

        return link.get_attr('IFLA_IFNAME')

    def get_link(self, *argv, **kwarg):
        '''
        Returns the first link info by wrapping a `get_links()` call and return
        `None` rather than raising any pyroute2 netlink exception on error.
        '''
        try:
            return next(iter(self.get_links(*argv, **kwarg)), None)
        except Exception as err:
            if not isinstance(err, libifstate.exception.netlinkerror_classes):
                raise

        return None

class NetNSExt(NetNS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # pyroute 0.9.1+
        # workaround: netns property was moved into the status dict
        if not hasattr(self, "netns"):
            assert(hasattr(self, "status"))
            self.netns = self.status["netns"]

        try:
            pyroute2.netns.pushns(self.netns)
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            os.makedirs("/run/libifstate/sysfs", exist_ok=True)
            self.sysfs_path = tempfile.mkdtemp(prefix=self.netns, dir="/run/libifstate/sysfs")
            rc = subprocess.run(['mount', '', self.sysfs_path, '-t', 'sysfs', '-o', 'ro,nosuid,nodev,noexec,noatime'])
            if rc.returncode != 0:
                logger.warning("Could not mount netns sysfs: {rc.stderr}")
            else:
                logger.debug('mounted sysfs for {} at {}'.format(self.netns, self.sysfs_path), extra={'netns': self.netns})
                atexit.register(self.umount_sysfs)
        finally:
            pyroute2.netns.popns()

    def umount_sysfs(self):
            rc = subprocess.run(['umount', self.sysfs_path, '-t', 'sysfs'])
            if rc.returncode != 0:
                logger.warning("Could not umount netns sysfs: {rc.stderr}")
            else:
                logger.debug('umounted sysfs for {} at {}'.format(self.netns, self.sysfs_path), extra={'netns': self.netns})

            try:
                os.rmdir(self.sysfs_path)
            except OSError:
                pass

    def get_ifname_by_index(self, index):
        link = next(iter(self.get_links(index)), None)

        if link is None:
            return index

        return link.get_attr('IFLA_IFNAME')

    def get_link(self, *argv, **kwarg):
        '''
        Returns the first link info by wrapping a `get_links()` call and return
        `None` rather than raising any pyroute2 netlink exception on error.
        '''
        try:
            return next(iter(self.get_links(*argv, **kwarg)), None)
        except Exception as err:
            if not isinstance(err, libifstate.exception.netlinkerror_classes):
                raise

        return None

class LinkDependency:
    def __init__(self, ifname, netns):
        self.ifname = ifname
        self.netns = netns

    def __hash__(self):
        return hash((self.ifname, self.netns))

    def __eq__(self, other):
        return (self.ifname, self.netns) == (other.ifname, other.netns)

    def __lt__(self, obj):
        if self.netns is None:
            if obj.netns is not None:
                return True
        elif obj.netns is None:
            return False

        if self.netns != obj.netns:
            return self.netns < obj.netns

        if self.ifname == obj.ifname:
            return False

        if self.ifname == 'lo':
            return True

        if obj.ifname == 'lo':
            return False

        return self.ifname < obj.ifname

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        if self.netns is None:
            return "{}".format(self.ifname)
        else:
            return "{}[netns={}]".format(self.ifname, self.netns)


root_ipr = IPRouteExt()
try:
    root_iw = IW()
except NetlinkError:
    root_iw = None
