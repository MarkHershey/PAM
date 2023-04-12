import React from "react";
import logo from "../assets/logo.png";

const Header = () => {
    return (
        <nav className="mt-5 px-2 bg-gray-900 border-gray-700">
            <div className="container flex flex-wrap justify-between items-center mx-auto">
                <a href="/PAM" className="flex items-center">
                    <img
                        src={logo}
                        className="mr-3 h-6 sm:h-10"
                        alt="Logo"
                    ></img>
                    <span className="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
                        Personal Activity Map
                    </span>
                </a>
            </div>
        </nav>
    );
};

Header.propTypes = {};

export default Header;
