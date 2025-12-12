console.log('Script loaded');

document.addEventListener("DOMContentLoaded", () => {

    // === UTILS ===
    const $ = selector => document.querySelector(selector);
    const $$ = selector => Array.from(document.querySelectorAll(selector));

    // === FONCTION POUR INITIALISER LES CHARTS DANS LES CARDS ===
    const initChartsInCards = () => {
        const palette = [
            'rgb(255,99,132)', 'rgb(54,162,235)', 'rgb(255,205,86)',
            'rgb(75,192,192)', 'rgb(153,102,255)', 'rgb(255,159,64)',
            'rgb(201,203,207)', 'rgb(100,149,237)', 'rgb(255,69,0)', 'rgb(0,128,0)'
        ];

        $$('canvas[id^="chart_"]').forEach(canvas => {
            const card = canvas.closest('.metadata-table');
            if (!card) return;

            // Récupérer les données JSON dans un attribut data-values (doit être ajouté côté serveur)
            const valuesAttr = card.dataset.values;
            if (!valuesAttr) {
                console.warn(`Pas de data-values pour la carte ${card.id}`);
                return;
            }
            let values;
            try {
                values = JSON.parse(valuesAttr);
            } catch (e) {
                console.error(`Erreur parsing JSON data-values pour ${card.id}`, e);
                return;
            }

            const labels = Object.keys(values);
            const data = Object.values(values);

            const colors = labels.map((_, i) => palette[i % palette.length]);

            // Créer le chart
            new Chart(canvas.getContext('2d'), {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: false,
                    plugins: {
                        legend: { display: true, position: 'bottom', labels: {boxWidth: 12}},
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.label}: ${ctx.raw}`
                            }
                        }
                    }
                }
            });
        });
    };

    initChartsInCards();

    // === GESTION FILTRES PAR CHECKBOX ===
    const setupCheckboxFilter = name => {
        $$(`input[name="${name}"]`).forEach(cb => {
            cb.addEventListener('change', () => {
                const params = new URLSearchParams(window.location.search);
                const selected = $$(`input[name="${name}"]:checked`).map(cb => cb.value);
                params.delete(name);
                selected.forEach(val => params.append(name, val));
                window.location.search = params.toString();
            });
        });
    };
    setupCheckboxFilter('bi_processes');
    setupCheckboxFilter('wet_processes');

    // === VARIABLES MODAL & CHART ===
    const modal = $('#chartModal');
    const closeBtn = $('#closeModalBtn');
    const ctx = $('#occurrencesChart')?.getContext('2d');
    const legendContainer = $('#chartLegend');
    const toggleChartTypeBtn = $('#toggleChartTypeBtn');

    let chartInstance = null;
    let currentChartType = 'doughnut';
    let lastChartData = null;
    let lastChartTitle = null;

    const renderLegend = (labels, data, colors) => {
        legendContainer.innerHTML = '';
        labels.forEach((label, i) => {
            const legendItem = document.createElement('div');
            legendItem.style = "display: flex; align-items: center; margin-bottom: 6px; gap: 8px;";
            legendItem.innerHTML = `
                <span style="display: inline-block; width: 18px; height: 18px; background-color: ${colors[i]}; border-radius: 3px;"></span>
                <span>${label} (${data[i]})</span>
            `;
            legendContainer.appendChild(legendItem);
        });
    };

    const showChart = (labels, data, colors, title) => {
        if (chartInstance) chartInstance.destroy();
        chartInstance = new Chart(ctx, {
            type: currentChartType,
            data: {
                labels,
                datasets: [{
                    label: title,
                    data,
                    backgroundColor: colors,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: false,
                plugins: {legend: {display: false}, title: {display: false}}
            }
        });
        renderLegend(labels, data, colors);
    };

    const showChartWithData = (metadataCounts, title) => {
        document.body.classList.add('modal-open');
        modal.style.display = 'flex';
        lastChartData = metadataCounts;
        lastChartTitle = title;

        if (toggleChartTypeBtn) {
            toggleChartTypeBtn.textContent = currentChartType === 'doughnut' ? 'Diagramme en bâtons' : 'Camembert';
        }

        const labels = [], data = [], colors = [];
        const palette = [
            'rgb(255,99,132)', 'rgb(54,162,235)', 'rgb(255,205,86)',
            'rgb(75,192,192)', 'rgb(153,102,255)', 'rgb(255,159,64)',
            'rgb(201,203,207)', 'rgb(100,149,237)', 'rgb(255,69,0)', 'rgb(0,128,0)'
        ];

        let i = 0;
        for (const [field, values] of Object.entries(metadataCounts)) {
            const label = field.split('.').pop().replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            for (const [val, count] of Object.entries(values)) {
                labels.push(`${label} → ${val}`);
                data.push(count);
                colors.push(palette[i++ % palette.length]);
            }
        }
        showChart(labels, data, colors, title);
    };

    const showChartWithCustomData = (chartData, title) => {
        document.body.classList.add('modal-open');
        modal.style.display = 'flex';
        lastChartData = chartData;
        lastChartTitle = title;

        const {labels, data} = chartData;
        const colors = labels.map((_, i) => `hsl(${(i * 360 / labels.length)}, 70%, 60%)`);

        if (toggleChartTypeBtn) {
            toggleChartTypeBtn.textContent = currentChartType === 'doughnut' ? 'Diagramme en bâtons' : 'Camembert';
        }

        showChart(labels, data, colors, title);
    };

    // === BOUTONS CHART ===
    document.body.addEventListener('click', e => {
        if (e.target.id === 'showOccurrencesWetBtn') {
            showChartWithData(metadataCountsWet, 'Occurrences des métadonnées wet-process');
        } else if (e.target.id === 'showOccurrencesBiBtn') {
            showChartWithData(metadataCountsBi, 'Occurrences des métadonnées bi-process');
        } else if (e.target.classList.contains('show-occurrences-btn')) {
            const label = e.target.dataset.label;
            const values = JSON.parse(e.target.dataset.values);
            showChartWithCustomData({
                labels: Object.keys(values),
                data: Object.values(values)
            }, `Occurrences pour ${label}`);
        }
    });

    toggleChartTypeBtn?.addEventListener('click', () => {
        if (!lastChartData || !lastChartTitle) return;
        currentChartType = currentChartType === 'doughnut' ? 'bar' : 'doughnut';
        toggleChartTypeBtn.textContent = currentChartType === 'doughnut' ? 'Diagramme en bâtons' : 'Camembert';
        lastChartData.labels
            ? showChartWithCustomData(lastChartData, lastChartTitle)
            : showChartWithData(lastChartData, lastChartTitle);
    });

    const closeModal = () => {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    };
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', e => {
        if (e.target === modal) closeModal();
    });
    document.addEventListener('keydown', e => {
        if (modal.style.display === 'flex' && e.key === 'Escape') closeModal();
    });

    // === TOGGLES VISIBILITÉ TABLES ===
    const toggles = $$('.meta-toggle');
    const allFiltersButton = $('#toggle-all-filters');
    const sectionButtons = [
        {button: $('#toggle-wet'), prefix: 'table_wet_', label: 'Index Wet-Processes'},
        {button: $('#toggle-bi'), prefix: 'table_bi_', label: 'Index Bi-Processes'}
    ];
    const allTables = {};
    $$('.metadata-table, .metadata-list').forEach(el => allTables[el.id] = el);

    const updateTablesVisibility = () => {
        toggles.forEach(t => {
            const el = allTables[t.dataset.target];
            if (el) el.style.display = t.checked ? '' : 'none';
        });
        updateAllFiltersButton();
        updateSectionButtons();
    };

    const updateAllFiltersButton = () => {
        const allChecked = toggles.every(t => t.checked);
        allFiltersButton.textContent = allChecked ? 'Tout masquer' : 'Tout afficher';
    };

    const updateSectionButtons = () => {
        sectionButtons.forEach(({button, prefix, label}) => {
            const related = toggles.filter(t => t.dataset.target.startsWith(prefix));
            const allChecked = related.every(t => t.checked);
            button.textContent = allChecked ? `Masquer ${label}` : `Afficher ${label}`;
        });
    };

    allFiltersButton.addEventListener('click', () => {
        const allChecked = toggles.every(t => t.checked);
        toggles.forEach(t => t.checked = !allChecked);
        updateTablesVisibility();
    });

    sectionButtons.forEach(({button, prefix}) => {
        button.addEventListener('click', () => {
            const related = toggles.filter(t => t.dataset.target.startsWith(prefix));
            const allChecked = related.every(t => t.checked);
            related.forEach(t => t.checked = !allChecked);
            updateTablesVisibility();
        });
    });

    toggles.forEach(t => t.addEventListener('change', updateTablesVisibility));
    updateTablesVisibility();

    // === SWITCH VUE TABLE/LISTE ===
    const viewTableBtn = $('#viewTableBtn');
    const viewListBtn = $('#viewListBtn');
    const tableView = $('#tableView');
    const listView = $('#listView');

    const switchView = isTable => {
        tableView.style.display = isTable ? '' : 'none';
        listView.style.display = isTable ? 'none' : '';
        viewTableBtn.classList.toggle('active', isTable);
        viewListBtn.classList.toggle('active', !isTable);
    };

    viewTableBtn?.addEventListener('click', () => switchView(true));
    viewListBtn?.addEventListener('click', () => switchView(false));

    // === ACCORDÉONS ===
    $$('.expand-all-btn').forEach(btn =>
        btn.addEventListener('click', () =>
            $$(`#accordion_${btn.dataset.target} .accordion-collapse`).forEach(el =>
                bootstrap.Collapse.getOrCreateInstance(el).show()
            )
        )
    );
    $$('.collapse-all-btn').forEach(btn =>
        btn.addEventListener('click', () =>
            $$(`#accordion_${btn.dataset.target} .accordion-collapse`).forEach(el =>
                bootstrap.Collapse.getOrCreateInstance(el).hide()
            )
        )
    );
    $$('.toggle-all-btn').forEach(btn =>
        btn.addEventListener('click', () =>
            $$(`#accordion_${btn.dataset.target} .accordion-collapse`).forEach(el => {
                const inst = bootstrap.Collapse.getOrCreateInstance(el);
                el.classList.contains('show') ? inst.hide() : inst.show();
            })
        )
    );

    // === TRI DES TABLEAUX PAR OCCURRENCE ===
    $$('.sort-btn').forEach(button => {
        let asc = true;
        button.addEventListener('click', () => {
            const tbody = button.closest('.card')?.querySelector('tbody');
            if (!tbody) return;

            const rows = Array.from(tbody.querySelectorAll('tr'));
            rows.sort((a, b) => {
                const aVal = parseInt(a.cells[1].textContent) || 0;
                const bVal = parseInt(b.cells[1].textContent) || 0;
                return asc ? aVal - bVal : bVal - aVal;
            });

            rows.forEach(row => tbody.appendChild(row));
            asc = !asc;
            button.textContent = asc ? 'Tri croissant' : 'Tri décroissant';
        });
    });
    const allCanvases = document.querySelectorAll('canvas[id^="chart_"]');
  allCanvases.forEach(canvas => {
    const ctx = canvas.getContext('2d');
    const label = canvas.dataset.label || '';
    const labels = JSON.parse(canvas.dataset.labels || '[]');
    const values = JSON.parse(canvas.dataset.values || '[]');
    if (labels.length && values.length) {
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: label,
            data: values,
            backgroundColor: labels.map((_, i) => `hsl(${Math.floor(i * 360 / labels.length)}, 70%, 60%)`)
          }]
        },
        options: {
          plugins: {
            legend: { display: true, position: 'bottom', labels: { boxWidth: 12 }},
            tooltip: {
              callbacks: {
                label: ctx => `${ctx.label}: ${ctx.raw}`
              }
            }
          }
        }
      });
    }
  });
  const selectedSet = new Set();
  const selectedContainer = document.getElementById('selectedMetadata');
  const cartCountBadge = document.getElementById('cartCount');

  function updateCartUI() {
    selectedContainer.innerHTML = '';
    if(selectedSet.size === 0) {
      selectedContainer.innerHTML = '<p class="text-muted fst-italic text-center">Aucune sélection</p>';
    }
    selectedSet.forEach(item => {
      const [field, value] = item.split('||');
      const cleanName = field.replace('metadata.', '').replace(/_/g, ' ').replace(/\./g, ' ');
      const displayText = `${cleanName.trim().replace(/\b\w/g, c => c.toUpperCase())}: ${value}`;

      const badge = document.createElement('div');
      badge.className = 'badge bg-primary d-flex justify-content-between align-items-center rounded-pill px-3 py-2';
      badge.style.cursor = 'default';
      badge.textContent = displayText;

      const btnClose = document.createElement('button');
      btnClose.type = 'button';
      btnClose.className = 'btn-close btn-close-white btn-sm ms-3';
      btnClose.setAttribute('aria-label', `Retirer ${displayText}`);
      btnClose.style.filter = 'drop-shadow(0 0 1px rgba(0,0,0,0.3))';
      btnClose.addEventListener('click', () => {
        selectedSet.delete(item);
        updateCartUI();
        updateCheckboxes();
      });

      badge.appendChild(btnClose);
      selectedContainer.appendChild(badge);
    });

    cartCountBadge.textContent = selectedSet.size;
    updateCheckboxes();
  }

  function updateCheckboxes() {
    document.querySelectorAll('.metadata-checkbox').forEach(checkbox => {
      const field = checkbox.dataset.field;
      const value = checkbox.dataset.value;
      const key = `${field}||${value}`;
      checkbox.checked = selectedSet.has(key);
    });
  }

  document.querySelectorAll('.metadata-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      const field = checkbox.dataset.field;
      const value = checkbox.dataset.value;
      const key = `${field}||${value}`;
      if (checkbox.checked) {
        selectedSet.add(key);
      } else {
        selectedSet.delete(key);
      }
      updateCartUI();
    });
  });

  document.getElementById('validateBtn').addEventListener('click', () => {
    console.log('Sélection validée:', Array.from(selectedSet));
    // TODO : envoyer la sélection au serveur ou agir en conséquence
  });

  document.getElementById('clearCartBtn').addEventListener('click', () => {
    selectedSet.clear();
    updateCartUI();
  });

  const toggleAllBtn = document.getElementById('toggleAllBtn');
  const accordionItems = document.querySelectorAll('.accordion-collapse');

  toggleAllBtn.addEventListener('click', () => {
    const allExpanded = Array.from(accordionItems).every(item => item.classList.contains('show'));

    if (allExpanded) {
      accordionItems.forEach(item => {
        const bsCollapse = bootstrap.Collapse.getInstance(item);
        if (bsCollapse) {
          bsCollapse.hide();
        } else {
          new bootstrap.Collapse(item, {toggle: false}).hide();
        }
      });
      toggleAllBtn.textContent = 'Tout dérouler';
    } else {
      accordionItems.forEach(item => {
        const bsCollapse = bootstrap.Collapse.getInstance(item);
        if (bsCollapse) {
          bsCollapse.show();
        } else {
          new bootstrap.Collapse(item, {toggle: false}).show();
        }
      });
      toggleAllBtn.textContent = 'Tout replier';
    }
  });

  // 👇 Afficher / masquer le panier au clic sur le bouton flottant
  document.getElementById('toggleCartBtn').addEventListener('click', () => {
    const cart = document.getElementById('floatingCart');
    cart.style.display = (cart.style.display === 'none') ? 'block' : 'none';
  });

  updateCartUI();

});
