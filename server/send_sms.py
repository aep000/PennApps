from twilio.rest import TwilioRestClient
                                 
def send_sms(to_number, the_body):
	account_sid = "AC7a14830568ec769f5f68d7d3d2ac7287"
	auth_token = "3a0cd8283b0788e463e43f6fcab93f46"
	client = TwilioRestClient(account_sid, auth_token)

	message = client.messages.create(to=to_number, from_="+19087524729",
                                     body=the_body)
	return True	
