import { Routes, Route, Outlet } from "react-router-dom";
import './App.css'
import Home from "@/pages/Home";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path=":userId" element={<Home />} />
      </Route>
    </Routes>
  );
}

function Layout() {
  return (
    <Outlet />
  );
}

