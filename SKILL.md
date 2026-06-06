---
name: docusaurus-github-pages-deploy-and-debug
description: >
  End-to-end skill for diagnosing, fixing, and deploying a Docusaurus static site
  to GitHub Pages via GitHub Actions, including KaTeX math rendering, Mermaid diagrams,
  SRI integrity validation, environment protection rules, and multi-account Git workflows.
version: 1.0.0
author: Agentic AI Coding Assistant
tools_required:
  - node >= 20.0 (LTS 22 recommended for GitHub Actions runners)
  - npm >= 10
  - git >= 2.30
  - gh (GitHub CLI) >= 2.40
  - python3 >= 3.8 (for QA scripts)
  - curl (for SRI hash verification and HTTP checks)
  - openssl (for computing SRI integrity hashes)
---

# Docusaurus + GitHub Pages: Deploy & Debug Skill

Quy trinh toan dien de xay dung, sua loi, va trien khai mot trang Docusaurus len GitHub Pages
thong qua GitHub Actions. Bao gom xu ly cac loi thuong gap nhu: KaTeX math rendering,
Mermaid diagram syntax, SRI integrity hash, environment protection rules, va cau hinh
da tai khoan Git.

---

## 1. DINH HUONG TU DUY & PHONG CACH VIET (Persona & Writing Style)

### Nguyen tac tiep can bai toan

Khi gap mot bao cao loi tu nguoi dung (vi du: "trang khong deploy duoc", "math hien sai"),
hay tuan thu trinh tu sau:

1. **Xac dinh hien tuong truoc, nguyen nhan sau.** Khong gia dinh nguyen nhan tu dau.
   Chay cac lenh chan doan (`git status`, `npm run build`, `gh run view --log-failed`)
   de thu thap bang chung cu the.

2. **Phan tach cac lop loi.** Mot trieu chung duy nhat co the do nhieu lop loi chong len:
   - Lop CI/CD: workflow YAML, Node version, branch trigger.
   - Lop Platform: GitHub Pages source config, environment protection rules.
   - Lop Content: KaTeX integrity hash, Mermaid syntax, broken links.

3. **Giai thich xung dot he thong truoc khi dua ra code fix.** Nguoi dung can hieu
   *tai sao* loi xay ra, khong chi la *lam gi* de sua. Dieu nay giup ho tu xu ly
   cac truong hop tuong tu trong tuong lai.

4. **Verify truoc khi commit.** Luon chay `npm run verify` (hoac tuong duong) truoc
   khi commit bat ky thay doi nao. Khong bao gio push code chua duoc kiem tra.

### Tong giong va ngon ngu

- Giai thich ky thuat ro rang, khong dung jargon khi khong can thiet.
- Khi viet noi dung giao duc (docs), su dung giong giang vien dai hoc: chinh xac,
  kien nhan, tu nhien, va thuc te.
- Khong su dung ky tu em dash (Unicode U+2014). Su dung dau phay, dau hai cham,
  hoac ngoac don thay the.

---

## 2. CAC RANG BUOC BAO MAT & QUYEN RIENG TU (Security & Privacy)

### 2.1 An danh thong tin nhay cam

- **KHONG BAO GIO** de lo cac duong dan tuyet doi cua may cuc bo
  (vi du: `/{HOME_DIR}/username/...`) trong bat ky file nao duoc commit.
- **KHONG** commit credentials, tokens, API keys, hoac private URLs.
- Su dung bien moi truong thay the:
  - `{TARGET_GIT_USERNAME}` - ten tai khoan GitHub muc tieu.
  - `{GITHUB_OWNER}` - chu so huu repository (co the trung voi username).
  - `{REPOSITORY_NAME}` - ten repository.
  - `{DEPLOY_BRANCH}` - nhanh kich hoat deploy (thuong la `main`).
  - `{NODE_VERSION}` - phien ban Node.js (khuyen nghi 22 LTS).

### 2.2 Chan bot tim kiem (SEO Privacy)

Neu du an yeu cau khong duoc index boi cong cu tim kiem:

1. **robots.txt** tai `static/robots.txt`:
   ```
   User-agent: *
   Disallow: /
   ```

2. **Meta tag noindex** trong `docusaurus.config.ts`:
   ```typescript
   headTags: [
     {
       tagName: 'meta',
       attributes: {
         name: 'robots',
         content: 'noindex,nofollow,noarchive,nosnippet',
       },
     },
   ],
   ```

