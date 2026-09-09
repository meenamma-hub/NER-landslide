const menuItems = [
  { label: "Dashboard", icon: "🏠" },
  { label: "Risk Map", icon: "🗺️" },
  { label: "Prediction", icon: "🤖" },
  { label: "Impact & Priority", icon: "📊" },
  { label: "Roads & Routes", icon: "🚧" },
  { label: "Hospitals & Rescue", icon: "🏥" },
  { label: "Field Reports", icon: "📸" },
  { label: "Alerts & SMS", icon: "🔔" },
  { label: "Analytics", icon: "📈" },
];

function Sidebar({
  isOpen,
  onClose,
  activePage,
  onNavigate,
}) {
  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed left-0 top-0 z-50
          h-screen w-64
          border-r border-[#1E3042]
          bg-[#07111D]
          transition-transform duration-300
          lg:sticky lg:top-20 lg:z-30
          lg:h-[calc(100vh-5rem)]
          lg:translate-x-0
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >

        {/* Mobile Header */}
        <div className="flex h-20 items-center justify-between border-b border-[#1E3042] px-5 lg:hidden">
          <div>
            <p className="font-semibold text-white">
              NER Landslide
            </p>

            <p className="text-xs text-slate-500">
              Control Panel
            </p>
          </div>

          <button
            onClick={onClose}
            className="text-xl text-slate-400 hover:text-white"
          >
            ✕
          </button>
        </div>

        {/* Navigation */}
        <nav className="space-y-1 p-4">
          {menuItems.map((item) => {
            const isActive = activePage === item.label;

            return (
              <button
                key={item.label}
                onClick={() => onNavigate(item.label)}
                className={`
                  flex w-full items-center gap-3
                  rounded-xl px-4 py-3
                  text-left text-sm
                  transition-all duration-200

                  ${
                    isActive
                      ? "border border-blue-500/20 bg-blue-500/10 text-blue-400"
                      : "text-slate-400 hover:bg-white/5 hover:text-white"
                  }
                `}
              >
                <span className="w-6 text-lg">
                  {item.icon}
                </span>

                <span>
                  {item.label}
                </span>
              </button>
            );
          })}
        </nav>

        {/* Settings */}
        <div className="absolute bottom-0 left-0 right-0 border-t border-[#1E3042] p-4">
          <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-slate-400 transition hover:bg-white/5 hover:text-white">
            <span>⚙️</span>
            Settings
          </button>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;