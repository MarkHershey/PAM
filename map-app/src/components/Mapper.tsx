import React from "react";
import {
    MapContainer,
    TileLayer,
    // CircleMarker,
    Polyline,
    // Popup,
} from "react-leaflet";

interface MapperProps {
    showCommute: boolean;
    showWalking: boolean;
    showDriving: boolean;
    commutePolyLines: any[];
    walkingPolyLines: any[];
    drivingPolyLines: any[];
}

// get API KEY from environment variable
const API_KEY = process.env.STADIA_API_KEY || "";

const Mapper: React.FC<MapperProps> = ({
    showCommute,
    showWalking,
    showDriving,
    commutePolyLines,
    walkingPolyLines,
    drivingPolyLines,
}) => {
    return (
        <div
            className="m-3 rounded-full overflow-clip ring-4 ring-cyan-500/20 hover:ring-cyan-500"
            style={{ minHeight: 500 }}
        >
            <MapContainer
                className="w-full h-full"
                center={[1.3599654500769531, 103.81338414844132]}
                zoom={11} // 11: show whole of Singapore, 12: show most of Singapore, 13: show heart of Singapore
                scrollWheelZoom={true}
                zoomControl={false}
                dragging={true}
                inertia={true}
            >
                <TileLayer
                    attribution=""
                    url={
                        "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png?api_key=" +
                        API_KEY
                    }
                />

                {showCommute &&
                    commutePolyLines.map((ployLine, index) => {
                        return (
                            <Polyline
                                key={index}
                                pathOptions={{
                                    color: "#3a86ff", // blue
                                    opacity: 0.3,
                                    weight: 3,
                                }}
                                positions={ployLine}
                            />
                        );
                    })}

                {showWalking &&
                    walkingPolyLines.map((ployLine, index) => {
                        return (
                            <Polyline
                                key={index}
                                pathOptions={{
                                    color: "#fb5607", // orange
                                    opacity: 0.3,
                                    weight: 3,
                                }}
                                positions={ployLine}
                            />
                        );
                    })}

                {showDriving &&
                    drivingPolyLines.map((ployLine, index) => {
                        return (
                            <Polyline
                                key={index}
                                pathOptions={{
                                    color: "#8338ec", // purple
                                    opacity: 0.3,
                                    weight: 3,
                                }}
                                positions={ployLine}
                            />
                        );
                    })}
            </MapContainer>
        </div>
    );
};

export default Mapper;
