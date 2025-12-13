# BotoEase

BotoEase is a smart, lightweight file storage library for Python that gives you a **unified API** for working with both **Local Storage** and **AWS S3**.  
It removes the complexity of `boto3` and lets developers upload, delete, and generate URLs in a clean and simple way.

Perfect for backend developers working with FastAPI, Flask, Django, or CLI tools.

---

## 🚀 Features

- Upload files to **Local Storage** with one line  
- Upload files to **AWS S3** without writing boto3 logic  
- Delete files (local & S3)  
- Generate S3 pre-signed URLs  
- Auto-create local upload directories  
- Clean unified API for both storage types  

---

## 📦 Installation

Install BotoEase directly from PyPI:

```bash
pip install botoease
```

-----

## 🔧 Usage

Import the Storage class:

```python
from botoease import Storage
```

### 🗂️ 1. Local Storage (Default)

Files are saved to a folder on your machine.

```python
storage = Storage(backend="local", folder="my_uploads")

result = storage.upload("example.png")
print(result)
```

**Example Output:**

```json
{
  "storage": "local",
  "path": "my_uploads/example.png",
  "filename": "example.png"
}
```

**Generate a local file path:**

```python
url = storage.generate_url("example.png")
print(url)
```

### ☁️ 2. AWS S3 Storage

Upload files to an S3 bucket without writing `boto3` code.

```python
storage = Storage(
    backend="s3",
    bucket="my-bucket-name",
    region="us-east-1",
    access_key="YOUR_AWS_ACCESS_KEY",
    secret_key="YOUR_AWS_SECRET_KEY"
)

result = storage.upload("image.jpg")
print(result)
```

**Example Output:**

```json
{
  "storage": "s3",
  "bucket": "my-bucket-name",
  "filename": "image.jpg",
  "url": "https://my-bucket-name.s3.us-east-1.amazonaws.com/image.jpg"
}
```

**Generate a pre-signed URL:**

```python
url = storage.generate_url("image.jpg", expires=3600)
print(url)
```

**Delete a file from S3:**

```python
storage.delete("image.jpg")
```

### 🧹 3. Delete a File (Local or S3)

```python
storage.delete("example.png")
```

-----

## 🔒 Security Notes

> **Important:** Your AWS credentials are used directly to create the boto3 client.
>
>   * Consider storing keys in environment variables (e.g., `.env`) for production.
>   * **Never commit real credentials to GitHub.**

-----

## 📈 Upcoming Features (Next Releases)

These improvements are planned for future versions of BotoEase:

### 🔜 Version Roadmap

**v0.1.0**

  - [ ] Automatic UUID renaming to prevent file collisions
  - [ ] Automatic year/month/day folder structure (e.g., `2025/02/09/file.jpg`)
  - [ ] File type validation (MIME detection)
  - [ ] File size limit enforcement

**v0.2.0**

  - [ ] Google Cloud Storage support
  - [ ] Azure Blob Storage support

**v0.3.0**

  - [ ] Optional encryption before upload
  - [ ] Custom domain support for S3 URLs

**v1.0.0**

  - [ ] Async API (perfect for FastAPI)
  - [ ] Background uploads
  - [ ] Multipart upload for large files

-----

View this project on PyPI: [https://pypi.org/project/botoease/](https://pypi.org/project/botoease/)

## 🤝 Contributing

Contributions are welcome!  
Open a pull request or start a discussion if you want to suggest new features.

## 📜 License

MIT License.  
Feel free to use BotoEase in personal and commercial projects.

## ⭐ Support

If you find this package helpful, please give it a star on GitHub!
