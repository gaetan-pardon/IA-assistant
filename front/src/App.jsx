import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RegistrationPage from "./pages/RegisterPage/register";
import LoginPage from "./pages/LoginPage/login";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationPage/>}/>
        <Route path="/login" element={<LoginPage/>}/>
      </Routes>
    </Router>
  )
}

export default App