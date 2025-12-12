from libifstate.link.base import Link
import enum

class VlanFlags(enum.IntFlag):
    reorder_hdr = 0x1
    gvrp = 0x2
    loose_binding = 0x4
    mvrp = 0x8
    bridge_binding = 0x10

class VlanLink(Link):
    def __init__(self, ifstate, netns, name, link, identify, ethtool, hooks, vrrp, brport):
        # build vlan_flags value
        if 'vlan_flags' in link:
            # add sensible default
            if VlanFlags.reorder_hdr.name in link['vlan_flags']:
                vlan_flags = 0
            else:
                vlan_flags = VlanFlags.reorder_hdr

            # build vlan_flags value
            for flag, enabled in link['vlan_flags'].items():
                if enabled:
                    vlan_flags |= VlanFlags[flag].value
            link['vlan_flags'] = vlan_flags

        super().__init__(ifstate, netns, name, link, identify, ethtool, hooks, vrrp, brport)
