import requests
import os.path

# URL Constants
SENDURL = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush"
LISTURL = "https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices"


# PushParams is a dictionary with some extra properties
# It is passed directly to requests
class PushParams(dict):
    def __init__(self, apikey=None, deviceId='group.all', deviceIds=None, deviceNames=None, text=None, url=None,
                 clipboard=None, smsnumber=None, smstext=None, smscontactname=None, find=None, title=None,
                 priority=None, vibration=None, dismissOnTouch=None, group=None, devices=None, sendUrl=SENDURL,
                 listUrl=LISTURL):
        dict.__init__(self)
        self["apikey"] = apikey
        self["deviceId"] = deviceId
        self["deviceIds"] = deviceIds
        self["deviceNames"] = deviceNames
        self["text"] = text
        self["url"] = url
        self["clipboard"] = clipboard
        self["smsnumber"] = smsnumber
        self["smstext"] = smstext
        self["smscontactname"] = smscontactname
        self["find"] = find
        self["title"] = title
        self["priority"] = priority
        self["vibration"] = vibration
        self["dismissOnTouch"] = dismissOnTouch
        self["group"] = group
        self.devices = devices
        self.sendUrl = sendUrl
        self.listUrl = listUrl

    def getDevices(self):
        payload = {'apikey': self['apikey']}
        response = requests.get(self.listUrl, params=payload).json()
        if response.get('success') and not response.get('userautherror'):
            self.devices = response['records']
            return self.devices
        self.devices = None
        return False

    def sendSmsTo(self, contact, contactType='number'):
        self["smsnumber"] = None
        self["smscontactname"] = None

        if contactType is 'number':
            self["smsnumber"] = contact
            return True
        if contactType is 'name':
            self["smscontactname"] = contact
            return True
        return False

    def sendTo(self, device, deviceType='id'):
        self["deviceId"] = None
        self["deviceIds"] = None
        self["deviceNames"] = None

        if deviceType is 'id':
            self["deviceId"] = device
            return True
        if deviceType is 'ids':
            self["deviceIds"] = ','.join(list(device))
            return True
        if deviceType is 'names' or deviceType is 'name':
            self["deviceNames"] = ','.join(list(device))
            return True
        return False


class Join:
    def __init__(self, apikey=None, device=None, deviceType=None, contact=None, contactType=None):
        self._apikey = apikey
        self._device = device
        self._deviceType = deviceType
        self._contact = contact
        self._contactType = contactType

    def findApikey(self, path=os.path.dirname(os.path.realpath(__file__))):
        with open(os.path.join(path, '.apikey'), 'r') as fp:
            key = fp.read()
            if key and key != "":
                self._apikey = key
                return True
            return False

    def setApikey(self, apikey):
        self._apikey = apikey

    def setDevice(self, device, deviceType):
        self._device = device
        self._deviceType = deviceType

    def setSmsContact(self, contact, contactType):
        self._contact = contact
        self._contactType = contactType

    def push(self, options):
        return requests.get(options.sendUrl, params=options)

    def sendNotification(self, title, text):
        options = PushParams(self._apikey, title=title, text=text)
        if self._device and self._deviceType:
            options.sendTo(self._device, self._deviceType)
        self.push(options)

    def ringPhone(self):
        options = PushParams(self._apikey, find=True)
        if self._device and self._deviceType:
            options.sendTo(self._device, self._deviceType)
        self.push(options)

    def sendUrl(self, url, title=None, text=None):
        options = PushParams(self._apikey, url=url, title=title, text=text)
        if self._device and self._deviceType:
            options.sendTo(self._device, self._deviceType)
        self.push(options)

    def sendSms(self, text):
        options = PushParams(self._apikey, smstext=text)
        if self._device and self._deviceType:
            options.sendTo(self._device, self._deviceType)
        options.sendSmsTo(self._contact, self._contactType)
        self.push(options)
