'''
Created on 04/19/2012

@author: zubietaroberto
'''

import ConfigParser
import tweepy
import urllib
import webbrowser

class TwitterInterface(tweepy.StreamListener):
    CONSUMER_KEY        = "prVSMIIlkF4p8sQBcSk4tw"
    CONSUMER_SECRET     = "uKeLYpofqGhyfPGlgCbZMXCzxCaGbt08IcB2RH7UDls"
    
    CONF_SECTION        = "UserKeys"
    CONF_OPTION_KEY     = "user_key"
    CONF_OPTION_SECRET  = "user_secret"
    CONF_FILENAME       = "token.cfg"
    
    mStreamer           = None
    
    def on_status(self, status):
        #Cada tweet nuevo que llega del streamer
        self.mStatusCount += 1
        try:
            print ("\n%s: %s" % (status.author.screen_name, status.text))
            return
        except Exception:
            pass   
            
    def on_error(self, status_code):
        #Error del Streamer
        print("\nError Received: %s" % status_code)
        return True
        
    def on_timeout(self):
        #timeout del streamer 
        print("\nTimeout")
        return True   
    
    def __init__(self):
        super(TwitterInterface, self).__init__()
        
        #registra los tokens de la aplicacion
        self.mAuth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        
        #intenta abrir los tokens de usuario existentes
        user_key = None
        user_secret = None
        try:
            conf = ConfigParser.RawConfigParser()
            conf.read(self.CONF_FILENAME)
            user_key = conf.get(self.CONF_SECTION, self.CONF_OPTION_KEY)
            user_secret = conf.get(self.CONF_SECTION, self.CONF_OPTION_SECRET)
        except:
        
            #le pide al usuario accesso para conseguir sus tokens
            webbrowser.open(self.mAuth.get_authorization_url())
            pin = raw_input("Escribir PIN: ").strip()
            token = self.mAuth.get_access_token(verifier=pin)
            user_key = token.key
            user_secret = token.secret
            
            #salva el token
            conf = ConfigParser.RawConfigParser()
            conf.add_section(self.CONF_SECTION)
            conf.set(self.CONF_SECTION, self.CONF_OPTION_KEY, user_key)
            conf.set(self.CONF_SECTION, self.CONF_OPTION_SECRET, user_secret)
            with open(self.CONF_FILENAME, 'wb') as configfile:
                conf.write(configfile)
        
        #activa el cliente
        self.mAuth.set_access_token(key=user_key, secret=user_secret)
        self.mApi = tweepy.API(self.mAuth)
        
        
    def startStream(self, words):
        self.mStatusCount = 0
        self.mStreamer = tweepy.Stream(auth=self.mAuth, listener=self, timeout=60)
        self.mStreamer.filter(None, words)
        
    def __del__(self):
        if self.mStreamer is not None:
            self.mStreamer.disconnect()
        

if __name__ == '__main__':
    ti = TwitterInterface()
    print ("Buscador de Hashtags por Twitter\nHecho por Roberto E. Zubieta\nConectado como: %s" % ti.mApi.me().name)
    busqueda = []
    while True:
        entrada = urllib.quote(raw_input("Buscar palabra (o escriba END para acabar): ").strip())
        if entrada == "END":
            break
        else:
            busqueda.append(entrada)
    if busqueda.__len__() > 0:
        try:
            ti.startStream(busqueda)
        except KeyboardInterrupt:
            print ("-"*40)
            print ("\nTotal de tweets contados: %s" % ti.mStatusCount)
            raw_input()
    else:
        print("Operacion Cancelada.")