# 161 порт
# 9100 порт к регистратору

import pyshark
import asyncio
import concurrent.futures
import time


class PacketCapture:
    def __init__(self):
        self.progress = 0
        self.is_running = False

    def _run_capture(self, packet_count=1000):
        """Захват пакетов с обновлением прогресса"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            self.is_running = True
            self.progress = 0

            capture = pyshark.LiveCapture(interface='Ethernet')
            nbns_count = mdns_count = llmnr_count = 0
            captured_packets = 0

            print(f"🚀 Начинаю захват {packet_count} пакетов...")

            for packet in capture.sniff_continuously(packet_count=packet_count):
                captured_packets += 1
                self.progress = (captured_packets / packet_count) * 100

                # Логируем прогресс каждые 10%
                if captured_packets % (packet_count // 10) == 0:
                    print(f"📦 Захвачено {captured_packets}/{packet_count} пакетов ({self.progress:.1f}%)")

                if hasattr(packet, 'ip') and packet.ip.src == '10.7.110.251':
                    if hasattr(packet, 'tcp'): nbns_count += 1
                    if hasattr(packet, 'mdns'): mdns_count += 1
                    if hasattr(packet, 'udp'): llmnr_count += 1

            print(f"✅ Захват завершен: {captured_packets} пакетов")
            return [nbns_count, mdns_count, llmnr_count, captured_packets]

        except Exception as e:
            print(f"❌ Ошибка захвата: {e}")
            return [0, 0, 0, 0]
        finally:
            self.is_running = False
            loop.close()


# Глобальный экземпляр
capture_manager = PacketCapture()


def packet_handler(packet_count=1000):
    """Основная функция захвата"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(capture_manager._run_capture, packet_count)
        try:
            return future.result(timeout=120)  # Таймаут 2 минуты
        except concurrent.futures.TimeoutError:
            print("⏰ Таймаут захвата пакетов")
            return [0, 0, 0, 0]


def get_capture_progress():
    """Возвращает текущий прогресс захвата"""
    return capture_manager.progress


def is_capture_running():
    """Проверяет, выполняется ли захват"""
    return capture_manager.is_running