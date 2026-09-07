import {
  X,
  MapPin,
  CloudRain,
  Activity,
  AlertTriangle,
  ShieldAlert,
} from "lucide-react";

function ZoneDetailsModal({ zone, onClose }) {
  if (!zone) return null;

  const priority =
    zone.score >= 80 ? "P1" : zone.score >= 60 ? "P2" : "P3";

  const priorityClass =
    priority === "P1"
      ? "text-red-400 bg-red-500/10 border-red-500/20"
      : priority === "P2"
      ? "text-orange-400 bg-orange-500/10 border-orange-500/20"
      : "text-yellow-400 bg-yellow-500/10 border-yellow-500/20";

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="w-full max-w-lg rounded-2xl border border-[#26384B] bg-[#07111D] shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#1E3042] p-5">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-red-500/10 text-red-400">
              <MapPin size={22} />
            </div>

            <div>
              <h2 className="text-lg font-semibold text-white">
                {zone.name}
              </h2>
              <p className="text-xs text-slate-500">
                Aizawl, Mizoram
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-white/5 hover:text-white"
          >
            <X size={20} />
          </button>
        </div>

        {/* Main information */}
        <div className="space-y-4 p-5">

          {/* Score */}
          <div className="rounded-xl border border-red-500/20 bg-red-500/[0.06] p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Activity size={18} className="text-red-400" />
                <span className="text-sm text-slate-400">
                  Danger Score
                </span>
              </div>

              <span className="text-2xl font-bold text-red-400">
                {zone.score}
                <span className="text-sm font-normal text-slate-600">
                  /100
                </span>
              </span>
            </div>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-[#162333]">
              <div
                className="h-full rounded-full bg-red-500"
                style={{ width: `${zone.score}%` }}
              />
            </div>
          </div>

          {/* Environmental data */}
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-4">
              <div className="flex items-center gap-2">
                <CloudRain size={17} className="text-blue-400" />
                <span className="text-xs text-slate-500">
                  Rainfall
                </span>
              </div>

              <p className="mt-2 text-xl font-bold text-white">
                {zone.rainfall}
                <span className="ml-1 text-xs font-normal text-slate-500">
                  mm
                </span>
              </p>
            </div>

            <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-4">
              <div className="flex items-center gap-2">
                <AlertTriangle size={17} className="text-orange-400" />
                <span className="text-xs text-slate-500">
                  Risk Level
                </span>
              </div>

              <p className="mt-2 text-lg font-bold uppercase text-red-400">
                {zone.level}
              </p>
            </div>
          </div>

          {/* Priority */}
          <div className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <ShieldAlert size={20} className="text-violet-400" />

                <div>
                  <p className="text-sm font-medium text-white">
                    Emergency Priority
                  </p>
                  <p className="text-xs text-slate-500">
                    Recommended response priority
                  </p>
                </div>
              </div>

              <span
                className={`rounded-full border px-3 py-1.5 text-xs font-bold ${priorityClass}`}
              >
                {priority}
              </span>
            </div>
          </div>

          {/* Demo note */}
          <p className="text-center text-[11px] text-slate-600">
            Demo data • Live environmental data will be integrated later
          </p>
        </div>
      </div>
    </div>
  );
}

export default ZoneDetailsModal;
