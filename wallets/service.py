from wallets.serializers import FundWalletSerializer, VerifyFundWalletSerializer, WithdrawWalletSerializer, TransferWalletSerializer
from payments.paystack import Paystack
from payments.models import Payment
from payments.service import PaymentService, PaymentStatus
from wallets.choices import WalletEntryTypes
from wallets.models import Wallet, WalletTransfer
from wallets.wallet_logger import WalletLogger
from accounts.service import UserService
from accounts.models import Phone
from django.db.transaction import atomic

class WalletService:
    paymentService = PaymentService()
    def init_fund_wallet(self, data):
        serializer = FundWalletSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        wallet = Wallet.objects.select_related("user").get(id=data.get("wallet_id"))

        payment_data = {
            "email": wallet.user.email,
            "user_id": wallet.user.id,
            "amount": data.get("amount"),
            "purpose": WalletEntryTypes.TOPUP
        }
        res = self.paymentService.init_payment(payment_data)
        return res

    def verify_fund_wallet(self, data):
        serializer = VerifyFundWalletSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        payment = self.paymentService.verify_payment(data)
        if payment:
            # log the payment here
            WalletLogger.log({
                "user_id": payment.user_id,
                "reference": payment.id,
                "entry_type": payment.purpose,
                "amount": payment.amount
            })
            return {"message": "payment Successful"}
        
        return {"message": "payment pending, pls wait"}

    def get_wallet_balance_using_phone(self, phone_number):
        phone = Phone.objects.filter(phone_with_ext=phone_number).first()
        if not phone:
            return None
        wallet = Wallet.objects.filter(user = phone.user).first()
        if not wallet:
            return None
        return wallet.balance

    def withdraw(self, data):
        serializer = WithdrawWalletSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        self.paymentService.deposit_to_bank(data)
        return {"message": "Transaction initialized"}

    def transfer(self, data):
        with atomic():
            serializer = TransferWalletSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            amount = data["amount"]
            sender = data["sender_id"]
            recipient_username = data["recipient_username"]
            recipient = UserService().retrieve(username=recipient_username).id

            transfer = WalletTransfer.objects.create(
                sender_id = sender, 
                recipient_id = recipient,
                amount = amount
            )

            WalletLogger().log({
                "user_id": sender,
                "reference": transfer.id,
                "entry_type": WalletEntryTypes.TRANSFER_DEBIT,
                "amount": amount
            })

            WalletLogger().log({
                "user_id": recipient,
                "reference": transfer.id,
                "entry_type": WalletEntryTypes.TRANSFER_CREDIT,
                "amount": amount
            })

            transfer.status = PaymentStatus.COMPLETED
            transfer.save()
            
            return {"message": "Tranfer completed"}
            

