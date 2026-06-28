# 161 порт
# 9100 порт к регистратору

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


HOST = "10.7.112.57"
COMMUNITY = "public"
oids = {
        'ecrModemState': '1.3.6.1.4.1.41391.1.1.3.1',       # Состояние модема (PhysLayer, PPP, IP) — 3 байта
        'ecrModemRSSI': '1.3.6.1.4.1.41391.1.1.3.3',        # Уровень сигнала (RSSI)
        'ecrModemIpAddr': '1.3.6.1.4.1.41391.1.1.3.4',      # IP-адрес модема
        'ecrCSEFWritePID': '1.3.6.1.4.1.41391.1.1.7.1',     # Последний записанный PID (номер пакета в КСЕФ)
        'ecrCSEFSendPID': '1.3.6.1.4.1.41391.1.1.7.2',      # Последний отправленный PID (номер пакета, ушедший в налоговую)
        'ecrACQXchgLastTime': '1.3.6.1.4.1.41391.1.1.6.3',  # Время с последнего обмена с эквайером
        'ecrACQXchgNextTime': '1.3.6.1.4.1.41391.1.1.6.4',  # Время до следующего обмена
        'ecrACQXchgResult': '1.3.6.1.4.1.41391.1.1.6.6'     # Результат последнего обмена (0 = успех)
    }

async def get_ecr_data():
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


asyncio.run(get_ecr_data())