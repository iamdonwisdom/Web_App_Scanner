import requests

target = input("Enter target URL: ")

try:
    response = requests.get(target)

    print("\n=== Target Information ===")
    print("Status Code:", response.status_code)

    print("\n=== HTTP Headers ===")

    for header, value in response.headers.items():
        print(f"{header}: {value}")

except Exception as e:
    print("Error:", e)

print("\n=== Security Header Analysis ===")

security_headers = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
]

for header in security_headers:
    if header in response.headers:
        print(f"[+] {header} Present")
    else:
        print(f"[-] {header} Missing")
