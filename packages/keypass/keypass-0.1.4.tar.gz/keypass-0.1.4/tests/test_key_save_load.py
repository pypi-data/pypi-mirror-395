import keypass as kp

account_ = kp.pass_account()

kp.save(account_)
print(account_)

account = kp.load()
print(account)

assert account["username"] == account_["username"]
assert account["password"] == account_["password"]
