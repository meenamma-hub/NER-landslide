import { useEffect, useState } from "react";

import {
  Building2,
  MapPin,
  Users,
  AlertTriangle,
} from "lucide-react";

import { getRiskOverview } from "../../services/riskService";


function ImpactSummary() {
  const [impactData, setImpactData] = useState([]);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    const loadImpactData = async () => {
      try {
        setLoading(true);

        const data = await getRiskOverview();

        const riskData = Array.isArray(data) ? data : [];

        setImpactData(riskData);

        console.log("IMPACT SUMMARY DATA:", riskData);

      } catch (error) {
        console.error("FAILED TO LOAD IMPACT DATA:", error);
      } finally {
        setLoading(false);
      }
    };

    loadImpactData();
  }, []);


  // Total people affected across all locations
  const totalPopulationAffected = impactData.reduce(
    (total, item) =>
      total + Number(item.population_affected || 0),
    0
  );


  // Number of locations currently marked HIGH or CRITICAL
  const highRiskLocations = impactData.filter((item) => {
    const level = String(item.risk_level || "").toUpperCase();

    return level === "HIGH" || level === "CRITICAL";
  }).length;


  // Average infrastructure factor
  const averageInfrastructure =
    impactData.length > 0
      ? (
          impactData.reduce(
            (total, item) =>
              total + Number(item.infrastructure_factor || 0),
            0
          ) / impactData.length
        ).toFixed(1)
      : "0";


  // Highest priority score
  const highestPriorityScore =
    impactData.length > 0
      ? Math.max(
          ...impactData.map((item) =>
            Number(item.priority_score || 0)
          )
        ).toFixed(1)
      : "0";


  const cards = [
    {
      label: "People Affected",
      value: totalPopulationAffected.toLocaleString(),
      icon: <Users size={20} />,
      iconClass: "bg-red-500/10 text-red-400",
    },
    {
      label: "High-Risk Locations",
      value: highRiskLocations,
      icon: <MapPin size={20} />,
      iconClass: "bg-orange-500/10 text-orange-400",
    },
    {
      label: "Avg Infrastructure",
      value: averageInfrastructure,
      icon: <Building2 size={20} />,
      iconClass: "bg-violet-500/10 text-violet-400",
    },
    {
      label: "Highest Priority",
      value: highestPriorityScore,
      icon: <AlertTriangle size={20} />,
      iconClass: "bg-yellow-500/10 text-yellow-400",
    },
  ];


  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400">
            <MapPin size={21} />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white sm:text-lg">
              Impact Summary
            </h2>

            <p className="text-xs text-slate-500">
              Estimated impact across current risk zones
            </p>
          </div>

        </div>

      </div>


      {/* Loading */}
      {loading ? (
        <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-5 text-center text-xs text-slate-500">
          Loading impact data...
        </div>
      ) : (

        <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">

          {cards.map((item) => (

            <div
              key={item.label}
              className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-3 sm:p-4"
            >

              <div
                className={`mb-3 flex h-9 w-9 items-center justify-center rounded-lg ${item.iconClass}`}
              >
                {item.icon}
              </div>

              <p className="text-xl font-bold text-white sm:text-2xl">
                {item.value}
              </p>

              <p className="mt-1 text-xs text-slate-500">
                {item.label}
              </p>

            </div>

          ))}

        </div>

      )}


      {/* Note */}
      <div className="mt-4 rounded-xl border border-[#1E3042] bg-[#0B1522] px-3 py-3">

        <p className="text-xs leading-relaxed text-slate-500">
          Impact estimates are calculated from the current risk
          overview, population exposure, infrastructure factors
          and priority scores.
        </p>

      </div>

    </section>
  );
}


export default ImpactSummary;
