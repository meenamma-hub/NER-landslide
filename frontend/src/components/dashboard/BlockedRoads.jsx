import {
  AlertTriangle,
  CheckCircle2,
  MapPin,
  Route,
} from "lucide-react";

function BlockedRoads() {
  // Temporary frontend data.
  // Later this will come from GIS/backend.
  const roads = [
    {
      id: 1,
      road: "NH-6",
      location: "Mamit, Mizoram",
      reason: "Landslide debris",
      severity: "Critical",
      status: "Blocked",
    },
    {
      id: 2,
      road: "NH-10",
      location: "Gangtok, Sikkim",
      reason: "Rockfall",
      severity: "High",
      status: "Blocked",
    },
    {
      id: 3,
      road: "Tawang Road",
      location: "Tawang, Arunachal Pradesh",
      reason: "Heavy rainfall",
      severity: "Moderate",
      status: "Restricted",
    },
  ];

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
              Connectivity affected by incidents
            </p>
          </div>
        </div>

        <span className="rounded-full bg-orange-500/10 px-2.5 py-1 text-xs font-semibold text-orange-400">
          {roads.length} Roads
        </span>
      </div>

      {/* Road List */}
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
                    className={`rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                      road.severity === "Critical"
                        ? "bg-red-500/10 text-red-400"
                        : road.severity === "High"
                        ? "bg-orange-500/10 text-orange-400"
                        : "bg-yellow-500/10 text-yellow-400"
                    }`}
                  >
                    {road.severity}
                  </span>
                </div>

                <div className="mt-2 flex items-center gap-1.5">
                  <MapPin size={13} className="text-slate-600" />

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
                ) : (
                  <>
                    <CheckCircle2
                      size={14}
                      className="text-yellow-400"
                    />

                    <span className="text-xs font-medium text-yellow-400">
                      Restricted
                    </span>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* View Map */}
      <button className="mt-4 w-full rounded-xl border border-[#1E3042] py-2.5 text-xs font-medium text-slate-400 transition hover:bg-white/[0.03] hover:text-white">
        View affected roads on map
      </button>
    </section>
  );
}

export default BlockedRoads;
