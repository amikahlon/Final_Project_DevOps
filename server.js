const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/odd-even/:n', (req, res) => {
    const n = Number(req.params.n);

    if (!Number.isFinite(n) || !Number.isInteger(n)) {
        return res.status(400).json({ ok: false, error: 'Please provide an integer number' });
    }
    const type = n % 2 === 0 ? 'even' : 'odd';
    res.json({ ok: true, number: n, type });
});

app.get('/api/health', (_req, res) => res.json({ ok: true }));

app.listen(PORT, () => {
    console.log(`Odd-or-Even running on http://localhost:${PORT}`);
});
