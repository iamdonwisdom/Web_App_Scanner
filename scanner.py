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

print("\n=== robots.txt Analysis ===")

robots_url = target.rstrip("/") + "/robots.txt"

try:
    robots_response = requests.get(robots_url)

    if robots_response.status_code == 200:
        print(f"[+] robots.txt found: {robots_url}")

        sensitive_paths = [
            "/admin",
            "/login",
            "/private",
            "/backup"
        ]

        for path in sensitive_paths:
            if path in robots_response.text:
                print(f"[FOUND] {path}")

    else:
        print("[-] robots.txt not found")

except Exception as e:
    print("Error checking robots.txt:", e)

print("\n=== Directory Enumeration ===")

try:
    with open("wordlist.txt", "r") as file:
        directories = file.readlines()

    for directory in directories:
        directory = directory.strip()

        url = target.rstrip("/") + "/" + directory

        try:
            response = requests.get(url, timeout=3)

            if response.status_code == 200:
                print(f"[FOUND] {url}")

        except:
            pass

except FileNotFoundError:
    print("wordlist.txt not found")
