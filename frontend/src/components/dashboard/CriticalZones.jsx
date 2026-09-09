import { useEffect, useState } from "react";

import { getRiskOverview } from "../../services/riskService";

import {
  AlertTriangle,
  MapPin,
  ChevronRight,
} from "lucide-react";

import ZoneDetailsModal from "./ZoneDetailsModal";


function CriticalZones() {
  const [selectedZone, setSelectedZone] = useState(null);
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);


  // ------------------------------------------
  // Load risk data from backend
  // ------------------------------------------

  useEffect(() => {
    const loadZones = async () => {
      try {
        setLoading(true);

        const data = await getRiskOverview();

        console.log("Critical Zones:", data);

        const formattedZones = data.map((item) => {
          const score = Number(item.risk_score);

          let levelClass =
            "text-green-400 bg-green-500/10 border-green-500/20";

          if (item.risk_level === "CRITICAL") {
            levelClass =
              "text-red-400 bg-red-500/10 border-red-500/20";
          } else if (item.risk_level === "HIGH") {
            levelClass =
              "text-orange-400 bg-orange-500/10 border-orange-500/20";
          } else if (item.risk_level === "MODERATE") {
            levelClass =
              "text-yellow-400 bg-yellow-500/10 border-yellow-500/20";
          }

          return {
            // Backend data
            name: item.location,
            state: item.state,
            district: item.district,

            score: score,

            rainfall: item.rainfall ?? "N/A",

            level:
              item.risk_level
                ? item.risk_level.charAt(0) +
                  item.risk_level.slice(1).toLowerCase()
                : "Unknown",

            priority: item.priority,
            priorityScore: item.priority_score,

            populationAffected:
              item.population_affected,

            recommendedAction:
              item.recommended_action,

            // Styling
            levelClass: levelClass,
          };
        });

        setZones(formattedZones);

      } catch (error) {
        console.error(
          "Failed to fetch critical zones:",
          error
        );

      } finally {
        setLoading(false);
      }
    };

    loadZones();
  }, []);


  // ------------------------------------------
  // Critical count
  // ------------------------------------------

  const criticalCount = zones.filter(
    (zone) => zone.level === "Critical"
  ).length;


  // ------------------------------------------
  // UI
  // ------------------------------------------

  return (
    <section className="rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

      {/* Header */}

      <div className="mb-5 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-red-500/10 text-red-400">
            <AlertTriangle size={23} />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white">
              Critical Zones
            </h2>

            <p className="text-xs text-slate-500">
              Aizawl, Mizoram • Current risk assessment
            </p>
          </div>

        </div>


        <span className="rounded-full border border-red-500/20 bg-red-500/10 px-3 py-1 text-xs font-medium text-red-400">
          {criticalCount} CRITICAL
        </span>

      </div>


      {/* Loading */}

      {loading && (
        <div className="py-8 text-center text-sm text-slate-500">
          Loading risk zones...
        </div>
      )}


      {/* Zone Cards */}

      {!loading && (
        <div className="space-y-3">

          {zones.map((zone) => (

            <button
              key={`${zone.name}-${zone.state}`}
              onClick={() => setSelectedZone(zone)}
              className="w-full rounded-xl border border-[#1E3042] bg-[#0B1522] p-4 text-left transition hover:border-[#30465D] hover:bg-[#0D1927]"
            >

              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                {/* Zone Info */}

                <div className="flex items-center gap-3">

                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-500/10 text-slate-400">
                    <MapPin size={19} />
                  </div>


                  <div>

                    <h3 className="text-base font-semibold text-white">
                      {zone.name}
                    </h3>

                    <p className="mt-1 text-xs text-slate-500">
                      {zone.state}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      Rainfall: {zone.rainfall} mm
                    </p>

                  </div>

                </div>


                {/* Score + Level */}

                <div className="flex items-center justify-between gap-4 sm:justify-end">

                  <div>

                    <p className="text-[10px] uppercase tracking-wider text-slate-600">
                      Danger Score
                    </p>

                    <p className="text-xl font-bold text-white">
                      {zone.score}
                      <span className="text-xs font-normal text-slate-600">
                        /100
                      </span>
                    </p>

                  </div>


                  <span
                    className={`rounded-full border px-3 py-1.5 text-xs font-semibold ${zone.levelClass}`}
                  >
                    {zone.level}
                  </span>


                  <ChevronRight
                    size={18}
                    className="text-slate-600"
                  />

                </div>

              </div>

            </button>

          ))}

        </div>
      )}


      {/* Zone Details Modal */}

      {selectedZone && (
        <ZoneDetailsModal
          zone={selectedZone}
          onClose={() => setSelectedZone(null)}
        />
      )}

    </section>
  );
}


export default CriticalZones;