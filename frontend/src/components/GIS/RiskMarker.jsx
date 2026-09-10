
import { Marker } from "react-leaflet";
import L from "leaflet";

function getRiskColor(riskLevel) {
  switch (String(riskLevel || "").toUpperCase()) {
    case "CRITICAL":
      return "#ef4444";

    case "HIGH":
      return "#f97316";

    case "MODERATE":
      return "#facc15";

    case "LOW":
      return "#22c55e";

    default:
      return "#64748b";
  }
}

function RiskMarker({ location, onSelect }) {
  const latitude = Number(location.latitude);
  const longitude = Number(location.longitude);
  const locationId = Number(location.location_id);

  if (
    !Number.isFinite(latitude) ||
    !Number.isFinite(longitude)
  ) {
    return null;
  }

  const color = getRiskColor(location.risk_level);

  const icon = L.divIcon({
    className: "custom-risk-marker",

    html: `
      <div
        style="
          width: 36px;
          height: 36px;
          background: ${color};
          border: 3px solid #ffffff;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #ffffff;
          font-family: Arial, sans-serif;
          font-size: 13px;
          font-weight: 700;
          box-shadow:
            0 2px 6px rgba(0, 0, 0, 0.45),
            0 0 0 1px rgba(0, 0, 0, 0.15);
          box-sizing: border-box;
        "
      >
        ${locationId}
      </div>
    `,

    iconSize: [36, 36],
    iconAnchor: [18, 18],
  });

  return (
    <Marker
      position={[latitude, longitude]}
      icon={icon}
      eventHandlers={{
        click: () => {
          if (onSelect) {
            onSelect(location);
          }
        },
      }}
    />
  );
}

export default RiskMarker;
