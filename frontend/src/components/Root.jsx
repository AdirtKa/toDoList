import {Link, NavLink, Outlet} from "react-router"
import '../css/root.css'
import ThemeSwitcher from "./ThemeSwitcher.jsx";

export default function Root() {

    return (
        <>
            <nav>
                <NavLink to={"/"} >На главную</NavLink>
                <NavLink to={"/profile"} end>Мой профиль</NavLink>
                <ThemeSwitcher/>
            </nav>
            <Outlet/>
        </>
    )
}