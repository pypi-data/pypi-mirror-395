  // توابع منو
  function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    sidebar.classList.toggle('active');
    mainContent.classList.toggle('menu-active');
}

// حالت شب/روز
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const btn = document.getElementById('darkModeBtn');
    
    if (document.body.classList.contains('dark-mode')) {
        btn.textContent = 'حالت روز';
        localStorage.setItem('darkMode', 'enabled');
    } else {
        btn.textContent = 'حالت شب';
        localStorage.setItem('darkMode', 'disabled');
    }
}

// بررسی حالت شب
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    document.getElementById('darkModeBtn').textContent = 'حالت روز';
}

// شمارنده کاراکترها
document.getElementById('inputText').addEventListener('input', function() {
    const count = this.value.length;
    document.getElementById('charCount').textContent = count;
    
    if (count > 500) {
        this.style.borderColor = '#ff4444';
    } else {
        this.style.borderColor = '';
    }
});

// کپی متن با افکت
function copyText() {
    const text = document.getElementById('outputText').textContent;
    if (!text) return;
    
    navigator.clipboard.writeText(text).then(() => {
        // نمایش اسنک بار
        const snackbar = document.getElementById('snackbar');
        snackbar.classList.add('show');
        
        // نمایش افکت روی دکمه کپی
        const copyBtn = document.querySelector('.copy-btn');
        copyBtn.classList.add('copied');
        
        setTimeout(() => {
            snackbar.classList.remove('show');
            copyBtn.classList.remove('copied');
        }, 2000);
    });
}

// تابع تبدیل متن
function convertText() {
    const text = document.getElementById('inputText').value;
    const language = document.getElementById('languageSelect').value;
    
    if (!text.trim()) {
        alert('لطفاً متن را وارد کنید');
        return;
    }
    
    const btn = document.getElementById('convertBtn');
    btn.disabled = true;
    btn.innerHTML = 'در حال تبدیل...';
    
    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text, language: language })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('outputText').textContent = data.result;
        btn.disabled = false;
        btn.innerHTML = 'تبدیل متن';
    })
    .catch(error => {
        console.error('Error:', error);
        btn.disabled = false;
        btn.innerHTML = 'تبدیل متن';
        alert('خطا در تبدیل متن');
    });
}