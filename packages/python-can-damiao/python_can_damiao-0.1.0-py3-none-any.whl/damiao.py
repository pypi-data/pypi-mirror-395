import logging
import struct
import time
from typing import Optional, Tuple, List, Dict, Any

import serial
import serial.tools.list_ports

from can import BusABC, Message, typechecking

logger = logging.getLogger(__name__)


class DamiaoBus(BusABC):
    """
    Interface for Damiao USB-CAN adapters.
    """

    # CAN Baudrates
    # index: bitrate
    _BAUDRATES = {
        1000000: 0,
        800000: 1,
        666000: 2,
        500000: 3,
        400000: 4,
        250000: 5,
        200000: 6,
        125000: 7,
        100000: 8,
        80000: 9,
        50000: 10,
        40000: 11,
        20000: 12,
        10000: 13,
        5000: 14,
    }

    def __init__(
        self,
        channel: str,
        bitrate: int = 500000,
        baudrate: int = 2000000,
        **kwargs,
    ) -> None:
        """
        :param channel:
            The serial port to use (e.g. /dev/ttyACM0 or COM3).
        :param bitrate:
            The CAN bitrate in bits/s. Default is 500000.
        :param baudrate:
            The serial port baudrate. Default is 2000000.
        """
        super().__init__(channel=channel, bitrate=bitrate, **kwargs)

        self.channel_info = f"Damiao USB-CAN: {channel}"

        if bitrate not in self._BAUDRATES:
            raise ValueError(f"Invalid bitrate: {bitrate}")

        self.ser = serial.Serial(
            channel,
            baudrate=baudrate,
            timeout=0.5,
        )

        self._set_bitrate(bitrate)
        self._recv_buffer = bytearray()  # Buffer for incomplete frames

    def _set_bitrate(self, bitrate: int) -> None:
        """
        Set the CAN bitrate.
        Protocol: 0x55 0x05 Index 0xAA 0x55
        """
        index = self._BAUDRATES[bitrate]
        cmd = struct.pack("BBBBB", 0x55, 0x05, index, 0xAA, 0x55)
        self.ser.write(cmd)
        time.sleep(0.2)  # Wait for device to apply

    def _crc8(self, data: bytes) -> int:
        """
        Calculate CRC8 using polynomial 0x8C (reversed 0x31).
        Initial value: 0x00.
        """
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x01:
                    crc = (crc >> 1) ^ 0x8C
                else:
                    crc >>= 1
        return crc

    def send(self, msg: Message, timeout: Optional[float] = None) -> None:
        """
        Send a message to the CAN bus.

        Frame Structure (30 bytes):
        - Header: 0x55 0xAA (2 bytes)
        - Length: 0x1E (1 byte)
        - Command: 0x03 (1 byte) - Non-feedback CAN forwarding
        - Send Times: 1 (4 bytes)
        - Interval: 10 (4 bytes, unit: 100us)
        - ID Type: 0=Standard, 1=Extended (1 byte)
        - CAN ID: 4 bytes (Little Endian)
        - Frame Type: 0=Data, 1=Remote (1 byte)
        - idAcc: 0 (1 byte)
        - dataAcc: 0 (1 byte)
        - Data Length: 0-8 (1 byte)
        - Data: 8 bytes (always 8 bytes, prepend zeros if needed)
        - CRC: 1 byte
        """
        header = b"\x55\xAA"
        length = 30
        cmd = 0x03
        send_times = 1
        interval = 10
        
        id_type = 1 if msg.is_extended_id else 0
        can_id = msg.arbitration_id
        frame_type = 1 if msg.is_remote_frame else 0
        id_acc = 0
        data_acc = 0
        data_len = msg.dlc
        
        # Pad data to 8 bytes (prepend zeros if needed)
        if len(msg.data) < 8:
            data = b"\x00" * (8 - len(msg.data)) + msg.data
        else:
            data = msg.data[:8]
        
        # Construct frame
        frame = bytearray()
        frame.extend(header)
        frame.append(length)
        frame.append(cmd)
        frame.extend(struct.pack("<I", send_times))
        frame.extend(struct.pack("<I", interval))
        frame.append(id_type)        
        frame.extend(struct.pack("<I", can_id & 0x1FFFFFFF))  # 29-bit ID
        frame.append(frame_type)
        frame.append(data_len)
        frame.append(id_acc)
        frame.append(data_acc)
        frame.extend(data)
        frame.append(0) # CRC placeholder
        
        # Calculate CRC over the whole frame (including the 0 placeholder at the end)
        crc = self._crc8(frame)
        frame[-1] = crc
        
        self.ser.write(frame)

    def _extract_frames(self, data: bytearray) -> list:
        """
        Extract complete frames from the data buffer.
        Returns a list of frames and updates the buffer with remaining data.
        """
        frames = []
        header = 0xAA
        footer = 0x55
        frame_length = 16
        i = 0
        remainder_pos = 0

        while i <= len(data) - frame_length:
            if data[i] == header and data[i + frame_length - 1] == footer:
                frame = bytes(data[i:i + frame_length])
                frames.append(frame)
                i += frame_length
                remainder_pos = i
            else:
                i += 1
        
        # Update buffer with remaining incomplete data
        self._recv_buffer = bytearray(data[remainder_pos:])
        return frames

    def _recv_internal(self, timeout: Optional[float] = None) -> Tuple[Optional[Message], bool]:
        """
        Receive a message from the CAN bus.

        Frame Structure (16 bytes):
        - Header: 0xAA (1 byte)
        - Command: 1 byte (0x11=Receive Success, 0x12=Send Success, etc.)
        - Info: 1 byte (reserved or flags)
        - CAN ID: 4 bytes (Big Endian)
        - Data: 8 bytes
        - Footer: 0x55 (1 byte)
        """
        start_time = time.time()
        
        while True:
            if timeout is not None and (time.time() - start_time) > timeout:
                return None, False
            
            # Read available data and append to buffer
            new_data = self.ser.read_all()
            if new_data:
                self._recv_buffer.extend(new_data)
            
            # Extract complete frames from buffer
            frames = self._extract_frames(self._recv_buffer)
            
            # Process each frame
            for frame in frames:
                cmd = frame[1]
                info = frame[2]
                can_id_bytes = frame[3:7]
                data = frame[7:15]
                
                # Parse CAN ID (Big Endian)
                arbitration_id = struct.unpack(">I", can_id_bytes)[0]
                
                # Parse Info byte (if available)
                # Bits 0-5: Data Length
                # Bit 6: Extended ID flag
                # Bit 7: Remote Frame flag
                if info != 0:
                    dlc = info & 0x3F
                    is_extended_id = bool((info >> 6) & 0x1)
                    is_remote_frame = bool((info >> 7) & 0x1)
                else:
                    # Fallback: determine based on CAN ID value
                    # Standard CAN: 11-bit (0x000-0x7FF)
                    # Extended CAN: 29-bit (0x00000000-0x1FFFFFFF)
                    is_extended_id = arbitration_id > 0x7FF
                    dlc = 8
                    is_remote_frame = False
                
                # Handle Commands
                # 0x11: Receive Success
                # 0x12: Send Success
                if cmd == 0x11:
                    msg = Message(
                        arbitration_id=arbitration_id,
                        is_extended_id=is_extended_id,
                        is_remote_frame=is_remote_frame,
                        dlc=dlc,
                        data=data[:dlc],
                        timestamp=time.time(),
                        channel=self.channel_info
                    )
                    return msg, False
                elif cmd == 0x12:
                    # Send confirmation (ignored for now)
                    continue
                else:
                    continue
            
            # No valid message yet, wait a bit and retry
            time.sleep(0.001)
            
    def shutdown(self) -> None:
        if self._is_shutdown:
            return
        self.ser.close()
        self._is_shutdown = True

    @staticmethod
    def _detect_available_configs() -> List[Dict[str, Any]]:
        """
        Detect available Damiao USB-CAN adapters.
        
        Damiao adapters have USB VID:PID = 2e88:4603
        Note: Damiao seems to use default VID for HDSC MCU, so this detection may not be reliable.
        
        :return: List of configurations for detected Damiao adapters
        """
        channels = []
        
        # Damiao USB-CAN adapter identifiers
        DAMIAO_VID = 0x2E88
        DAMIAO_PID = 0x4603
        
        try:
            # Enumerate all serial ports
            ports = serial.tools.list_ports.comports()
            
            for port in ports:
                # Check if this port matches Damiao VID/PID
                if port.vid == DAMIAO_VID and port.pid == DAMIAO_PID:
                    config = {
                        "interface": "damiao",
                        "channel": port.device,
                    }
                    if port.serial_number:
                        config["serial_number"] = port.serial_number
                    channels.append(config)
                    
        except Exception as e:
            logger.warning(f"Error detecting Damiao adapters: {e}")
        
        return channels
