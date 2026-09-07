import {
  AlertTriangle,
  ChevronRight,
  MapPin,
} from "lucide-react";

function PriorityAlerts() {
  // Temporary frontend data.
  // Later this will come from the backend/API.
  const alerts = [
    {
      id: 1,
      location: "Aizawl, Mizoram",
      message: "High landslide risk detected",
      priority: "P1",
      type: "Critical",
    },
    {
      id: 2,
      location: "Tawang, Arunachal Pradesh",
      message: "Heavy rainfall increasing risk",
      priority: "P2",
      type: "High",
    },
    {
      id: 3,
      location: "Gangtok, Sikkim",
      message: "Road connectivity at risk",
      priority: "P2",
      type: "High",
    },
  ];

  return (
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
          3 Active
        </span>
      </div>

      {/* Alerts */}
      <div className="space-y-3">
        {alerts.map((alert) => (
          <button
            key={alert.id}
            className="group flex w-full items-center justify-between rounded-xl border border-[#1E3042] bg-[#0B1522] p-3 text-left transition hover:border-red-500/30 hover:bg-white/[0.03]"
          >
            <div className="flex min-w-0 items-center gap-3">

              {/* Priority */}
              <div
                className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-xs font-bold ${
                  alert.priority === "P1"
                    ? "bg-red-500/10 text-red-400"
                    : "bg-orange-500/10 text-orange-400"
                }`}
              >
                {alert.priority}
              </div>

              {/* Information */}
              <div className="min-w-0">
                <div className="flex items-center gap-1.5">
                  <MapPin
                    size={14}
                    className="shrink-0 text-slate-500"
                  />

                  <span className="truncate text-sm font-medium text-slate-200">
                    {alert.location}
                  </span>
                </div>

                <p className="mt-1 truncate text-xs text-slate-500">
                  {alert.message}
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

      {/* View All */}
      <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-[#1E3042] py-2.5 text-xs font-medium text-slate-400 transition hover:bg-white/[0.03] hover:text-white">
        View all alerts
        <ChevronRight size={15} />
      </button>
    </section>
  );
}

export default PriorityAlerts;