3. **Tat Sitemap** trong preset config:
   ```typescript
   sitemap: false,
   ```

### 2.3 README.md

Neu QA script yeu cau README.md phai rong (0 bytes), tuyệt doi khong viet noi dung
vao file nay. Kiem tra bang:
```bash
test -s README.md && echo "ERROR: README.md must be empty" || echo "OK"
```

---

## 3. QUY TRINH THUC THI & TU DONG HOA (Execution Workflow)

### Buoc 1: Chan doan trang thai hien tai

```bash
# Kiem tra nhanh cuc bo va remote
git status
git branch -a
git remote -v
gh auth status

# Fetch trang thai moi nhat tu remote
git fetch --all --prune

# Kiem tra nhanh mac dinh tren remote
git remote show origin | grep "HEAD branch"
```

### Buoc 2: Chuyen doi tai khoan GitHub CLI (neu can)

Khi may tinh co nhieu tai khoan GitHub dang nhap:

```bash
# Liet ke cac tai khoan da dang nhap
gh auth status

# Chuyen sang tai khoan muc tieu
gh auth switch --user {TARGET_GIT_USERNAME}

# Xac nhan tai khoan active
gh auth status
```

### Buoc 3: Cau hinh Docusaurus cho GitHub Pages

Trong `docusaurus.config.ts`, dam bao cac gia tri sau dung:

```typescript
const config: Config = {
  url: 'https://{GITHUB_OWNER}.github.io',
  baseUrl: '/{REPOSITORY_NAME}/',
  organizationName: '{GITHUB_OWNER}',
  projectName: '{REPOSITORY_NAME}',
  trailingSlash: false,
  // ...
};
```

**Luu y quan trong:** Neu doi ten repository (vi du tu `project` sang `project-v2`),
PHAI cap nhat ca `baseUrl` va `projectName`. Neu khong, tat ca duong dan CSS/JS se bi
sai va trang web se hien thi trang trang.

### Buoc 4: Cau hinh GitHub Actions workflow

File `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - {DEPLOY_BRANCH}
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: {NODE_VERSION}
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Quy tac chon Node version:** Luon dung phien ban LTS (Long Term Support) hien tai.
Node 22 la LTS stable tinh den 2026. Tranh dung phien ban non-LTS (vi du 23, 25)
vi chung co the khong duoc cai san tren GitHub Actions runners, gay cham va loi.

### Buoc 5: Bat GitHub Pages bang API

**Day la buoc QUAN TRONG NHAT** ma nhieu nguoi bo qua. Neu khong bat GitHub Pages
voi source la "GitHub Actions", workflow se LUON that bai voi loi 404.

```bash
# Bat GitHub Pages voi source la GitHub Actions
gh api repos/{GITHUB_OWNER}/{REPOSITORY_NAME}/pages \
  -X POST --input - <<'EOF'
{
  "build_type": "workflow",
  "source": {
    "branch": "{DEPLOY_BRANCH}",
    "path": "/"
  }
}
EOF
```

Neu Pages da duoc bat truoc do (vi du bang "Deploy from a branch"), chuyen sang
GitHub Actions bang lenh PUT:

```bash
gh api repos/{GITHUB_OWNER}/{REPOSITORY_NAME}/pages \
  -X PUT --input - <<'EOF'
{
  "build_type": "workflow",
  "source": {
    "branch": "{DEPLOY_BRANCH}",
    "path": "/"
  }
}
EOF
```

### Buoc 6: Tao repository moi (khi can thiet)

Khi repository cu bi vuong environment protection rules hoac cau hinh khong the
sua duoc, tao repository moi la cach nhanh nhat:

```bash
# Doi ten remote cu
git remote rename origin origin-old

# Tao repo moi va push code
gh repo create {REPOSITORY_NAME} --public --source=. --remote=origin --push
```

Sau khi tao repo moi, PHAI thuc hien lai Buoc 3 (cap nhat baseUrl) va Buoc 5
(bat GitHub Pages).

### Buoc 7: Verify, commit, va push

```bash
# Verify toan bo truoc khi commit
npm run verify   # hoac: npm run build

