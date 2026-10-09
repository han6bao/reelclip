// Contact form -> email via Resend (https://resend.com).
// Set in Vercel > Project > Settings > Environment Variables:
//   RESEND_API_KEY  (required)  your Resend API key
//   CONTACT_TO      (optional)  where inquiries go, default thereelclip@gmail.com
//   CONTACT_FROM    (optional)  sender, default "Reelclip <hello@reel-clip.com>" (reel-clip.com must be verified in Resend)
const esc = (s) => String(s || '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

module.exports = async (req, res) => {
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ ok: false, error: 'Method not allowed' }); }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};
  if (body.website) return res.status(200).json({ ok: true }); // honeypot: bots fill the hidden field

  const name = String(body.name || '').trim().slice(0, 200);
  const email = String(body.email || '').trim().slice(0, 200);
  const brand = String(body.brand || '').trim().slice(0, 200);
  const service = String(body.service || '').trim().slice(0, 100);
  const budget = String(body.budget || '').trim().slice(0, 100);
  const message = String(body.message || '').trim().slice(0, 5000);
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return res.status(400).json({ ok: false, error: 'Name and a valid email are required' });

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ ok: false, error: 'Email is not configured' });

  const rows = [['Name', name], ['Email', email], ['Brand / artist', brand], ['Needs', service], ['Budget', budget]];
  const html = '<h2 style="font-family:sans-serif">New Reelclip inquiry</h2><table style="font-family:sans-serif;font-size:14px">' +
    rows.map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0;color:#666">${k}</td><td><b>${esc(v) || '—'}</b></td></tr>`).join('') +
    `</table><p style="font-family:sans-serif;font-size:14px;white-space:pre-wrap">${esc(message) || '(no message)'}</p>`;
  const text = rows.map(([k, v]) => `${k}: ${v || '-'}`).join('\n') + '\n\n' + (message || '(no message)');

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.CONTACT_FROM || 'Reelclip <hello@reel-clip.com>',
        to: [process.env.CONTACT_TO || 'thereelclip@gmail.com'],
        reply_to: email,
        subject: `New inquiry: ${name}${brand ? ' / ' + brand : ''}`,
        html, text,
      }),
    });
    if (!r.ok) { console.error('Resend error', r.status, await r.text()); return res.status(502).json({ ok: false, error: 'Could not send' }); }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error(e); return res.status(502).json({ ok: false, error: 'Could not send' });
  }
};
