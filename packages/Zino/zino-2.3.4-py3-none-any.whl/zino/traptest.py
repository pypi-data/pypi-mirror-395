import asyncio

from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import config, engine
from pysnmp.entity.rfc3413 import ntfrcv

# from pysnmp.hlapi.asyncio import UdpTransportTarget, Udp6TransportTarget


stop = asyncio.Event()


def main():
    try:
        asyncio.run(mofo())
    except (KeyboardInterrupt, SystemExit):
        stop.set()


async def mofo():
    await setup_trapd()
    await stop.wait()


async def setup_trapd():
    loop = asyncio.get_event_loop()
    # await loop.create_datagram_endpoint(lambda: EchoProtocol(), ("127.0.0.1", 1162))
    # Create SNMP engine with autogenernated engineID and pre-bound
    # to socket transport dispatcher
    snmpEngine = engine.SnmpEngine()

    # Transport setup

    # UDP over IPv4, first listening interface/port
    transport = udp.UdpTransport(loop=asyncio.get_event_loop()).openServerMode(("127.0.0.1", 1162))
    # This attribute needs to be awaited to ensure the socket is really opened,
    # unsure of why PySNMP doesn't do this, or how else it's supposed to be achieved
    await transport._lport
    config.addTransport(snmpEngine, udp.domainName + (1,), transport)
    print("transport added")
    config.addV1System(snmpEngine, "one", "public")
    config.addV1System(snmpEngine, "two", "public2")
    # Specify security settings per SecurityName (SNMPv1 - 0, SNMPv2c - 1)
    # config.addTargetParams(snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 1)

    # Register SNMP Application at the SNMP engine
    ntfrcv.NotificationReceiver(snmpEngine, callback)
    snmpEngine.transportDispatcher.jobStarted(1)  # this job would never finish
    # try:
    #     snmpEngine.transportDispatcher.runDispatcher()
    #
    # finally:
    #     snmpEngine.transportDispatcher.closeDispatcher()

    loop = asyncio.get_event_loop()


def callback(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    print(
        'Notification from ContextEngineId "%s", ContextName "%s"'
        % (contextEngineId.prettyPrint(), contextName.prettyPrint())
    )
    for name, val in varBinds:
        print("%s = %s" % (name.prettyPrint(), val.prettyPrint()))


class EchoProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        message = data.decode()
        print(f"Received {message} from {addr}")


if __name__ == "__main__":
    main()
