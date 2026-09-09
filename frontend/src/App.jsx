import { useEffect, useState } from "react";

const API_URL = "http://localhost:8000";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [showReportForm, setShowReportForm] = useState(false);

  const [reportType, setReportType] = useState("Visible Crack");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("Zone A");
  const [latitude, setLatitude] = useState(0);
  const [longitude, setLongitude] = useState(0);
  const [image, setImage] = useState(null);

  const [locationLoading, setLocationLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  // --------------------------------------------------
  // GET ACTIVE ALERTS
  // --------------------------------------------------
  const fetchAlerts = async () => {
    try {
      const response = await fetch(`${API_URL}/alerts/`);

      if (!response.ok) {
        throw new Error("Failed to fetch alerts");
      }

      const data = await response.json();

      // Show only active alerts
      const activeAlerts = data.filter(
        (alert) => alert.status === "ACTIVE"
      );

      setAlerts(activeAlerts);
    } catch (error) {
      console.error("Alert error:", error);
      setAlerts([]);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  // --------------------------------------------------
  // GET USER LOCATION
  // --------------------------------------------------
  const getLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by this browser.");
      return;
    }

    setLocationLoading(true);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(position.coords.latitude);
        setLongitude(position.coords.longitude);

        setLocation("Current Location");

        setLocationLoading(false);
      },
      (error) => {
        console.error("Location error:", error);
        alert("Unable to get your location. Please allow location access.");

        setLocationLoading(false);
      }
    );
  };

  // --------------------------------------------------
  // SUBMIT CITIZEN REPORT
  // --------------------------------------------------
  const submitReport = async (event) => {
    event.preventDefault();

    if (!description.trim()) {
      alert("Please enter a description.");
      return;
    }

    setSubmitting(true);

    try {
      const formData = new FormData();

      // These names MUST match the FastAPI backend
      formData.append("location", location);
      formData.append("description", description);
      formData.append("latitude", latitude);
      formData.append("longitude", longitude);
      formData.append("report_type", reportType);

      // Only send image if user selected one
      if (image) {
        formData.append("image", image);
      }

      console.log("Submitting report...");
      console.log({
        location,
        description,
        latitude,
        longitude,
        reportType,
        image,
      });

      const response = await fetch(`${API_URL}/reports/`, {
        method: "POST",
        body: formData,
      });

      // Get response even when server returns an error
      const responseText = await response.text();

      console.log("Backend response:", response.status, responseText);

      if (!response.ok) {
        throw new Error(
          `Server returned ${response.status}: ${responseText}`
        );
      }

      const result = JSON.parse(responseText);

      console.log("Report successfully submitted:", result);

      setSubmitted(true);

      // Clear form
      setDescription("");
      setImage(null);
      setReportType("Visible Crack");
      setLocation("Zone A");
      setLatitude(0);
      setLongitude(0);
    } catch (error) {
      console.error("Report submission error:", error);

      alert(
        `Unable to submit report.\n\n${error.message}`
      );
    } finally {
      setSubmitting(false);
    }
  };

  // --------------------------------------------------
  // RESET REPORT FORM
  // --------------------------------------------------
  const closeReportForm = () => {
    setShowReportForm(false);
    setSubmitted(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f4f7fb",
        fontFamily: "Arial, sans-serif",
        color: "#172033",
      }}
    >
      {/* HEADER */}
      <header
        style={{
          background: "#0b1f3a",
          color: "white",
          padding: "24px 7%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "15px",
        }}
      >
        <div>
          <h1
            style={{
              margin: 0,
              fontSize: "28px",
            }}
          >
            NER Landslide Risk Monitoring
          </h1>

          <p
            style={{
              margin: "8px 0 0",
              color: "#b9c7dc",
            }}
          >
            Early Warning • Citizen Reporting • Emergency Response
          </p>
        </div>

        <div
          style={{
            background: "#d9fbe5",
            color: "#087a35",
            padding: "9px 15px",
            borderRadius: "20px",
            fontWeight: "bold",
            fontSize: "14px",
          }}
        >
          ● SYSTEM ONLINE
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main
        style={{
          width: "86%",
          maxWidth: "1200px",
          margin: "35px auto",
        }}
      >
        {/* ALERT SECTION */}
        <section
          style={{
            background: "white",
            borderRadius: "16px",
            padding: "25px",
            marginBottom: "25px",
            boxShadow: "0 5px 20px rgba(0,0,0,0.06)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "10px",
            }}
          >
            <div>
              <h2 style={{ margin: 0 }}>Emergency Alerts</h2>

              <p style={{ color: "#687386" }}>
                Live alerts received from the disaster monitoring system
              </p>
            </div>

            <button
              onClick={fetchAlerts}
              style={{
                padding: "10px 16px",
                border: "none",
                borderRadius: "8px",
                background: "#e8eef7",
                cursor: "pointer",
                fontWeight: "bold",
              }}
            >
              Refresh
            </button>
          </div>

          {alerts.length === 0 ? (
            <div
              style={{
                padding: "20px",
                background: "#f5f7fa",
                borderRadius: "10px",
                color: "#657184",
              }}
            >
              No active emergency alerts.
            </div>
          ) : (
            <div
              style={{
                display: "grid",
                gap: "15px",
              }}
            >
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  style={{
                    border: "2px solid #e53935",
                    borderRadius: "12px",
                    padding: "20px",
                    background: "#fff7f7",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      gap: "10px",
                      flexWrap: "wrap",
                    }}
                  >
                    <h3
                      style={{
                        margin: 0,
                        color: "#c62828",
                      }}
                    >
                      🚨 {alert.title}
                    </h3>

                    <span
                      style={{
                        background: "#c62828",
                        color: "white",
                        padding: "5px 10px",
                        borderRadius: "15px",
                        fontWeight: "bold",
                        fontSize: "12px",
                      }}
                    >
                      {alert.priority}
                    </span>
                  </div>

                  <p>
                    <strong>Location:</strong>{" "}
                    {alert.location_id === 1
                      ? "Zone A"
                      : `Location ${alert.location_id}`}
                  </p>

                  <p>
                    <strong>Risk Level:</strong>{" "}
                    {alert.risk_level}
                  </p>

                  <p>{alert.message}</p>

                  <p
                    style={{
                      marginBottom: 0,
                      fontWeight: "bold",
                      color: "#b71c1c",
                    }}
                  >
                    Recommended Action: Deploy field team immediately.
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* CITIZEN REPORTING */}
        <section
          style={{
            background: "white",
            borderRadius: "16px",
            padding: "25px",
            marginBottom: "25px",
            boxShadow: "0 5px 20px rgba(0,0,0,0.06)",
          }}
        >
          <h2>Citizen Incident Reporting</h2>

          <p style={{ color: "#687386" }}>
            Report road blockages, cracks, slope movement or heavy rainfall.
          </p>

          {!showReportForm && (
            <button
              onClick={() => {
                setShowReportForm(true);
                setSubmitted(false);
              }}
              style={{
                background: "#0b1f3a",
                color: "white",
                border: "none",
                padding: "13px 22px",
                borderRadius: "8px",
                fontWeight: "bold",
                cursor: "pointer",
              }}
            >
              REPORT INCIDENT
            </button>
          )}

          {showReportForm && !submitted && (
            <form
              onSubmit={submitReport}
              style={{
                marginTop: "20px",
                display: "grid",
                gap: "15px",
                maxWidth: "650px",
              }}
            >
              {/* REPORT TYPE */}
              <div>
                <label>
                  <strong>Incident Type</strong>
                </label>

                <select
                  value={reportType}
                  onChange={(e) => setReportType(e.target.value)}
                  style={{
                    width: "100%",
                    padding: "12px",
                    marginTop: "6px",
                    borderRadius: "8px",
                    border: "1px solid #ccd3df",
                  }}
                >
                  <option>Road Blockage</option>
                  <option>Visible Crack</option>
                  <option>Slope Movement</option>
                  <option>Heavy Rainfall</option>
                  <option>Other</option>
                </select>
              </div>

              {/* LOCATION */}
              <div>
                <label>
                  <strong>Location</strong>
                </label>

                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  placeholder="Enter location"
                  style={{
                    width: "100%",
                    padding: "12px",
                    marginTop: "6px",
                    borderRadius: "8px",
                    border: "1px solid #ccd3df",
                    boxSizing: "border-box",
                  }}
                />
              </div>

              {/* DESCRIPTION */}
              <div>
                <label>
                  <strong>Description</strong>
                </label>

                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe what you observed..."
                  rows="5"
                  style={{
                    width: "100%",
                    padding: "12px",
                    marginTop: "6px",
                    borderRadius: "8px",
                    border: "1px solid #ccd3df",
                    resize: "vertical",
                    boxSizing: "border-box",
                  }}
                />
              </div>

              {/* LOCATION BUTTON */}
              <button
                type="button"
                onClick={getLocation}
                disabled={locationLoading}
                style={{
                  padding: "12px",
                  borderRadius: "8px",
                  border: "1px solid #0b1f3a",
                  background: "white",
                  color: "#0b1f3a",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                {locationLoading
                  ? "Getting Location..."
                  : "📍 Get My Location"}
              </button>

              {/* COORDINATES */}
              <div
                style={{
                  background: "#f4f7fb",
                  padding: "12px",
                  borderRadius: "8px",
                  fontSize: "14px",
                }}
              >
                <strong>Coordinates:</strong>

                <br />

                Latitude: {latitude}

                <br />

                Longitude: {longitude}
              </div>

              {/* IMAGE */}
              <div>
                <label>
                  <strong>Upload Image</strong>
                </label>

                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) =>
                    setImage(e.target.files?.[0] || null)
                  }
                  style={{
                    display: "block",
                    marginTop: "8px",
                  }}
                />

                {image && (
                  <p
                    style={{
                      fontSize: "14px",
                      color: "#536174",
                    }}
                  >
                    Selected: {image.name}
                  </p>
                )}
              </div>

              {/* BUTTONS */}
              <div
                style={{
                  display: "flex",
                  gap: "10px",
                  flexWrap: "wrap",
                }}
              >
                <button
                  type="submit"
                  disabled={submitting}
                  style={{
                    background: "#0b1f3a",
                    color: "white",
                    border: "none",
                    padding: "13px 22px",
                    borderRadius: "8px",
                    fontWeight: "bold",
                    cursor: "pointer",
                  }}
                >
                  {submitting
                    ? "Submitting..."
                    : "Submit Report"}
                </button>

                <button
                  type="button"
                  onClick={closeReportForm}
                  style={{
                    background: "#e8eef7",
                    color: "#172033",
                    border: "none",
                    padding: "13px 22px",
                    borderRadius: "8px",
                    fontWeight: "bold",
                    cursor: "pointer",
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          {/* SUCCESS */}
          {submitted && (
            <div
              style={{
                marginTop: "20px",
                background: "#e9f9ef",
                border: "1px solid #8bd5a5",
                padding: "20px",
                borderRadius: "10px",
              }}
            >
              <h3
                style={{
                  color: "#087a35",
                  marginTop: 0,
                }}
              >
                ✅ Report Submitted Successfully
              </h3>

              <p>
                Your incident report has been sent to the
                disaster monitoring system.
              </p>

              <button
                onClick={closeReportForm}
                style={{
                  background: "#087a35",
                  color: "white",
                  border: "none",
                  padding: "10px 18px",
                  borderRadius: "7px",
                  cursor: "pointer",
                  fontWeight: "bold",
                }}
              >
                Done
              </button>
            </div>
          )}
        </section>

        {/* HOW SYSTEM WORKS */}
        <section
          style={{
            background: "white",
            borderRadius: "16px",
            padding: "25px",
            boxShadow: "0 5px 20px rgba(0,0,0,0.06)",
          }}
        >
          <h2>How the System Works</h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(180px, 1fr))",
              gap: "15px",
              marginTop: "20px",
            }}
          >
            {[
              [
                "01",
                "Detect",
                "Environmental and ground-level data are collected.",
              ],
              [
                "02",
                "Predict",
                "ML generates a dynamic landslide risk level.",
              ],
              [
                "03",
                "Assess Impact",
                "Population, villages and infrastructure are evaluated.",
              ],
              [
                "04",
                "Prioritize",
                "Emergency incidents receive response priorities.",
              ],
              [
                "05",
                "Alert",
                "Authorities and citizens receive actionable warnings.",
              ],
            ].map(([number, title, text]) => (
              <div
                key={number}
                style={{
                  padding: "18px",
                  background: "#f4f7fb",
                  borderRadius: "10px",
                }}
              >
                <div
                  style={{
                    fontSize: "24px",
                    fontWeight: "bold",
                    color: "#2d6cdf",
                  }}
                >
                  {number}
                </div>

                <h3>{title}</h3>

                <p
                  style={{
                    color: "#687386",
                    fontSize: "14px",
                    lineHeight: "1.5",
                  }}
                >
                  {text}
                </p>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer
        style={{
          marginTop: "40px",
          padding: "25px",
          textAlign: "center",
          background: "#0b1f3a",
          color: "#b9c7dc",
          fontSize: "14px",
        }}
      >
        NER Landslide Risk Monitoring System • SIH Prototype
      </footer>
    </div>
  );
}

export default App;