document.addEventListener('DOMContentLoaded', function () {
  const eventSource = new EventSource('/stream');

  eventSource.onmessage = function (event) {
    if (!event.data.trim()) return; // Ignoriraj prazne linije
    console.log('RAW DATA:', event.data); // Debug u konzoli

    try {
      const jsonData = event.data.replace(/^data: /, ''); // Ukloni 'data: ' na početku
      const data = JSON.parse(jsonData); // Parsiraj JSON

      const polje = data.polje;
      const poruka = data.poruka;
      const strategija = data.strategija;

      document.getElementById('strategija').innerText = strategija;
      document.getElementById('poruka').innerText = poruka;
      const cells = document.querySelectorAll('#tabla td');
      let index = 0;

      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          cells[index].innerText = polje[i][j];
          index++;
        }
      }

      if (poruka.includes('Pobjednik') || poruka.includes('Neriješeno')) {
        eventSource.close(); // Zatvori stream kada igra završi
      }
    } catch (error) {
      console.error(
        'Greška u parsiranju JSON-a:',
        error,
        'Podaci:',
        event.data
      );
    }
  };
});
