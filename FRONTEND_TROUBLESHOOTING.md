# Frontend npm install Troubleshooting

## Problem: npm install gets stuck or takes too long

### Quick Solutions

#### Option 1: Wait (if it's still running)
`npm install` can take 2-5 minutes depending on your internet speed. Check if:
- The terminal shows any activity (downloading packages)
- Your internet connection is working
- You see progress indicators

#### Option 2: Cancel and Retry
1. Press `Ctrl+C` to cancel
2. Delete `node_modules` folder (if it exists):
   ```powershell
   cd frontend
   Remove-Item -Recurse -Force node_modules
   ```
3. Clear npm cache:
   ```powershell
   npm cache clean --force
   ```
4. Try again:
   ```powershell
   npm install
   ```

#### Option 3: Use npm with verbose output
See what's happening:
```powershell
npm install --verbose
```

#### Option 4: Use yarn instead (faster alternative)
```powershell
# Install yarn globally (if not installed)
npm install -g yarn

# Use yarn instead
cd frontend
yarn install
```

#### Option 5: Skip optional dependencies
If it's stuck on optional dependencies:
```powershell
npm install --no-optional
```

### Check if installation completed

After running `npm install`, check if it completed:
```powershell
# Check if node_modules exists and has content
Test-Path node_modules
Get-ChildItem node_modules | Measure-Object
```

### If installation completed, just run dev server

If `node_modules` exists and has packages, you can skip `npm install` and go straight to:
```powershell
npm run dev
```

---

## Common Issues

### 1. Network/Firewall Issues
- Check if you're behind a corporate firewall
- Try using a different network
- Configure npm proxy if needed

### 2. Node.js Version
Make sure you have Node.js 18+ installed:
```powershell
node --version
```

### 3. npm Version
Update npm to latest:
```powershell
npm install -g npm@latest
```

### 4. Permission Issues (Windows)
Run PowerShell as Administrator if you see permission errors.

---

## Quick Test

After installation, verify it worked:
```powershell
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

---

## Alternative: Minimal Installation

If you just want to test quickly, you can install only essential packages:
```powershell
npm install react react-dom react-router-dom axios vite @vitejs/plugin-react typescript
```

Then run:
```powershell
npm run dev
```

