import asyncio
from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    CommunityData,
    ContextData,
    UdpTransportTarget,
    ObjectType,
    ObjectIdentity,
    get_cmd
)

HOST = "10.7.110.2"
COMMUNITY = "public"
oids = {
        'sysDescr': '1.3.6.1.2.1.1.1.0',
        'sysObjectID': '1.3.6.1.2.1.1.2.0',
        'sysUpTime': '1.3.6.1.2.1.1.3.0',
        'sysName': '1.3.6.1.2.1.1.5.0'
}

async def main():
    engine = SnmpEngine()
    target = await UdpTransportTarget.create((HOST, 161))

    for name, oid in oids.items():
        error_indication, error_status, error_index, var_binds = await get_cmd(
            engine,
            CommunityData(COMMUNITY),
            target,
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        if error_indication:
            print(f"{name}: ERROR -> {error_indication}")
            continue

        if error_status:
            print(f"{name}: ERROR -> {error_status.prettyPrint()}")
            continue

        for oid_obj, value in var_binds:
            print(f"{name}")
            print(f"OID      : {oid_obj}")
            print(f"Value    : {value}")
            print("-" * 40)


asyncio.run(main())