import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RegistrationPage from "./pages/RegisterPage/register";
import LoginPage from "./pages/LoginPage/login";
import HomePage from "./pages/HomePage/home";
import { ProtectedRoute } from "./components/ProtectedRoute/ProtectedRoute";
import ChatPage from "./pages/ChatPage/chat";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationPage/>}/>
        <Route path="/login" element={<LoginPage/>}/>
        <Route path="/home" element={<HomePage/>}/>
        <Route path="/chat" element={<ProtectedRoute><ChatPage/></ProtectedRoute>}/>
      </Routes>
    </Router>
  )
}

export default App