# Stage, commit, push
git add -A
git commit -m "fix: [mo ta ngan gon]"
git push origin {DEPLOY_BRANCH}
```

### Buoc 8: Theo doi va xac nhan deploy

```bash
# Xem trang thai cac workflow runs
gh run list --repo {GITHUB_OWNER}/{REPOSITORY_NAME} --limit 5

# Xem log chi tiet cua run bi loi
gh run view {RUN_ID} --repo {GITHUB_OWNER}/{REPOSITORY_NAME} --log-failed

# Chay lai workflow bi loi (sau khi da sua cau hinh)
gh run rerun {RUN_ID} --repo {GITHUB_OWNER}/{REPOSITORY_NAME}
```

---

## 4. XU LY LOI THUONG GAP (Troubleshooting Guide)

### 4.1 Loi: "Branch X is not allowed to deploy to github-pages due to environment protection rules"

**Nguyen nhan:** GitHub da tao environment `github-pages` voi quy tac chi cho phep
mot nhanh cu (vi du `codex/init`) deploy. Khi chuyen sang nhanh `main`, bi chan.

**Cach 1 - Sua protection rules (khuyen nghi):**
1. Vao `Settings` > `Environments` > `github-pages`.
2. Trong muc "Deployment branches and tags", chuyen sang "All branches" hoac them
   nhanh `{DEPLOY_BRANCH}` vao danh sach.
3. Chay lai workflow: `gh run rerun {RUN_ID}`.

**Cach 2 - Tao repository moi:** Xem Buoc 6 o tren.

### 4.2 Loi: "Failed to create deployment (status: 404) - Ensure GitHub Pages has been enabled"

**Nguyen nhan:** GitHub Pages chua duoc bat tren repository, hoac source dang de la
"Deploy from a branch" thay vi "GitHub Actions".

**Khac phuc:** Chay lenh bat Pages bang API o Buoc 5.

### 4.3 Loi: Math formula hien thi sai (khong co styling, raw text)

**Nguyen nhan:** SRI (Subresource Integrity) hash cua KaTeX CSS stylesheet bi sai.
Khi hash khong khop, trinh duyet CHAN HOAN TOAN viec tai file CSS, khien tat ca
cong thuc toan mat styling.

**Chan doan:**
```bash
# Tinh hash thuc te tu CDN
curl -s "https://cdn.jsdelivr.net/npm/katex@{KATEX_VERSION}/dist/katex.min.css" \
  | openssl dgst -sha384 -binary | openssl base64 -A

