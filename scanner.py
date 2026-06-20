import requests

target = input("Enter target URL: ")

try:
    response = requests.get(target)

    findings = []

    print("\n=== Target Information ===")
    print("Status Code:", response.status_code)

    print("\n=== HTTP Headers ===")

    for header, value in response.headers.items():
        print(f"{header}: {value}")

except Exception as e:
    print("Error:", e)
    exit()

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

        if header == "Strict-Transport-Security":
            findings.append(("Missing HSTS Header", "HIGH"))

        elif header == "Content-Security-Policy":
            findings.append(("Missing CSP Header", "MEDIUM"))

        else:
            findings.append((f"Missing {header}", "LOW"))

if "Server" in response.headers:
    findings.append(("Server Header Exposed", "LOW"))

if "X-Powered-By" in response.headers:
    findings.append(("X-Powered-By Header Exposed", "MEDIUM"))

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
            directory_response = requests.get(url, timeout=3)

            if directory_response.status_code == 200:
                print(f"[FOUND] {url}")

        except:
            pass

except FileNotFoundError:
    print("wordlist.txt not found")

print("\n=== Risk Assessment ===")

for issue, risk in findings:
    print(f"[{risk}] {issue}")

html_content = f"""
<html>
<head>
    <title>Web Security Report</title>
</head>
<body>

<h1>Web Application Security Assessment</h1>

<p><strong>Target:</strong> {target}</p>

<h2>Findings</h2>

<table border="1">
<tr>
<th>Issue</th>
<th>Risk</th>
</tr>
"""

for issue, risk in findings:
    html_content += f"""
<tr>
<td>{issue}</td>
<td>{risk}</td>
</tr>
"""

html_content += """
</table>

</body>
</html>
"""

with open("reports/report.html", "w") as report:
    report.write(html_content)

print("\n[+] HTML report generated: reports/report.html")
