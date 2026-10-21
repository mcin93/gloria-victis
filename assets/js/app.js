// Gloria Victis: menu, katalog specjalistów, tabela realizacji, formularz (demo)
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const osoby = window.SPECJALISCI || [];
  const NA_STRONE = 12;

  // bez polskich znaków i wielkości liter, żeby „lodz” znalazło „Łódź”
  const norm = t => t.toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '');
  const esc = t => String(t).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // menu na telefonie
  const menuBtn = $('.menu-btn');
  const menu = $('#menu');
  menuBtn.addEventListener('click', () => {
    const otwarte = menu.classList.toggle('otwarte');
    menuBtn.setAttribute('aria-expanded', otwarte);
  });
  $$('a', menu).forEach(a => a.addEventListener('click', () => {
    menu.classList.remove('otwarte');
    menuBtn.setAttribute('aria-expanded', 'false');
  }));

  // dziedziny posortowane od najliczniejszej
  const liczby = {};
  osoby.forEach(o => { liczby[o.dziedzina] = (liczby[o.dziedzina] || 0) + 1; });
  const dziedziny = Object.keys(liczby).sort((a, b) => liczby[b] - liczby[a]);

  // katalog
  const stan = { dziedzina: '', stopien: '', dost: '', szukaj: '', ile: NA_STRONE };
  const chipy = $('#k-dziedziny');
  chipy.innerHTML = [`<button class="filtr" data-d="" aria-pressed="true">Wszyscy<span>${osoby.length}</span></button>`]
    .concat(dziedziny.map(d => `<button class="filtr" data-d="${esc(d)}" aria-pressed="false">${esc(d)}<span>${liczby[d]}</span></button>`))
    .join('');
  chipy.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    ustawDziedzine(b.dataset.d);
  });

  function ustawDziedzine(d) {
    stan.dziedzina = d;
    stan.ile = NA_STRONE;
    $$('button', chipy).forEach(b => b.setAttribute('aria-pressed', b.dataset.d === d));
    rysujKatalog();
  }

  $('#k-stopien').addEventListener('change', e => { stan.stopien = e.target.value; stan.ile = NA_STRONE; rysujKatalog(); });
  $('#k-dost').addEventListener('change', e => { stan.dost = e.target.value; stan.ile = NA_STRONE; rysujKatalog(); });
  $('#k-szukaj').addEventListener('input', e => { stan.szukaj = norm(e.target.value.trim()); stan.ile = NA_STRONE; rysujKatalog(); });
  $('#k-wiecej').addEventListener('click', () => { stan.ile += NA_STRONE; rysujKatalog(); });

  const KOLEJNOSC = { prof: 0, drhab: 1, dr: 2, mgr: 3 };

  function pasujace() {
    return osoby.filter(o =>
      (!stan.dziedzina || o.dziedzina === stan.dziedzina) &&
      (!stan.stopien || o.stopien === stan.stopien) &&
      (!stan.dost || o.dost === stan.dost || (stan.dost === '3m' && o.dost === 'teraz')) &&
      (!stan.szukaj || norm([o.imie, o.tytul, o.dziedzina, o.miasto, ...o.spec].join(' ')).includes(stan.szukaj))
    ).sort((a, b) => KOLEJNOSC[a.stopien] - KOLEJNOSC[b.stopien] || a.id - b.id);
  }

  function karta(o) {
    return `<article class="osoba">
      <img src="assets/img/ludzie/${o.foto}.jpg" alt="" loading="lazy" width="88" height="88">
      <div>
        <div class="tytul">${esc(o.tytul)}, ${esc(o.miasto)}</div>
        <h3>${esc(o.imie)}</h3>
        <div class="dz">${esc(o.dziedzina)}</div>
        <p class="spec">${esc(o.spec.join(', '))}</p>
        <p class="osi">${esc(o.osiagniecia.join(', '))}</p>
      </div>
      <div class="dol">
        <span class="dost" data-d="${o.dost}">${esc(o.kiedy)}</span>
        <button class="zapytaj" data-id="${o.id}">Zapytaj o tę osobę</button>
      </div>
    </article>`;
  }

  function rysujKatalog() {
    const lista = pasujace();
    const widoczne = lista.slice(0, stan.ile);
    $('#k-osoby').innerHTML = widoczne.length
      ? widoczne.map(karta).join('')
      : `<div class="pusto">Nikt nie pasuje do tych filtrów. Zmień dziedzinę albo dostępność, albo napisz do nas, a dobierzemy kogoś spoza katalogu.<br><button class="btn btn-2" id="k-reset">Wyczyść filtry</button></div>`;
    $('#k-licznik').textContent = lista.length
      ? `Pokazuję ${widoczne.length} z ${lista.length} ${lista.length === 1 ? 'osoby' : 'osób'}`
      : '';
    const wiecej = $('#k-wiecej');
    wiecej.hidden = widoczne.length >= lista.length;
    wiecej.textContent = `Pokaż kolejne ${Math.min(NA_STRONE, lista.length - widoczne.length)}`;
    const reset = $('#k-reset');
    if (reset) reset.addEventListener('click', () => {
      stan.stopien = stan.dost = stan.szukaj = '';
      $('#k-stopien').value = $('#k-dost').value = $('#k-szukaj').value = '';
      ustawDziedzine('');
    });
  }

  $('#k-osoby').addEventListener('click', e => {
    const b = e.target.closest('.zapytaj');
    if (!b) return;
    const o = osoby.find(x => x.id === Number(b.dataset.id));
    otworzFormularz('projekt', `Chcemy porozmawiać o projekcie z udziałem: ${o.tytul} ${o.imie} (${o.dziedzina}).`);
  });

  // lista dziedzin w sekcji kadry przenosi do przefiltrowanego katalogu
  $('#dziedziny').innerHTML = dziedziny
    .map(d => `<li><button data-d="${esc(d)}">${esc(d)}<span>${liczby[d]}</span></button></li>`).join('');
  $('#dziedziny').addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    ustawDziedzine(b.dataset.d);
    $('#katalog').scrollIntoView();
  });

  rysujKatalog();

  // realizacje: filtr statusu, sortowanie po kwocie, suma
  const tbody = $('#real-tabela tbody');
  const zl = n => n.toLocaleString('pl-PL').replace(/\s/g, ' ') + ' zł';
  $$('tr', tbody).forEach(tr => {
    tr.dataset.status = $('.status', tr).textContent;
    $('td.kwota', tr).textContent = zl(Number(tr.dataset.kwota));
  });

  function suma() {
    const widoczne = $$('tr', tbody).filter(tr => !tr.hidden);
    const s = widoczne.reduce((acc, tr) => acc + Number(tr.dataset.kwota), 0);
    $('#real-suma').innerHTML = `${widoczne.length} ${widoczne.length < 5 && widoczne.length > 1 ? 'projekty' : 'projektów'} w tabeli, razem <b>${zl(s)}</b> dofinansowania.`;
  }
  $('#real-filtry').addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    $$('button', e.currentTarget).forEach(x => x.setAttribute('aria-pressed', x === b));
    $$('tr', tbody).forEach(tr => { tr.hidden = !!b.dataset.status && tr.dataset.status !== b.dataset.status; });
    suma();
  });
  $('.sortuj').addEventListener('click', e => {
    const btn = e.currentTarget;
    const kier = btn.dataset.kier === 'malejaco' ? 'rosnaco' : 'malejaco';
    btn.dataset.kier = kier;
    $$('tr', tbody)
      .sort((a, b) => (kier === 'malejaco' ? -1 : 1) * (a.dataset.kwota - b.dataset.kwota))
      .forEach(tr => tbody.appendChild(tr));
  });
  suma();

  // formularz: trzy ścieżki, wersja demo
  const form = $('#formularz');
  const TEKSTY = {
    pomysl: { opis: 'Co w firmie zjada najwięcej czasu albo pieniędzy', przycisk: 'Umów rozmowę z doradcą' },
    projekt: { opis: 'Opisz projekt: co ma powstać i do kiedy', przycisk: 'Wyślij opis projektu' },
    specjalista: { opis: 'Czym się zajmujesz i przy jakich projektach chcesz pracować', przycisk: 'Dołącz do katalogu' },
  };
  $('#f-dziedzina').innerHTML = dziedziny.map(d => `<option>${esc(d)}</option>`).join('') + '<option>Inna</option>';

  function ustawSciezke(s) {
    $$('input[name="sciezka"]', form).forEach(r => { r.checked = r.value === s; });
    $$('[data-dla]', form).forEach(el => {
      const widoczne = el.dataset.dla.split(' ').includes(s);
      el.hidden = !widoczne;
      $$('input, select, textarea', el).forEach(p => { p.disabled = !widoczne; });
    });
    $('#f-opis-l').textContent = TEKSTY[s].opis;
    $('#f-wyslij').textContent = TEKSTY[s].przycisk;
  }
  $$('input[name="sciezka"]', form).forEach(r => r.addEventListener('change', () => ustawSciezke(r.value)));

  function otworzFormularz(s, opis) {
    ustawSciezke(s);
    if (opis) $('#f-opis').value = opis;
    $('#zglos').scrollIntoView();
  }
  $$('[data-sciezka]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    otworzFormularz(a.dataset.sciezka);
  }));

  form.addEventListener('submit', e => {
    e.preventDefault();
    const blad = $('#f-blad');
    const zle = $$('input, select, textarea', form).filter(p => !p.disabled && !p.checkValidity());
    if (zle.length) {
      const nazwy = zle.map(p => p.type === 'checkbox' ? 'zgoda na kontakt' : (p.closest('label').querySelector('span')?.textContent || p.name).toLowerCase());
      blad.textContent = `Uzupełnij: ${nazwy.join(', ')}.`;
      blad.hidden = false;
      zle[0].focus();
      return;
    }
    blad.hidden = true;
    $$('.sciezki, fieldset, .zgoda, #f-wyslij', form).forEach(el => { el.hidden = true; });
    const dzieki = $('#f-dzieki');
    dzieki.hidden = false;
    dzieki.focus();
  });
  $('#f-nowe').addEventListener('click', () => {
    form.reset();
    $$('.sciezki, fieldset, .zgoda, #f-wyslij', form).forEach(el => { el.hidden = false; });
    $('#f-dzieki').hidden = true;
    ustawSciezke('pomysl');
  });
  ustawSciezke('pomysl');
})();
