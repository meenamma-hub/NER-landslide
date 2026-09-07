import {
  ChevronRight,
  MapPin,
  ShieldCheck,
  Users,
} from "lucide-react";

function RescueTeams() {
  // Temporary frontend data.
  // Later this will come from the backend/impact API.
  const teams = [
    {
      id: 1,
      name: "NER Response Team",
      location: "Aizawl, Mizoram",
      distance: "3.8 km",
      members: 12,
      status: "Available",
    },
    {
      id: 2,
      name: "District Rescue Unit",
      location: "Mamit, Mizoram",
      distance: "7.4 km",
      members: 8,
      status: "Available",
    },
    {
      id: 3,
      name: "Mountain Rescue Team",
      location: "Tawang, Arunachal Pradesh",
      distance: "10.6 km",
      members: 6,
      status: "Deploying",
    },
  ];

  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
            <ShieldCheck size={21} />
          </div>

          <div>
            <h2 className="text-base font-semibold text-white sm:text-lg">
              Rescue Teams
            </h2>

            <p className="text-xs text-slate-500">
              Nearby emergency response teams
            </p>
          </div>
        </div>

        <span className="rounded-full bg-cyan-500/10 px-2.5 py-1 text-xs font-semibold text-cyan-400">
          {teams.length} Nearby
        </span>
      </div>

      {/* Teams */}
      <div className="space-y-3">
        {teams.map((team) => (
          <div
            key={team.id}
            className="rounded-xl border border-[#1E3042] bg-[#0B1522] p-3"
          >
            <div className="flex items-start justify-between gap-3">

              {/* Team info */}
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="truncate text-sm font-semibold text-white">
                    {team.name}
                  </h3>

                  <span
                    className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                      team.status === "Available"
                        ? "bg-emerald-500/10 text-emerald-400"
                        : "bg-yellow-500/10 text-yellow-400"
                    }`}
                  >
                    {team.status}
                  </span>
                </div>

                <div className="mt-2 flex items-center gap-1.5">
                  <MapPin
                    size={13}
                    className="shrink-0 text-slate-600"
                  />

                  <span className="truncate text-xs text-slate-500">
                    {team.location}
                  </span>
                </div>
              </div>

              {/* Distance */}
              <div className="shrink-0 text-right">
                <p className="text-sm font-semibold text-slate-200">
                  {team.distance}
                </p>

                <p className="text-[10px] text-slate-600">
                  distance
                </p>
              </div>
            </div>

            {/* Team capacity */}
            <div className="mt-3 flex items-center justify-between border-t border-[#1E3042] pt-3">
              <div className="flex items-center gap-2">
                <Users
                  size={15}
                  className="text-slate-500"
                />

                <span className="text-xs text-slate-400">
                  Team members
                </span>
              </div>

              <span className="text-xs font-semibold text-slate-200">
                {team.members} members
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* View on map */}
      <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-[#1E3042] py-2.5 text-xs font-medium text-slate-400 transition hover:bg-white/[0.03] hover:text-white">
        View rescue teams on map
        <ChevronRight size={15} />
      </button>
    </section>
  );
}

export default RescueTeams;