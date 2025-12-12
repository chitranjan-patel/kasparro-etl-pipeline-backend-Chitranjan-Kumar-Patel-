#!/bin/bash
# KASPARRO BACKEND - RENDER.COM DEPLOYMENT SCRIPT
# यह script tumhe Render पर deploy करने में मदद करेगा

echo "════════════════════════════════════════════════════════"
echo "  KASPARRO BACKEND - RENDER.COM DEPLOYMENT HELPER"
echo "════════════════════════════════════════════════════════"
echo ""

# Step 1: GitHub Setup
echo "📝 STEP 1: GitHub Setup"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "अगर तुम्हारे पास GitHub account नहीं है:"
echo "  1. जाओ: https://github.com/signup"
echo "  2. Sign up करो"
echo ""
echo "अगर GitHub account है:"
echo "  1. इस project को अपने GitHub पर push करो:"
echo ""
echo "    git init"
echo "    git add ."
echo "    git commit -m 'Kasparro Backend - Production Ready'"
echo "    git branch -M main"
echo "    git remote add origin https://github.com/YOUR_USERNAME/kasparro-backend.git"
echo "    git push -u origin main"
echo ""
echo "✅ अगर यह successful है तो STEP 2 पर जाओ"
echo ""
read -p "GitHub पर push कर दिया? (y/n): " github_done

if [ "$github_done" != "y" ]; then
    echo "❌ पहले GitHub पर push करो, फिर दोबारा run करना"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "📝 STEP 2: Render.com Setup"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "1. जाओ: https://render.com"
echo "2. 'Sign up with GitHub' पर click करो"
echo "3. GitHub authorization दो"
echo ""
echo "✅ Render account बना दिया?"
echo ""
read -p "Render पर account बना लिया? (y/n): " render_account

if [ "$render_account" != "y" ]; then
    echo "❌ पहले Render पर account बनाओ"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "📝 STEP 3: Create Web Service"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "1. Render Dashboard पर जाओ: https://dashboard.render.com"
echo "2. Top-right में '+' बटन दबाओ"
echo "3. 'Web Service' चुनो"
echo "4. अपना GitHub repo select करो (kasparro-backend)"
echo "5. 'Connect' पर click करो"
echo ""
echo "✅ GitHub repo Render से connect हो गया?"
echo ""
read -p "GitHub connect कर दिया? (y/n): " github_connected

if [ "$github_connected" != "y" ]; then
    echo "❌ GitHub को Render से connect करो"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "📝 STEP 4: Configure Service"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "ये settings करो:"
echo ""
echo "  Name: kasparro-backend"
echo "  Environment: Docker"
echo "  Region: अपने पास वाला region चुनो (India अगर available हो)"
echo "  Plan: Free (unlimited for free tier)"
echo ""
echo "✅ Configuration complete किया?"
echo ""
read -p "Configuration complete? (y/n): " config_done

if [ "$config_done" != "y" ]; then
    echo "❌ Configuration को complete करो"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "📝 STEP 5: Environment Variables"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "'Environment' section में यह variables add करो:"
echo ""
echo "  Name: DATABASE_URL"
echo "  Value: sqlite:///./etl.db"
echo ""
echo "  Name: API_SOURCE_URL"
echo "  Value: https://api.coingecko.com/api/v3/coins/markets"
echo ""
echo "  Name: API_KEY"
echo "  Value: (खाली छोड़ दो - CoinGecko को auth की जरूरत नहीं)"
echo ""
echo "✅ Environment variables add कर दिए?"
echo ""
read -p "Environment variables add किए? (y/n): " env_done

if [ "$env_done" != "y" ]; then
    echo "❌ Environment variables को add करो"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "📝 STEP 6: Deploy"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "अब बस 'Create Web Service' या 'Deploy' बटन दबाओ"
echo ""
echo "⏳ Render अब:"
echo "  1. तुम्हारे repo को clone करेगा"
echo "  2. Dockerfile को read करेगा"
echo "  3. Docker image build करेगा"
echo "  4. Container start करेगा"
echo "  5. Public URL generate करेगा"
echo ""
echo "यह 2-5 minutes लग सकता है..."
echo ""
echo "✅ Deploy बटन दबाया?"
echo ""
read -p "Deploy शुरू हो गया? (y/n): " deploy_done

if [ "$deploy_done" != "y" ]; then
    echo "❌ 'Deploy' या 'Create Web Service' बटन दबाओ"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "📝 STEP 7: Check Deployment Status"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "Dashboard में अपना service देखो:"
echo "  • 'Building...' - Docker image बन रहा है"
echo "  • 'Deploying...' - Container start हो रहा है"  
echo "  • 'Live' - ✅ Deploy successful!"
echo ""
echo "Logs देखने के लिए 'Logs' tab पर click करो"
echo ""
echo "✅ Status देख सकते हो?"
echo ""
read -p "Status check किया? (y/n): " status_done

echo ""
echo "════════════════════════════════════════════════════════"
echo "📝 STEP 8: Test Your API"
echo "─────────────────────────────────────────────────────────"
echo ""
echo "जब 'Live' status show हो, तो:"
echo ""
echo "तुम्हारा public URL होगा कुछ ऐसा:"
echo "  https://kasparro-backend-xxxxx.onrender.com"
echo ""
echo "इन endpoints को test करो:"
echo ""
echo "  📊 API Docs:"
echo "  https://your-url.onrender.com/docs"
echo ""
echo "  📈 Get Data:"
echo "  https://your-url.onrender.com/data"
echo ""
echo "  ✅ Health Check:"
echo "  https://your-url.onrender.com/health"
echo ""
echo "  📊 Statistics:"
echo "  https://your-url.onrender.com/stats"
echo ""
read -p "Public URL का status: 'Live' है? (y/n): " live_done

if [ "$live_done" = "y" ]; then
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "🎉 DEPLOYMENT SUCCESSFUL! 🎉"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "तुम्हारा Kasparro backend अब publicly live है!"
    echo ""
    echo "अब क्या करना है:"
    echo "  1. अपना public URL copy करो"
    echo "  2. Kasparro के form में submit करो"
    echo "  3. URLs test करो (browser में खोलकर देखो)"
    echo ""
    echo "✅ सब ready है!"
else
    echo ""
    echo "⏳ अभी deployment चल रही है..."
    echo "कुछ minutes में दोबारा check करना"
    echo ""
    echo "अगर error मिले तो logs देखो:"
    echo "  Render Dashboard → Logs"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "Need help? Check these files:"
echo "  • README.md - Complete guide"
echo "  • QUICK_START.md - Quick reference"
echo "  • DEPLOYMENT_CHANGES.md - What changed"
echo "════════════════════════════════════════════════════════"
