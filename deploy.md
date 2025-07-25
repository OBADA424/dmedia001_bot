# دليل النشر - Deployment Guide

## خيارات الاستضافة المتاحة

### 1. Railway (الأسهل والأسرع) ⭐ مُوصى به

Railway منصة استضافة حديثة وسهلة الاستخدام:

**الخطوات:**
1. اذهب إلى [railway.app](https://railway.app)
2. سجل دخول بحساب GitHub
3. اضغط "New Project" → "Deploy from GitHub repo"
4. ارفع الكود إلى GitHub واختر المستودع
5. Railway سيكتشف `railway.json` تلقائياً
6. البوت سيعمل فوراً!

**المميزات:**
- ✅ مجاني حتى 5$ شهرياً
- ✅ نشر تلقائي عند تحديث الكود
- ✅ قواعد بيانات مدمجة
- ✅ SSL مجاني

### 2. Render (بديل ممتاز)

**الخطوات:**
1. اذهب إلى [render.com](https://render.com)
2. سجل دخول وأنشئ "New Web Service"
3. اربط مستودع GitHub
4. Render سيستخدم `render.yaml` تلقائياً
5. انتظر النشر!

**المميزات:**
- ✅ خطة مجانية متاحة
- ✅ SSL تلقائي
- ✅ نشر من GitHub

### 3. Heroku (الأكثر شهرة)

**الخطوات:**
1. أنشئ حساب على [heroku.com](https://heroku.com)
2. ثبت Heroku CLI
3. في مجلد المشروع:
```bash
heroku create your-bot-name
git add .
git commit -m "Deploy bot"
git push heroku main
```

**أو استخدم الزر السريع:**
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### 4. Fly.io (للمطورين المتقدمين)

**الخطوات:**
1. ثبت flyctl: `curl -L https://fly.io/install.sh | sh`
2. سجل دخول: `flyctl auth login`
3. في مجلد المشروع:
```bash
flyctl launch
flyctl deploy
```

### 5. DigitalOcean App Platform

**الخطوات:**
1. اذهب إلى [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. أنشئ "App" جديد
3. اربط مستودع GitHub
4. اختر "Dockerfile" كطريقة البناء
5. انشر!

### 6. Google Cloud Run

**الخطوات:**
1. فعل Google Cloud Run API
2. ثبت gcloud CLI
3. في مجلد المشروع:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/media-bot
gcloud run deploy --image gcr.io/PROJECT-ID/media-bot --platform managed
```

## إعداد متغيرات البيئة

لكل منصة، تأكد من إضافة:
- `TELEGRAM_BOT_TOKEN`: 8434259985:AAFFJ-EEj2x5HzysYvK4Ag0t8yJHz0Hy4o8
- `ADMIN_USER_ID`: 933343496

## نصائح مهمة

### الأمان:
- ✅ لا تشارك التوكن مع أحد
- ✅ استخدم متغيرات البيئة دائماً
- ✅ فعل المصادقة الثنائية لحسابات الاستضافة

### الأداء:
- ✅ راقب استخدام الذاكرة والمعالج
- ✅ استخدم CDN للملفات الكبيرة
- ✅ فعل التخزين المؤقت

### المراقبة:
- ✅ راجع السجلات بانتظام
- ✅ اضبط تنبيهات للأخطاء
- ✅ راقب وقت التشغيل

## استكشاف الأخطاء

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

## التحديثات التلقائية

معظم المنصات تدعم النشر التلقائي عند تحديث الكود في GitHub:

1. اربط المستودع بمنصة الاستضافة
2. فعل "Auto Deploy" أو "Continuous Deployment"
3. كل تحديث في GitHub سيُنشر تلقائياً!

## الدعم

إذا واجهت مشاكل:
1. راجع السجلات أولاً
2. تحقق من إعدادات متغيرات البيئة
3. تأكد من تحديث المتطلبات
4. راجع وثائق منصة الاستضافة

---

**نصيحة:** ابدأ بـ Railway أو Render للسهولة، ثم انتقل لمنصات أخرى حسب احتياجاتك.