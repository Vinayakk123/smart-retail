# Start Guide

Run all commands from the project root:

`C:\Users\wanna\Desktop\data-for-shops`

## 1) Create and set up Python virtual environment (PowerShell)

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2) Start backend server (new terminal)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
cd Backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 3) Start frontend server (another new terminal)

```powershell
cd Frontend
npm install
npm run dev
```

## URLs

- Frontend: http://localhost:8080
- Backend API docs: http://localhost:8000/docs
