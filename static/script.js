document.addEventListener("DOMContentLoaded", function () {
    const bookSelect = document.getElementById("bible-book");
    const chapterSelect = document.getElementById("bible-chapter");
    const verseSelect = document.getElementById("bible-verse");

    // Função para atualizar os capítulos ao escolher um livro
    bookSelect.addEventListener("change", function () {
      chapterSelect.innerHTML = "<option selected disabled>Selecione o Capítulo...</option>"; // Limpa os capítulos anteriores
      verseSelect.innerHTML = '<option selected disabled>Selecione o Versículo...</option>'; // Reseta os versículos

      let selectedBook = bookSelect.options[bookSelect.selectedIndex];
      let numChapters = selectedBook.getAttribute("data-chapters");

      for (let i = 1; i <= numChapters; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.textContent = `Capítulo ${i}`;
        chapterSelect.appendChild(option);
      }
    });

    // Função para atualizar os versículos ao escolher um capítulo
    chapterSelect.addEventListener("change", function () {
      verseSelect.innerHTML = '<option selected disabled>Selecione o Versículo...</option>'; // Reseta os versículos

      let selectedBook = bookSelect.value;
      let selectedChapter = chapterSelect.value;
      let url_api = `https://bible-api.com/${selectedBook} ${selectedChapter}`;

      fetch(url_api)
        .then((response) => response.json())
        .then((data) => {
          let numVerses = data.verses.length;

          for (let i = 1; i <= numVerses; i++) {
            let option = document.createElement("option");
            option.value = i;
            option.textContent = `Versículo ${i}`;
            verseSelect.appendChild(option);
          }
        })
        .catch((error) => console.error("Erro ao buscar versículos:", error));
    });
  });