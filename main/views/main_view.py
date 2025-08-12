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
    # +998 dan keyin 2 xonali operator kodi va 7 xonali raqam bo'lishi kerak
    return bool(re.match(r'^\+998(33|50|55|77|87|88|90|91|93|94|95|97|98|99)\d{7}$', phone))


def clean_phone_number(raw_number):
    # Faqat raqamlarni qoldiramiz
    digits_only = re.sub(r'\D', '', raw_number)  # 998941234567
    # Agar boshida 998 bo'lmasa, avtomatik qo'shmaymiz (frontend allaqachon qo'yadi)
    if digits_only.startswith("998"):
        return "+" + digits_only
    return "+" + digits_only  # fallback

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

        patients = Patients.objects.all()

        if not all([name, number]):
            messages.error(request, "Ism va telefon raqamini to‘ldiring!")
            return render(request, 'index.html', {'patients': patients})

        # ✅ Raqamni tozalash
        number = clean_phone_number(number)

        # ✅ Format tekshirish
        if not is_valid_uzbek_phone(number):
            messages.error(request, "Telefon raqami noto‘g‘ri formatda! (+998 9X XXX XX XX)")
            return render(request, 'index.html', {'patients': patients})

        # Bazaga yozish
        try:
            ContactUs.objects.create(name=name, number=number)
        except Exception as e:
            print("❌ Bazaga yozishda xatolik:", e)
            messages.error(request, "Maʼlumotni saqlab boʻlmadi.")
            return render(request, 'index.html', {'patients': patients})

        # Telegramga yuborish
        message = f"📥 Yangi murojaat:\n👤 Ism: {name}\n📞 Raqam: {number}"
        send_telegram_message(BOT_TOKEN, CHAT_ID, message)

        messages.success(request, "Muvaffaqiyatli yuborildi!")
        return redirect('main:home')








def categoryDetail(request, slug):

    operations_qs = Operations.objects.prefetch_related('operation_images')
    first_image = None
    

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

    if request.method == 'GET':
        return render(request, 'category_detail.html', context)


    name = request.POST.get('name')
    number = request.POST.get('number')

    if not all([name, number]):
        messages.error(request, "Ism va telefon raqamini to‘ldiring!")
        return render(request, 'category_detail.html', context)

    # ✅ Raqamni tozalash
    number = clean_phone_number(number)

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


