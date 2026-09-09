import { AlertTriangle, FileWarning } from "lucide-react";
import QuickStatCard from "./QuickStatCard";

function QuickStats({ onNavigate, riskOverview = [] }) {
  const handleCriticalZones = () => {
    onNavigate("Critical Zones");
  };

  const handleReports = () => {
    onNavigate("Field Reports");
  };

  const criticalCount = riskOverview.filter(
    (item) => item.risk_level === "CRITICAL"
  ).length;

  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <QuickStatCard
        title="Critical Zones"
        subtitle={`${criticalCount} Critical Locations`}
        icon={<AlertTriangle size={25} />}
        iconClass="bg-red-500/10 text-red-400"
        cardClass="border-red-500/25 bg-gradient-to-r from-red-500/[0.08] to-[#0B1522]"
        onClick={handleCriticalZones}
      />

      <QuickStatCard
        title="Field Reports"
        subtitle="36 Reports Today"
        icon={<FileWarning size={25} />}
        iconClass="bg-violet-500/10 text-violet-400"
        cardClass="border-violet-500/25 bg-gradient-to-r from-violet-500/[0.08] to-[#0B1522]"
        onClick={handleReports}
      />
    </div>
  );
}

export default QuickStats;