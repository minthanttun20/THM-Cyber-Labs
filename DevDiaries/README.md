# Dev Diaries

![Header](./img/header.png)

---

## 1. What is the subdomain where the development version of the website is hosted?

Install subfinder:

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

> **Command not found fix:**
> ```bash
> export PATH=$PATH:$(go env GOPATH)/bin
> ```

Run:

```bash
subfinder -d marvenly.com
```

![Output1](./img/output1.png)

---

## 2. What is the GitHub username of the developer?

Go to `uat-testing.marvenly.com`, open the site → Right-click → **View Page Source**

![Output2](./img/output2.png)

---

## 3. What is the developer's email address?

Clone the repo and run:

```bash
git log
```

![Output3](./img/output3.png)

---

## 4. What reason did the developer mention in the commit history for removing the source code?

![Output4](./img/output4.png)

---

## 5. What is the value of the hidden flag?

![Output5](./img/output5.png)