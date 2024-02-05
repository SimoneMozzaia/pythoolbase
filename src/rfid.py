from epc import utils
from epc.schemes import SGTIN


class EpcConverter:
    def matricola_to_epc(self, matricola):
        gtin = matricola[0:13]
        serial = matricola[18:25] + matricola[13:18]
        prefix_len = 7
        tag_size = 96
        tag_filter = 1

        # Create EPC object
        my_tag = SGTIN()
        my_tag.tag_size(tag_size)
        my_tag.filter(tag_filter)
        my_tag.decode_gtin(gtin, company_prefix_length=prefix_len, serial_number=serial)
        _tag = str(hex(my_tag))
        tag = _tag[2::]

        return tag.upper()

    def epc_to_matricola(self, epc_code):
        my_tag = utils.decode_epc(epc_code)
        gtin = str(my_tag.gtin)[1:24]
        __serial = str(my_tag._serial).zfill(12)
        return gtin + __serial[7:12] + __serial[0:7]

