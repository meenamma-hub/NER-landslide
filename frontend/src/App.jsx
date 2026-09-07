import { useState } from "react";

import Navbar from "./components/layout/Navbar";
import Sidebar from "./components/layout/Sidebar";

import DashboardHeader from "./components/dashboard/DashboardHeader";
import QuickStats from "./components/dashboard/QuickStats";
import MapSection from "./components/dashboard/MapSection";
import LivePrediction from "./components/dashboard/LivePrediction";
import PriorityAlerts from "./components/dashboard/PriorityAlerts";
import BlockedRoads from "./components/dashboard/BlockedRoads";
import ImpactSummary from "./components/dashboard/ImpactSummary";
import NearestHospitals from "./components/dashboard/NearestHospitals";
import RescueTeams from "./components/dashboard/RescueTeams";
import AlertsSMS from "./components/dashboard/AlertsSMS";
import CriticalZones from "./components/dashboard/CriticalZones";
import RainfallInput from "./components/dashboard/RainfallInput";
import { dashboardData } from "./data/dashboardData";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activePage, setActivePage] = useState("Dashboard");
  const [demoData, setDemoData] = useState(dashboardData);
  const handleNavigation = (page) => {
    setActivePage(page);
    setSidebarOpen(false);
  };
 
  return (
    <div className="min-h-screen bg-[#020812] text-slate-100">

      {/* Navbar */}
      <Navbar
        onMenuClick={() => setSidebarOpen(true)}
      />

      <div className="flex">

        {/* Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          activePage={activePage}
          onNavigate={handleNavigation}
        />

        {/* Main Content */}
        <main className="min-w-0 flex-1">
          <div className="mx-auto w-full max-w-[1600px] p-4 sm:p-5 lg:p-6">

            {activePage === "Dashboard" && (
              <>
                <DashboardHeader />
                <QuickStats onNavigate={handleNavigation} />
                <MapSection riskLevel={demoData.riskLevel} />
                <RainfallInput
  rainfall={demoData.rainfall}
  onRainfallChange={(value) =>
    setDemoData((prev) => ({
      ...prev,
      rainfall: value,
    }))
  }
/>
                <LivePrediction
                  dangerScore={demoData.dangerScore}
                  rainfall={demoData.rainfall}
                  riskLevel={demoData.riskLevel}
                />
                <PriorityAlerts />
                <BlockedRoads />
                <ImpactSummary />
                <NearestHospitals />
                <RescueTeams />
                <AlertsSMS />
              </>
            )}
            {activePage === "Critical Zones" && (
              <>
                <DashboardHeader />
                <CriticalZones />
              </>
            )}

            {activePage === "Risk Map" && (
              <>
                <DashboardHeader />
                <MapSection riskLevel={demoData.riskLevel} />
              </>
            )}

            {activePage === "Prediction" && (
              <>
                <DashboardHeader />
                <LivePrediction
                  rainfall={demoData.rainfall}
                  dangerScore={demoData.dangerScore}
                  riskLevel={demoData.riskLevel}
                />
              </>
            )}

            {activePage === "Impact & Priority" && (
              <>
                <DashboardHeader />
                <PriorityAlerts />
                <ImpactSummary />
              </>
            )}

            {activePage === "Roads & Routes" && (
              <>
                <DashboardHeader />
                <BlockedRoads />
              </>
            )}

            {activePage === "Hospitals & Rescue" && (
              <>
                <DashboardHeader />
                <NearestHospitals />
                <RescueTeams />
              </>
            )}

            {activePage === "Alerts & SMS" && (
              <>
                <DashboardHeader />
                <AlertsSMS />
              </>
            )}

            {activePage === "Field Reports" && (
              <>
                <DashboardHeader />

                <div className="rounded-2xl border border-[#1E3042] bg-[#07111D] p-6">
                  <h2 className="text-lg font-semibold text-white">
                    Field Reports
                  </h2>

                  <p className="mt-2 text-sm text-slate-500">
                    Field reporting module will be integrated here.
                  </p>
                </div>
              </>
            )}

            {activePage === "Analytics" && (
              <>
                <DashboardHeader />

                <div className="rounded-2xl border border-[#1E3042] bg-[#07111D] p-6">
                  <h2 className="text-lg font-semibold text-white">
                    Analytics
                  </h2>

                  <p className="mt-2 text-sm text-slate-500">
                    Analytics module will be integrated here.
                  </p>
                </div>
              </>
            )}

          </div>
        </main>
      </div>
    </div>
  );
}

export default App;