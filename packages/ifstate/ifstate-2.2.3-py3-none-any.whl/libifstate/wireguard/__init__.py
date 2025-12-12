from libifstate.util import logger, IfStateLogging
from libifstate.exception import netlinkerror_classes, FeatureMissingError
import ipaddress
import collections
from copy import deepcopy
import os
import pyroute2
import pyroute2.netns
from pyroute2 import NetlinkError
import socket
from urllib.parse import urlparse

DEFAULT_PORT = 51820
SECRET_SETTINGS = ['private_key', 'preshared_key']

class WireGuard():
    def __init__(self, netns, iface, wireguard):
        self.netns = netns
        self.iface = iface
        self.wireguard = wireguard

        if self.netns.netns is not None:
            pyroute2.netns.pushns(self.netns.netns)

        try:
            self.wg = pyroute2.WireGuard()
        finally:
            if self.netns.netns is not None:
                pyroute2.netns.popns()

        if 'private_key' in wireguard:
            wireguard['private_key'] = wireguard['private_key'].encode('ascii')

        # prepare peer settings to match rtnetlink representation
        peer_routes = []
        if 'peers' in self.wireguard:
            for peer, opts in self.wireguard['peers'].items():
                if 'preshared_key' in opts:
                    opts['preshared_key'] = opts['preshared_key'].encode('ascii')
                if 'allowedips' in opts:
                    opts['allowedips'] = set(
                        [str(ipaddress.ip_network(ip)) for ip in opts['allowedips']])
                    peer_routes.extend(opts['allowedips'])
                if 'endpoint' in opts:
                    url = urlparse("//" + opts['endpoint'])
                    del(opts['endpoint'])
                    try:
                        (family, *ignore, sockaddr) = socket.getaddrinfo(url.hostname, url.port or DEFAULT_PORT)[0]
                        opts['endpoint'] = {'family': int(family)}
                        for i, field in enumerate({
                            socket.AF_INET: ('addr', 'port'),
                            socket.AF_INET6: ('addr', 'port', 'flowinfo', 'scope_id'),
                        }[family]):
                            opts['endpoint'][field] = sockaddr[i]
                        if family == socket.AF_INET:
                            opts['endpoint']['__pad'] = ()
                    except Exception as err:
                        logger.warn(f"ignore failed peer endpoint lookup {url.hostname}: {err}")
                        
            self.wireguard['peers'] = {k.encode('ascii'): v for k, v in self.wireguard['peers'].items()}

        # add peer routes on demand
        self.routes = []
        table = self.wireguard.get('table')
        if table is not None and peer_routes:
            for route in set(peer_routes):
                self.routes.append({
                    'to': route,
                    'dev': self.iface,
                    'table': table,
                })
        if 'table' in self.wireguard:
            del (self.wireguard['table'])

    def get_routes(self) -> list:
        '''
        Returns a list of route definitions derived from the configured peers allowedips setting.
        '''
        return self.routes

    def __deepcopy__(self, memo):
        '''
        Add custom deepcopy implementation to keep single WireGuard instances.
        '''
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == 'wg':
                if self.netns.netns is not None:
                    pyroute2.netns.pushns(self.netns.netns)

                try:
                    setattr(result, k, pyroute2.WireGuard())
                finally:
                    if self.netns.netns is not None:
                        pyroute2.netns.popns()
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def _do_peer_apply(self, action, public_key, opts):
        try:
            peer = {k: v for k, v in opts.items() if k != 'allowedips'}
            peer['public_key'] = public_key
            if 'allowedips' in opts:
                peer['allowed_ips'] = opts['allowedips']
                peer['replace_allowed_ips'] = True
            if 'endpoint' in opts:
                peer['endpoint_addr'] = opts['endpoint']['addr']
                peer['endpoint_port'] = opts['endpoint']['port']
            if 'persistent_keepalive_interval' in opts:
                peer['persistent_keepalive'] = opts['persistent_keepalive_interval']

            self.wg.set(self.iface, peer=peer)
        except netlinkerror_classes as err:
            logger.warning('{} peer to {} failed: {}'.format(
                action, self.iface, err.args[1]))

    def apply(self, do_apply):
        # get kernel's wireguard settings for the interface
        try:
            infos = self.wg.info(self.iface)
        except NetlinkError as err:
            logger.warning('query wireguard details failed: {}'.format(
                os.strerror(err.code)), extra={'iface': self.iface, 'netns': self.netns})
            return

        # check base settings (not the peers, yet)
        has_changes = False
        for setting in [x for x in self.wireguard.keys() if x != 'peers']:
            # find first occurence of attr
            current = None
            for info in infos:
                current = info.get_attr(f"WGDEVICE_A_{setting.upper()}")
                if current is not None:
                    break

            logger.debug('  %s: %s => %s', setting, current,
                         self.wireguard[setting], extra={'iface': self.iface})
            has_changes |= self.wireguard[setting] != current

        if has_changes:
            logger.log_change('wireguard')
            if do_apply:
                try:
                    self.wg.set(
                        self.iface, **{k: v for k, v in self.wireguard.items() if k != "peers"})
                except NetlinkError as err:
                    logger.warning('updating iface {} failed: {}'.format(
                        self.iface, err.args[1]))
        else:
            logger.log_ok('wireguard')

        # check peers list if provided
        if 'peers' in self.wireguard:
            peers = {
                peer.get_attr("WGPEER_A_PUBLIC_KEY"): peer
                for info in infos
                for peer in info.get('WGDEVICE_A_PEERS') or []
            }
            has_pchanges = False

            avail = []
            for public_key, opts in self.wireguard['peers'].items():
                avail.append(public_key)
                if public_key not in peers:
                    has_pchanges = True
                    if do_apply:
                        self._do_peer_apply('add', public_key, opts)
                else:
                    pchange = False
                    for setting in opts.keys():
                        attr = peers[public_key].get_attr(f"WGPEER_A_{setting.upper()}", [])
                        if setting == 'allowedips':
                            attr = set(ip['addr'] for ip in attr)
                        logger.debug('  peer.%s: %s => %s', setting, attr,
                                     opts[setting], extra={'iface': self.iface})
                        if type(attr) == set:
                            pchange |= not (attr == opts[setting])
                        else:
                            pchange |= opts[setting] != peers[public_key].get_attr(f"WGPEER_A_{setting.upper()}")

                    if pchange:
                        has_pchanges = True
                        if do_apply:
                            self._do_peer_apply('change', public_key, opts)

            for peer in peers:
                if not peer in avail:
                    has_pchanges = True
                    if do_apply:
                        try:
                            self.wg.set(self.iface, peer={
                                'public_key': peer,
                                'remove': True
                            })
                        except Exception as err:
                            if not isinstance(err, netlinkerror_classes):
                                raise
                            logger.warning('remove peer from {} failed: {}'.format(
                                self.iface, err.args[1]))
            if has_pchanges:
                logger.log_change('wg.peers')
            else:
                logger.log_ok('wg.peers')

    def safe_set_peer(self, public_key, opts):
        try:
            self.wg.set_peer(self.iface, public_key=public_key, **opts)
        except (socket.gaierror, ValueError) as err:
            logger.warning('failed to set wireguard endpoint for peer {} at {}: {}'.format(
                public_key, self.iface, err))

            del (opts['endpoint'])
            self.wg.set_peer(self.iface, public_key=public_key, **opts)

    def show(netns, show_all, show_secrets, name, config):
        if netns.netns is not None:
            pyroute2.netns.pushns(netns.netns)

        try:
            wg = pyroute2.WireGuard()
        finally:
            if netns.netns is not None:
                pyroute2.netns.popns()

        infos = wg.info(name)

        config['wireguard'] = {
            'peers': {},
        }

        def _dump_value(key, value):
            if type(value) is list:
                result = []
                for v in value:
                    result.append(_dump_value(key, v))
                return result
            elif key == "allowedips":
                return value['addr']
            elif key == "endpoint":
                if value['family'] == socket.AF_INET6:
                    return f"[{value['addr']}]:{value['port']}"
                return f"{value['addr']}:{value['port']}"
            else:
                return value

        def _dump_values(cfg, key, value):
            if show_all:
                if value is None:
                    return
            else:
                if not value:
                    return

            if key in SECRET_SETTINGS:
                if key == 'preshared_key' and value == b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=':
                    return
                if show_secrets:
                    cfg[key] = value.decode('ascii')
                else:
                    cfg[key] = f"# VALUE IS HIDDEN - USE --show-secrets TO REVEAL"
            else:
                cfg[key] = _dump_value(key, value)

        for info in infos:
            for key in ['private_key', 'listen_port', 'fwmark']:
                value = info.get_attr(f"WGDEVICE_A_{key.upper()}")
                _dump_values(config['wireguard'], key, value)

            for peers in info.get_attrs('WGDEVICE_A_PEERS'):
                for peer in peers:
                    public_key = peer.get_attr(
                        "WGPEER_A_PUBLIC_KEY").decode('ascii')
                    config['wireguard']['peers'][public_key] = {}
                    for key in ['preshared_key', 'endpoint', 'persistent_keepalive_interval', 'allowedips']:
                        value = peer.get_attr(f"WGPEER_A_{key.upper()}")
                        _dump_values(config['wireguard']
                                     ['peers'][public_key], key, value)
