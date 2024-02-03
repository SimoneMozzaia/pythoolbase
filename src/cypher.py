from .configuration_file import Configuration
import rsa
import logging


class EncryptAndDecryptData:
    """A simple class to Encrypt and Decrypt data. Value is encrypted with a 1024bits key

    Attributes:
        instance        Instance of the EncryptAndDecryptData class. Used for Singleton
        custom_logger   Instance of the custom logger class. Used for logging purposes
        private_key     Private RSA key
        public_key      Public RSA key
        config_class    Instance of the Configuration class
    """
    __instance = None
    __custom_logger = None
    __private_key = None
    __public_key = None
    __config_class = None
    
    def __call__(cls, *args, **kwargs):
        """Singleton implementation of the class"""
        if cls.__instance is None:
            cls.__instance = super(EncryptAndDecryptData, cls).__call__(*args, **kwargs)
        return cls.__instance

    def __init__(self):
        """At class instantiation two new public and private keys are generated"""
        self.__custom_logger = logging.getLogger(__name__)
        self.__config_class = Configuration()
        (self.__public_key, self.__private_key) = rsa.newkeys(1024, poolsize=8)
        
    def get_private_key(self):
        return self.__private_key
    
    def encrypt_message(self, message):
        encoded_message = message.encode('utf-8')
        
        return rsa.encrypt(encoded_message, self.__public_key)
    
    def decrypt_message(self, encrypted_message):
        return rsa.decrypt(encrypted_message, self.get_private_key()).decode('utf-8')
