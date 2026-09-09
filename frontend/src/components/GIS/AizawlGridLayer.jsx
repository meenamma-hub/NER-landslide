import { Rectangle, Popup } from "react-leaflet";

const aizawlGrids = [
  ["IMERG_r1136_c2725", 23.65, 92.55],
  ["IMERG_r1136_c2726", 23.65, 92.65],
  ["IMERG_r1136_c2727", 23.65, 92.75],

  ["IMERG_r1137_c2725", 23.75, 92.55],
  ["IMERG_r1137_c2726", 23.75, 92.65],
  ["IMERG_r1137_c2727", 23.75, 92.75],

  ["IMERG_r1138_c2725", 23.85, 92.55],
  ["IMERG_r1138_c2726", 23.85, 92.65],
  ["IMERG_r1138_c2727", 23.85, 92.75],

  ["IMERG_r1139_c2725", 23.95, 92.55],
  ["IMERG_r1139_c2726", 23.95, 92.65],
  ["IMERG_r1139_c2727", 23.95, 92.75],

  ["IMERG_r1140_c2725", 24.05, 92.55],
  ["IMERG_r1140_c2726", 24.05, 92.65],
  ["IMERG_r1140_c2727", 24.05, 92.75],
];


// =====================================================
// ML RISK LEVEL → GIS COLOR
// =====================================================

function getRiskColor(riskLevel) {
  switch (String(riskLevel || "").toUpperCase()) {
    case "LOW":
      return "#22c55e";

    case "MODERATE":
      return "#facc15";

    case "HIGH":
      return "#f97316";

    case "CRITICAL":
      return "#ef4444";

    default:
      return "#64748b";
  }
}


// =====================================================
// AIZAWL GRID LAYER
// =====================================================

function AizawlGridLayer({ risk }) {
  const hasRisk = Boolean(risk);

  const riskLevel = risk?.risk_level;
  const riskScore = risk?.risk_score;

  const color = getRiskColor(riskLevel);

  return (
    <>
      {aizawlGrids.map(([cellId, lat, lng]) => {
        const bounds = [
          [lat - 0.05, lng - 0.05],
          [lat + 0.05, lng + 0.05],
        ];

        return (
          <Rectangle
            key={cellId}
            bounds={bounds}
            pathOptions={{
              color: hasRisk ? color : "#64748b",
              fillColor: hasRisk ? color : "#64748b",
              fillOpacity: hasRisk ? 0.4 : 0.15,
              weight: 1.5,
            }}
          >
            <Popup>
              <strong>{cellId}</strong>

              <br />
              Aizawl IMERG Grid

              <br />
              Center: {lat}, {lng}

              {hasRisk && (
                <>
                  <br />
                  Risk Score: {riskScore}%

                  <br />
                  Risk Level: {riskLevel}

                  <br />
                  Priority: {risk.priority}

                  <br />
                  Action: {risk.recommended_action}
                </>
              )}
            </Popup>
          </Rectangle>
        );
      })}
    </>
  );
}

export default AizawlGridLayer;