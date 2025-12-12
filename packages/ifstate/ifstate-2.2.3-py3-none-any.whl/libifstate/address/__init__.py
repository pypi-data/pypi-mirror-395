from libifstate.util import logger, IfStateLogging, cmp_fields
from libifstate.exception import netlinkerror_classes
from libifstate.routing import RTLookups
from ipaddress import ip_interface, ip_network
from pyroute2.netlink.rtnl.ifaddrmsg import IFA_F_DADFAILED, IFA_F_PERMANENT
import re

RE_MOD_EU64_LLA = re.compile(r'fe80:0000:0000:0000:[0-9a-f]{4}:[0-9a-f]{2}ff:fe[0-9a-f]{2}:[0-9a-f]{4}/64')

class AddressIgnore():
    def __init__(self, address):
        self.match_mod_eui64 = False
        self.prefix = None
        self.attrs = {}

        if type(address) is str:
            self.prefix = ip_network(address)
        else:
            if 'prefix' in address:
                # special hack to allow to regex… for Linux'
                # inconsistent LLA handling: it seems to not
                # always set the kernel_ll proto reliable :-(
                if address['prefix'] == '__MATCH_MOD_EU64_LLA__':
                    self.match_mod_eui64 = True
                else:
                    self.prefix = ip_network(address["prefix"])

            for k, v in address.items():
                if k in ["address", "prefix"]:
                    continue

                if k == "proto":
                    self.attrs[k] = RTLookups.addrprotos.lookup_id(v)
                if k == "scope":
                    self.attrs[k] = RTLookups.scopes.lookup_id(v)
                else:
                    self.attrs[k] = v

    def matches(self, ip, attrs:dict, indent:str=None)->bool:
        # hack: match for a pattern
        if self.match_mod_eui64:
            if not RE_MOD_EU64_LLA.match(ip.exploded):
                return False

        # match for a prefix
        if self.prefix:
            if not ip in self.prefix:
                return False

        # Do we have additional attributes to match?
        if self.attrs:
            return cmp_fields(attrs, self.attrs, self.attrs.keys(), indent)

        return True

def parse_address(address, implicit_proto:bool=True)->dict:
    if type(address) is str:
        ip = address
    elif 'address' in address:
        ip = address["address"]
    else:
        ip = None

    if ip is None:
        addr = {
        }
    else:
        ip = ip_interface(ip)
        addr = {
            "address": str(ip.ip),
            "prefixlen": ip.network.prefixlen,
        }

    if implicit_proto:
        addr["proto"] = 0

    if type(address) is dict:
        for k, v in address.items():
            if k == "address":
                continue

            if k == "proto":
                addr[k] = RTLookups.addrprotos.lookup_id(v)
            if k == "scope":
                addr[k] = RTLookups.scopes.lookup_id(v)
            else:
                addr[k] = v

    return (ip, addr)

class Addresses():
    def __init__(self, netns, iface, addresses):
        self.netns = netns
        self.iface = iface
        self.addresses = {}
        for address in addresses:
            (ip, addr) = parse_address(address, iface != "lo")
            self.addresses[ip] = addr

    def apply(self, ignores, ign_dynamic, do_apply):
        logger.debug('getting addresses', extra={'iface': self.iface, 'netns': self.netns})

        # get ifindex
        idx = next(iter(self.netns.ipr.link_lookup(ifname=self.iface)), None)

        # check if interface exists
        if idx == None:
            return

        # get active ip addresses
        ipr_addr = {}
        addr_add = []
        addr_renew = []
        for addr in self.netns.ipr.get_addr(index=idx):
            flags = addr.get_attr('IFA_FLAGS', 0)
            ip = ip_interface(addr.get_attr('IFA_ADDRESS') +
                              '/' + str(addr['prefixlen']))
            ipr_addr[ip] = addr
            if flags & IFA_F_DADFAILED == IFA_F_DADFAILED:
                logger.debug('{} has failed dad'.format(ip), extra={'iface': self.iface, 'netns': self.netns})
                addr_renew.append(ip)
            else:
                if ip in self.addresses:
                    for k, v in self.addresses[ip].items():
                        # don't check address info again
                        if k in ['address', 'prefixlen']:
                            continue

                        # pyroute2's ip.get_attr does not handle attribute naming, do it manually
                        attr_name = f'IFA_{k.upper()}'

                        # proto 0 means no proto should be set in the kernel (unspec)
                        if k == 'proto' and not v and addr.get_attr(attr_name) is None:
                            continue

                        # continue if the expected value just matches
                        if addr.get_attr(attr_name) == v:
                            continue

                        # lets read the address as the attribute value is different
                        logger.debug('{}.{} {} != {}'.format(ip, k, addr.get_attr(f'IFA_{k.upper()}'), v), extra={'iface': self.iface, 'netns': self.netns})
                        addr_renew.append(ip)
                        break

        # get addresses to be added
        for addr in self.addresses.keys():
            if addr in ipr_addr and addr not in addr_renew:
                logger.log_ok('addresses', '= {}'.format(addr.with_prefixlen))
                del ipr_addr[addr]
            else:
                addr_add.append(addr)
                for ip in ipr_addr.keys():
                    if addr.ip == ip.ip:
                        addr_renew.append(ip)
                        break

        for ip, addr in ipr_addr.items():
            # skip ignored IP addresses
            ignore = False
            for iaddr in ignores:
                if iaddr.matches(ip, addr, self.iface):
                    ignore = True
                    break

            if ip in addr_renew or not ignore:
                if not ign_dynamic or ipr_addr[ip]['flags'] & IFA_F_PERMANENT == IFA_F_PERMANENT:
                    logger.log_del('addresses', '- {}'.format(ip.with_prefixlen))
                    try:
                        kv = {
                            'index': idx,
                            'address': str(ip.ip),
                            'prefixlen': ip.network.prefixlen,
                        }
                        local = addr.get_attr('IFA_LOCAL')
                        if local:
                            kv["local"] = local
                        logger.debug('ip address del: {}'.format(
                            ' '.join(f'{k}={v}' for k, v in kv.items())))
                        if do_apply:
                            self.netns.ipr.addr("del", **kv)
                    except Exception as err:
                        if not isinstance(err, netlinkerror_classes):
                            raise
                        logger.warning('removing ip {}/{} failed: {}'.format(
                            str(ip.ip), ip.network.prefixlen, err.args[1]))

        # (re)add configured addresses
        for addr in addr_add:
            logger.log_change('addresses', f'+ {addr.with_prefixlen}')
            logger.debug('ip address add: {}'.format(
                ' '.join(f'{k}={v}' for k, v in self.addresses[addr].items())))
            if do_apply:
                try:
                    self.netns.ipr.addr("add", index=idx, **(self.addresses[addr]))
                except Exception as err:
                    if not isinstance(err, netlinkerror_classes):
                        raise
                    logger.warning('adding ip {}/{} failed: {}'.format(
                        str(addr.ip), addr.network.prefixlen, err.args[1]))
