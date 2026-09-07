import { MapPinned } from "lucide-react";

function MapSection({ riskLevel = "CRITICAL" }) {
  return (
    <section className="mt-4 overflow-hidden rounded-2xl border border-[#1E3042] bg-[#07111D]">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[#1E3042] px-4 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
            <MapPinned size={22} />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white">
              GIS Risk Map
            </h2>
            <p className="text-xs text-slate-500">
              Live landslide risk zones
            </p>
          </div>
        </div>

        <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-400">
          LIVE
        </span>
      </div>

      {/* Map Container */}
      <div className="relative h-[320px] w-full overflow-hidden bg-[#0A1623] sm:h-[400px] lg:h-[500px]">
        
        {/* Temporary placeholder */}
        <div className="flex h-full items-center justify-center">
          <div className="text-center">
            <MapPinned
              size={48}
              className="mx-auto mb-3 text-slate-600"
            />

            <p className="text-sm font-medium text-slate-400">
              GIS Map Loading Area
            </p>

            <p className="mt-1 text-xs text-slate-600">
              Map component will be integrated here
            </p>
          </div>
        </div>

        {/* Risk Legend */}
        <div className="absolute bottom-4 left-4 rounded-xl border border-[#26384B] bg-[#07111D]/95 p-3 backdrop-blur-md">
          <p className="mb-2 text-xs font-semibold text-slate-300">
            Risk Level
          </p>

          <div className="flex flex-wrap gap-3 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full bg-red-500" />
              <span className="text-slate-400">Critical</span>
            </div>

            <div className="flex items-center gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full bg-orange-500" />
              <span className="text-slate-400">High</span>
            </div>

            <div className="flex items-center gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full bg-yellow-400" />
              <span className="text-slate-400">Moderate</span>
            </div>

            <div className="flex items-center gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full bg-green-500" />
              <span className="text-slate-400">Low</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default MapSection;