import {
  CalendarDays,
  Globe,
  ChevronDown,
} from "lucide-react";

function DashboardHeader() {
  return (
    <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

      {/* Date */}
      <div className="flex items-center gap-2 text-sm text-slate-400">
        <CalendarDays size={18} />

        <span>
          28 Aug 2025, 10:30 AM
        </span>
      </div>

      {/* Language */}
      <button className="flex items-center gap-2 self-start text-sm text-slate-300 transition hover:text-white sm:self-auto">
        <Globe size={18} />

        <span>English</span>

        <ChevronDown size={16} />
      </button>

    </div>
  );
}

export default DashboardHeader;
