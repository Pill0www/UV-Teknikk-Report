import numpy as np
import matplotlib.pyplot
import gzip
import struct

# Filsti til LSF-filen
filsti = '/Users/thebigmac/Documents/GitHub/UV-Teknikk-Report/Fritjof/data/Data.lsf'

def les_lsf_header(filsti):
    # Åpne .gz-filen
    with gzip.open(filsti, 'rb') as f:
        while True:
            # Les header (24 bytes)
            header = f.read(24)
            if len(header) < 24:
                break  # slutt på fil

            # Pakk header: (uint32, uint32, uint32, uint32, uint32, uint32)
            try:
                sync, size, msg_type, device_id, timestamp_sec, timestamp_nsec = struct.unpack('<6I', header)
            except struct.error:
                print("Klarte ikke å pakke header, antagelig slutt på fil")
                break

            # Sync-ordet for LSF er vanligvis 0x1acffc1d
            if sync != 0x1ACFFC1D:
                print(f"Ugyldig sync: {hex(sync)}, hopper ut")
                break

            print(f"Melding: type={msg_type}, device={device_id}, size={size}")

            # Hopp over resten av meldingen
            payload_size = size - 24  # total size inkluderer header
            f.seek(payload_size, 1)

les_lsf_header(filsti)

