import { useEffect, useState } from "react";

import {
  MapContainer,
  TileLayer,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import {
  getRiskOverview,
  getRiskData,
} from "../../services/riskService";

import api from "../../services/api";

import RiskMarker from "./RiskMarker";
import AizawlGridLayer from "./AizawlGridLayer";
import ZoneDetailsModal from "../dashboard/ZoneDetailsModal";


function GISMap({ rainfall = 0 }) {
  const [locations, setLocations] = useState([]);
  const [aizawlRisk, setAizawlRisk] = useState(null);

  const [loading, setLoading] = useState(true);
  const [predictionLoading, setPredictionLoading] = useState(false);

  const [error, setError] = useState("");
  const [selectedZone, setSelectedZone] = useState(null);

  // =====================================================
  // 1. LOAD NER RISK DATA
  // =====================================================

  useEffect(() => {
    let isMounted = true;

    const loadLocations = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await getRiskOverview();

        if (!isMounted) return;

        const data = Array.isArray(response)
          ? response
          : Array.isArray(response?.locations)
          ? response.locations
          : [];

        setLocations(data);

        console.log("NER RISK OVERVIEW:", data);

      } catch (err) {
        console.error("FAILED TO LOAD RISK OVERVIEW:", err);

        if (isMounted) {
          setError("Unable to load risk data");
        }

      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadLocations();

    return () => {
      isMounted = false;
    };
  }, []);


  // =====================================================
  // 2. RAINFALL SLIDER → AIZAWL ML PREDICTION
  // =====================================================

  useEffect(() => {
    let isMounted = true;

    const currentRainfall = Number(rainfall);

    if (!Number.isFinite(currentRainfall)) {
      console.log("INVALID RAINFALL VALUE");
      return;
    }

    const predictAizawlRisk = async () => {
      try {
        setPredictionLoading(true);
        setError("");

        // -----------------------------------------------
        // Get existing Aizawl parameters
        // -----------------------------------------------

        const aizawlData = await getRiskData(4);

        if (!isMounted) return;

        console.log("AIZAWL BASE DATA:", aizawlData);


        // -----------------------------------------------
        // Prepare ML input
        // -----------------------------------------------

        const predictionInput = {
          rainfall_24h_mm: currentRainfall,

          rainfall_7d_mm: Number(
            aizawlData.rainfall_7d
          ),

          elevation_m: Number(
            aizawlData.elevation
          ),

          slope_degrees: Number(
            aizawlData.slope
          ),

          historical_landslide_count_5y: Number(
            aizawlData.historical_landslide_count
          ),
        };


        console.log("SENDING TO ML:", predictionInput);


        // -----------------------------------------------
        // Call backend ML prediction
        // -----------------------------------------------

        const response = await api.post(
          "/risk/predict",
          predictionInput
        );

        if (!isMounted) return;

        const result = response.data;

        console.log("ML RESPONSE:", result);


        // -----------------------------------------------
        // Store latest prediction
        // -----------------------------------------------

        setAizawlRisk({
          location: result.location,

          risk_score: Number(
            result.risk_score
          ),

          ml_risk_score: Number(
            result.ml_risk_score
          ),

          risk_level: result.risk_level,

          population_factor: Number(
            result.population_factor
          ),

          infrastructure_factor: Number(
            result.infrastructure_factor
          ),

          connectivity_factor: Number(
            result.connectivity_factor
          ),

          population_affected: Number(
            result.population_affected
          ),

          connectivity_status:
            result.connectivity_status,

          priority_score: Number(
            result.priority_score
          ),

          priority: result.priority,

          recommended_action:
            result.recommended_action,
        });

      } catch (err) {
        console.error(
          "AIZAWL PREDICTION FAILED:",
          err
        );

        if (isMounted) {
          setError(
            "Unable to calculate Aizawl risk"
          );
        }

      } finally {
        if (isMounted) {
          setPredictionLoading(false);
        }
      }
    };

    predictAizawlRisk();

    return () => {
      isMounted = false;
    };

  }, [rainfall]);


  // =====================================================
  // 3. VALIDATE LOCATION COORDINATES
  // =====================================================

  const validLocations = locations.filter((location) => {
    const lat = Number(location.latitude);
    const lng = Number(location.longitude);

    return (
      Number.isFinite(lat) &&
      Number.isFinite(lng) &&
      lat >= -90 &&
      lat <= 90 &&
      lng >= -180 &&
      lng <= 180
    );
  });


  // =====================================================
  // 4. MAP
  // =====================================================

  return (
    <div className="relative h-[320px] w-full sm:h-[400px] lg:h-[500px]">

      <MapContainer
        center={[25.5, 92.5]}
        zoom={6}
        scrollWheelZoom={true}
        className="h-full w-full"
      >

        {/* OpenStreetMap */}

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        />


        {/* =================================================
            NER LOCATION RISK MARKERS
            ================================================= */}

        {validLocations.map((location) => (
          <RiskMarker
            key={location.location_id}
            location={location}
          />
        ))}


        {/* =================================================
            AIZAWL IMERG GRID
            Current MVP:
            One Aizawl ML prediction is applied
            to the 15 grid cells.
            ================================================= */}

        <AizawlGridLayer
          risk={aizawlRisk}
        />

      </MapContainer>


      {/* =================================================
          LOADING
          ================================================= */}

      {(loading || predictionLoading) && (
        <div className="absolute left-1/2 top-4 z-[1000] -translate-x-1/2 rounded-lg border border-[#26384B] bg-[#07111D]/95 px-3 py-2 text-xs text-slate-400">

          {predictionLoading
            ? `Updating Aizawl risk... ${currentRainfallValue(rainfall)} mm`
            : "Loading risk data..."}

        </div>
      )}


      {/* =================================================
          ERROR
          ================================================= */}

      {error && (
        <div className="absolute left-1/2 top-4 z-[1000] -translate-x-1/2 rounded-lg border border-red-500/20 bg-[#07111D]/95 px-3 py-2 text-xs text-red-400">

          {error}

        </div>
      )}


      {/* =================================================
          CURRENT RAINFALL
          ================================================= */}

      <div className="absolute bottom-4 left-4 z-[1000] rounded-xl border border-[#26384B] bg-[#07111D]/95 px-3 py-2 backdrop-blur-md">

        <p className="text-[10px] uppercase tracking-wide text-slate-500">
          Aizawl Rainfall
        </p>

        <p className="text-sm font-semibold text-blue-400">
          {currentRainfallValue(rainfall)} mm
        </p>

      </div>

    </div>
  );
}


// =====================================================
// SAFE RAINFALL VALUE
// =====================================================

function currentRainfallValue(value) {
  const number = Number(value);

  return Number.isFinite(number)
    ? number
    : 0;
}


export default GISMap;