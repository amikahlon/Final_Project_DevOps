const input = document.getElementById('numberInput');
const checkBtn = document.getElementById('checkBtn');
const clearBtn = document.getElementById('clearBtn');
const message = document.getElementById('message');

checkBtn.addEventListener('click', async () => {
    const raw = input.value.trim();

    if (raw === '') {
        showMsg('Please enter a number', 'error');
        return;
    }

    const n = Number(raw);
    if (!Number.isFinite(n) || !Number.isInteger(n)) {
        showMsg('Please enter an integer (no decimals)', 'error');
        return;
    }

    try {
        const res = await fetch(`/api/odd-even/${n}`);
        const data = await res.json();

        if (!data.ok) {
            showMsg(data.error || 'Something went wrong', 'error');
            return;
        }

        const label = data.type === 'even' ? 'Even' : 'Odd';
        showMsg(`Result: ${label}`, data.type);
    } catch {
        showMsg('Server is not reachable', 'error');
    }
});

clearBtn.addEventListener('click', () => {
    input.value = '';
    message.textContent = '';
    message.className = '';
    input.focus();
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') checkBtn.click();
});

function showMsg(text, kind) {
    message.textContent = text;
    message.className = kind;
}
