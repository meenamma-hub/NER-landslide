import {
  Activity,
  CloudRain,
  Clock,
} from "lucide-react";

function LivePrediction({
  dangerScore = 86,
  riskLevel = "CRITICAL",
  rainfall = 124,
}) {

  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">
      
      {/* Section Header */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-white sm:text-lg">
            Live Prediction
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Current environmental risk assessment
          </p>
        </div>

        <div className="flex items-center gap-1.5 text-xs text-emerald-400">
          <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
          Live
        </div>
      </div>

      {/* Prediction Cards */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">

        {/* Danger Score */}
        <div className="rounded-xl border border-red-500/20 bg-red-500/[0.06] p-4">
          <div className="mb-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-red-500/10 text-red-400">
                <Activity size={20} />
              </div>

              <span className="text-sm text-slate-400">
                Danger Score
              </span>
            </div>

            <span className="text-xs text-slate-500">
              / 100
            </span>
          </div>

          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-red-400">
              {dangerScore}
            </span>

            <span className="mb-1 rounded-full bg-red-500/10 px-2.5 py-1 text-xs font-semibold text-red-400">
              {riskLevel}
            </span>
          </div>

          {/* Progress */}
          <div className="mt-4 h-2 overflow-hidden rounded-full bg-[#162333]">
            <div
              className="h-full rounded-full bg-red-500"
              style={{ width: `${dangerScore}%` }}
            />
          </div>
        </div>

        {/* Rainfall */}
        <div className="rounded-xl border border-blue-500/20 bg-blue-500/[0.06] p-4">
          <div className="mb-3 flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
              <CloudRain size={20} />
            </div>

            <span className="text-sm text-slate-400">
              Rainfall
            </span>
          </div>

          <div className="flex items-end gap-2">
            <span className="text-4xl font-bold text-blue-400">
              {rainfall}
            </span>

            <span className="mb-1 text-sm text-slate-500">
              mm
            </span>
          </div>

          <p className="mt-3 text-xs text-slate-500">
            Recorded rainfall
          </p>
        </div>
      </div>

      {/* Updated Time */}
      <div className="mt-4 flex items-center gap-2 text-xs text-slate-500">
        <Clock size={14} />
        Last updated: 2 minutes ago
      </div>
    </section>
  );
}

export default LivePrediction;