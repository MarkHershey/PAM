import React from "react";

interface NumberStatsProps {
    caption: string;
    value: number;
    unit: string;
    color: string;
    onClick?: () => void;
    active: boolean;
}

const NumberStats: React.FC<NumberStatsProps> = ({
    caption,
    value,
    unit,
    color,
    onClick,
    active,
}) => {
    const valueStyle = {
        color: "grey",
        fontSize: "5rem",
        fontWeight: "bold",
        opacity: 0.7,
    };

    const valueStyleActive = {
        color,
        fontSize: "5rem",
        fontWeight: "bold",
        opacity: 0.7,
    };

    return (
        <div
            className="transition flex flex-col items-center bg-gradient-to-b from-slate-800 shadow-md m-3 p-6 rounded-lg hover:to-slate-800 hover:-translate-y-1"
            onClick={onClick}
        >
            <p className="text-gray-700 text-lg font-semibold">{caption}</p>
            <div
                style={active ? valueStyleActive : valueStyle}
                className="mt-4"
            >
                {value}
                <span className="text-2xl ml-2">{unit}</span>
            </div>
        </div>
    );
};

export default NumberStats;
