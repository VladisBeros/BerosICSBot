# 161 порт
# 9100 порт к регистратору

import pyshark
import datetime


def packet_handler(pkt):
    try:
        # Время захвата пакета
        timestamp = datetime.datetime.fromtimestamp(float(pkt.sniff_timestamp))
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        print(f"[{time_str}] ", end="")

        # IP слой (источник и назначение)
        if hasattr(pkt, 'ip'):
            print(f"IP: {pkt.ip.src} -> {pkt.ip.dst} | ", end="")

        # TCP слой - именно то, что вам нужно!
        if hasattr(pkt, 'tcp'):
            src_port = pkt.tcp.srcport
            dst_port = pkt.tcp.dstport
            flags = pkt.tcp.flags  # Это поле содержит флаги

            print(f"TCP: {src_port} -> {dst_port} | Flags: {flags} | ", end="")

            # Декодируем флаги для лучшей читаемости
            flags_int = int(flags, 16)  # Флаги в HEX, конвертируем в int
            flags_str = ""
            if flags_int & 0x01: flags_str += "FIN "
            if flags_int & 0x02: flags_str += "SYN "
            if flags_int & 0x04: flags_str += "RST "
            if flags_int & 0x08: flags_str += "PSH "
            if flags_int & 0x10: flags_str += "ACK "
            if flags_int & 0x20: flags_str += "URG "
            if flags_int & 0x40: flags_str += "ECE "
            if flags_int & 0x80: flags_str += "CWR "

            print(f"Flags decoded: [{flags_str.strip()}] | ", end="")

        # UDP слой (на случай, если пакет UDP)
        elif hasattr(pkt, 'udp'):
            print(f"UDP: {pkt.udp.srcport} -> {pkt.udp.dstport} | ", end="")

        # Длина пакета
        print(f"Length: {pkt.length} bytes")

        # Дополнительная информация для TCP пакетов
        if hasattr(pkt, 'tcp'):
            # Номер последовательности и подтверждения
            seq = getattr(pkt.tcp, 'seq', 'N/A')
            ack = getattr(pkt.tcp, 'ack', 'N/A')
            print(f"   SEQ: {seq}, ACK: {ack}")

            # Размер окна
            window = getattr(pkt.tcp, 'window', 'N/A')
            print(f"   Window: {window}")

        print("-" * 80)

    except AttributeError as e:
        # Пропускаем пакеты без IP (например, чистый Ethernet)
        print(f"Skipped non-IP packet: {e}")
        pass


# Создаем захват (укажите свой интерфейс)
# Чтобы узнать доступные интерфейсы: pyshark.LiveCapture.list_interfaces()
capture = pyshark.LiveCapture(interface='Ethernet')  # Замените на ваш интерфейс

print("Starting TCP traffic capture...")
print("Press Ctrl+C to stop.\n")

try:
    # Захватываем только TCP трафик для чистоты вывода
    for packet in capture.sniff_continuously(packet_count=50):
        # Фильтруем только TCP пакеты
        if hasattr(packet, 'tcp'):
            packet_handler(packet)
except KeyboardInterrupt:
    print("\nCapture stopped by user.")