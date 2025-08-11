import os
import re
import requests
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages  
from dotenv import load_dotenv
from main.models import ContactUs, Patients , Category
from django.db.models import Prefetch
from main.models import Operations
from django.shortcuts import get_object_or_404

# .env fayldan token va chat_id ni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def is_valid_uzbek_phone(phone):
    return bool(re.match(r'^\+998(33|50|55|77|87|88|90|91|93|94|95|97|98|99)\d{7}$', phone))


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Telegramga yuborishda xatolik:", e)


class homePage(View):
    def get(self, request):
        patients = Patients.objects.all()
        categories = Category.objects.all()
        context = {
            'patients': patients,
            'categories': categories
        }
        return render(request, 'index.html', context)

    def post(self, request):
        name = request.POST.get('name')
        number = request.POST.get('number')
        print(name, number)

        patients = Patients.objects.all()  # qayta render uchun

        # 🔸 1. Bo‘sh joylarni tekshirish
        if not all([name, number]):
            messages.error(request, "Ism va telefon raqamini to‘ldiring!")
            return render(request, 'index.html', {'patients': patients})

        # 🔸 2. Telefon formatini tekshirish
        number = number.replace(' ', '')
        if not is_valid_uzbek_phone(number):
            messages.error(request, "Telefon raqami noto‘g‘ri formatda! (+998 9X XXX XX XX)")
            return render(request, 'index.html', {'patients': patients})

        # 🔸 3. Bazaga yozish
        try:
            ContactUs.objects.create(name=name, number=number)
        except Exception as e:
            print("❌ Bazaga yozishda xatolik:", e)
            messages.error(request, "Maʼlumotni saqlab boʻlmadi.")
            return render(request, 'index.html', {'patients': patients})

        # 🔸 4. Telegramga yuborish
        message = f"📥 Yangi murojaat:\n👤 Ism: {name}\n📞 Raqam: {number}"
        send_telegram_message(BOT_TOKEN, CHAT_ID, message)

        messages.success(request, "Muvaffaqiyatli yuborildi!")
        return redirect('main:home')








def categoryDetail(request, slug):
    # OperationImages'ni oldindan olish
    operations_qs = Operations.objects.prefetch_related('operation_images')
    first_image = None
    
    # Category'ni olish
    category = get_object_or_404(
        Category.objects.prefetch_related(
            Prefetch('operations', queryset=operations_qs)
        ).defer('img'),
        slug=slug
    )

    context = {
        'category': category,
        'operations': category.operations.all(),
    }

    # 🔹 GET request bo‘lsa, faqat sahifani render qilamiz
    if request.method == 'GET':
        return render(request, 'category_detail.html', context)

    # 🔹 POST bo‘lsa, formani tekshiramiz
    name = request.POST.get('name')
    number = request.POST.get('number')

    if not all([name, number]):
        messages.error(request, "Ism va telefon raqamini to‘ldiring!")
        return render(request, 'category_detail.html', context)

    number = number.replace(' ', '')
    if not is_valid_uzbek_phone(number):
        messages.error(request, "Telefon raqami noto‘g‘ri formatda! (+998 9X XXX XX XX)")
        return render(request, 'category_detail.html', context)

    try:
        ContactUs.objects.create(name=name, number=number)
    except Exception as e:
        print("❌ Bazaga yozishda xatolik:", e)
        messages.error(request, "Maʼlumotni saqlab boʻlmadi.")
        return render(request, 'category_detail.html', context)

    message = f"📥 Yangi murojaat:\n👤 Ism: {name}\n📞 Raqam: {number}"
    send_telegram_message(BOT_TOKEN, CHAT_ID, message)

    messages.success(request, "Muvaffaqiyatli yuborildi!")
    return redirect('main:category_detail', slug=slug)

