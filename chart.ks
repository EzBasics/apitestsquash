/* === Chart.js and Data Fetching Code === */
    // Ratings History Chart (with reversed data so current dates are at the right)
    let ratingsHistoryChart = null;
    function updateRatingsHistoryChart() {
      fetch('/proxy/user/328331/ratings_history')
        .then(response => response.json())
        .then(data => {
          const labels = data.map(entry => {
            const date = new Date(entry.RankingPeriod);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          }).reverse();
          const ratings = data.map(entry => entry.NewRating).reverse();
          const ctx = document.getElementById('ratingsHistoryChart').getContext('2d');
    
          if (ratingsHistoryChart) { ratingsHistoryChart.destroy(); }
    
          ratingsHistoryChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: labels,
              datasets: [{
                label: 'Rating',
                data: ratings,
                borderColor: '#4facfe',
                backgroundColor: 'rgba(79, 172, 254, 0.3)',
                fill: true,
                tension: 0.3,
                pointRadius: 3,
                pointHoverRadius: 5
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: true,
              scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Rating' } }
              },
              plugins: {
                legend: { display: false },
                tooltip: {
                  backgroundColor: '#fff',
                  titleColor: '#333',
                  bodyColor: '#666',
                  borderColor: '#ddd',
                  borderWidth: 1,
                  padding: 8
                }
              }
            }
          });
        })
        .catch(error => console.error('Error fetching ratings history:', error));
    }
    updateRatingsHistoryChart();
    
    // Doughnut Chart Helpers and Creation Functions
    function updateTotal(chart) {
      const total = chart.data.datasets[0].data.reduce((sum, value) => sum + value, 0);
      const headerElement = document.getElementById(chart.canvas.id + '-header');
      if (headerElement) {
        const titleTotalElement = headerElement.querySelector('.chart-title-total');
        if (titleTotalElement) {
          titleTotalElement.textContent = chart._chartTitle + " - " + total;
        }
      }
    }
    function toggleSegment(chart, index) {
      if (!chart._hidden) { chart._hidden = [] }
      if (chart._hidden[index]) {
        chart.data.datasets[0].data[index] = chart._originalData[index];
        chart._hidden[index] = false;
      } else {
        chart.data.datasets[0].data[index] = 0;
        chart._hidden[index] = true;
      }
      chart.update();
      renderLegend(chart, chart.canvas.id + '-legend');
      updateTotal(chart);
    }
    function renderLegend(chart, containerId) {
      const container = document.getElementById(containerId);
      container.innerHTML = '';
      chart.data.labels.forEach((label, index) => {
        if (chart._originalData[index] <= 0) return;
        const legendItem = document.createElement('div');
        legendItem.style.display = 'inline-block';
        legendItem.style.marginRight = '10px';
        legendItem.style.cursor = 'pointer';
        
        const swatch = document.createElement('span');
        swatch.style.display = 'inline-block';
        swatch.style.width = '8px';
        swatch.style.height = '8px';
        swatch.style.backgroundColor = chart._originalColors[index];
        swatch.style.marginRight = '5px';
        if (chart._hidden && chart._hidden[index]) {
          swatch.style.opacity = '0.3';
        }
        legendItem.appendChild(swatch);
        
        const text = document.createElement('span');
        text.textContent = label + " (" + chart._originalData[index] + ")";
        legendItem.appendChild(text);
        
        legendItem.addEventListener('click', function() {
          toggleSegment(chart, index);
        });
        container.appendChild(legendItem);
      });
    }
    function createStyledDoughnutChart(canvasId, dataValues, titleText, colors) {
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext('2d');
      
      const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['3-game match', '4-game match', '5-game match'],
          datasets: [{
            data: dataValues,
            backgroundColor: colors,
            hoverOffset: 0,
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            title: { display: false },
            tooltip: {
              backgroundColor: '#fff',
              titleColor: '#333',
              bodyColor: '#666',
              borderColor: '#ddd',
              borderWidth: 1,
              padding: 8
            }
          }
        }
      });
      
      chart._originalData = dataValues.slice();
      chart._hidden = [false, false, false];
      chart._originalColors = colors;
      chart._chartTitle = titleText;
      
      renderLegend(chart, canvasId + '-legend');
      updateTotal(chart);
      
      return chart;
    }
    
    // Build Doughnut Charts for Singles and Doubles records
    fetch('/proxy/userRecord')
      .then(response => response.json())
      .then(data => {
        let singlesWins = { 3: 0, 4: 0, 5: 0 };
        let singlesLosses = { 3: 0, 4: 0, 5: 0 };
        let doublesWins = { 3: 0, 4: 0, 5: 0 };
        let doublesLosses = { 3: 0, 4: 0, 5: 0 };
    
        data.forEach(item => {
          if (item.type === 'S') {
            singlesWins[item.matchesType] += item.matchesWon;
            singlesLosses[item.matchesType] += item.matchesLost;
          } else if (item.type === 'D') {
            doublesWins[item.matchesType] += item.matchesWon;
            doublesLosses[item.matchesType] += item.matchesLost;
          }
        });
        
        const fixedColors = ['#4facfe', '#ff4b4b', '#4caf50'];
        
        createStyledDoughnutChart(
          'singlesWinsChart',
          [singlesWins[3], singlesWins[4], singlesWins[5]],
          'Singles Wins',
          fixedColors
        );
        createStyledDoughnutChart(
          'singlesLossesChart',
          [singlesLosses[3], singlesLosses[4], singlesLosses[5]],
          'Singles Losses',
          fixedColors
        );
        createStyledDoughnutChart(
          'doublesWinsChart',
          [doublesWins[3], doublesWins[4], doublesWins[5]],
          'Doubles Wins',
          fixedColors
        );
        createStyledDoughnutChart(
          'doublesLossesChart',
          [doublesLosses[3], doublesLosses[4], doublesLosses[5]],
          'Doubles Losses',
          fixedColors
        );
      })
      .catch(error => console.error('Error fetching user record data:', error));
    
    // Fetch additional profile/ratings info
    fetch('/proxy/user/328331')
      .then(response => response.json())
      .then(data => {
        const profileName = document.querySelector('.profile-name');
        profileName.firstChild.textContent = data.name + " ";
        const subtexts = document.querySelectorAll('.profile-subtext');
        if (data.mainAffiliation) {
          subtexts[0].textContent = data.mainAffiliation.shortName || "Chevy Chase Athletic Club";
          subtexts[1].textContent = data.mainAffiliation.City || "Chevy Chase";
        }
      })
      .catch(error => console.error('Error fetching user profile:', error));
    
    fetch('/proxy/user/328331/ratings-top')
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          document.getElementById('highestRatingValue').textContent =
            parseFloat(data[0].rating).toFixed(2);
          const topDate = new Date(data[0].ratingPeriod);
          const formattedDate = topDate.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
          document.getElementById('highestRatingDateValue').textContent = formattedDate;
        }
      })
      .catch(error => console.error('Error fetching highest rating:', error));
    
    fetch('/proxy/user/328331/ratings')
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          document.getElementById('currentRatingValue').textContent =
            parseFloat(data[0].rating).toFixed(2);
        }
      })
      .catch(error => console.error('Error fetching current rating:', error));
    //////////

    ///////


    ////// 