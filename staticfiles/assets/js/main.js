const swiper = new Swiper('.mySwiper', {
  slidesPerView: 4,
  spaceBetween: 20,
  loop: true,
  autoplay: {
    delay: 5000,
    disableOnInteraction: false,
  },
  breakpoints: {
    0: { slidesPerView: 1 },
    576: { slidesPerView: 2 },
    768: { slidesPerView: 3 },
    992: { slidesPerView: 4 }
  }
});

const videoSwiper = new Swiper('.videoSwiper', {
  slidesPerView: 4,
  spaceBetween: 20,
  loop: true,
  navigation: {
    nextEl: '.swiper-button-next-custom',
    prevEl: '.swiper-button-prev-custom',
  },
  breakpoints: {
    0: { slidesPerView: 1 },
    576: { slidesPerView: 2 },
    768: { slidesPerView: 3 },
    992: { slidesPerView: 4 }
  }
});

document.querySelectorAll(".faq-question").forEach(button => {
  button.addEventListener("click", () => {
    const faqItem = button.parentElement;
    const isActive = faqItem.classList.contains("active");

    // Yopilgan bo‘lsa ochamiz, ochilgan bo‘lsa yopamiz
    document.querySelectorAll(".faq-item").forEach(item => {
      item.classList.remove("active");
      item.querySelector(".faq-question").setAttribute("aria-expanded", "false");
    });

    if (!isActive) {
      faqItem.classList.add("active");
      button.setAttribute("aria-expanded", "true");
    }
  });
});



const allThumbs = document.querySelectorAll('.video-thumb');
let currentIframe = null;
let currentThumb = null;

allThumbs.forEach(thumb => {
  const url = thumb.dataset.videoUrl;
  let videoId = '';

  if (url.includes('/shorts/')) videoId = url.split('/shorts/')[1].split('?')[0];
  else if (url.includes('watch?v=')) videoId = url.split('watch?v=')[1].split('&')[0];
  else if (url.includes('youtu.be/')) videoId = url.split('youtu.be/')[1].split('?')[0];

  thumb.dataset.videoId = videoId;

  const img = document.createElement('img');
  img.src = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
  img.alt = 'video';
  img.className = 'img-fluid rounded';
  thumb.insertBefore(img, thumb.querySelector('.play-icon'));

  // Saqlab qo'yish
  thumb.dataset.original = thumb.innerHTML;

  // Video ochish
  thumb.addEventListener('click', (e) => {
    e.stopPropagation(); // boshqa click eventlarga ta’sir qilmasin

    closeCurrentVideo(); // avvalgi video yopiladi

    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    iframe.allowFullscreen = true;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
    iframe.style.borderRadius = '12px';

    thumb.innerHTML = '';
    thumb.appendChild(iframe);

    currentIframe = iframe;
    currentThumb = thumb;
  });
});





// 🟡 Funksiya — avvalgi videoni yopish
function closeCurrentVideo() {
  if (currentIframe && currentThumb) {
    currentThumb.innerHTML = currentThumb.dataset.original;
    currentIframe = null;
    currentThumb = null;
  }
}

// 🟢 Ekrandagi boshqa joyga bosilsa video yopiladi
document.addEventListener('click', (e) => {
  if (currentIframe && !currentThumb.contains(e.target)) {
    closeCurrentVideo();
  }
});

// 🟢 Swiper slide o'zgarsa video yopiladi
if (typeof videoSwiper !== 'undefined') {
  videoSwiper.on('slideChange', () => {
    closeCurrentVideo();
  });
}

   AOS.init({
      duration: 800,
      mirror: false,
    });

    // Sanash funksiyasi
    function animateCounter(el, target, duration) {
      let start = 0;
      let startTime = null;

      function update(currentTime) {
        if (!startTime) startTime = currentTime;
        const progress = currentTime - startTime;
        const rate = Math.min(progress / duration, 1);
        const current = Math.floor(rate * target);
        el.textContent = current;
        if (current < target) {
          requestAnimationFrame(update);
        }
      }

      requestAnimationFrame(update);
    }

    const counters = document.querySelectorAll(".counter");

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute("data-target"));
          animateCounter(el, target, 2000); // 2000ms = 2s

          obs.unobserve(el);
        }
      });
    }, {
      threshold: 0.5
    });

    counters.forEach(counter => {
      observer.observe(counter);
    });




(function(){
  const LEADING = "998";
  const REQUIRED_LEN = 9; 
  const FULL_DIGITS = LEADING.length + REQUIRED_LEN;
  const validOperatorPrefixes = ["33","50","55","77","87","88","90","91","93","94","95","97","98","99"];

  function formatUzPhone(digits) {
    const after = digits.slice(LEADING.length);
    let out = "+998";
    if (after.length === 0) return out;
    out += " (" + after.slice(0, 2);
    if (after.length < 2) return out;
    out += ")";
    if (after.length <= 2) return out;
    out += " " + after.slice(2, 5);
    if (after.length <= 5) return out;
    out += "-" + after.slice(5, 7);
    if (after.length <= 7) return out;
    out += "-" + after.slice(7, 9);
    return out;
  }

  function extractDigits(s) {
    return (s || "").replace(/\D/g, "");
  }

  function validatePhoneField(input, digits) {
    if (digits.length < FULL_DIGITS) {
      input.setCustomValidity("Telefon nomerni to'liq kiriting");
      return;
    }
    if (digits.length > FULL_DIGITS) {
      input.setCustomValidity("Telefon juda uzun");
      return;
    }
    const op = digits.slice(LEADING.length, LEADING.length + 2);
    if (!validOperatorPrefixes.includes(op)) {
      input.setCustomValidity("Telefon operator kodi noto'g'ri");
      return;
    }
    input.setCustomValidity("");
  }

  document.querySelectorAll('input[name="number"]').forEach(input => {
    if (!input.value) input.value = "+998 ";

    // O‘chirishni bloklash (Backspace va Delete uchun)
    input.addEventListener('keydown', function(e){
      const cursorPos = input.selectionStart;
      // +998 dan oldin yoki ichida bo‘lsa o‘chirishni bloklash
      if ((e.key === "Backspace" && cursorPos <= 5) || 
          (e.key === "Delete" && cursorPos < 5)) {
        e.preventDefault();
      }
    });

    // Yozishda
    input.addEventListener('input', function(e){
      let pos = input.selectionStart;
      let ds = extractDigits(input.value);

      if (!ds.startsWith(LEADING)) ds = LEADING + ds.replace(/^0+/, '');
      ds = ds.slice(0, FULL_DIGITS);

      input.value = formatUzPhone(ds);
      validatePhoneField(input, ds);

      if (e.inputType === 'deleteContentBackward' && pos > 0) {
        input.setSelectionRange(pos, pos);
      }
    });

    // Paste
    input.addEventListener('paste', function(e){
      e.preventDefault();
      let ds = extractDigits(e.clipboardData.getData('text'));
      if (!ds.startsWith(LEADING)) ds = LEADING + ds;
      ds = ds.slice(0, FULL_DIGITS);
      input.value = formatUzPhone(ds);
      validatePhoneField(input, ds);
    });

    validatePhoneField(input, extractDigits(input.value));
  });
})();