from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from wallets.service import WalletService
from accounts.service import UserService
# Create your views here.

class USSDCallbackView(APIView):
    def post(self, request):
        try:
            print(request.data)
            session_id = request.data.get("sessionId", None)
            service_code = request.data.get("serviceCode", None)
            phone_number = request.data.get("phoneNumber", None)
            text = request.data.get("text", "").strip()
            ussd_res = "" 
            
            if text == "":
                # this is a new request
                user = UserService().retrieve_user_by_phone_with_ext(phone_with_ext=phone_number)
                if not user:
                    ussd_res += "END Can't locate your paynow wallet \n"
                    ussd_res += "Make sure this phone number is registered on PayNow \n"
                else:
                    ussd_res += "CON Welcome to PayNow \n"
                    ussd_res += "Select an option \n"
                    ussd_res += "1. Recieve Money \n"
                    ussd_res += "2. Send Money \n"
                    ussd_res += "3. Check Balance \n"


            if text == "1":
                ussd_res += "CON What AMOUNT do you want to recieve ? \n"

            if text == "2":
                ussd_res += "CON What AMOUNT do you want to send ? \n"

            if text == "3":
                balance = WalletService().get_wallet_balance_using_phone(phone_number)
                ussd_res += "END Your PayNow wallet balance is \n"
                ussd_res += "{} \n".format(balance)

            
            if len(text.split("*")) == 2:
                # a recieve TR has been initiated and the person is providing an amount
                amount = text.split("*")[1]
                # we can validate the amount here
                print("Amount to be sent or recieved: ", amount)
                if text.split("*")[0] == "1":
                    # wants to recive payment
                    ussd_res += "CON Provide the Sender's paynow ID ? \n"
                if text.split("*")[0] == "2":
                    # wants to send payment
                    ussd_res += "CON Provide the Reciever's paynow ID ? \n"
                

            if len(text.split("*")) == 3:
                # a recieve TR has been initiated and the person is providing an amount
                if text.split("*")[0] == "1":
                    # wants to recive payment
                    sender_username = text.split("*")[2]
                    ussd_res += "CON Enter Paynow PIN for {} ? \n".format(sender_username)

                if text.split("*")[0] == "2":
                    # wants to send payment
                    reciever_username = text.split("*")[2]
                    ussd_res += "CON Enter your Paynow PIN ? \n"
                    pass

            
            if len(text.split("*")) == 4:
                # a recieve TR has been initiated and the person is providing an PIN
                amount = text.split("*")[1]
                if text.split("*")[0] == "1":
                    # wants to recive payment
                    reciever_phone = phone_number
                    sender_username = text.split("*")[2]
                    sender_pin = text.split("*")[3]
                    print("Sender creds", sender_username, sender_pin)
                    sender = UserService().authenticate(sender_username, sender_pin)
                    reciever = UserService().retrieve_user_by_phone_with_ext(phone_with_ext = reciever_phone)
                    
                    if not sender:
                        ussd_res += "END Invalid Sender credentials \n"
                        ussd_res += "Try again \n"
                    else:
                        transfer_data = {
                            "sender_id": sender.id,
                            "recipient_username": reciever.username,
                            "amount": amount
                        }
                        WalletService().transfer(transfer_data)
                        ussd_res += "END You have recieve {} from {} \n".format(amount, sender.username)
                        balance = WalletService().get_wallet_balance_using_phone(phone_number)
                        ussd_res += "Your new balance is {} \n".format(balance)

                if text.split("*")[0] == "2":
                    # wants to send payment
                    sender_phone = phone_number
                    sender_pin = text.split("*")[3]
                    sender = UserService().retrieve_user_by_phone_with_ext(phone_with_ext = sender_phone)
                    UserService().authenticate(sender.username, sender_pin)
                    
                    reciever_username = text.split("*")[2]
                    reciever = UserService().retrieve(username=reciever_username)

                    if not reciever:
                        ussd_res += "END Invalid credentials \n"
                        ussd_res += "Try again \n"
                    else:
                        transfer_data = {
                            "sender_id": sender.id,
                            "recipient_username": reciever.username,
                            "amount": amount
                        }
                        WalletService().transfer(transfer_data)
                        ussd_res += "END You have sent {} to {} \n".format(amount, reciever.username)
                        balance = WalletService().get_wallet_balance_using_phone(phone_number)
                        ussd_res += "Your new balance is {} \n".format(balance)




            print(session_id, service_code, phone_number, text)
            return HttpResponse(ussd_res, content_type="text/plain")
        except Exception as e:
            print(e)
            ussd_res += "END {} \n".format(e)
            ussd_res += "Try Again"
            return HttpResponse(ussd_res, content_type="text/plain")