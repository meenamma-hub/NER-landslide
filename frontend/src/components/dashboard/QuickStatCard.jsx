import { ChevronRight } from "lucide-react";

function QuickStatCard({
  title,
  subtitle,
  icon,
  iconClass,
  cardClass,
  onClick,
}) {
  return (
    <button
      onClick={onClick}
      className={`
        group flex w-full items-center justify-between
        rounded-xl border p-4
        text-left
        transition-all duration-200
        hover:-translate-y-0.5
        hover:brightness-110
        ${cardClass}
      `}
    >
      <div className="flex items-center gap-3">

        {/* Icon */}
        <div
          className={`
            flex h-11 w-11 shrink-0 items-center justify-center
            rounded-xl
            ${iconClass}
          `}
        >
          {icon}
        </div>

        {/* Text */}
        <div>
          <h2 className="text-base font-medium text-slate-100 sm:text-lg">
            {title}
          </h2>

          <p className="mt-0.5 text-xs text-slate-400 sm:text-sm">
            {subtitle}
          </p>
        </div>

      </div>

      <ChevronRight
        size={24}
        className="shrink-0 text-slate-300 transition-transform group-hover:translate-x-1"
      />
    </button>
  );
}

export default QuickStatCard;
