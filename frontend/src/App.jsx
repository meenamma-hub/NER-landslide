import { useEffect, useState } from "react";

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

import { getRiskOverview } from "./services/riskService";
import { getLocations } from "./services/locationsService";


function App() {
  // =====================================================
  // STATE
  // =====================================================

  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [activePage, setActivePage] = useState("Dashboard");

  const [demoData, setDemoData] = useState(dashboardData);

  const [locations, setLocations] = useState([]);

  const [riskOverview, setRiskOverview] = useState([]);


  // =====================================================
  // LOAD BACKEND DATA
  // =====================================================

  useEffect(() => {
    getLocations()
      .then((data) => {
        console.log("Locations:", data);
        setLocations(data);
      })
      .catch((error) => {
        console.error(
          "Failed to fetch locations:",
          error
        );
      });


    getRiskOverview()
      .then((data) => {
        console.log("Risk Overview:", data);
        setRiskOverview(data);
      })
      .catch((error) => {
        console.error(
          "Failed to fetch risk overview:",
          error
        );
      });
  }, []);


  // =====================================================
  // NAVIGATION
  // =====================================================

  const handleNavigation = (page) => {
    setActivePage(page);
    setSidebarOpen(false);
  };


  // =====================================================
  // RAINFALL SLIDER
  // =====================================================

  const handleRainfallChange = (value) => {
    console.log(
      "SLIDER RAINFALL:",
      value
    );

    setDemoData((prev) => ({
      ...prev,
      rainfall: Number(value),
    }));
  };


  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="min-h-screen bg-[#020812] text-slate-100">

      {/* =================================================
          NAVBAR
          ================================================= */}

      <Navbar
        onMenuClick={() => setSidebarOpen(true)}
      />


      <div className="flex">

        {/* =================================================
            SIDEBAR
            ================================================= */}

        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          activePage={activePage}
          onNavigate={handleNavigation}
        />


        {/* =================================================
            MAIN CONTENT
            ================================================= */}

        <main className="min-w-0 flex-1">

          <div className="mx-auto w-full max-w-[1600px] p-4 sm:p-5 lg:p-6">


            {/* =================================================
                DASHBOARD
                ================================================= */}

            {activePage === "Dashboard" && (
              <>

                <DashboardHeader />


                <QuickStats
                  onNavigate={handleNavigation}
                  riskOverview={riskOverview}
                />


                {/* IMPORTANT:
                    rainfall is now passed to MapSection
                */}

                <MapSection
                  riskLevel={demoData.riskLevel}
                  rainfall={demoData.rainfall}
                />


                {/* Rainfall Slider */}

                <RainfallInput
                  rainfall={demoData.rainfall}
                  onRainfallChange={handleRainfallChange}
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


            {/* =================================================
                CRITICAL ZONES
                ================================================= */}

            {activePage === "Critical Zones" && (
              <>

                <DashboardHeader />

                <CriticalZones />

              </>
            )}


            {/* =================================================
                RISK MAP
                ================================================= */}

            {activePage === "Risk Map" && (
              <>

                <DashboardHeader />


                {/* IMPORTANT:
                    rainfall is also passed here
                */}

                <MapSection
                  riskLevel={demoData.riskLevel}
                  rainfall={demoData.rainfall}
                />

              </>
            )}


            {/* =================================================
                PREDICTION
                ================================================= */}

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


            {/* =================================================
                IMPACT & PRIORITY
                ================================================= */}

            {activePage === "Impact & Priority" && (
              <>

                <DashboardHeader />

                <PriorityAlerts />

                <ImpactSummary />

              </>
            )}


            {/* =================================================
                ROADS & ROUTES
                ================================================= */}

            {activePage === "Roads & Routes" && (
              <>

                <DashboardHeader />

                <BlockedRoads />

              </>
            )}


            {/* =================================================
                HOSPITALS & RESCUE
                ================================================= */}

            {activePage === "Hospitals & Rescue" && (
              <>

                <DashboardHeader />

                <NearestHospitals />

                <RescueTeams />

              </>
            )}


            {/* =================================================
                ALERTS & SMS
                ================================================= */}

            {activePage === "Alerts & SMS" && (
              <>

                <DashboardHeader />

                <AlertsSMS />

              </>
            )}


            {/* =================================================
                FIELD REPORTS
                ================================================= */}

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


            {/* =================================================
                ANALYTICS
                ================================================= */}

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