from wallets.serializers import WalletLogSerializer

from wallets.models import Wallet, WalletEntryTypes, WalletEntry

class WalletLogger():
    def unlog(self, data):
        # used to unlog an already logged withdrawal
        serializer = WalletLogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        wallet = Wallet.objects.get(user_id = data["user_id"])
        amount = data["amount"]
        entry_type = data["entry_type"]
        reference = data['reference']

        negated_entry = entry_type in WalletEntryTypes.nagated_entries()

        if negated_entry:
            # this means we removed the money from the wallet already 
            # so we need to add it back here
            # create a reverse wallet entry
            WalletEntry.objects.create(
                wallet = wallet, amount=amount, 
                entry_type="reverse_"+entry_type, reference=reference, 
            )
            wallet.balance += amount 
            wallet.save()

        else:
            # the money was added to the wallet
            # So now we need to remove it
            # Dont have a use case for this yet 
            raise Exception("Unlog Not yet implemented for this usecase")
            
        
        return {"status": True}

    def log(self, data):
        serializer = WalletLogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        wallet = Wallet.objects.get(user_id = data["user_id"])
        amount = data["amount"]
        entry_type = data["entry_type"]
        reference = data['reference']
        negated_entry = entry_type in WalletEntryTypes.nagated_entries()

        if negated_entry:
            if wallet.balance < amount:
                raise Exception("Insuficient balance in wallet")
            WalletEntry.objects.create(
                wallet = wallet, amount=amount, 
                entry_type=entry_type, reference=reference, 
            )
            wallet.balance -= amount 
            wallet.save()

        else:
            WalletEntry.objects.create(
                wallet = wallet, amount=amount, 
                entry_type=entry_type, reference=reference, 
            )
            wallet.balance += amount 
            wallet.save()
        
        return {"status": True}



