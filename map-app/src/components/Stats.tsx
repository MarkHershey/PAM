import React from "react";
import NumberStats from "./NumberStats";

interface StatsProps {
    commuteOnClick: () => void;
    walkingOnClick: () => void;
    drivingOnClick: () => void;
    commuteActive: boolean;
    walkingActive: boolean;
    drivingActive: boolean;
}

const Stats: React.FC<StatsProps> = ({
    commuteOnClick,
    walkingOnClick,
    drivingOnClick,
    commuteActive,
    walkingActive,
    drivingActive,
}) => {
    return (
        <div className="container mx-auto p-4 flex flex-row justify-center">
            <NumberStats
                caption="Total Commute Distance"
                value={5738}
                unit="KM"
                color="#3a86ff"
                onClick={commuteOnClick}
                active={commuteActive}
            />
            <NumberStats
                caption="Total Driving Distance"
                value={2246}
                unit="KM"
                color="#8338ec"
                onClick={drivingOnClick}
                active={drivingActive}
            />
            <NumberStats
                caption="Total Walking Distance"
                value={1313}
                unit="KM"
                color="#fb5607"
                onClick={walkingOnClick}
                active={walkingActive}
            />
        </div>
    );
};

export default Stats;
