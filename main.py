from mysite.spotify.models import Account

print(Account.objects.all())


# Získání účtu s ID 2
account = Account.objects.get(pk=2)
print()
# Vypsání všech informací o účtu
print("Account ID:", account.account_id)
print("Username:", account.username)
print("Email:", account.email)
print("Password:", account.password)
print("Creation Date:", account.creation_date)
print("Name:", account.name)
print("Surname:", account.surname)
print("Phone:", account.phone)
print("Last Payment Date:", account.last_payment_date)
print("Next Payment Date:", account.next_payment_date)
print("Account Subtype:", account.acc_sub_type)
