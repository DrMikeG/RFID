import time
import logging
import ctypes
import string
import nfc


### NFC device setup
class NFCReader(object):
    MC_AUTH_A = 0x60
    MC_AUTH_B = 0x61
    MC_READ = 0x30
    MC_WRITE = 0xA0
    card_timeout = 10

    def __init__(self, logger):
        self.__context = None
        self.__device = None
        self.log = logger

        self._card_present = False
        self._card_last_seen = None
        self._card_uid = None

        mods = [(nfc.NMT_ISO14443A, nfc.NBR_106)]

        self.__modulations = (nfc.nfc_modulation * len(mods))()
        for i in range(len(mods)):
            self.__modulations[i].nmt = mods[i][0]
            self.__modulations[i].nbr = mods[i][1]

    def run(self):
        """Starts the looping thread"""
        self.__context = ctypes.pointer(nfc.nfc_context())
        nfc.nfc_init(ctypes.byref(self.__context))
        loop = True
        try:
            self._card_uid = None
            conn_strings = (nfc.nfc_connstring * 10)()
            devices_found = nfc.nfc_list_devices(self.__context, conn_strings, 10)
            if devices_found >= 1:
                self.__device = nfc.nfc_open(self.__context, conn_strings[0])
                try:
                    _ = nfc.nfc_initiator_init(self.__device)
                    while True:
                        self._poll_loop()
                finally:
                    nfc.nfc_close(self.__device)
            else:
                self.log("NFC Waiting for device.")
                time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            loop = False
        except IOError, e:
            self.log("Exception: " + str(e))
            loop = True  # not str(e).startswith("NFC Error whilst polling")
        # except Exception, e:
        # loop = True
        #    print "[!]", str(e)
        finally:
            nfc.nfc_exit(self.__context)
            self.log("NFC Clean shutdown called")
        return loop

    def _poll_loop(self):
        """Starts a loop that constantly polls for cards"""
        nt = nfc.nfc_target()
        res = nfc.nfc_initiator_poll_target(self.__device, self.__modulations, len(self.__modulations), 10, 2,
                                            ctypes.byref(nt))
        # print "RES", res
        if res < 0:
            raise IOError("NFC Error whilst polling")
        elif res >= 1:
            uid = None
            print nt.nti.nai.szUidLen
            if nt.nti.nai.szUidLen == 4:
                uid = "".join([chr(nt.nti.nai.abtUid[i]) for i in range(4)])
            if nt.nti.nai.szUidLen == 7:
                uid = "".join([chr(nt.nti.nai.abtUid[i]) for i in range(7)])
            if uid:
                print "Reading card", uid.encode("hex")        
            self._card_uid = uid
            self._card_present = True
            self._card_last_seen = time.mktime(time.gmtime())
        else:
            self._card_present = False
            self._card_uid = None



if __name__ == '__main__':
    logger = logging.getLogger("cardhandler").info
    while NFCReader(logger).run():
        pass
