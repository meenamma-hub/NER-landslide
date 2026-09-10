import {
  Bell,
  CheckCircle2,
  ChevronRight,
  MessageSquare,
  Smartphone,
} from "lucide-react";

function AlertsSMS() {
  // Temporary frontend data.
  // Later this will come from the reporting/backend API.
  const alertStats = [
    {
      label: "Active Alerts",
      value: "12",
      icon: <Bell size={19} />,
      iconClass: "bg-red-500/10 text-red-400",
    },
    {
      label: "SMS Sent",
      value: "248",
      icon: <MessageSquare size={19} />,
      iconClass: "bg-blue-500/10 text-blue-400",
    },
    {
      label: "Delivered",
      value: "96%",
      icon: <CheckCircle2 size={19} />,
      iconClass: "bg-emerald-500/10 text-emerald-400",
    },
  ];

  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
            <Smartphone size={21} />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white sm:text-lg">
              Alerts & SMS
            </h2>

            <p className="text-xs text-slate-500">
              Emergency communication status
            </p>
          </div>
        </div>

        <span className="flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs font-semibold text-emerald-400">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          Active
        </span>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-3 gap-2 sm:gap-3">
        {alertStats.map((stat) => (
          <div
            key={stat.label}
            className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-3"
          >
            <div
              className={`mb-2 flex h-8 w-8 items-center justify-center rounded-lg ${stat.iconClass}`}
            >
              {stat.icon}
            </div>

            <p className="text-lg font-bold text-white sm:text-xl">
              {stat.value}
            </p>

            <p className="mt-1 text-[10px] leading-tight text-slate-500 sm:text-xs">
              {stat.label}
            </p>
          </div>
        ))}
      </div>

      {/* Alert Message Preview */}
      <div className="mt-4 rounded-xl border border-red-500/20 bg-red-500/[0.05] p-3">
        <div className="flex items-start gap-3">
          <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-red-500/10 text-red-400">
            <Bell size={17} />
          </div>

          <div className="min-w-0">
            <p className="text-xs font-semibold text-red-400">
              Latest Emergency Alert
            </p>

            <p className="mt-1 text-xs leading-relaxed text-slate-400">
              Critical landslide risk detected in the affected zone.
              Residents are advised to move to designated safe areas.
            </p>

            <p className="mt-2 text-[10px] text-slate-600">
              Sent 2 minutes ago
            </p>
          </div>
        </div>
      </div>

      {/* Action */}
      <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-[#1E3042] py-2.5 text-xs font-medium text-slate-400 transition hover:bg-white/[0.03] hover:text-white">
        Manage alerts & notifications
        <ChevronRight size={15} />
      </button>
    </section>
  );
}

export default AlertsSMS;