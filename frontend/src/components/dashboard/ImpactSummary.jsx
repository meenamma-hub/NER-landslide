import {
  Building2,
  MapPin,
  Users,
  Home,
  Route,
} from "lucide-react";

function ImpactSummary() {
  // Temporary frontend values.
  // Later these will come from the Impact/Backend API.
  const impactData = [
    {
      label: "People Affected",
      value: "12,450",
      icon: <Users size={20} />,
      iconClass: "bg-red-500/10 text-red-400",
    },
    {
      label: "Villages",
      value: "18",
      icon: <Home size={20} />,
      iconClass: "bg-orange-500/10 text-orange-400",
    },
    {
      label: "Roads",
      value: "7",
      icon: <Route size={20} />,
      iconClass: "bg-yellow-500/10 text-yellow-400",
    },
    {
      label: "Infrastructure",
      value: "24",
      icon: <Building2 size={20} />,
      iconClass: "bg-violet-500/10 text-violet-400",
    },
  ];

  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400">
            <MapPin size={21} />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white sm:text-lg">
              Impact Summary
            </h2>

            <p className="text-xs text-slate-500">
              Estimated impact in high-risk areas
            </p>
          </div>
        </div>
      </div>

      {/* Impact Cards */}
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {impactData.map((item) => (
          <div
            key={item.label}
            className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-3 sm:p-4"
          >
            <div
              className={`mb-3 flex h-9 w-9 items-center justify-center rounded-lg ${item.iconClass}`}
            >
              {item.icon}
            </div>

            <p className="text-xl font-bold text-white sm:text-2xl">
              {item.value}
            </p>

            <p className="mt-1 text-xs text-slate-500">
              {item.label}
            </p>
          </div>
        ))}
      </div>

      {/* Note */}
      <div className="mt-4 rounded-xl border border-[#1E3042] bg-[#0B1522] px-3 py-3">
        <p className="text-xs leading-relaxed text-slate-500">
          Impact estimates are based on current risk zones,
          population exposure and affected infrastructure.
        </p>
      </div>
    </section>
  );
}

export default ImpactSummary;