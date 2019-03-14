# we import the Twilio client from the dependency we just installed
from twilio.rest import Client #TwilioRestClient

# the following line needs your Twilio Account SID and Auth Token
client = Client("AC4811e14869ed1e9fd36c071d6cad19be", "4e5f7d6661f83707525cdda549895cf1")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
def send_sms_alert(msg):

    client.messages.create(to="+447741161585", from_="+441653272018",body=msg)


