from payments.models import Payment, PaymentStatus
from payments.paystack import Paystack
from django.db.transaction import atomic
from wallets.wallet_logger import WalletLogger
import uuid
from accounts.service import BankAccountService
SUCESS_STATUS = "success"
FAILED_STATUS = "failed"
class PaymentService:
    def __init__(self,):
        pass

    def init_payment(self, data):
        with atomic():
            res = Paystack().init_transaction({"email": data.get("email"), "amount": 100 * int(data.get("amount", 0))})
            payment_obj = Payment.objects.create(
                external_authorization_url = res["authorization_url"], 
                external_access_code = res["access_code"],
                external_reference = res["reference"],
                purpose = data.get("purpose"),
                amount = data.get("amount"),
                user_id = data.get("user_id")
            )
            res["payment_id"] = payment_obj.id
            return res


    def verify_payment(self, data):
        with atomic():
            res = Paystack().verify_transaction(data)

            payment = Payment.objects.get(
                external_reference = data.get("reference")
            )

            if payment.status in [PaymentStatus.COMPLETED, PaymentStatus.FAILED]:
                return

            if res["status"] and res["data"]["status"] == SUCESS_STATUS:
                payment.status = PaymentStatus.COMPLETED
                payment.meta = res["data"]
                payment.save()
                return payment

            if res["status"] and res["data"]["status"] == FAILED_STATUS:
              
                payment.status = PaymentStatus.FAILED
                payment.meta = res["data"]
                payment.save()


    def deposit_to_bank(self, data):
        with atomic():
            # thoughts 
            # we should deduct the money from your wallet here
            # and reverse it if the transfer fails in the webhook
            bank_acc_id = data["bank_account_id"]
            user_id = data["user_id"]
            bank_account = BankAccountService().retrieve(id=bank_acc_id, user_id=user_id)

            if not bank_account.external_reciepient_id:
                reciepient_data = {
                    "type": "nuban", 
                    "name": bank_account.account_name, 
                    "account_number": bank_account.account_number, 
                    "bank_code": bank_account.bank_code, 
                    "currency": bank_account.currency
                }
                res = Paystack().create_recipient(data=reciepient_data)
                bank_account.external_reciepient_id = res["data"]["recipient_code"]
                bank_account.save()
            
            ref = str(uuid.uuid4())
            transfer_data = {
                "amount": 100*int(data["amount"]),
                "source": "balance",
                "reason": "Withdrawal from PayNow wallet",
                "reference": ref,
                "recipient": bank_account.external_reciepient_id
            }

            res = Paystack().deposit_to_bank(transfer_data)

            payment_obj = Payment.objects.create(
                external_reference = ref,
                purpose = data.get("entry_type"),
                amount = data.get("amount"),
                user_id = data.get("user_id"),
                meta = res
            )
            res["payment_id"] = payment_obj.id
            return res

    def get_list_of_banks(self):
        with atomic():
            res = Paystack().get_list_of_banks()
            return res

    def list(self, **kwargs):
        with atomic():
            res = Payment.objects.filter(**kwargs)
            return res

    def acknoledge_webhook(self, data):
        with atomic():
            event = data.get("event")
            data = data.get("data", {})
            reference = data.get("reference")
            payment = Payment.objects.get(external_reference = reference)

            if payment.status in [PaymentStatus.COMPLETED, PaymentStatus.FAILED]:
                return {}
            
            if event == "transfer.success":
                payment.status = PaymentStatus.COMPLETED
                payment.meta = data
                payment.save()
                # log to wallet
                WalletLogger().log({
                    "user_id": payment.user_id,
                    "reference": payment.id,
                    "entry_type": payment.purpose,
                    "amount": payment.amount
                })

            elif event ==  "transfer.failed":
                payment.status = PaymentStatus.FAILED
                payment.meta = data
                payment.save()

            elif event == "transfer.reversed":
                payment.status = PaymentStatus.FAILED
                payment.meta = data
                payment.save()

            elif event == "charge.success":
                payment.status = PaymentStatus.COMPLETED
                payment.meta = data
                payment.save()

                WalletLogger().log({
                    "user_id": payment.user_id,
                    "reference": payment.id,
                    "entry_type": payment.purpose,
                    "amount": payment.amount
                })

                return {}
