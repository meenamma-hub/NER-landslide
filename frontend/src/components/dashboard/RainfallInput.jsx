import { CloudRain } from "lucide-react";

function RainfallInput({ rainfall, onRainfallChange }) {
  return (
    <section className="mt-4 rounded-2xl border border-[#1E3042] bg-[#07111D] p-4 sm:p-5">
      <div className="mb-4 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
          <CloudRain size={22} />
        </div>

        <div>
          <h2 className="text-base font-semibold text-white sm:text-lg">
            Rainfall Input
          </h2>
          <p className="mt-1 text-xs text-slate-500">
            Adjust rainfall to simulate changing conditions
          </p>
        </div>
      </div>

      <div className="rounded-xl border border-[#1E3042] bg-[#0A1623] p-4">
        <div className="mb-4 flex items-end justify-between">
          <div>
            <p className="text-xs text-slate-500">Current Rainfall</p>
            <p className="mt-1 text-3xl font-bold text-blue-400">
              {rainfall}
              <span className="ml-1 text-sm font-medium text-slate-500">
                mm
              </span>
            </p>
          </div>

          <span className="rounded-full bg-blue-500/10 px-3 py-1 text-xs text-blue-400">
            Aizawl
          </span>
        </div>

        <input
          type="range"
          min="0"
          max="200"
          value={rainfall}
          onChange={(e) => onRainfallChange(Number(e.target.value))}
          className="w-full accent-blue-500"
        />

        <div className="mt-2 flex justify-between text-xs text-slate-600">
          <span>0 mm</span>
          <span>200 mm</span>
        </div>
      </div>
    </section>
  );
}

export default RainfallInput;