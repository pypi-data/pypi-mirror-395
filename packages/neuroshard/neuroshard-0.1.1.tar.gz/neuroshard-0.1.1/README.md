# NeuroShard

**NeuroShard — Content-Addressed, Chunked Model Versioning**

> "Git for AI models. Fast. Deduplicated. Reproducible."

NeuroShard is a version control system designed specifically for large AI models and datasets. It solves the "Git LFS problem" by splitting large files into deduplicated, compressed chunks (shards) and storing only the changes. Manifests are small JSON files that track these chunks and are committed directly to Git, ensuring perfect reproducibility.

## 🚀 Key Features

- **⚡ Fast Incremental Pushes**: Only upload changed chunks (4MB blocks).
- **🧱 Deduplication**: Store unique blocks once, across all model versions.
- **🔒 Integrity**: SHA-256 verification for every block.
- **📝 Git Integration**: Manifests live in Git; data lives in NeuroShard.
- **🧰 Storage Agnostic**: Works with local storage and HTTP remotes (S3 coming soon).

## 📦 Installation

```bash
pip install neuroshard
```

## ⚡ Quickstart

### 1. Initialize
Initialize a NeuroShard repository in your project. This sets up the `.shard` directory.

```bash
nshard init
nshard git-init  # Configures .gitignore
```

### 2. Track a Model
Tell NeuroShard to track your large model files.

```bash
nshard track models/resnet50.pth
```

### 3. Commit
Chunk the file, compute hashes, and create a manifest.

```bash
nshard commit -m "Initial checkpoint"
```
This creates a `models/resnet50.pth.shard.json` file. **Commit this JSON file to Git.**

```bash
git add models/resnet50.pth.shard.json
git commit -m "Add model checkpoint"
```

### 4. Push to Remote (Data)
Upload your shards (the heavy data) to a Shard server.

```bash
# Start a local server for testing (in a separate terminal)
python -m shard.server.app

# Push data to the server
nshard push --remote http://localhost:8000
```

### 5. Push to Git (Manifests)
Upload the manifests (the lightweight JSON pointers) to GitHub.

```bash
git add models/resnet50.pth.shard.json
git commit -m "Add model checkpoint"
git push origin main
```

### 6. Pull and Checkout
On another machine:
1. `git pull` (gets the manifest)
2. `nshard pull ...` (gets the data)

```bash
git pull
nshard pull models/resnet50.pth.shard.json --remote http://localhost:8000
nshard checkout models/resnet50.pth.shard.json
```

## 🌍 Real World Workflow (Example)

Imagine you are working on **MedScan-AI** and have a **10GB model file** (`models/brain_scan_v1.pth`). You cannot push this to GitHub.

### 0. Prerequisite (Colleague's Machine)
Your colleague needs NeuroShard to get the data. They can install it easily:

```bash
# Option A: Install globally
pip install neuroshard

# Option B: Run without installing (like npx)
# First, install pipx if you don't have it:
python -m pip install --user pipx
python -m pipx ensurepath

# Then run nshard:
pipx run neuroshard help
```

### 1. Setup (One time)
```bash
cd MedScan-AI
nshard init
nshard git-init
```

### 2. Version the Heavy Model
```bash
# 1. Track the big file
nshard track models/brain_scan_v1.pth

# 2. Commit it (Chunks it locally)
nshard commit -m "Add v1 model"
# -> Creates models/brain_scan_v1.pth.shard.json
```

### 3. Push Data (To Shard Server)
Send the 10GB of data to your storage server (not GitHub).
```bash
nshard push --remote http://your-shard-server.com
```

### 4. Push Code (To GitHub)
Send the tiny manifest file to GitHub.
```bash
git add models/brain_scan_v1.pth.shard.json
git commit -m "Add model v1"
git push origin main
```

### 5. Colleague Pulls
Your colleague clones the repo and gets the model.
```bash
git pull
nshard pull models/brain_scan_v1.pth.shard.json --remote http://your-shard-server.com
nshard checkout models/brain_scan_v1.pth.shard.json
```

## 🛠 CLI Commands

- `nshard init`: Initialize a new NeuroShard repo.
- `nshard track <file>`: Start tracking a file.
- `nshard commit -m <msg>`: Chunk and commit tracked files.
- `nshard status`: Show status of tracked files.
- `nshard diff <file>`: Show block-level diff stats.
- `nshard push`: Push to remote.
- `nshard pull`: Pull from remote.
- `nshard gc`: Garbage collect unused blocks.

## 🤝 Contributing

Contributions are welcome! Please run tests before submitting a PR.

```bash
python -m unittest discover tests
```

## 📜 License

MIT
