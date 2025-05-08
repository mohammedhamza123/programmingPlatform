


document.getElementById('loginForm').onsubmit = async function(e) {
    e.preventDefault();
    const phone_number = this.phone_number.value;
    const password_hash = this.password_hash.value;
    const errorMsg = document.getElementById('errorMsg');
    errorMsg.textContent = "";
    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ phone_number, password_hash })
        });
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem("access_token", data.access_token);
            window.location.href = '/home';
            
        } else {
            const err = await res.json();
            errorMsg.textContent = err.detail || 'بيانات غير صحيحة';
        }
    } catch (err) {
        errorMsg.textContent = 'حدث خطأ أثناء الاتصال بالخادم';
    }
}
