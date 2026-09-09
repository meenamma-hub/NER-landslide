import { useEffect, useState } from "react";

import {
  Bed,
  ChevronRight,
  Hospital,
  MapPin,
} from "lucide-react";

import { getHospitals } from "../../services/hospitalService";


function NearestHospitals() {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    const loadHospitals = async () => {
      try {
        setLoading(true);
        setError("");

        const data = await getHospitals();

        const hospitalData = Array.isArray(data)
          ? data
          : [];

        setHospitals(hospitalData);

        console.log("HOSPITALS DATA:", hospitalData);

      } catch (err) {
        console.error(
          "FAILED TO LOAD HOSPITALS:",
          err
        );

        setError("Unable to load hospital data");

      } finally {
        setLoading(false);
      }
    };

    loadHospitals();
  }, []);


  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400">
            <Hospital size={21} />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white sm:text-lg">
              Nearest Hospitals
            </h2>

            <p className="text-xs text-slate-500">
              Emergency medical facilities nearby
            </p>
          </div>

        </div>

        <span className="rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs font-semibold text-emerald-400">
          {hospitals.length} Nearby
        </span>

      </div>


      {/* Loading */}
      {loading && (
        <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-5 text-center text-xs text-slate-500">
          Loading hospitals...
        </div>
      )}


      {/* Error */}
      {!loading && error && (
        <div className="rounded-xl border border-red-500/20 bg-[#0B1522] p-5 text-center text-xs text-red-400">
          {error}
        </div>
      )}


      {/* Empty */}
      {!loading && !error && hospitals.length === 0 && (
        <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-5 text-center text-xs text-slate-500">
          No hospitals available.
        </div>
      )}


      {/* Hospital List */}
      {!loading && !error && hospitals.length > 0 && (
        <div className="space-y-3">

          {hospitals.map((hospital) => (

            <div
              key={hospital.id}
              className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-3"
            >

              <div className="flex items-start justify-between gap-3">

                {/* Hospital info */}
                <div className="min-w-0">

                  <div className="flex items-center gap-2">

                    <h3 className="truncate text-sm font-semibold text-white">
                      {hospital.name}
                    </h3>

                    <span
                      className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                        hospital.status === "Available"
                          ? "bg-emerald-500/10 text-emerald-400"
                          : "bg-yellow-500/10 text-yellow-400"
                      }`}
                    >
                      {hospital.status}
                    </span>

                  </div>


                  <div className="mt-2 flex items-center gap-1.5">

                    <MapPin
                      size={13}
                      className="shrink-0 text-slate-600"
                    />

                    <span className="truncate text-xs text-slate-500">
                      {hospital.location}
                    </span>

                  </div>

                </div>


                {/* Distance */}
                <div className="shrink-0 text-right">

                  <p className="text-sm font-semibold text-slate-200">
                    {Number(hospital.distance).toFixed(1)} km
                  </p>

                  <p className="text-[10px] text-slate-600">
                    distance
                  </p>

                </div>

              </div>


              {/* Beds */}
              <div className="mt-3 flex items-center justify-between border-t border-[#1E3042] pt-3">

                <div className="flex items-center gap-2">

                  <Bed
                    size={15}
                    className="text-slate-500"
                  />

                  <span className="text-xs text-slate-400">
                    Emergency beds
                  </span>

                </div>

                <span className="text-xs font-semibold text-slate-200">
                  {hospital.emergency_beds} available
                </span>

              </div>

            </div>

          ))}

        </div>
      )}


      {/* View all */}
      <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-[#1E3042] py-2.5 text-xs font-medium text-slate-400 transition hover:bg-white/[0.03] hover:text-white">
        View hospitals on map
        <ChevronRight size={15} />
      </button>

    </section>
  );
}


export default NearestHospitals;
