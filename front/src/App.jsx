import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RegistrationPage from "./pages/register";

function App() {

  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/register">Home</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/register" element={<RegistrationPage/>}/>
      </Routes>
    </Router>
  )
}

export default App