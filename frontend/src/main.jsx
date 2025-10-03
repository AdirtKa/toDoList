import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './css/index.css'
import {
    createBrowserRouter,
    RouterProvider,
} from "react-router";
import Root from "./components/Root.jsx";
import Profile from "./components/Profile.jsx";


let router = createBrowserRouter([
    {
        path: "/",
        Component: Root,
        children: [
            {
                path: "/profile",
                Component: Profile,
            }
        ]
    }
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router}/>
  </StrictMode>,
)
