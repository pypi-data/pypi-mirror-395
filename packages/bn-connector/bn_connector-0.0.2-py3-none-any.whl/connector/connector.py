from byneuron import Byneuron, Entity
import logging

log = logging.getLogger('connector')
class Connector(Byneuron):

    def __init__(self, name=None, exid=None, profile=False, **kwargs):
        super(Connector, self).__init__(**kwargs)
        self.gw_name_regex = name
        self.gw_exid_regex = exid
        self.gw_active = True
        self.gd_active = True
        self.pf_required = bool(profile)

    def iter_gateways(self):
        """
        iterator between gateways. yields entities Gateway, Device, Profile.
        note: activates the indexset.
        :return:
        """
        gw_exid = f'attribute:externalId regex:"{self.gw_exid_regex}"; ' if self.gw_exid_regex else ''
        gw_name = f'attribute:name regex:"{self.gw_name_regex}"; ' if self.gw_name_regex else ''
        gw_active = 'attribute:active true; ' if self.gw_active is True else ''
        gda = 'attribute:active true; ' if self.gd_active is True else ''
        gdp = 'link:hasFeature Profile:?pf; ' if self.pf_required is True else ''
        q = [
            f'Gateway:?gw {gw_active} {gw_name} {gw_exid} link:isAssignedTo IndexSet:?is.',
            f'Device:?gd {gda} {gdp} link:isMemberOf #?gw.'
        ]
        r = self.query(q, ['gw', 'gd', 'pf'])
        for gdkey, gd in r.get('gd', {}).items():
            # switch indexset
            self.set_indexset(gd.indexset)
            gwkey = gd.gateway
            gw = r.get('gw', {}).get(gwkey)
            pfkey = gd.profile  # 'hasFeatureProfile')
            pf = r.get('pf', {}).get(pfkey)
            yield gw, gd, pf

    def _iter_devices(self, gd, gdd_type=None):
        """
        -> rather use iter_devices()
        iterator that yields the active devices linked to a gateway device.
        :param gd:
        :param gdd_type: optional, filter on deviceType.
        :return: Entity() of type device
        """
        gdd_type = f'attribute:deviceType "deviceType#{gdd_type}";' if gdd_type else ''
        q = [
            f'IndexSet:?is entity:key {gd.indexset}.',
            f'Device:?gd entity:key {gd.key}.',
            'DeviceDeviceRelation:?ddr link:hasTarget #Device:?gd; attribute:active true; link:hasSource Device:?gdd.',
            f'Device:?gdd {gdd_type} attribute:active true.',
        ]
        devices = self.query(q, 'gdd')
        for device in devices.values():
            yield device

    def _iter_devices_items(self, gd, gdd_type=None):
        """
        -> rather use iter_devices()
        iterate related devices with their hasFeatureItem
        :param gd: Entity, gatewaydevice
        :param gdd_type: optional deviceType filter, deviceType#{gdd_type}
        :return: iterates Entities -> gdd, [gddi]
        """
        gdd_type = f'attribute:deviceType "deviceType#{gdd_type}";' if gdd_type else ''
        q = [
            f'IndexSet:?is entity:key {gd.indexset}.',
            f'Device:?gd entity:key {gd.key}.',
            'DeviceDeviceRelation:?ddr link:hasTarget #Device:?gd; attribute:active true; link:hasSource Device:?gdd.',
            f'Device:?gdd {gdd_type} attribute:active true.',
            'Device:?gdd>?gdd_feat link:hasFeature Item:?gddi.',
            f'Item:?gddi attribute:active true.'
        ]
        r = self.query(q, ['gdd', 'gddi'])
        gdd = r.get('gdd', {})
        gddi = r.get('gddi', {})

        for device in gdd.values():
            feature_keys = device.items
            yield device, [gddi.get(k) for k in feature_keys if k in gddi]

    def iter_items(self, gdd):
        """
        iterator yielding the active Items of a device.
        :param gdd:
        :return:
        """
        q = [
            f'IndexSet:?is entity:key {gdd.indexset}.',
            f'Device:?gdd entity:key {gdd.key}; link:hasFeature Item:?gddi.',
            f'Item:?gddi attribute:active true.'
        ]
        items = self.query(q, 'gddi')
        for item in items.values():
            yield item

    def iter_devices(self, device=None, gdd_type=None, features=False):
        """
        endpoint to iterate gdd's (when profile.data is not needed)
        if 'device' is None; all gdd's are iterated
        else 'device' is gateway or gateway-device; only linked gdd,s are iterated
        :param device: None, gateway or device
        :param gdd_type: optional - filter for deviceType of gdd
        :param features: optional - adds the active featured items for the gdd
        :return:
        """
        for _gw, _gd, _pf in self.iter_gateways():
            print(_gw, _gd, _pf)
            if _gd is None:
                continue
            if isinstance(device, Entity):
                if device.type == "Gateway":
                    if _gw.key != device.key:
                        continue
                elif device.gateway is not None:
                    if device.gateway != device.key:
                        continue
            if features:
                for gdd, gddi in self._iter_devices_items(_gd, gdd_type):
                    yield gdd, gddi

            else:
                print(_gd)
                for gdd in self._iter_devices(_gd, gdd_type):
                    yield gdd

    def add_events(self, events):
        # add events that have no duplicate
        # not needed here since we only call for last event
        log.info('add %s events', len(events))
        if events:
            return [e for e in self.datamodel(events)]

    def iter_relations(self, device, active_relation=True):
        """ test to investigate relations like used with electric and solar devices """
        active = ' attribute:active true;' if active_relation else ''
        q = [
            f'IndexSet:?is entity:key {device.indexset}.',
            f'Device:?d entity:key {device.key}.',
            f'DeviceDeviceRelation:?ddr link:hasTarget #Device:?d;{active} link:hasSource Device:?rd.',
            f'Device:?rd attribute:active true.',
            f'ItemDeviceRelation:?idr link:hasTarget #Device:?d;{active} link:hasSource Item:?ri.',
            f'Item:?ri attribute:active true.',

        ]
        r = self.query(q, ['ddr', 'idr', 'rd', 'ri'])
        for relation in r.get('ddr',{}).values():
            device = r.get('rd',{}).get(relation.source)
            yield relation, device
        for relation in r.get('idr',{}).values():
            item = r.get('ri',{}).get(relation.source)
            yield relation, item


