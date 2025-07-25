# دليل رفع البوت على استضافة تليجرام

## 🤖 أفضل منصات الاستضافة للبوتات

### 1. **PythonAnywhere** ⭐ (الأفضل للمبتدئين)
- **مجاني**: 3 شهور مجانية
- **سهل الاستخدام**: واجهة ويب بسيطة
- **دعم Python**: مخصص للغة Python
- **رابط التسجيل**: [pythonanywhere.com](https://www.pythonanywhere.com)

**خطوات الرفع:**
1. أنشئ حساب مجاني
2. اذهب إلى "Files" وارفع ملفات المشروع
3. افتح "Bash Console" ونفذ:
   ```bash
   pip3.10 install --user -r requirements.txt
   python3.10 main.py
   ```

### 2. **Replit** 🚀 (سهل ومجاني)
- **مجاني تماماً**
- **تشغيل مباشر**: بدون إعداد معقد
- **رابط التسجيل**: [replit.com](https://replit.com)

**خطوات الرفع:**
1. أنشئ حساب على Replit
2. اضغط "Create Repl" → "Import from GitHub"
3. الصق رابط مستودع GitHub الخاص بك
4. اضغط "Run" والبوت سيعمل!

### 3. **Heroku** 💪 (للمحترفين)
- **خطة مجانية محدودة**
- **موثوق جداً**
- **رابط التسجيل**: [heroku.com](https://heroku.com)

### 4. **Railway** ⚡ (حديث وسريع)
- **5$ مجانية شهرياً**
- **نشر تلقائي**
- **رابط التسجيل**: [railway.app](https://railway.app)

### 5. **Render** 🌟 (بديل ممتاز)
- **خطة مجانية**
- **SSL مجاني**
- **رابط التسجيل**: [render.com](https://render.com)

## 📋 الإعداد السريع

### للمنصات السحابية:
1. **ارفع الكود على GitHub**
2. **اربط المستودع بمنصة الاستضافة**
3. **اضبط متغيرات البيئة:**
   - `TELEGRAM_BOT_TOKEN`: 8434259985:AAFFJ-EEj2x5HzysYvK4Ag0t8yJHz0Hy4o8
   - `ADMIN_USER_ID`: 933343496

### للخوادم الخاصة (VPS):
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Python و pip
sudo apt install python3 python3-pip git -y

# استنساخ المشروع
git clone YOUR_REPO_URL
cd media-downloader-bot

# تثبيت المتطلبات
pip3 install -r requirements.txt

# تشغيل البوت
python3 main.py
```

## 🔧 إعداد البوت للعمل 24/7

### استخدام systemd (Linux):
```bash
# إنشاء ملف الخدمة
sudo nano /etc/systemd/system/telegram-bot.service
```

محتوى الملف:
```ini
[Unit]
Description=Telegram Media Downloader Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/your/bot
ExecStart=/usr/bin/python3 /path/to/your/bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

تفعيل الخدمة:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
```

### استخدام PM2 (Node.js):
```bash
# تثبيت PM2
npm install -g pm2

# تشغيل البوت
pm2 start main.py --name telegram-bot --interpreter python3

# حفظ التكوين
pm2 save
pm2 startup
```

## 🌐 الاستضافة المجانية الموصى بها

### 1. **Replit** (الأسهل):
- مجاني 100%
- لا يحتاج خبرة تقنية
- واجهة سهلة

### 2. **PythonAnywhere** (الأفضل):
- 3 شهور مجانية
- مخصص لـ Python
- دعم فني ممتاز

### 3. **Railway** (الأسرع):
- 5$ مجانية شهرياً
- نشر تلقائي
- أداء عالي

## 🔒 نصائح الأمان

1. **لا تشارك التوكن**: احتفظ بتوكن البوت سرياً
2. **استخدم متغيرات البيئة**: لا تضع التوكن في الكود
3. **فعل المصادقة الثنائية**: لحسابات الاستضافة
4. **راقب السجلات**: تحقق من الأخطاء بانتظام

## 📊 مراقبة البوت

### فحص حالة البوت:
```bash
# فحص السجلات
tail -f bot.log

# فحص استخدام الذاكرة
ps aux | grep python

# فحص المساحة المتاحة
df -h
```

### تنبيهات تلقائية:
يمكنك إضافة تنبيهات عبر البريد الإلكتروني أو تليجرام عند توقف البوت.

## 🚨 استكشاف الأخطاء

### البوت لا يرد:
1. تحقق من صحة التوكن
2. راجع السجلات للأخطاء
3. تأكد من تشغيل الخدمة

### مشاكل التحميل:
1. تحقق من اتصال الإنترنت
2. راجع حدود حجم الملفات
3. تحقق من صلاحيات المجلدات

### نفاد الذاكرة:
1. قلل عدد التحميلات المتزامنة
2. احذف الملفات المؤقتة بانتظام
3. ارفع خطة الاستضافة

## 📞 الدعم

إذا واجهت مشاكل:
1. راجع السجلات في `bot.log`
2. تحقق من إعدادات التكوين
3. تأكد من تحديث المتطلبات
4. راجع وثائق منصة الاستضافة

---

**نصيحة**: ابدأ بـ Replit للتجربة السريعة، ثم انتقل لـ PythonAnywhere أو Railway للاستخدام طويل المدى.