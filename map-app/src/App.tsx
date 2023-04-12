import React, { useState } from "react";
import Header from "./components/Header";
import Mapper from "./components/Mapper";
import Profile from "./components/Profile";
import Stats from "./components/Stats";
import { AVATARS } from "./assets/avatars";
import { NAMES } from "./assets/names";
import {
    multiPolyline0,
    multiPolyline1,
    multiPolyline2,
    multiPolyline3,
    multiPolyline4,
    multiPolyline5,
} from "./assets/routes/RoutesSG";

const getPolyLines = () => {
    const multiPolyLines = [
        multiPolyline0,
        multiPolyline1,
        multiPolyline2,
        multiPolyline3,
        multiPolyline4,
        multiPolyline5,
    ];

    let commutePolyLines =
        multiPolyLines[Math.floor(Math.random() * multiPolyLines.length)];
    commutePolyLines = shuffle(commutePolyLines);
    commutePolyLines = commutePolyLines.slice(0, commutePolyLines.length / 2);

    let walkingPolyLines =
        multiPolyLines[Math.floor(Math.random() * multiPolyLines.length)];
    walkingPolyLines = shuffle(walkingPolyLines);
    walkingPolyLines = walkingPolyLines.slice(0, walkingPolyLines.length / 3);

    let drivingPolyLines =
        multiPolyLines[Math.floor(Math.random() * multiPolyLines.length)];
    drivingPolyLines = shuffle(drivingPolyLines);
    drivingPolyLines = drivingPolyLines.slice(0, drivingPolyLines.length / 4);

    return {
        commutePolyLines,
        walkingPolyLines,
        drivingPolyLines,
    };
};

const { commutePolyLines, walkingPolyLines, drivingPolyLines } = getPolyLines();

const pickNameAndAvatar = () => {
    const avatars = shuffle(AVATARS);
    const theAvatar = avatars[0];
    const names = shuffle(NAMES);
    const theName = names[0];
    return {
        theAvatar,
        theName,
    };
};

const { theAvatar, theName } = pickNameAndAvatar();

function shuffle(array: any[]): any[] {
    let currentIndex = array.length;
    let randomIndex;
    while (currentIndex !== 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex],
            array[currentIndex],
        ];
    }
    return array;
}

function App() {
    const [showCommute, setShowCommute] = useState(true);
    const [showWalking, setShowWalking] = useState(true);
    const [showDriving, setShowDriving] = useState(true);

    return (
        <div className=" bg-slate-900 select-none">
            <Header />
            <div className="container mt-10 flex justify-between mx-auto items-center">
                <Profile
                    avatar={theAvatar}
                    name={theName}
                    year={2015}
                    month={4}
                />
            </div>

            <div
                className="px-0 sm:px-0 md:px-0 lg:px-32 xl:px-32 grid grid-cols-1 gap-1"
                style={{ height: "calc(100% - 250px)" }}
            >
                <Mapper
                    showCommute={showCommute}
                    showWalking={showWalking}
                    showDriving={showDriving}
                    commutePolyLines={commutePolyLines}
                    walkingPolyLines={walkingPolyLines}
                    drivingPolyLines={drivingPolyLines}
                />
            </div>
            <div className="container p-4 m-auto">
                <Stats
                    commuteOnClick={() => setShowCommute(!showCommute)}
                    walkingOnClick={() => setShowWalking(!showWalking)}
                    drivingOnClick={() => setShowDriving(!showDriving)}
                    commuteActive={showCommute}
                    walkingActive={showWalking}
                    drivingActive={showDriving}
                />
            </div>
        </div>
    );
}

export default App;
