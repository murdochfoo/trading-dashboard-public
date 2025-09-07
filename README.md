# 🚀 **SUPER SIMPLE COMMANDS** 

Just run these in Claude Code terminal:

## **Daily Work** (95% of the time)
```bash
cd /home/ib/trading-dashboard-dev

./dev                           # Start coding (opens localhost:8000)
./save "what you changed"       # Save your work
./deploy-staging               # Send to staging
./deploy-production            # Make it live
```

## **Check Status**
```bash
./status                       # See what needs deployment
./check-live                   # Test if website works
./help                         # Show all commands
```

## **Emergency**
```bash
./rollback                     # Undo last deployment
```

---

## **That's It! 🎉**

- **Work**: `./dev` → edit files → save/refresh browser
- **Deploy**: `./deploy-staging` → `./deploy-production`  
- **Check**: `./status` and `./check-live`

**No more complex git commands to remember!**

---

### **The old way** ❌:
```bash
cd /home/ib/trading-dashboard-dev
git checkout development  
git add .
git commit -m "message"
git push origin development
git checkout staging
git pull origin staging
git merge development
git push origin staging
# ... 10 more commands
```

### **The new way** ✅:
```bash
./deploy-staging
```

**Done!** 🎯