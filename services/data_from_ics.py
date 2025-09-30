# 161 порт
# 9100 порт к регистратору

import pyshark
import asyncio
import threading

def packet_handler():
    def _run_capture():
        # Создаем новый event loop для этого потока
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            capture = pyshark.LiveCapture(interface='Ethernet')
            nbns_count = 0
            mdns_count = 0
            llmnr_count = 0

            for packet in capture.sniff_continuously(packet_count=1000):
                if hasattr(packet, 'ip') and packet.ip.src == '10.7.110.20':
                    try:
                        if hasattr(packet, 'nbns'):
                            nbns_count += 1
                        if hasattr(packet, 'mdns'):
                            mdns_count += 1
                        if hasattr(packet, 'llmnr'):
                            llmnr_count += 1
                    except AttributeError:
                        continue

            return [nbns_count, mdns_count, llmnr_count]
        except Exception as e:
            print(f"Capture error: {e}")
            return [0, 0, 0]
        finally:
            loop.close()

    # Запускаем в отдельном потоке
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(_run_capture)
        return future.result()