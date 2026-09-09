
import { useEffect, useState } from "react";

import {
  AlertTriangle,
  CheckCircle2,
  MapPin,
  Route,
} from "lucide-react";

import { getRiskOverview } from "../../services/riskService";


function BlockedRoads() {
  const [roads, setRoads] = useState([]);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    const loadRoadRisk = async () => {
      try {
        setLoading(true);

        const data = await getRiskOverview();

        const riskData = Array.isArray(data) ? data : [];

        // Use locations with connectivity impact.
        const affectedLocations = riskData
          .filter(
            (item) =>
              Number(item.connectivity_factor || 0) > 0
          )
          .sort(
            (a, b) =>
              Number(b.connectivity_factor || 0) -
              Number(a.connectivity_factor || 0)
          )
          .slice(0, 5);


        const roadData = affectedLocations.map((item, index) => {
          const riskLevel = String(
            item.risk_level || ""
          ).toUpperCase();

          const connectivity = Number(
            item.connectivity_factor || 0
          );


          let severity = "Moderate";
          let status = "Restricted";


          if (riskLevel === "CRITICAL") {
            severity = "Critical";
            status = "Blocked";
          } else if (riskLevel === "HIGH") {
            severity = "High";
            status = "Blocked";
          } else if (riskLevel === "MODERATE") {
            severity = "Moderate";
            status = "Restricted";
          } else {
            severity = "Low";
            status = "Open";
          }


          let reason = "Landslide risk";

          if (riskLevel === "CRITICAL") {
            reason = "Critical landslide risk";
          } else if (riskLevel === "HIGH") {
            reason = "High landslide risk";
          } else if (riskLevel === "MODERATE") {
            reason = "Moderate landslide risk";
          }


          return {
            id: item.location_id || index,
            road: `${item.district || item.location} Road`,
            location: `${item.location}, ${item.state}`,
            reason,
            severity,
            status,
            connectivity,
          };
        });


        setRoads(roadData);

        console.log("BLOCKED ROADS DATA:", roadData);

      } catch (error) {
        console.error(
          "FAILED TO LOAD BLOCKED ROAD DATA:",
          error
        );
      } finally {
        setLoading(false);
      }
    };


    loadRoadRisk();
  }, []);


  const getSeverityClass = (severity) => {
    if (severity === "Critical") {
      return "bg-red-500/10 text-red-400";
    }

    if (severity === "High") {
      return "bg-orange-500/10 text-orange-400";
    }

    if (severity === "Moderate") {
      return "bg-yellow-500/10 text-yellow-400";
    }

    return "bg-green-500/10 text-green-400";
  };


  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500/10 text-orange-400">
            <Route size={21} />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white sm:text-lg">
              Blocked Roads
            </h2>

            <p className="text-xs text-slate-500">
              Connectivity affected by current risk conditions
            </p>
          </div>

        </div>


        <span className="rounded-full bg-orange-500/10 px-2.5 py-1 text-xs font-semibold text-orange-400">
          {roads.length} Roads
        </span>

      </div>


      {/* Loading */}
      {loading && (
        <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-5 text-center text-xs text-slate-500">
          Loading road risk data...
        </div>
      )}


      {/* No affected roads */}
      {!loading && roads.length === 0 && (
        <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-5 text-center text-xs text-slate-500">
          No connectivity-affected locations available.
        </div>
      )}


      {/* Road List */}
      {!loading && roads.length > 0 && (
        <div className="space-y-3">

          {roads.map((road) => (

            <div
              key={road.id}
              className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-3"
            >

              <div className="flex items-start justify-between gap-3">

                {/* Road information */}
                <div className="min-w-0">

                  <div className="flex items-center gap-2">

                    <span className="text-sm font-semibold text-white">
                      {road.road}
                    </span>

                    <span
                      className={`rounded-full px-2 py-0.5 text-[10px] font-semibold ${getSeverityClass(
                        road.severity
                      )}`}
                    >
                      {road.severity}
                    </span>

                  </div>


                  <div className="mt-2 flex items-center gap-1.5">

                    <MapPin
                      size={13}
                      className="text-slate-600"
                    />

                    <span className="truncate text-xs text-slate-500">
                      {road.location}
                    </span>

                  </div>


                  <p className="mt-1 text-xs text-slate-500">
                    Cause: {road.reason}
                  </p>

                </div>


                {/* Status */}
                <div className="flex shrink-0 items-center gap-1.5">

                  {road.status === "Blocked" ? (
                    <>
                      <AlertTriangle
                        size={14}
                        className="text-red-400"
                      />

                      <span className="text-xs font-medium text-red-400">
                        Blocked
                      </span>
                    </>
                  ) : road.status === "Restricted" ? (
                    <>
                      <AlertTriangle
                        size={14}
                        className="text-yellow-400"
                      />

                      <span className="text-xs font-medium text-yellow-400">
                        Restricted
                      </span>
                    </>
                  ) : (
                    <>
                      <CheckCircle2
                        size={14}
                        className="text-green-400"
                      />

                      <span className="text-xs font-medium text-green-400">
                        Open
                      </span>
                    </>
                  )}

                </div>

              </div>

            </div>

          ))}

        </div>
      )}


      {/* View Map */}
      <button
        className="mt-4 w-full rounded-xl border border-[#1E3042] py-2.5 text-xs font-medium text-slate-400 transition hover:bg-white/[0.03] hover:text-white"
      >
        View affected roads on map
      </button>

    </section>
  );
}


export default BlockedRoads;