# So sanh voi hash trong docusaurus.config.ts
grep 'integrity' docusaurus.config.ts
```

**Khac phuc:** Cap nhat truong `integrity` trong `docusaurus.config.ts` bang hash
dung vua tinh duoc.

**Phong ngua:** Khi nang cap phien ban KaTeX, LUON tinh lai SRI hash. Khong copy
hash tu tai lieu cu hoac tu cac du an khac.

### 4.4 Loi: Mermaid diagram parse error

**Nguyen nhan:** Mermaid parser su dung cac ky tu `{`, `}`, `(`, `)`, `[`, `]`
lam ky tu dac biet de dinh nghia hinh dang node. Khi noi dung nhan (label) chua
cac ky tu nay, parser bi nham lan.

**Cac truong hop thuong gap va cach sua:**

| Loi | Nguyen nhan | Cach sua |
|-----|-------------|----------|
| `x_{i+1}` trong nhan node | `{` bi hieu la DIAMOND_START | Dung `x_i+1` hoac boc trong dau ngoac kep `"x_{i+1}"` |
| `subgraph Title (N=5)` | `(` bi hieu la node shape | Dung `subgraph Title N=5` hoac `subgraph Title ["N=5"]` |
| `D_off[Decoder State t]` trong subgraph co `(...)` | Loi noi tiep tu subgraph title | Sua subgraph title truoc |
| Node label chua `>`, `<` | Bi hieu la HTML hoac arrow | Escape hoac dung dau ngoac kep |

**Quy tac vang cho Mermaid labels:**
- Boc nhan node phuc tap trong dau ngoac kep: `A["Label co ky tu dac biet {x}"]`
- Tranh dung `{}`, `()` trong subgraph title. Dung `[]` neu can nhom.
- Test diagram tai https://mermaid.live truoc khi commit.

### 4.5 Loi: "Permission denied to {username}" khi push

**Nguyen nhan:** Tai khoan Git dang active khong co quyen ghi vao repository.

**Khac phuc:**
```bash
# Kiem tra tai khoan nao dang active
gh auth status

# Chuyen sang tai khoan co quyen
gh auth switch --user {TARGET_GIT_USERNAME}

# Thu push lai
git push origin {DEPLOY_BRANCH}
```

### 4.6 Loi: Trang hien thi trang trang (blank page) sau deploy

**Nguyen nhan:** `baseUrl` trong `docusaurus.config.ts` khong khop voi ten repository.

**Chan doan:**
```bash
# Kiem tra baseUrl hien tai
grep 'baseUrl' docusaurus.config.ts

# So sanh voi ten repo
git remote get-url origin
```

**Khac phuc:** Dam bao `baseUrl: '/{REPOSITORY_NAME}/'` khop chinh xac voi ten
repository tren GitHub.

---

## 5. TIEU CHUAN XAC MINH HOAN THANH (Verification Checklist)

### 5.1 Kiem tra cuc bo (Local Verification)

```bash
# 1. QA docs (neu co script)
npm run qa:docs 2>&1 | tail -5

# 2. TypeScript typecheck
npm run typecheck

# 3. Build thanh cong
npm run build

# 4. Hoac chay tat ca mot lenh
npm run verify
```

### 5.2 Kiem tra Git clean

```bash
# Khong con file chua commit
test -z "$(git status --porcelain)" && echo "OK: Clean" || echo "ERROR: Uncommitted changes"

# Nhanh hien tai dung
git branch --show-current
```

### 5.3 Kiem tra deploy thanh cong

```bash
# Workflow moi nhat phai la "success"
gh run list --repo {GITHUB_OWNER}/{REPOSITORY_NAME} --limit 1

# Trang web tra ve HTTP 200
curl -sI "https://{GITHUB_OWNER}.github.io/{REPOSITORY_NAME}/" | head -1
# Ky vong: HTTP/2 200
```

### 5.4 Kiem tra noi dung trang web

```bash
# KaTeX CSS duoc load (khong bi chan boi SRI)
curl -s "https://{GITHUB_OWNER}.github.io/{REPOSITORY_NAME}/" \
  | grep -c 'katex'
# Ky vong: >= 1

# Meta noindex ton tai (neu yeu cau privacy)
curl -s "https://{GITHUB_OWNER}.github.io/{REPOSITORY_NAME}/" \
  | grep -o 'noindex[^"]*'
# Ky vong: noindex,nofollow,noarchive,nosnippet

# Sitemap KHONG ton tai (neu yeu cau privacy)
curl -sI "https://{GITHUB_OWNER}.github.io/{REPOSITORY_NAME}/sitemap.xml" \
  | head -1
# Ky vong: HTTP/2 404
```

### 5.5 Kiem tra bao mat

```bash
# robots.txt chan tat ca crawler
curl -s "https://{GITHUB_OWNER}.github.io/{REPOSITORY_NAME}/robots.txt"
# Ky vong:
# User-agent: *
# Disallow: /

# Khong co duong dan cuc bo trong source code
grep -rE '/{HOME_DIR}/' docs/ src/ --include='*.md' --include='*.ts' \
  --include='*.tsx' --include='*.json' && echo "ERROR: Local path found" || echo "OK"

# Khong co em dash (U+2014)
grep -rP '\x{2014}' docs/ src/ --include='*.md' 2>/dev/null \
  && echo "ERROR: Em dash found" || echo "OK"
```

---

## PHU LUC: Lenh tham khao nhanh

| Muc dich | Lenh |
|----------|------|
| Kiem tra tai khoan Git | `gh auth status` |
| Chuyen tai khoan | `gh auth switch --user {USERNAME}` |
| Tao repo moi | `gh repo create {NAME} --public --source=. --remote=origin --push` |
| Bat GitHub Pages | `gh api repos/{OWNER}/{REPO}/pages -X POST --input -` |
| Xem workflow loi | `gh run view {ID} --repo {OWNER}/{REPO} --log-failed` |
| Chay lai workflow | `gh run rerun {ID} --repo {OWNER}/{REPO}` |
| Tinh SRI hash | `curl -s {URL} \| openssl dgst -sha384 -binary \| openssl base64 -A` |
| Build Docusaurus | `npm run build` |
| Serve cuc bo | `npm run serve` |
