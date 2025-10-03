import {useEffect, useState} from "react";
import "../css/themeSwitcher.css"

export default function ThemeSwitcher() {
    const [theme, setTheme] = useState(() => {
        return localStorage.getItem('theme') || 'auto'
    });

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);


    function handleThemeSwap(e) {
        setTheme(e.target.value)
    }

    return (
        <div className="theme-switcher">
            <input type="radio"
                   id={"theme-dark"}
                   name={"theme-dark"}
                   value={"dark"}
                   checked={theme === "dark"}
                   onChange={handleThemeSwap}
            />
            <label htmlFor={"theme-dark"}>D</label>
            <input type="radio"
                   id={"theme-auto"}
                   name={"theme-auto"}
                   value={"auto"}
                   checked={theme === "auto"}
                   onChange={handleThemeSwap}
            />
            <label htmlFor={"theme-auto"}>A</label>
            <input type="radio"
                   id={"theme-light"}
                   name={"theme-light"}
                   value={"light"}
                   checked={theme === "light"}
                   onChange={handleThemeSwap}
                />
            <label htmlFor={"theme-light"}>L</label>
            <div className={"theme-slider"}></div>
        </div>
    )
}