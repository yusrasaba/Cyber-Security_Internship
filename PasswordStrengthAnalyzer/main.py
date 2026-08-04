from password_checker import check_password, check_common_password
from password_generator import generate_password
from password_history import (
    is_password_reused,
    save_password
)

print("=" * 50)
print("      PASSWORD STRENGTH ANALYZER")
print("=" * 50)

password = input("Enter your password: ")

if not password.strip():
    print("\n❌ Password cannot be empty.")
    exit()

if is_password_reused(password):

    print("\n⚠ Password Reuse Detected! \nThis password has been used before.\nFor better security, choose a new password.")

else:

    save_password(password)

result = check_password(password)
is_common = check_common_password(password)

print("\nPassword Analysis")
print("-" * 50)

print(f"Length            : {result['length']}")
print(f"Uppercase         : {'✅ Yes' if result['uppercase'] else '❌ No'}")
print(f"Lowercase         : {'✅ Yes' if result['lowercase'] else '❌ No'}")
print(f"Numbers           : {'✅ Yes' if result['number'] else '❌ No'}")
print(f"Special Character : {'✅ Yes' if result['special'] else '❌ No'}")
print(f"Score             : {result['score']}/100")
print(f"Strength         : {result['strength']}")
if is_common:
    print("\n⚠ WARNING")
    print("This password is commonly used.")
    print("Choose a more unique password.")
print("\nSuggestions:")

if result["length"] < 8:
    print("- Use at least 8 characters.")

if not result["uppercase"]:
    print("- Add an uppercase letter.")

if not result["lowercase"]:
    print("- Add a lowercase letter.")

if not result["number"]:
    print("- Add at least one number.")

if not result["special"]:
    print("- Add at least one special character.")

if result["score"] == 100:
    print("- Excellent! Your password follows all basic security rules.")

if result["score"] < 90:
    print("\nSuggested Strong Password:")
    print(generate_password())

print("\n" + "=" * 50)
print("Thank you for using Password Strength Analyzer!")
print("=" * 50)