
import { useEffect, useState } from "react";

import {
  AlertTriangle,
  ChevronRight,
  MapPin,
} from "lucide-react";

import { getRiskOverview } from "../../services/riskService";
import ZoneDetailsModal from "./ZoneDetailsModal";

function PriorityAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAlert, setSelectedAlert] = useState(null);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        setLoading(true);

        const data = await getRiskOverview();

        const riskData = Array.isArray(data) ? data : [];

        const priorityAlerts = riskData
          .filter((item) => {
            const priority = String(item.priority || "").toUpperCase();
            const riskLevel = String(item.risk_level || "").toUpperCase();

            return (
              priority === "P1" ||
              priority === "P2" ||
              riskLevel === "CRITICAL" ||
              riskLevel === "HIGH"
            );
          })
          .sort(
            (a, b) =>
              Number(b.priority_score || 0) -
              Number(a.priority_score || 0)
          )
          .slice(0, 3);

        setAlerts(priorityAlerts);

        console.log("PRIORITY ALERTS:", priorityAlerts);
      } catch (error) {
        console.error("FAILED TO LOAD PRIORITY ALERTS:", error);
      } finally {
        setLoading(false);
      }
    };

    loadAlerts();
  }, []);

  const getPriorityClass = (priority) => {
    if (priority === "P1") {
      return "bg-red-500/10 text-red-400";
    }

    if (priority === "P2") {
      return "bg-orange-500/10 text-orange-400";
    }

    return "bg-yellow-500/10 text-yellow-400";
  };

  const getRiskMessage = (riskLevel) => {
    switch (String(riskLevel || "").toUpperCase()) {
      case "CRITICAL":
        return "Critical landslide risk detected";

      case "HIGH":
        return "High landslide risk detected";

      case "MODERATE":
        return "Moderate landslide risk detected";

      case "LOW":
        return "Low landslide risk";

      default:
        return "Risk assessment available";
    }
  };

  return (
    <>
      <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

        {/* Header */}
        <div className="mb-4 flex items-center justify-between">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-500/10 text-red-400">
              <AlertTriangle size={21} />
            </div>

            <div>
              <h2 className="text-base font-semibold text-white sm:text-lg">
                Top Priority Alerts
              </h2>

              <p className="text-xs text-slate-500">
                Locations requiring immediate attention
              </p>
            </div>

          </div>

          <span className="rounded-full bg-red-500/10 px-2.5 py-1 text-xs font-semibold text-red-400">
            {alerts.length} Active
          </span>

        </div>

        {/* Loading */}
        {loading && (
          <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-4 text-center text-xs text-slate-500">
            Loading priority alerts...
          </div>
        )}

        {/* No alerts */}
        {!loading && alerts.length === 0 && (
          <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-4 text-center text-xs text-slate-500">
            No priority alerts available.
          </div>
        )}

        {/* Alerts */}
        {!loading && alerts.length > 0 && (
          <div className="space-y-3">

            {alerts.map((alert) => (

              <button
                key={alert.location_id}
                onClick={() => setSelectedAlert(alert)}
                className="group flex w-full items-center justify-between rounded-xl border border-[#1E3042] bg-[#0B1522] p-3 text-left transition hover:border-red-500/30 hover:bg-white/[0.03]"
              >

                <div className="flex min-w-0 items-center gap-3">

                  {/* Priority */}
                  <div
                    className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-xs font-bold ${getPriorityClass(
                      alert.priority
                    )}`}
                  >
                    {alert.priority || "P3"}
                  </div>

                  {/* Information */}
                  <div className="min-w-0">

                    <div className="flex items-center gap-1.5">

                      <MapPin
                        size={14}
                        className="shrink-0 text-slate-500"
                      />

                      <span className="truncate text-sm font-medium text-slate-200">
                        {alert.location}, {alert.state}
                      </span>

                    </div>

                    <p className="mt-1 truncate text-xs text-slate-500">
                      {getRiskMessage(alert.risk_level)}
                    </p>

                  </div>

                </div>

                {/* Arrow */}
                <ChevronRight
                  size={19}
                  className="ml-2 shrink-0 text-slate-600 transition group-hover:translate-x-1 group-hover:text-slate-300"
                />

              </button>

            ))}

          </div>
        )}

        {/* View All */}
        <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-[#1E3042] py-2.5 text-xs font-medium text-slate-400 transition hover:bg-white/[0.03] hover:text-white">

          View all alerts

          <ChevronRight size={15} />

        </button>

      </section>

      {/* Location Details Modal */}
      <ZoneDetailsModal
        zone={selectedAlert}
        onClose={() => setSelectedAlert(null)}
      />
    </>
  );
}

export default PriorityAlerts;
