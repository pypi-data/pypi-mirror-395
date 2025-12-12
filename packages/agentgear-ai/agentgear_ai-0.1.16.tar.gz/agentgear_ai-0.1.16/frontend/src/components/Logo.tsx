export const Logo = ({ className = "w-10 h-10" }: { className?: string }) => (
    <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
        <circle cx="50" cy="50" r="45" fill="#0EA5E9" fillOpacity="0.2" />
        <path
            d="M50 25C36.1929 25 25 36.1929 25 50C25 63.8071 36.1929 75 50 75C63.8071 75 75 63.8071 75 50C75 36.1929 63.8071 25 50 25ZM50 65C41.7157 65 35 58.2843 35 50C35 41.7157 41.7157 35 50 35C58.2843 35 65 41.7157 65 50C65 58.2843 58.2843 65 50 65Z"
            fill="#0284C7"
        />
        <path
            d="M50 10V20M50 80V90M10 50H20M80 50H90M21.7157 21.7157L28.7868 28.7868M71.2132 71.2132L78.2843 78.2843M21.7157 78.2843L28.7868 71.2132M71.2132 28.7868L78.2843 21.7157"
            stroke="#0284C7"
            strokeWidth="8"
            strokeLinecap="round"
        />
        <circle cx="38" cy="45" r="4" fill="#E0F2FE" />
        <circle cx="62" cy="45" r="4" fill="#E0F2FE" />
    </svg>
);
