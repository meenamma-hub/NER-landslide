function DashboardCard({ children, className = "" }) {
  return (
    <section
      className={`
        mt-4 rounded-2xl
        border border-[#1E3042]
        bg-[#07111D]
        ${className}
      `}
    >
      {children}
    </section>
  );
}

export default DashboardCard;