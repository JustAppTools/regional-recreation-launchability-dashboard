const statusClass = {
  "Likely usable": "status--likely",
  "Marginal": "status--marginal",
  "Below threshold": "status--below",
};

const statusColor = {
  "Likely usable": "#218368",
  "Marginal": "#d58e35",
  "Below threshold": "#b54842",
};

function formatNumber(value, digits = 1) {
  return Number(value).toLocaleString(undefined, {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function formatRetrievedAt(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en-US", {
    timeZone: "America/Denver",
    month: "long",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
  }).format(date);
}

function statusBadge(status) {
  return `<span class="status ${statusClass[status] || ""}">${status}</span>`;
}

function markerIcon(status) {
  return L.divIcon({
    className: "",
    html: `<div class="marker-dot" style="background:${statusColor[status] || "#607080"}"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
    popupAnchor: [0, -10],
  });
}

function updateSummary(data) {
  const metadata = data.metadata;
  const features = data.features;
  const counts = features.reduce(
    (acc, feature) => {
      acc[feature.properties.status] = (acc[feature.properties.status] || 0) + 1;
      return acc;
    },
    {}
  );
  const retrievedAt = formatRetrievedAt(metadata.retrieved_at);

  document.getElementById("lakeElevation").textContent = `${formatNumber(metadata.current_lake_elevation_ft)} ft`;
  document.getElementById("observedAt").textContent = `Observed: ${metadata.observed_at}`;
  document.getElementById("lastUpdated").textContent = `Dashboard data retrieved: ${retrievedAt}`;
  document.getElementById("metadataObserved").textContent = metadata.observed_at;
  document.getElementById("metadataRetrieved").textContent = retrievedAt;
  document.getElementById("metadataSource").textContent = metadata.lake_elevation_source;
  document.getElementById("likelyCount").textContent = counts["Likely usable"] || 0;
  document.getElementById("marginalCount").textContent = counts.Marginal || 0;
  document.getElementById("belowCount").textContent = counts["Below threshold"] || 0;
}

function buildTable(features) {
  const tbody = document.getElementById("launchRows");
  tbody.innerHTML = "";
  features.forEach((feature) => {
    const props = feature.properties;
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${props.launch_name}</td>
      <td>${formatNumber(props.minimum_launch_elevation_ft)}</td>
      <td>${formatNumber(props.margin_ft)}</td>
      <td>${statusBadge(props.status)}</td>
    `;
    tbody.appendChild(row);
  });
}

function buildMap(features) {
  const map = L.map("map", {
    scrollWheelZoom: false,
  }).setView([48.25, -118.45], 8);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  const layer = L.geoJSON(features, {
    pointToLayer: (feature, latlng) => L.marker(latlng, { icon: markerIcon(feature.properties.status) }),
    onEachFeature: (feature, marker) => {
      const props = feature.properties;
      marker.bindPopup(`
        <strong>${props.launch_name}</strong><br>
        ${statusBadge(props.status)}<br>
        Lake elevation: ${formatNumber(props.current_lake_elevation_ft)} ft<br>
        Minimum: ${formatNumber(props.minimum_launch_elevation_ft)} ft<br>
        Margin: ${formatNumber(props.margin_ft)} ft
      `);
    },
  }).addTo(map);

  map.fitBounds(layer.getBounds(), { padding: [28, 28] });
}

function renderDashboard(data) {
  updateSummary(data);
  buildTable(data.features);
  buildMap(data.features);
}

if (window.LAUNCH_STATUS_DATA) {
  renderDashboard(window.LAUNCH_STATUS_DATA);
} else {
  fetch("data/launch_status.geojson")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Unable to load launch status: ${response.status}`);
      }
      return response.json();
    })
    .then(renderDashboard)
    .catch((error) => {
      document.getElementById("launchRows").innerHTML = `<tr><td colspan="4">${error.message}</td></tr>`;
    });
}
