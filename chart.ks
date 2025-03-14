/* === Search Functionality === */
    function debounce(func, delay) {
      let timeoutId;
      return function(...args) {
        if (timeoutId) clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
      };
    }
    
    const performSearchDebounced = debounce(performSearch, 300);
    searchInput.addEventListener('input', performSearchDebounced);
    
    function performSearch() {
      const query = searchInput.value.trim();
      if (!query) {
        searchResultsDiv.style.display = "none";
        searchResultsDiv.innerHTML = "";
        return;
      }
      fetch(`/proxy/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
          searchResultsDiv.innerHTML = "";
          const players = data.filter(item => item.ObjectType === "Player");
          if (!players || players.length === 0) { 
            searchResultsDiv.style.display = "none"; 
            return; 
          }
          players.forEach(item => {
            const div = document.createElement('div');
            let imgHTML = "";
            if (item.LogoImageUrl) {
              imgHTML = `<img src="${item.LogoImageUrl}" alt="${item.ObjectName}">`;
            }
            const locText = item.ObjectLocation ? ` - ${item.ObjectLocation}` : "";
            div.innerHTML = `${imgHTML}<span>${item.ObjectName}${locText}</span>`;
            div.addEventListener('click', () => {
              updateUserWidgets(item.ObjectId, item.ObjectLocation);
              searchResultsDiv.style.display = "none";
              searchResultsDiv.innerHTML = "";
              searchInput.value = "";
            });
            searchResultsDiv.appendChild(div);
          });
          const rect = searchInput.getBoundingClientRect();
          searchResultsDiv.style.top = (rect.bottom + window.scrollY) + "px";
          searchResultsDiv.style.left = (rect.left + window.scrollX) + "px";
          searchResultsDiv.style.width = rect.width + "px";
          searchResultsDiv.style.display = "block";
        })
        .catch(err => console.error('Error during search:', err));
    }