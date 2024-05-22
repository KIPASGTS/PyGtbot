import logging
import struct
import math
class Variant:
    def __init__(self):
        self.VariantData = []
        self.VariantDataSize = 0

    def log(self):
        for i, data in enumerate(self.VariantData):
            logging.info("[%d] %s", i, data)

    def get_variant_int(self, index):
        if index < 0 or index >= len(self.VariantData):
            return 0

        int_data = self.VariantData[index]
        if not isinstance(int_data, int):
            return 0

        return int_data

    def get_variant_vec2f(self, index):
        if index < 0 or index >= len(self.VariantData):
            return [0.0, 0.0]

        float_data = self.VariantData[index]
        if not isinstance(float_data, list) or len(float_data) != 2:
            return [0.0, 0.0]

        return float_data

    def get_variant_vec3f(self, index):
        if index < 0 or index >= len(self.VariantData):
            return [0.0, 0.0, 0.0]

        float_data = self.VariantData[index]
        if not isinstance(float_data, list) or len(float_data) != 3:
            return [0.0, 0.0, 0.0]

        return float_data

    def get_string(self, index):
        if index < 0 or index >= len(self.VariantData):
            return ""

        str_data = self.VariantData[index]
        if not isinstance(str_data, str):
            return ""

        return str_data

    def unpack(self, packet):
        data = packet.data[60:]  # extra data
        mem_pos = 0
        self.VariantDataSize = data[mem_pos]
        mem_pos += 1
        for i in range(self.VariantDataSize):
            _ = data[mem_pos]  # index
            mem_pos += 1
            data_type = data[mem_pos]
            mem_pos += 1
            if data_type == 1:
                float_data = struct.unpack('<f', data[mem_pos:mem_pos + 4])[0]
                self.VariantData.append(float_data)
                mem_pos += 4
            elif data_type == 2:
                str_len = struct.unpack('<I', data[mem_pos:mem_pos + 4])[0]
                mem_pos += 4
                str_data = data[mem_pos:mem_pos + str_len].decode('utf-8')
                self.VariantData.append(str_data)
                mem_pos += str_len
            elif data_type == 3:
                float_data1 = struct.unpack('<f', data[mem_pos:mem_pos + 4])[0]
                mem_pos += 4
                float_data2 = struct.unpack('<f', data[mem_pos:mem_pos + 4])[0]
                self.VariantData.append([float_data1, float_data2])
                mem_pos += 4
            elif data_type == 4:
                float_data1 = struct.unpack('<f', data[mem_pos:mem_pos + 4])[0]
                mem_pos += 4
                float_data2 = struct.unpack('<f', data[mem_pos:mem_pos + 4])[0]
                mem_pos += 4
                float_data3 = struct.unpack('<f', data[mem_pos:mem_pos + 4])[0]
                self.VariantData.append([float_data1, float_data2, float_data3])
                mem_pos += 4
            elif data_type == 5:
                value_data = struct.unpack('<I', data[mem_pos:mem_pos + 4])[0]
                self.VariantData.append(value_data)
                mem_pos += 4
            elif data_type == 9:
                value_data = struct.unpack('<I', data[mem_pos:mem_pos + 4])[0]
                self.VariantData.append(int(value_data))
                mem_pos += 4