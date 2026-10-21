// Gloria Victis, wersja B: menu, kropki rozdziałów, oś procesu, ściana kadry, tor realizacji, katalog, formularz (demo)
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const osoby = window.SPECJALISCI || [];
  const norm = t => t.toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '');
  const esc = t => String(t).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const zl = n => n.toLocaleString('pl-PL').replace(/\s/g, ' ') + ' zł';

  // menu na cały ekran
  const menu = $('#menu');
  const menuBtn = $('.menu-btn');
  const ustawMenu = otwarte => {
    menu.hidden = !otwarte;
    menuBtn.setAttribute('aria-expanded', otwarte);
    menuBtn.textContent = otwarte ? 'Zamknij' : 'Menu';
    document.body.style.overflow = otwarte ? 'hidden' : '';
  };
  menuBtn.addEventListener('click', () => ustawMenu(menu.hidden));
  $$('a', menu).forEach(a => a.addEventListener('click', () => ustawMenu(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) ustawMenu(false); });

  // kropki: zaznacz rozdział, który zajmuje środek ekranu
  const kropki = $$('.kropki a');
  const obserwator = new IntersectionObserver(wpisy => {
    wpisy.filter(w => w.isIntersecting).forEach(w => {
      kropki.forEach(k => k.setAttribute('aria-current', k.dataset.cel === w.target.id));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  kropki.forEach(k => { const s = document.getElementById(k.dataset.cel); if (s) obserwator.observe(s); });

  // oś czasu procesu
  const KROKI = [
    ['Rozmowa u ciebie', '1 dzień', 'Nasz doradca przyjeżdża, ogląda halę i biuro, pyta o procesy, które zjadają najwięcej czasu, i o budżet na wkład własny.'],
    ['Burza mózgów', '1 tydzień', 'Siadamy w 6-10 osób: doradca, ekonomista i naukowcy z dziedzin pasujących do twojej branży. Wychodzi z tego lista pomysłów z szacunkiem kosztów.'],
    ['Koncepcja w PDF', '2-3 tygodnie', 'Dostajesz 2-3 warianty innowacji z wizualizacjami, kosztorysem, pokazem prototypu i oceną szans w konkretnych naborach.'],
    ['Zespół i harmonogram', '1 tydzień', 'Pokazujemy, kto z imienia i nazwiska zrobi projekt i kiedy ma wolne okna. Nie obiecujemy ludzi, których nie mamy.'],
    ['Wniosek', '4-8 tygodni', 'Piszemy wniosek, biznesplan i część badawczą. Odpowiadamy na uwagi oceniających i poprawiamy, aż przejdzie.'],
    ['Realizacja', '12-36 miesięcy', 'Jako generalny wykonawca budujemy technologię: oprogramowanie, automatykę, modele AI, prototypy i linie pilotażowe.'],
    ['Rozliczenie i trwałość', 'do 5 lat', 'Wnioski o płatność, kontrole, raporty z okresu trwałości. Zostajemy z tobą, dopóki instytucja nie zamknie projektu.'],
  ];
  const os = $('#os');
  os.innerHTML = '<div class="os-pasek" id="os-pasek"></div>' + KROKI.map((k, i) =>
    `<button role="tab" id="krok-${i}" aria-controls="etap" aria-selected="false" tabindex="-1" data-i="${i}"><b>${i + 1}</b><span>${esc(k[0])}</span></button>`).join('');
  let aktywny = 0;
  function pokazKrok(i, fokus) {
    aktywny = Math.max(0, Math.min(KROKI.length - 1, i));
    $$('button', os).forEach((b, j) => {
      b.setAttribute('aria-selected', j === aktywny);
      b.tabIndex = j === aktywny ? 0 : -1;
      b.classList.toggle('za', j < aktywny);
    });
    $('#os-pasek').style.width = `calc((100% - 100% / 7) * ${aktywny / (KROKI.length - 1)})`;
    const [t, czas, opis] = KROKI[aktywny];
    $('#etap').innerHTML = `<div class="etap-nr">${aktywny + 1}</div><h3>${esc(t)}</h3><p class="etap-czas">${czas}</p><p>${esc(opis)}</p>`;
    $('#etap').setAttribute('aria-labelledby', `krok-${aktywny}`);
    $('#etap-wstecz').disabled = aktywny === 0;
    $('#etap-dalej').disabled = aktywny === KROKI.length - 1;
    if (fokus) $(`#krok-${aktywny}`).focus();
  }
  os.addEventListener('click', e => { const b = e.target.closest('button'); if (b) pokazKrok(Number(b.dataset.i)); });
  os.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') pokazKrok(aktywny + 1, true);
    if (e.key === 'ArrowLeft') pokazKrok(aktywny - 1, true);
  });
  $('#etap-wstecz').addEventListener('click', () => pokazKrok(aktywny - 1));
  $('#etap-dalej').addEventListener('click', () => pokazKrok(aktywny + 1));
  pokazKrok(0);

  // dziedziny od najliczniejszej
  const liczby = {};
  osoby.forEach(o => { liczby[o.dziedzina] = (liczby[o.dziedzina] || 0) + 1; });
  const dziedziny = Object.keys(liczby).sort((a, b) => liczby[b] - liczby[a]);

  // kadra: ściana zdjęć i dziedziny prowadzące do katalogu
  $('#sciana').innerHTML = osoby.map(o => `<img src="../assets/img/ludzie/${o.foto}.jpg" alt="" loading="lazy">`).join('');
  $('#kadra-dziedziny').innerHTML = dziedziny.map(d => `<button data-d="${esc(d)}">${esc(d)}<span>${liczby[d]}</span></button>`).join('');
  $('#kadra-dziedziny').addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    ustawDziedzine(b.dataset.d);
    $('.katalog').scrollIntoView();
  });

  // realizacje: tor kart
  const PROJEKTY = [
    ['Producent konstrukcji stalowych, 210 osób, Śląskie', 'FENG, Ścieżka SMART', 7840000, 'Zrobotyzowana linia spawania z kamerową kontrolą spoin', 'Rozliczony'],
    ['Zakład mięsny, 460 osób, Wielkopolskie', 'FENG, Ścieżka SMART', 12400000, 'System wizyjny do klasyfikacji elementów i odzysk ciepła z chłodni', 'W realizacji'],
    ['Spółka medyczna, 12 osób, Mazowieckie', 'EIC Accelerator', 10800000, 'Przenośny analizator krwi z oprogramowaniem diagnostycznym', 'W realizacji'],
    ['Producent farb przemysłowych, 85 osób, Małopolskie', 'FENG, Ścieżka SMART', 3260000, 'Powłoka antykorozyjna bez rozpuszczalników i linia pilotażowa', 'W realizacji'],
    ['Producent okien, 230 osób, Opolskie', 'FENG, Ścieżka SMART', 5600000, 'Linia z robotami współpracującymi i kontrolą jakości szyb', 'Wniosek w ocenie'],
    ['Odlewnia aluminium, 95 osób, Dolnośląskie', 'KPO', 4100000, 'Druk 3D form piaskowych i zbieranie danych z pieców', 'Rozliczony'],
    ['Przetwórnia owoców, 60 osób, Lubelskie', 'KPO', 3900000, 'Sortownia z wizją maszynową i chłodnia zasilana z fotowoltaiki', 'Wniosek w ocenie'],
    ['Producent mebli, 140 osób, Podkarpackie', 'Program regionalny 2021-2027', 2150000, 'Cyfrowy model hali i planowanie produkcji', 'Rozliczony'],
    ['Firma logistyczna, 340 osób, Łódzkie', 'KPO', 1980000, 'Automatyczny obieg faktur i planowanie tras z AI', 'Rozliczony'],
    ['Biuro rachunkowe, 40 osób, Śląskie', 'FESL 1.8, Innowacje cyfrowe w MŚP', 640000, 'Asystent AI do dokumentów księgowych', 'Rozliczony'],
  ];
  const tor = $('#tor');
  tor.innerHTML = PROJEKTY.map(([klient, program, kwota, co, status]) => `<article class="karta">
      <div class="kwota">${zl(kwota)}</div>
      <div class="program">${esc(program)}</div>
      <p class="klient">${esc(klient)}</p>
      <p class="co">${esc(co)}</p>
      <span class="status" data-s="${esc(status)}">${esc(status)}</span>
    </article>`).join('');
  const krokToru = () => ($('.karta', tor)?.getBoundingClientRect().width || 380) + 16;
  $('#real-wstecz').addEventListener('click', () => tor.scrollBy({ left: -krokToru(), behavior: 'smooth' }));
  $('#real-dalej').addEventListener('click', () => tor.scrollBy({ left: krokToru(), behavior: 'smooth' }));

  // katalog
  const NA_STRONE = 8;
  const stan = { dziedzina: '', stopien: '', szukaj: '', ile: NA_STRONE };
  const chipy = $('#k-dziedziny');
  chipy.innerHTML = [`<button class="filtr" data-d="" aria-pressed="true">Wszyscy<span>${osoby.length}</span></button>`]
    .concat(dziedziny.map(d => `<button class="filtr" data-d="${esc(d)}" aria-pressed="false">${esc(d)}<span>${liczby[d]}</span></button>`)).join('');
  chipy.addEventListener('click', e => { const b = e.target.closest('button'); if (b) ustawDziedzine(b.dataset.d); });
  function ustawDziedzine(d) {
    stan.dziedzina = d;
    stan.ile = NA_STRONE;
    $$('button', chipy).forEach(b => b.setAttribute('aria-pressed', b.dataset.d === d));
    rysujKatalog();
  }
  $('#k-stopien').addEventListener('change', e => { stan.stopien = e.target.value; stan.ile = NA_STRONE; rysujKatalog(); });
  $('#k-szukaj').addEventListener('input', e => { stan.szukaj = norm(e.target.value.trim()); stan.ile = NA_STRONE; rysujKatalog(); });
  $('#k-wiecej').addEventListener('click', () => { stan.ile += NA_STRONE; rysujKatalog(); });
  const KOLEJNOSC = { prof: 0, drhab: 1, dr: 2, mgr: 3 };
  function rysujKatalog() {
    const lista = osoby.filter(o =>
      (!stan.dziedzina || o.dziedzina === stan.dziedzina) &&
      (!stan.stopien || o.stopien === stan.stopien) &&
      (!stan.szukaj || norm([o.imie, o.tytul, o.dziedzina, o.miasto, ...o.spec].join(' ')).includes(stan.szukaj))
    ).sort((a, b) => KOLEJNOSC[a.stopien] - KOLEJNOSC[b.stopien] || a.id - b.id);
    const widoczne = lista.slice(0, stan.ile);
    $('#k-osoby').innerHTML = widoczne.length ? widoczne.map(o => `<article class="osoba">
        <img src="../assets/img/ludzie/${o.foto}.jpg" alt="" loading="lazy" width="128" height="128">
        <div>
          <span class="t">${esc(o.tytul)}, ${esc(o.miasto)}</span>
          <h4>${esc(o.imie)}</h4>
          <span class="dz">${esc(o.dziedzina)}</span>
          <p class="spec">${esc(o.spec.join(', '))}</p>
          <span class="dost" data-d="${o.dost}">${esc(o.kiedy)}</span>
          <button class="zapytaj" data-id="${o.id}">Zapytaj o tę osobę</button>
        </div>
      </article>`).join('')
      : '<div class="pusto">Nikt nie pasuje do tych filtrów. Zmień dziedzinę albo tytuł, albo napisz do nas, a dobierzemy kogoś spoza katalogu.</div>';
    $('#k-licznik').textContent = lista.length ? `Pokazuję ${widoczne.length} z ${lista.length} ${lista.length === 1 ? 'osoby' : 'osób'}` : '';
    const wiecej = $('#k-wiecej');
    wiecej.hidden = widoczne.length >= lista.length;
    wiecej.textContent = `Pokaż kolejne ${Math.min(NA_STRONE, lista.length - widoczne.length)}`;
  }
  $('#k-osoby').addEventListener('click', e => {
    const b = e.target.closest('.zapytaj');
    if (!b) return;
    const o = osoby.find(x => x.id === Number(b.dataset.id));
    wybierzDroge('projekt', `Chcemy porozmawiać o projekcie z udziałem: ${o.tytul} ${o.imie} (${o.dziedzina}).`);
    $('#zglos').scrollIntoView();
  });
  rysujKatalog();

  // formularz: najpierw wybór drogi, potem pola dla tej drogi
  const form = $('#formularz');
  const DROGI = {
    pomysl: ['Mam budżet, szukam pomysłu', 'Co w firmie zjada najwięcej czasu albo pieniędzy', 'Umów rozmowę z doradcą'],
    projekt: ['Mam projekt do zrobienia', 'Opisz projekt: co ma powstać i do kiedy', 'Wyślij opis projektu'],
    specjalista: ['Jestem specjalistą', 'Czym się zajmujesz i przy jakich projektach chcesz pracować', 'Dołącz do katalogu'],
  };
  $('#f-dziedzina').innerHTML = dziedziny.map(d => `<option>${esc(d)}</option>`).join('') + '<option>Inna</option>';
  function wybierzDroge(s, opis) {
    $$('.droga').forEach(b => b.setAttribute('aria-pressed', b.dataset.sciezka === s));
    $$('[data-dla]', form).forEach(el => {
      const tak = el.dataset.dla.split(' ').includes(s);
      el.hidden = !tak;
      $$('input, select, textarea', el).forEach(p => { p.disabled = !tak; });
    });
    $('#f-wybrana').textContent = DROGI[s][0];
    $('#f-opis-l').textContent = DROGI[s][1];
    $('#f-wyslij').textContent = DROGI[s][2];
    if (opis) $('#f-opis').value = opis;
    form.hidden = false;
    $('#f-dzieki').hidden = true;
  }
  $$('.droga').forEach(b => b.addEventListener('click', () => {
    wybierzDroge(b.dataset.sciezka);
    $('input:not([disabled]), select:not([disabled])', form).focus();
  }));
  $('#f-zmien').addEventListener('click', () => {
    form.hidden = true;
    $$('.droga').forEach(b => b.setAttribute('aria-pressed', 'false'));
    $('.droga').focus();
  });
  form.addEventListener('submit', e => {
    e.preventDefault();
    const blad = $('#f-blad');
    const zle = $$('input, select, textarea', form).filter(p => !p.disabled && !p.checkValidity());
    if (zle.length) {
      blad.textContent = 'Uzupełnij: ' + zle.map(p => p.type === 'checkbox' ? 'zgoda na kontakt' : p.closest('label').querySelector('span').textContent.toLowerCase()).join(', ') + '.';
      blad.hidden = false;
      zle[0].focus();
      return;
    }
    blad.hidden = true;
    form.hidden = true;
    $('#f-dzieki').hidden = false;
    $('#f-dzieki').focus();
  });
  $('#f-nowe').addEventListener('click', () => {
    form.reset();
    $('#f-dzieki').hidden = true;
    $$('.droga').forEach(b => b.setAttribute('aria-pressed', 'false'));
    $('.droga').focus();
  });
})();
