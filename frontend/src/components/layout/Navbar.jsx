function Navbar({ onMenuClick }) {
  return (
    <header className="sticky top-0 z-40 h-20 border-b border-[#1E3042] bg-[#020812]/95 backdrop-blur-md">
      <div className="flex h-full items-center justify-between px-4 sm:px-6 lg:px-8">

        {/* Left Section */}
        <div className="flex items-center gap-3">

          {/* Menu Button */}
          <button
            onClick={onMenuClick}
            className="flex h-11 w-11 items-center justify-center rounded-xl text-slate-200 transition hover:bg-white/5 lg:hidden"
            aria-label="Open menu"
          >
            <span className="text-2xl">☰</span>
          </button>

          {/* Logo */}
          <div className="flex items-center gap-3">

            <div className="flex h-11 w-11 items-center justify-center rounded-full bg-emerald-500/10 text-2xl">
              🏔️
            </div>

            <div className="hidden sm:block">
              <h1 className="text-lg font-semibold leading-tight text-white">
                NER Landslide
              </h1>

              <p className="text-xs text-slate-400">
                Early Warning System
              </p>
            </div>

          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2 sm:gap-4">

          {/* High Alert */}
          <div className="hidden items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm font-medium text-red-400 sm:flex">
            <span>⚠</span>
            HIGH ALERT
          </div>

          {/* Notification */}
          <button
            className="relative flex h-11 w-11 items-center justify-center rounded-xl text-xl transition hover:bg-white/5"
            aria-label="Notifications"
          >
            🔔

            <span className="absolute right-0 top-0 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white">
              12
            </span>
          </button>

          {/* Profile */}
          <button
            className="flex h-11 w-11 items-center justify-center rounded-full border border-[#26384B] bg-[#0B1522] text-xl"
            aria-label="Profile"
          >
            👤
          </button>

        </div>

      </div>
    </header>
  );
}

export default Navbar;