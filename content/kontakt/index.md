# Kontakt

<!-- opis: Kontaktni podatki in obrazec za povpraševanje. -->

Pokličite nas, pišite na WhatsApp ali e-pošto, ali izpolnite obrazec spodaj. Odgovorimo v enem delovnem dnevu.

<div class="contact-buttons">
  <a class="btn" href="tel:{{ site.phone }}">Pokliči {{ site.phone_display }}</a>
  <a class="btn btn-whatsapp" href="https://wa.me/{{ site.whatsapp }}?text=Pozdravljeni%2C%20zanima%20me%20va%C5%A1a%20storitev." rel="noopener">WhatsApp</a>
  <a class="btn btn-ghost" href="mailto:{{ site.email }}">{{ site.email }}</a>
  <a class="btn btn-ghost" href="https://instagram.com/{{ site.instagram }}" rel="noopener">Instagram</a>
</div>

**Naslov:** {{ site.address }}

## Obrazec za povpraševanje

<form id="povprasevanje" class="contact-form" action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="{{ site.web3forms_key }}">
  <input type="hidden" name="subject" value="Novo povpraševanje s strani {{ site.name }}">
  <input type="checkbox" name="botcheck" class="hidden" tabindex="-1" autocomplete="off">
  <label>Ime in priimek *<input type="text" name="ime" autocomplete="name" required></label>
  <label>Telefon *<input type="tel" name="telefon" autocomplete="tel" inputmode="tel" required></label>
  <label>E-pošta<input type="email" name="email" autocomplete="email"></label>
  <label>Storitev<select name="storitev"><option value="">Izberite ...</option><option>Storitev ena</option><option>Storitev dve</option><option>Storitev tri</option><option>Drugo</option></select></label>
  <label>Sporočilo *<textarea name="sporocilo" rows="5" required></textarea></label>
  <label class="consent"><input type="checkbox" name="soglasje" required> Strinjam se z obdelavo podatkov za odgovor na povpraševanje.</label>
  <button class="btn" type="submit">Pošlji povpraševanje</button>
  <p class="form-note">Podatke uporabimo samo za odgovor. Več v <a href="/zasebnost">politiki zasebnosti</a>.</p>
</form>
